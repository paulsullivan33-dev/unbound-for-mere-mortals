# Limits

What Unbound cannot do, stated
plainly. The first group the project
states itself; the lab met the second
group while working, and both are
labelled. The lab's own limits — what
its sandbox prevented it from proving
— are a third list, kept in
`criteria.md` where they belong.

**Not an authoritative server.** It
will not host your public zone for the
world. The `local-data` machinery
answers *your* clients for names you
define; it does no zone transfers, no
public service, no NOTIFY — and
pointing the internet at it is
chapter 1's open-resolver mistake,
not a hosting strategy. BIND or NSD
(the project's sibling) hold that job.

**No filtering of its own.** No
blocklists, no per-client rules beyond
address ranges, no dashboard, no
graphs. The refuse-zone trick
(chapters 5 and 11) is a scalpel for
individual names, not a filter
platform. If your requirement starts
"block ads on every device", the
answer is Pi-hole or AdGuard Home —
with Unbound behind them, chapter 11.

**It believes TTLs, even when you
wish it wouldn't.** An owner who sets
a week-long TTL has set it; Unbound
will serve that answer for a week
(chapter 7). `cache-min-ttl` and
`cache-max-ttl` exist and bend the
rule — this guide leaves them alone,
because a resolver that edits other
people's lifetimes makes debugging
everyone's problem. Your own records
are the ones to set short TTLs on.

**Validation is a cliff, not a
slope.** A zone whose signatures break
is bogus, and bogus is SERVFAIL —
there is no "answer anyway, with a
warning" mode a client would ever see.
That is the correct security posture,
and it means a mis-signed zone, an
expired signature, or your own wrong
clock (chapter 8) presents as total
failure for that name. `domain-insecure`
and local trust anchors are the
surgical tools; there is no dimmer.

**One protocol shape upstream.** It
walks with ordinary DNS and can ask
upstreams over TLS (chapter 9). It is
not a DNS-over-HTTPS *client* upstream;
if a design requires DoH on the
upstream side, a small proxy joins the
cast or a different resolver takes
the job.

**It is only as reachable as its
network.** Recursion needs to *reach*
the roots and every authority below
them. Firewalls that pass port 53 to
one approved resolver but not to the
world, hotel and campus networks, and
the lab's own sandbox all produce the
same shape of failure — the walk
cannot start or cannot finish — and
Unbound's answer is the honest
SERVFAIL, not a fallback to something
you did not configure. A resolver you
control on a network you don't is a
design that needs the forwarding
chapter, or a different network.

**No DHCP, no discovery.** It answers
questions; it does not hand out
addresses, announce services, or find
your printer. The names in chapter 6
are true because you typed them.
