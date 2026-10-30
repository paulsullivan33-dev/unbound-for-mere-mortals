# Recipes

Four setups this guide has already
built the pieces for. Each is complete
as written; the config fragments add
to a distribution install's
`unbound.conf.d/` unless stated.

## 1. The Pi-hole pairing (the classic)

**The job:** network-wide advert and
tracker filtering *without* handing
your lookups to a public resolver.

**The shape:** clients ask **Pi-hole**,
which refuses the names on its
blocklists and passes the rest to
**Unbound on the same machine**, which
recurses and validates. Pi-hole's own
guide covers its install; the Unbound
half is a resolver bound to loopback
on a second port, since Pi-hole owns
53:

```yaml
server:
    interface: 127.0.0.1
    port: 5335
    access-control: 127.0.0.0/8 allow
```

Then in Pi-hole's settings, the single
upstream is `127.0.0.1#5335` — and
crucially, *only* that one: every
extra upstream ticked in Pi-hole is a
door around Unbound. Two warnings
from experience, this series' and the
projects' own docs: never point
Pi-hole at anything that points back
at Pi-hole (a loop of polite refusals
presents as total DNS failure), and
remember which of the pair owns
filtering when a name won't resolve —
`dig` it against each in turn, and
the one that refuses is the author.

## 2. One noisy name, refused

**The job:** a single domain — a
telemetry endpoint, a television's
phone-home — that you want dead on
your whole network, without adopting
a blocklist.

```yaml
    local-zone: "telemetry.example.com" refuse
```

Chapter 5 ran exactly this pattern:
every name under the zone is answered
REFUSED, instantly, for every client.
Two lines of counsel: use a scalpel,
not a tree — refuse the specific host
zone, not its parent domain, unless
the parent is itself the problem; and
write a comment above the line saying
*why*, dated. Future-you, debugging a
"broken" app at midnight, is the
reader that comment is for.

## 3. The router's names, by stub

**The job:** your router hands out
addresses and remembers the names it
gave them; you want Unbound to answer
for those names without retyping them
into `local-data`.

```yaml
stub-zone:
    name: "lan"
    stub-addr: 192.168.1.1
```

…with the zone name matching whatever
ending your router uses. Chapter 9
explains the mechanism and labels it
documented-only in this guide; the
readiness check is to ask the router
directly first — `dig @192.168.1.1
some-device.lan` — and only build the
stub once the router proves it answers
for its own zone.

## 4. A starter set of house names

**The job:** the first evening's worth
of `home.arpa` definitions (chapter
6's pattern), in the order that pays
back fastest:

```yaml
    local-zone: "home.arpa." static
    # the infrastructure you reach for when things break
    local-data: 'router.home.arpa. 3600 IN A 192.168.1.1'
    local-data: 'nas.home.arpa. 3600 IN A 192.168.1.60'
    local-data-ptr: '192.168.1.60 3600 nas.home.arpa.'
    # the things with web pages of their own
    local-data: 'printer.home.arpa. 3600 IN A 192.168.1.50'
    local-data-ptr: '192.168.1.50 3600 printer.home.arpa.'
```

Infrastructure first, because the name
you want most urgently is always the
box you are trying to fix. Keep the
TTL at 3600 while a setup is young —
an hour forgives mistakes; lower it
once the list has settled. And keep
the list in the config file itself,
not in `unbound-control local-data`
additions made at a prompt: the file
is the copy that survives reboots and
the one `unbound-checkconf` reads.
