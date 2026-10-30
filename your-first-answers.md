# Your First Answers

The outcome: Unbound running, and a
page of its answers you can read line
by line — each status word met in the
wild, not just defined.

The lab starts its instance directly
(the service route is chapter 3's
`systemctl` line; the behaviour is the
same):

```bash
$ unbound -c unbound.conf
$ cat unbound.pid
68096
```

Questions are asked with `dig`, the
standard DNS tool (in the `dnsutils`
package, if your machine lacks it).
One lab habit needs explaining before
the first answer: every query here is
`dig +tcp`. DNS normally travels on
UDP, with TCP for large answers, and
on your network plain `dig` is fine.
The lab's sandbox refuses UDP sends
entirely — even between two programs
on the same machine (`t01`) — so the
lab asks over TCP throughout. The
answers are identical either way.

Also note the address: the lab's
Unbound listens on 127.0.0.1, port
18086, so every question is aimed with
`-p 18086 @127.0.0.1`. Yours will be
`-p 53` on whatever address you bound.

## One answer, read in full

```text
$ dig +tcp -p 18086 @127.0.0.1 printer.home.arpa A

;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 3979
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; QUESTION SECTION:
;printer.home.arpa.		IN	A

;; ANSWER SECTION:
printer.home.arpa.	3600	IN	A	192.168.1.50

;; Query time: 0 msec
;; SERVER: 127.0.0.1#18086(127.0.0.1) (TCP)
```

Read it as a receipt. **status:
NOERROR** — the question was answered.
The **flags**: `qr` (this is a
response), `aa` (authoritative answer
— Unbound *is* the authority for this
name, because the lab defined it),
`rd ra` (recursion was desired, and is
available). The **ANSWER SECTION** is
the payload: the name, its remaining
lifetime in seconds, class `IN`, type
`A`, and the address. **SERVER:** names
who actually answered — the line to
check first whenever a reply surprises
you, because it proves which resolver
you really asked. Nothing left the
machine; Query time is 0 msec.

## The other four answers

From here the transcripts use dig's
compact form (`+noall +comments
+answer`); all four are real, from
`unbound-lab/transcripts/t03-local-answers.txt`.

A second defined name behaves exactly
like the first — `nas.home.arpa`
answers 192.168.1.60. The interesting
answers are the refusals and the
empties:

**NODATA.** Ask for a type that does
not exist at a name that does:

```text
$ dig ... printer.home.arpa AAAA
;; status: NOERROR ... ANSWER: 0
```

NOERROR with an empty answer section
is not an error at all: the name is
real, it simply has no AAAA record.
Clients read this correctly as "no
IPv6 address here" and move on.

**NXDOMAIN.** Ask inside a `static`
local zone for a name nobody defined:

```text
$ dig ... unknown.home.arpa A
;; status: NXDOMAIN ... ANSWER: 0
```

The static zone is a promise — *my
list is complete* — so an unlisted
name is answered "does not exist",
authoritatively, instead of being
passed on to the internet (where, for
`home.arpa`, it should never be asked
anyway). The same shape appears for
`other.example.internal`, the lab's
second static zone, while its defined
`wiki.example.internal` answers
192.168.1.70.

**REFUSED.** The lab's third zone,
`ads.example`, is typed `refuse`:

```text
$ dig ... tracker.ads.example A
;; status: REFUSED ... ANSWER: 0
```

Not "does not exist" but "I will not
answer that" — the whole zone, every
name under it, refused in one line of
config. Chapter 11 turns this into a
single-purpose recipe.

**The way back.** `local-data-ptr`
gave the printer a reverse record, and
the reverse question is answered from
it:

```text
$ dig ... -x 192.168.1.50
50.1.168.192.in-addr.arpa. 3600 IN PTR printer.home.arpa.
```

Finally, the daemon's own view of what
it holds, through the control channel:

```text
$ unbound-control -c unbound.conf list_local_data | grep -E "home\.arpa|example\.internal"
nas.home.arpa.		3600	IN	A	192.168.1.60
printer.home.arpa.	3600	IN	A	192.168.1.50
50.1.168.192.in-addr.arpa. 3600	IN	PTR	printer.home.arpa.
wiki.example.internal.	3600	IN	A	192.168.1.70
```

(The unfiltered list also carries the
built-in localhost zones Unbound always
serves.) You now have a resolver that
answers for names you chose, in all
four voices a resolver has: *here it
is*, *nothing there*, *no such name*,
and *not telling you*. Chapter 6 puts
it to work for a whole network.
