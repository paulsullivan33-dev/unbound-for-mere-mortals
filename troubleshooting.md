# Troubleshooting

The failures the lab met for real are
marked with their transcript; the rest
are the documented shapes of the same
trouble, in roughly the order a new
operator meets them.

## Unbound will not start, and says almost nothing

Run the checker first — it is rarely
silent:

```text
$ unbound-checkconf
.../unbound.conf:3: error: unknown keyword 'verbosit'
read .../unbound.conf failed: 3 errors in configuration file
```

(`t02`, for a misspelling; a bad value
reads `error: port number expected`.)
The checker gives the file and the
line; fix that line, re-check, then
restart. If the config is clean but
the service still dies, the cause is
usually the **port**: something
already owns 53 — very often
`systemd-resolved`'s stub on
127.0.0.53, or a second resolver from
an earlier experiment.
`sudo ss -lunp | grep :53` names the
owner; either stop it, or bind
Unbound to a different address/port
deliberately (chapter 6), never by
killing strangers.

## A name is answered that you never defined — or not answered that you did

Check who answered before anything
else: dig's `;; SERVER:` line (chapter
5). Half of all DNS mysteries are a
client quietly using a different
resolver — a browser's built-in DoH,
a DHCP lease from before your change,
a phone on mobile data. If the server
*is* yours, ask it what it holds:
`unbound-control list_local_data` for
definitions, and a plain dig for the
cache's current answer, TTL included.

## The special ending that swallows everything

You built a forward zone for a test
name and every answer is NXDOMAIN,
with no query ever reaching the
upstream. The lab did this
(`t04`): names under `.test`,
`.invalid`, `.example` and
`.localhost` are answered from
Unbound's **built-in local zones** —
those endings cannot exist on the
public internet, so Unbound correctly
refuses to forward them anywhere.
`unbound-control list_local_zones`
shows the set. Rename the test zone
to something undelegated but not
special (the lab used `lab`), or use a
name under a domain you control.

## The answer that will not die

You changed a record; clients still
get the old one. That is the cache
honouring the *old answer's TTL*
(chapter 7) — working as designed,
not stuck. Two honest exits: wait out
the remaining TTL dig shows you, or
`unbound-control flush <name>` and
ask again (the lab's `t06` shows the
TTL jump back to full on the refetch).
For next time, lower the record's TTL
a day *before* you plan to change it.

## Everything is SERVFAIL, all of a sudden

Suspect the clock before the network
(chapter 8): DNSSEC signatures are
only valid inside their time windows,
and a machine that wakes up believing
it is last Tuesday calls every signed
answer a forgery. `timedatectl` shows
the truth. After the clock, suspect
one zone, not the sky: use
`delv @127.0.0.1 <name>` (from the
BIND utilities) to see the validation
verdict in words, raise `verbosity: 2`
briefly for the validator's own
account, and check whether the zone's
operator has announced an expired
signature — a failure mode common
enough to have its own monitoring
sites. A bogus answer is Unbound
*working*; the fix belongs to the
zone, the clock, or your
`domain-insecure` list, never to
turning validation off.

## REFUSED, from your own resolver

Your clients are outside your
`access-control` lines (chapter 6) —
a new subnet, a VPN range, the
machine's second address — or they
are hitting a `refuse` local-zone you
wrote and forgot (recipe 2's dated
comment exists because of this entry).
`list_local_zones` and the config
file, read fresh, settle which.

## "Connection refused" after it worked yesterday

The daemon is not running: someone —
a package update, a tidy operator
with `unbound-control stop` (the lab
ends `t06` in exactly this state), a
reboot without the service enabled —
stopped it. `systemctl status unbound`
says which story it was, and
`sudo systemctl enable --now unbound`
is the ending where it does not
happen again.
