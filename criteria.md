# Writing criteria for this guide

Every "for Mere Mortals" guide is written to the same nine-point
standard, so a reader who trusts one can trust the rest. Here it
is, with the verification notes for this particular guide below.

1. **Fix it first.** Reader outcomes lead, not action items: each
   chapter opens by naming the outcome it delivers, shows a check
   the reader can run to confirm they got it, and a reasonable
   reader finishes able to state what was done, what it means,
   and what to try next.
2. **Plain language.** Short sentences, everyday vocabulary,
   technical terms defined on first use. No slang, and no
   idioms that only make sense in one country — the reader may
   be translating as they go.
3. **No dead ends.** A guide never tells the reader to do
   something it cannot show them how to verify. Every claim a
   reader relies on — an install, a command, an output — is
   something this guide demonstrates or clearly labels
   documented-only below.
4. **Live-verified where it matters.** Procedures are run for
   real in the guide's lab wherever the build machine allows it,
   and the transcripts kept in the repository are the evidence.
   What could not be run is listed honestly below, never
   presented as if it had been.
5. **General audiences.** Nothing in this guide — examples,
   fixtures, names, addresses — is modelled on any particular
   reader or author's real life, network, or organisations.
   The lab's devices are a generic printer and NAS; its upstream
   answers use the documentation-only TEST-NET-3 range.
6. **Standalone.** A reader needs this guide, its lab, and
   nothing else. Where another guide would genuinely help, it
   is pointed to once, by name, and the chapter still completes
   without it.
7. **Honest about limits.** Chapter 13 names what the tool
   cannot do: no authoritative service, no filtering of its
   own, TTLs it will not edit, validation that fails closed,
   no DNS-over-HTTPS upstream, and no answers at all when the
   network will not let it walk. The lab's own ceiling is
   named in chapter 8 and itemised below.
8. **The ethics rule is in the text, early.** A resolver sees
   every name its clients look up, so chapter 1 draws the line
   before any procedure depends on it: run one for yourself and
   your household, never as an open service for strangers, and
   chapter 10 treats logging every query as a decision to make
   on purpose, not a default to inherit.
9. **Builds clean.** The site builds with MkDocs in strict mode
   with no warnings, and a fresh reader following the chapters
   in order reaches the stated outcome of each.

## Verification notes for this guide

The build machine is a small Ubuntu 24.04 sandbox shared with
other work throughout (timings in the transcripts are the
lab's own, not benchmarks). Unbound **1.19.2** (Ubuntu package
1.19.2-1ubuntu3.12) was the subject. The sandbox's package
manager lock was held by another tenant's `apt-get`, so the
lab downloaded the identical distribution packages with
`apt-get download` — `unbound`, `libunbound8`, `unbound-anchor`
and `dns-root-data` (2024071801), plus `libhiredis1.1.0` and
`libprotobuf-c1`, the two dependencies not already present —
and unpacked them unmodified with `dpkg -x` into a scratch
tree, running the binaries from there through thin wrappers
that set `LD_LIBRARY_PATH`. Same publisher, same version,
same files; only the prefix differs. On a reader's machine
`apt install unbound` is the route, and chapter 3 says so.
Every transcript lives in `unbound-lab/transcripts/`; the
config they all use is `unbound-lab/unbound.conf`; the
stand-in upstream is `unbound-lab/fake-upstream.py`.

The lab ran the daemon on 127.0.0.1, port 18086 only, with the
control channel on a unix socket in the lab directory. All
client queries were made with `dig +tcp`, for the reason the
next paragraph gives.

**The sandbox boundary, measured, not assumed.** The sandbox
refuses every UDP send at the system-call level — a minimal
Python round trip between two programs on the same loopback
interface dies with `PermissionError: [Errno 1] Operation not
permitted` on the `sendto()` (t01). TCP to the outside fares
no better: Unbound's own attempts to reach the root servers
are answered `Connection reset by peer`, against their real
addresses out of the hints file (t05). So there is no path
from this lab to the public DNS at all, and everything in the
guide that needs one is documented-only, listed below.
Everything that does *not* need one was run for real:

- Install route, package identity and `unbound -V`, including
  its compiled module list (t00).
- The root trust anchor read from the tool itself
  (`. IN DS 20326 8 2 E06D44B8…`) and matched against the
  `dns-root-data` package's `root.key` (root DNSKEYs, keytags
  20326 and 38696); `unbound-anchor`'s online repair attempted
  and its refusal kept verbatim — "the anchor is NOT ok and
  could not be fixed" — because verification needs the network
  the sandbox withholds (t02).
- `unbound-checkconf` passing the lab config, and failing two
  deliberately broken ones with the exact messages and exit
  codes the guide quotes (t02).
- Local service, complete: `local-data` A answers with the
  `aa` flag, an AAAA ask answered NODATA, undefined names in
  two `static` local zones answered NXDOMAIN, every name in a
  `refuse` zone answered REFUSED, a `local-data-ptr` reverse
  answer, and `list_local_data` read back through the control
  channel (t03).
- Caching, proven against the lab's own stand-in upstream
  (a forward-zone target on 127.0.0.1:18087 that logs every
  query it receives): a miss and a hit told apart by the
  upstream's log (1 query) and by the TTL counting down
  120 → 115, with Unbound's counters agreeing
  (cachemiss 1, cachehits 1); prefetch firing in an answer's
  last tenth (a third, unprompted upstream query; the next
  ask served at TTL 10); and serve-expired returning an
  answer — at the capped TTL of 30 — after the upstream was
  killed and the entry had expired (t04).
- The boundary itself: `example.com` asked of the real
  configuration returns SERVFAIL, and the daemon log shows
  the iterator reaching for a, b, c, g and i root servers
  over TCP port 53 and being reset, five times over (t05).
- The control channel: `flush` emptying one name (its next
  answer fetched fresh, TTL back at 120), the statistics
  counters after the day's asks (8 queries, 4 misses, 2
  prefetches), and a clean `stop`, after which the port
  refuses connections (t06).

One accident is kept in the record rather than tidied away:
the lab's private zone was first named `lab.test`, and every
query for it returned NXDOMAIN with no upstream traffic at
all — `.test` is one of the special-use endings Unbound
answers from built-in local zones (`list_local_zones` shows
`test. static`, `invalid. static`, `localhost. redirect`).
The zone was renamed to the undelegated, non-special `lab`
and the caching evidence above was gathered under that name
(t04 keeps both attempts).

Documented only — described from NLnet Labs' documentation
and the tool's own manuals, not run, and the text does not
claim otherwise:

- Successful recursion on the public internet, and with it
  end-to-end DNSSEC validation of public names (including the
  `dnssec.works` check chapter 8 offers the reader to run).
  The anchor, the priming and the attempts are real (t02,
  t05); the successful walk is not the lab's to show.
- Encrypted upstreams (DNS over TLS), and serving DoT/DoH to
  clients.
- `stub-zone` against a real authoritative server (the
  router pattern in chapters 9 and 11); the forward-zone
  mechanism it resembles is live-verified (t04).
- Serving other machines over a LAN — chapter 6's binding and
  access-control lines are the same mechanisms the lab
  verified on loopback ranges, but no second machine existed
  to ask from.
- Pi-hole itself (chapter 11's recipe describes the pairing;
  Pi-hole was not installed), `delv`, and unattended service
  operation under systemd beyond the commands quoted.
- The neighbours of chapter 12 — characterised, not run or
  benchmarked.

Fixtures are this guide's own and deliberately generic: a
printer and a NAS on `home.arpa` (RFC 8375), a throwaway
second zone, and upstream answers in 203.0.113.0/24 —
TEST-NET-3 (RFC 5737), reserved for documentation and never
routed. No real organisation, network or person is modelled.
