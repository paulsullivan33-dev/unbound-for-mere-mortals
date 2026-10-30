# The Cache at Work

The outcome: cache behaviour you do
not have to take on faith — a miss, a
hit, a prefetch and a rescue, each
counted at the place that would know.

A cache claim is easy to make and hard
to check from the client's chair: a
fast second answer might be memory, or
might just be a fast network. The
lab's method removes the doubt. It ran
a **stand-in upstream** — a small
program of the lab's own, kept at
`unbound-lab/fake-upstream.py` — that
answers one private zone and *logs
every query it receives*. A
`forward-zone` in Unbound's config
sent that zone to it. Then "did
Unbound go upstream?" is a line count,
not an impression. Everything in this
chapter is from
`unbound-lab/transcripts/t04-caching.txt`.

## The miss and the hit

The stand-in answers `www.lab` with
the address 203.0.113.7 and a lifetime
(TTL) of **120 seconds**. First ask:

```text
$ dig ... www.lab A
www.lab.		120	IN	A	203.0.113.7
$ cat upstream.log
22:28:31 qtype=1 name=www.lab.
```

One query in the log: a **cache miss**.
Unbound had nothing, so it fetched —
and kept the answer, the address
*and* the 120 seconds together.

Five seconds later, the same ask:

```text
$ sleep 5; dig ... www.lab A
www.lab.		115	IN	A	203.0.113.7
$ wc -l < upstream.log
1
```

The log has not grown, and the answer
reports **115**: Unbound serves the
*remaining* lifetime, counting down,
so no client mistakes a five-second-old
answer for a fresh 120. That countdown
is the cache's honesty mechanism, and
both halves of the proof — no upstream
query, a smaller TTL — are worth
looking for whenever you test a
resolver. Unbound's own counters agree
(`t04`): after these two asks,
`total.num.cachemiss=1`,
`total.num.cachehits=1`.

Why it matters beyond speed: while an
answer lives in cache, upstream
trouble — a cut cable, a rebooting
server — is invisible to your clients,
and the root and authoritative servers
are spared a question they already
answered. TTLs are set by each name's
owner, not by Unbound; the resolver's
job is to honour them exactly, neither
dropping early nor holding on late.
(The two knobs that bend that rule on
purpose are the rest of this chapter.)

## Prefetch: refreshing before the funeral

The stand-in's second name, `short.lab`,
lives only **12 seconds**. Ask once
(miss, logged), wait eleven, ask
again. The answer comes back with TTL
**1** — a hit, served from cache a
second before death. But an ask that
arrives in an answer's last moments —
the final tenth of its life — makes
Unbound do more:

```text
$ wc -l < upstream.log
3
```

A *third* upstream query, which no
client sent: the **prefetch**. Unbound
refetched the answer in the
background, so the next ask — two
seconds later, after the original
would have died — returns a lively
TTL of 10, and the clients never
waited on a fetch at all. That is
`prefetch: yes`: one wasted upstream
query per popular name, traded for no
client ever paying the miss. On a busy
resolver it is nearly free; it is off
by default, and the lab turned it on
to show it.

## Serve-expired: the rescue

Immediately after, the lab killed the
stand-in outright and waited out the
TTL. Then:

```text
$ dig ... short.lab A
short.lab.		30	IN	A	203.0.113.8
$ grep -c . upstream.log
3
```

An answer — for a name whose only
source no longer exists. That is
`serve-expired: yes`: when a refresh
fails, Unbound serves the expired
answer rather than telling the client
SERVFAIL. Notice the TTL of **30**:
the served-past-expiry answer gets a
small fixed lifetime (the default
cap), so clients treat it as the
short-lived stand-in it is, and
Unbound keeps retrying the refresh in
the background. It is a deliberate,
labelled bending of the TTL rule —
a stale address is usually better
than no address — and it is also off
by default, because for some networks
a wrong answer is worse than none.
Both knobs live in `server:` in the
config (chapter 4); the guide's
opinion is that a home network wants
both on, and should know it chose.

## The first attempt, kept

Honesty requires the chapter's
footnote: the zone was first named
`lab.test`, and every ask returned
NXDOMAIN without a single upstream
query. The AUTHORITY section named
the culprit — `test.` is one of the
special-use endings Unbound answers
from a built-in local zone (`.test`,
`.invalid`, `.example`, `.localhost`
can never exist on the public
internet, so asking out would be
wrong). The zone was renamed `lab`
and the chapter rerun. When your own
forwarding is silently ignored, check
the name's ending first — chapter 14
keeps this story for exactly that
reason.
