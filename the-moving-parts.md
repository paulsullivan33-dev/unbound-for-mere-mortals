# The Moving Parts

Unbound is one program with one config
file, but inside it five jobs are kept
deliberately separate. Knowing which
job owns a behaviour turns every later
surprise — a refused name, a stale
answer, a failed check — into a named
problem with an address.

**The listener.** The daemon binds to
addresses and ports you choose (`interface:`
and `port:` in the config) and takes
questions from the clients you allow
(`access-control:`). By default it
listens on localhost, port 53. It
speaks ordinary DNS on UDP and TCP, and
can also serve encrypted DNS to clients
(DoT and DoH) when configured — the
listener is where that policy lives.

**The local zones.** Before any walking
happens, Unbound checks its own
definitions. Names you declare with
`local-data:` are answered on the spot,
out of `local-zone:` areas whose type
decides the fate of everything else in
them: a `static` zone says *these names
are all there is* (anything else in it
is NXDOMAIN), a `refuse` zone refuses
every question, a `transparent` zone
answers what it knows and passes the
rest on. Chapter 5 shows each behaviour
in the lab. Unbound also carries
built-in zones for names that must
never be asked outside — localhost and
the special-use endings like `.test` —
which chapter 7's first attempt ran
into headfirst.

**The iterator.** The walker. Given a
name nobody local can answer, it starts
from the **root hints** — a small file
naming the thirteen root server groups
at the top of the DNS — and asks its
way down: the roots point to the
servers for the last part of the name
(`.org`, say), those point to the
domain's own servers, and those give
the answer. It needs no configuration
beyond the hints, and it is the part
that needs the open internet. In the
lab it could reach out and be cut off;
its attempts are in the log, chapter 8.

**The validator.** The checker. Where
a zone is signed with DNSSEC, each
answer arrives with signatures, and the
validator verifies them against a chain
of trust that starts at one thing you
hold locally: the **root trust anchor**,
the hash of the root's own key. A
failed check makes the whole answer
*bogus*, and the client is told
SERVFAIL — a lie detected is an answer
refused. The anchor is installed with
the package and kept current by
`unbound-anchor` and by Unbound's own
RFC 5011 tracking; chapter 8 opens
that machinery up.

**The cache.** Two stores: one for
answers, one for the directions (which
server is authoritative for what, and
how long each delegation lasts). Every
entry keeps the lifetime its owner set,
and Unbound serves the remaining time,
counting down, so no client is ever
told a stale number is fresher than it
is. Chapter 7 measures all of this:
the countdown, the hit that never left
the machine, prefetch refreshing an
answer before it dies, and an answer
served past its expiry when its source
had vanished.

**The control channel.** A separate,
private line into the running daemon —
by default an encrypted socket on
localhost — spoken by `unbound-control`.
It is how you ask for statistics, list
or change local data, flush one name
from the cache, and stop the daemon
politely. Chapter 10 uses it; the lab's
transcripts use it throughout. Nothing
a client can ask arrives on this
channel; it is the operator's door,
not a second listener.

The config file itself is the sixth
part, and chapter 4 is devoted to it:
four kinds of clause — `server:`,
`remote-control:`, `forward-zone:` and
`stub-zone:` — each introduced in the
chapter that needs it.
