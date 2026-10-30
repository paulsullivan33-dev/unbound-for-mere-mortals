# Running It Well

The outcome: a running Unbound you can
interrogate — what it holds, what it
has done, whether it is healthy — and
a logging setup that tells you what
you need without building an archive
of your household's questions.

## The control channel

`unbound-control` is the operator's
handle from chapter 2. On a
distribution install it talks to the
daemon over an encrypted localhost
socket whose certificates
`unbound-control-setup` creates; in
the lab it used a plain unix socket in
the lab directory, which the config's
`remote-control:` clause arranges:

```yaml
remote-control:
    control-enable: yes
    control-interface: ".../control.sock"
    control-use-cert: no
```

The commands on a real install need
the certificates (run it as root, or
via `sudo`); the commands themselves
are the same. The four the lab used
constantly, all from `t06` and
earlier transcripts:

```text
$ unbound-control -c unbound.conf list_local_data
... (what chapter 5 read)

$ unbound-control -c unbound.conf flush www.lab
ok
$ dig ... www.lab A        (a miss again: fetched fresh, TTL back at 120)
www.lab.		120	IN	A	203.0.113.7
```

**`flush`** is the one to learn first:
it removes one name from the cache,
which is the correct answer to "I
changed the record but the old answer
won't die" — the record's TTL, not
Unbound, was keeping it alive.
`flush_zone` does a whole zone;
`reload` rereads the config without
dropping the cache; `stop` is the
tidy shutdown the lab finished with,
after which the same dig that worked
all day reports, honestly,
`connection refused`.

## Reading the counters

```text
$ unbound-control -c unbound.conf stats_noreset
total.num.queries=8
total.num.cachemiss=4
total.num.prefetch=2
total.num.recursivereplies=4
```

(`stats_noreset` reads without zeroing;
plain `stats` resets as it reports —
pick deliberately.) The handful worth
watching on a home resolver, all of
which the lab's runs exercised:
**queries** (how much you ask),
**cachehits/cachemiss** (how much of
it was memory — a healthy home cache
answers most asks from memory),
**prefetch** (chapter 7's background
refreshes, counted), and in the full
output, the histogram of reply times
and `unwanted` counts of refused
traffic. A resolver whose cachemiss
equals its queries is a resolver whose
cache is not working — usually because
something restarts it constantly, and
each restart starts the cache empty.

## Logging without drowning — or spying

`verbosity:` is the volume knob, 0 to
5. The working range is small:

- **0–1** — errors and start/stop
  notices. The lab ran at 1, and its
  log is the one quoted in chapter 8:
  a page of startup notices, then
  silence except real failures. This
  is the right setting for a machine
  that must run for months.
- **2** — adds the signature
  *failures* (which name failed
  validation, and why) — worth raising
  to when chapter 14 sends you hunting
  a bogus zone, then putting back.
- **3 and up** — the iterator's diary,
  query by query. For an afternoon's
  debugging, fascinating; as a steady
  state, a disk-filling machine.

One option deserves a decision, not a
default: `log-queries: yes` writes
every question asked. On your own
resolver that log is the complete list
chapter 1 worried about, in your own
hands — which is either the point
(debugging a device's chatter) or a
liability (an archive nobody needs).
Leave it off unless you are actively
looking for something, and delete the
results when you have found it.

## The small rituals

Three habits keep a home resolver
boring, which is praise: run
`unbound-checkconf` after every edit
(chapter 3's gate); glance at the
counters monthly — mostly to learn
what normal looks like before the day
it isn't; and let the distribution
update the package, since the root
anchor and hints it ships are data
with birthdays (chapter 8). Everything
else in this chapter is for the day
something feels wrong — and chapter 14
is for naming what.
