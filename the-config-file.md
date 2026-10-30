# The Config File

The outcome: you can read an Unbound
config top to bottom and say what each
clause does — and when one is wrong,
the checker's message points you at
the exact line.

Everything Unbound does is governed by
one text file. It is built from
**clauses**: a header line ending in a
colon, then indented `option: value`
lines belonging to it. Four clause
types cover nearly everything:

- `server:` — the daemon itself: where
  it listens, who may ask, the local
  zones, the cache's behaviour. Most of
  this guide lives here.
- `remote-control:` — the operator's
  channel from chapter 2: whether it is
  on, and how `unbound-control` reaches
  the daemon.
- `forward-zone:` — names to hand to
  *another* resolver instead of walking
  (chapter 9).
- `stub-zone:` — names whose
  authoritative servers you name
  yourself — your router's zone is the
  classic case (chapter 9).

Comments begin with `#`. Quoting values
in double quotes is always safe and
sometimes required. There is no save
button and no web form: you edit the
file, run `unbound-checkconf`, and
restart or reload the service.

## The lab's config, walked through

The lab's whole config is kept at
`unbound-lab/unbound.conf`; it is the
one every transcript uses. Its shape,
with the lab-only paths left as they
ran:

```yaml
server:
    verbosity: 1
    num-threads: 1
    interface: 127.0.0.1
    port: 18086
    do-ip6: no
    do-daemonize: yes
    ...
    tcp-upstream: yes
    root-hints: ".../usr/share/dns/root.hints"
    auto-trust-anchor-file: ".../root.key"
    domain-insecure: "lab"
    do-not-query-localhost: no
    access-control: 127.0.0.0/8 allow
    prefetch: yes
    serve-expired: yes
    local-zone: "home.arpa." static
    local-data: 'printer.home.arpa. 3600 IN A 192.168.1.50'
    ...
```

The first block is plumbing the lab
needed: it listens only on loopback
and on a test port (18086, not the
standard 53, so it could never collide
with anything else on the shared
machine), writes its own log file, and
runs as the user who started it. On
your machine the distribution's
defaults cover all of this and you
will likely never write these lines.
Three lines, though, deserve their
story because a reader reusing the lab
config will meet them:

- `tcp-upstream: yes` tells Unbound to
  make its own upstream queries over
  TCP only. The sandbox refuses UDP
  outright (`t01`), so this was the
  lab's accommodation; **on a real
  network, leave it out** — UDP is
  DNS's normal, lighter transport, and
  Unbound falls back to TCP when an
  answer is too big.
- `do-not-query-localhost: no` permits
  asking an upstream on the same
  machine. Unbound's default refuses
  loopback upstreams as a safety rail;
  the lab's stand-in upstream *is* on
  loopback, so the rail is lifted,
  deliberately and in writing.
- `domain-insecure: "lab"` exempts the
  lab's private zone from DNSSEC
  checking — an unsigned private zone
  behind a signed root would otherwise
  be called a liar. Chapter 8 explains;
  every private zone you define will
  want the same line or its cousins.

The remaining lines are the guide in
miniature: who may ask
(`access-control`), the two cache
kindnesses (`prefetch`, `serve-expired`)
that chapter 7 measures, and the local
names chapter 5 asks about.

## When the config is wrong

The checker is exact and unembarrassed.
A misspelled option:

```text
$ unbound-checkconf broken1.conf
.../broken1.conf:3: error: unknown keyword 'verbosit'
.../broken1.conf:3: error: stray ':'
read .../broken1.conf failed: 3 errors in configuration file
(exit 1)
```

A value of the wrong shape:

```text
$ unbound-checkconf broken2.conf
.../broken2.conf:6: error: port number expected
read .../broken2.conf failed: 1 errors in configuration file
(exit 1)
```

Both are from the lab's transcript
(`unbound-lab/transcripts/t02-anchor-and-checkconf.txt`),
where the good config passes with the
single line `unbound-checkconf: no
errors in ...`. Learn the rhythm now:
edit, check, then restart. Chapter 14
starts here for almost every "Unbound
won't start" story.
