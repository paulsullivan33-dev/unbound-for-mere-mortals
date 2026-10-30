# The Neighbours

Unbound's job — recursion, validation,
caching — is one chair at a table of
name-serving tools. These are the ones
it is most often confused with, or
found sitting beside.

**Pi-hole.** A filtering *forwarder*
with a web dashboard and blocklists.
It answers the names it blocks and
hands the rest to an upstream you
choose. What it does that Unbound
doesn't: the filtering, the lists, the
pretty graphs. What Unbound does that
it doesn't: the recursion itself —
Pi-hole has no iterator, so its
upstream choice *is* its answer's
pedigree. That is why the pairing in
chapter 11 is the standard stack, and
why this series has a
[Pi-hole guide](https://paulsullivan33-dev.github.io/pi-hole-for-mere-mortals/)
of its own.

**AdGuard Home.** The same chair as
Pi-hole, plus two differences that
matter: it can itself recurse-adjacent
tricks via parallel upstreams, and it
speaks encrypted DNS (DoH/DoT) to
clients out of the box. If you want
filtering and encrypted *client*
access in one program, it is the
neighbour to visit; if you want the
resolver itself to be a small,
single-purpose daemon, Unbound stays
the shape.

**dnsmasq.** The home router's classic:
a lightweight forwarder that also does
DHCP and reads your `/etc/hosts` as
DNS. It is probably running on your
router right now. It forwards rather
than recurses, and its DNSSEC support
is a client of someone else's
validation. For one small box doing
three jobs adequately it has no
rival; Unbound replaces only its DNS
third, and only when you want the
real thing.

**systemd-resolved.** Not a resolver
but a *stub*: a tiny listener on
127.0.0.53 that receives your own
machine's questions and hands them to
the real resolvers your network
announced. It is the reason a desktop
can have "something on port 53" that
isn't a server. Unbound and resolved
coexist by pointing resolved *at*
Unbound — or by letting resolved own
the desktop's questions and running
Unbound for the network instead. (The
[systemd guide](https://paulsullivan33-dev.github.io/systemd-for-mere-mortals/)
covers its service side.)

**BIND 9 and Knot Resolver.** The
full-service servers. BIND can be
authoritative *and* recursive in one
daemon, with views, transfers and
forty years of operational folklore;
Knot Resolver is a modern, modular
recursive resolver with a Lua
configuration language. Both are
excellent; both are more machinery
than a household's questions need.
Unbound's pitch against them is
narrowness: one job, one file, a
small default surface.

**The public resolvers** — Cloudflare
1.1.1.1, Google 8.8.8.8, Quad9 9.9.9.9.
Not software but *services*, and the
real neighbour Unbound competes with.
They are fast, global, and free; Quad9
adds threat filtering, Cloudflare
publishes a strict privacy policy and
audits it. What they have that
Unbound never will: someone else's
24-hour operations team. What you
have with Unbound that they cannot
offer: chapter 1's trade, taken the
other way. Neither choice is naive;
this guide exists so the choice is
informed.

And beneath them all, the subject
itself has a guide in this series:
[DNS for Mere Mortals](https://paulsullivan33-dev.github.io/dns-for-mere-mortals/)
covers the name system end to end,
of which resolving is one act.
