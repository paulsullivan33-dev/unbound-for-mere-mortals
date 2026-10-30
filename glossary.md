# Glossary

**Access control** — Unbound's
per-client-address policy
(`access-control:`): which subnets may
ask, and whether the rest are refused
or silently denied.

**Authoritative server** — the server
that *owns* a zone's records and
answers for them finally. Unbound asks
them; it is not one (except for its
own local zones).

**Bogus** — DNSSEC's verdict on an
answer whose signatures do not check
out. A validating resolver answers
SERVFAIL instead of passing it on.

**Cache** — a resolver's memory of
answers and directions, each kept
exactly as long as its owner's TTL
allows.

**Cache hit / cache miss** — an answer
served from memory, versus one that
had to be fetched. Counted separately
in Unbound's statistics.

**DNSSEC** — the signature system that
lets a resolver verify an answer's
authenticity: RRSIG signatures, DNSKEY
keys, DS hashes in the parent zone.

**DoH / DoT** — DNS over HTTPS (port
443) and DNS over TLS (port 853):
encrypted transports for the same
questions and answers.

**Domain-insecure** — a config
statement exempting one named zone
from DNSSEC checking — the correct
tool for private zones the public
chain of trust has never heard of.

**Forwarding** — handing a question to
another *resolver* to answer
(`forward-zone:`), instead of walking
the DNS oneself.

**Iterator** — Unbound's walking
module: roots to TLD to authority,
one referral at a time.

**Local zone / local data** — names
and areas Unbound answers from its own
config: `local-data:` records inside
`local-zone:` areas typed static,
refuse, transparent and kin.

**NODATA** — NOERROR with an empty
answer: the name exists, the type
asked for does not. Not an error.

**NXDOMAIN** — the status meaning
*this name does not exist*.

**Prefetch** — refreshing a cached
answer in the background when a query
arrives in the last tenth of its TTL,
so the next asker never waits.

**QNAME minimisation** — asking each
server only for the part of the name
it needs to see. Unbound does it by
default.

**Recursion** — resolving a name fully
oneself, walking from the roots down.
The opposite posture to forwarding.

**REFUSED** — the status meaning *I
will not answer that*: a refuse zone,
or an access-control refusal.

**Resolver** — the program that takes
a name question and returns the
answer: Unbound, in this guide.

**Root hints** — the small file naming
the root servers' addresses; where
every walk begins.

**Root trust anchor** — the hash of
the root zone's key, held locally;
the first link of every DNSSEC chain
of trust.

**Serve-expired** — serving an answer
past its TTL when refreshing it has
failed, with a small capped TTL of
its own.

**SERVFAIL** — the status meaning
*the lookup failed*: unreachable
authorities, or an answer the
validator called bogus.

**Stub zone** — a zone whose
*authoritative* servers are named in
the config (`stub-zone:`), where
Unbound starts its walk.

**TTL** — time to live: the lifetime,
in seconds, an answer's owner grants
it. Caches serve the remaining time,
counting down.

**Validator** — Unbound's checking
module: verifies DNSSEC chains from
the root anchor down to the answer.
