# Forwarding on Purpose

The outcome: you can choose, name by
name, between Unbound walking the DNS
itself and handing the question to
another server — and you know what
each choice gives up.

Recursion is Unbound's default and
this guide's recommendation for a home
network: no middleman, answers checked
against the root's chain of trust.
But *forwarding* — sending a question
to a resolver someone else runs — is
sometimes the right design, and
Unbound supports it per zone, so the
exception can be exactly as wide as
its reason:

- Your employer's names live behind
  their resolver; those, and only
  those, must be asked there.
- Your router already knows the names
  it handed out by DHCP; asking it for
  its own zone beats retyping them.
- You *choose* an upstream with a
  policy you want — a filtering
  resolver, say — knowing chapter 1's
  trade: they see those questions.

## forward-zone: ask another resolver

```yaml
forward-zone:
    name: "lab"
    forward-addr: 127.0.0.1@18087
```

That is the lab's own clause — the
stand-in upstream of chapter 7 — and
it is why that chapter's evidence is
also this chapter's: forwarding really
was how the lab's Unbound answered.
The mechanics to notice: the named
zone and everything under it goes to
the listed addresses; `name: "."`
forwards *everything*, turning
Unbound into a caching, validating
front-end for somebody else's
recursion — a legitimate design (it
is how the Pi-hole recipe in chapter
11 is *not* built, and how many people
do build it), as long as it is chosen
with open eyes. A forwarded zone
usually also wants `domain-insecure`
(chapter 8) if it is private, since
the public chain of trust has never
heard of it.

Addresses may carry a port (`@18087`
above; the default is 53) and, for
encrypted upstreams, a name after
`#`. Which brings up the documented
half of this chapter:

## Encrypted upstreams (documented-only)

The sandbox could not carry this
traffic, so the following is from
NLnet Labs' documentation, labelled
as the criteria require. Unbound can
ask its upstreams over **DNS over TLS
(DoT)**:

```yaml
server:
    ssl-upstream: yes        # or per-zone, below
forward-zone:
    name: "."
    forward-addr: 1.1.1.1@853#cloudflare-dns.com
    forward-tls-upstream: yes
```

The `#name` is the certificate name to
expect — TLS needs to know who it is
talking to, not just where. With this
on, your provider sees connections to
an encrypted port but not the names
inside them; the upstream operator
still sees the names themselves
(chapter 1's trade, once more). DoH —
DNS over HTTPS — Unbound serves to its
*clients* when configured, but as an
upstream transport upstream it is not
Unbound's trick; tools that need it
put a small proxy in front.

## stub-zone: ask the authority directly

A **stub zone** looks like a forward
zone with one difference that matters:
the addresses are not another
*resolver* but the zone's own
*authoritative* servers, and Unbound
still does the walking and validating
below that point itself:

```yaml
stub-zone:
    name: "example.internal"
    stub-addr: 192.168.1.1
```

The classic job is your router's zone:
the router is authoritative for the
names it issued, so instead of copying
them into `local-data` (chapter 6) you
can point Unbound at the source and
let the records stay in one place.
The lab did not run a stub zone — its
stand-in upstream poses as a resolver,
not an authority — so this section is
documented-only, and the difference to
hold onto is the one above: forward
says *ask them, they will do the
work*; stub says *start the walk
there*.

One sentence of hygiene for both:
forward and stub clauses are
per-zone scalpels. If you find one
named `"."` in a config you inherited,
you have found the decision that
defines the whole resolver — read it
first.
