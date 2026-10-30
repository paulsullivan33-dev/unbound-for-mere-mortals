# Names for Your Network

The outcome: Unbound answering for a
household — listening on a network
address, answering only your clients,
and giving the machines down the hall
names instead of numbers.

Chapter 5's resolver answered one
machine. Serving a network changes
three lines:

```yaml
server:
    interface: 192.168.1.2        # the server's own LAN address
    access-control: 192.168.1.0/24 allow
    access-control: 0.0.0.0/0 refuse
```

**`interface:`** is where questions
arrive. Binding the LAN address (not
just loopback) is the step that makes
it a network service — and the step to
take deliberately, because before it,
nothing outside the machine *can* ask.
Binding `0.0.0.0` listens on every
address the machine has, including
any it gains later; naming the one
address is the tidier habit.

**`access-control:`** is who may ask,
decided by the client's address. The
pair of lines above is the shape this
guide recommends: allow your own
subnet, refuse everyone else, in that
order — the first match wins. The
actions are `allow` (answer),
`refuse` (answer REFUSED, as chapter 5
saw), and `deny` (drop the question
silently, for clients whose existence
you do not want to confirm). On a home
network, allow-your-subnet and a
default refuse is the whole policy.
Unbound's out-of-the-box default
already refuses non-local clients;
these lines make the intent explicit
and survive being copied to a machine
whose defaults differ.

Then the clients must be *told*. The
usual route is your router's DHCP
settings: the place that hands out
addresses also hands out "your DNS
server is…", and pointing that at
Unbound's address recruits every
device that joins the network, phones
and televisions included. Setting one
device by hand — its network settings
take a manual DNS address — is the way
to try it on yours alone first.

## Choosing your private ending

Local names need a last part that is
yours. Use **`home.arpa`**. It exists
for exactly this (RFC 8375), it is
guaranteed never to be a public
ending, and resolvers treat it as
special: Unbound will not leak
`home.arpa` questions to the internet,
and chapter 5's static zone answers
unlisted names NXDOMAIN on the spot.
The names you grew up with are traps
by comparison: `.local` belongs to
mDNS (the Bonjour/Avahi world) and
mixing the two causes intermittent,
baffling behaviour; `.lan`, `.home`
and `.internal` are folk practice —
widely used, and with no guarantee a
future public ending won't collide
with them. (The lab used
`example.internal` as a throwaway
second zone, labelled as lab
furniture, not advice.)

Inside the zone, name things after
what they are, and add the reverse
records while each is fresh:

```yaml
    local-zone: "home.arpa." static
    local-data: 'printer.home.arpa. 3600 IN A 192.168.1.50'
    local-data-ptr: '192.168.1.50 3600 printer.home.arpa.'
    local-data: 'nas.home.arpa. 3600 IN A 192.168.1.60'
    local-data-ptr: '192.168.1.60 3600 nas.home.arpa.'
```

Give devices fixed addresses first
(a DHCP reservation on the router), so
the names cannot drift away from the
numbers. Reload with a check —
`unbound-checkconf`, then restart or
`unbound-control reload` — and ask
once per name with `dig` from *another*
machine before declaring victory.

## The warnings that come with it

**You are now infrastructure.** When
this resolver stops, every client
pointed at it loses names, which
presents as "the internet is down".
Run it on a machine that stays on,
and know the stop command (chapter
10) before you need the start one.

**Never expose it.** If the machine
also faces the internet — a port
forwarded, a cloud VM — port 53 must
not be open to the world. An open
resolver is abused for amplification
attacks and lands its operator on
blocklists; chapter 1's rule is a
working rule, not a nicety. The
access-control lines
above are the second lock; keeping
the port off the internet is the
first.

**Split answers are a feature you now
own.** `nas.home.arpa` resolving at
home and nowhere else is the point —
but the same mechanism means a name
can answer differently here than
anywhere else, and future confusion
("it works on my phone's data but not
on Wi-Fi") starts with forgetting you
did that. The list of your definitions
is one `list_local_data` away; keep
it short and current.
