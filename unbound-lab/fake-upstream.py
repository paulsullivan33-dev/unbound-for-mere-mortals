#!/usr/bin/env python3
"""Fake upstream DNS server for the Unbound lab.

Listens on 127.0.0.1:18087 (UDP and TCP). Answers A queries in
lab.test with TEST-NET-3 addresses and per-name TTLs, appends one
line per received query to upstream.log so the lab can count how
many times Unbound really went upstream.
"""
import socket
import struct
import sys
import threading
import time

LOG = "/home/hatch/workspace/unbound-labwork/upstream.log"
ADDR = ("127.0.0.1", 18087)

ANSWERS = {
    "www.lab.": ("203.0.113.7", 120),
    "short.lab.": ("203.0.113.8", 12),
}
DEFAULT_TTL = 120


def parse_question(data):
    # header is 12 bytes; then labels until a zero byte
    i = 12
    labels = []
    while data[i] != 0:
        n = data[i]
        labels.append(data[i + 1 : i + 1 + n].decode("ascii", "replace"))
        i += 1 + n
    name = ".".join(labels) + "."
    qtype, qclass = struct.unpack(">HH", data[i + 1 : i + 5])
    question_end = i + 5
    return name, qtype, qclass, data[12:question_end]


def build_response(data):
    name, qtype, qclass, question = parse_question(data)
    with open(LOG, "a") as fh:
        fh.write(f"{time.strftime('%H:%M:%S')} qtype={qtype} name={name}\n")
    tid = data[0:2]
    qdcount = struct.unpack(">H", data[4:6])[0]
    answer = b""
    ancount = 0
    if qtype == 1 and name.lower() in ANSWERS:  # A query we know
        ip, ttl = ANSWERS[name.lower()]
        answer = (
            b"\xc0\x0c"  # pointer to the question name
            + struct.pack(">HHIH", 1, 1, ttl, 4)
            + socket.inet_aton(ip)
        )
        ancount = 1
    header = (
        tid
        + struct.pack(">HHHHH", 0x8180, qdcount, ancount, 0, 0)
    )
    return header + question + answer


def serve_udp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(ADDR)
    while True:
        data, peer = s.recvfrom(4096)
        try:
            s.sendto(build_response(data), peer)
        except Exception as exc:  # keep the log honest
            with open(LOG, "a") as fh:
                fh.write(f"error: {exc}\n")


def serve_tcp():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(5)
    while True:
        conn, _ = s.accept()
        try:
            raw = conn.recv(2)
            if len(raw) < 2:
                continue
            (n,) = struct.unpack(">H", raw)
            data = b""
            while len(data) < n:
                chunk = conn.recv(n - len(data))
                if not chunk:
                    break
                data += chunk
            resp = build_response(data)
            conn.sendall(struct.pack(">H", len(resp)) + resp)
        except Exception as exc:
            with open(LOG, "a") as fh:
                fh.write(f"tcp error: {exc}\n")
        finally:
            conn.close()


if __name__ == "__main__":
    open(LOG, "a").close()
    threading.Thread(target=serve_udp, daemon=True).start()
    serve_tcp()
