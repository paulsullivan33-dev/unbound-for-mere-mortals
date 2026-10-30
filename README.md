# Unbound for Mere Mortals

Every name your computer uses — every
website, mail server and update check —
starts as a question: *what address
belongs to this name?* The familiar way
to get that answer is to ask a big
company's resolver: your internet
provider's, or a public service run by
Google or Cloudflare. It works well. It
also means that company sees every name
you look up, and you take their answer
on trust. **Unbound** is the same job
with the middleman removed. It is a
resolver that runs on your own machine
or your own little server, walks the
DNS itself from the roots down, checks
the answers cryptographically with
DNSSEC, remembers them in a cache, and
answers your network's questions
locally.

This guide explains how a resolver
works, how to install Unbound, how its
one config file is put together, and
how to give your own machines names it
answers for. Then it does something
most resolver guides skip: it **proves**
the cache works — with a stand-in
upstream whose log shows exactly when
Unbound went asking and when it
answered from memory instead.

The lab that wrote this guide ran the
real thing: **Unbound 1.19.2**, the
Ubuntu 24.04 package, on a small Linux
machine. Against it the lab defined
local names and read its answers,
watched a name come back NXDOMAIN from
a static zone and REFUSED from a refuse
zone, reversed an address to its name,
counted an upstream's queries to prove
a cache hit, caught prefetch refreshing
an answer seconds before it expired,
killed the upstream and watched an
expired answer served anyway, and
flushed one name out of the cache to
see it fetched fresh.

What the lab could not do, it did not
fake. Its sandbox refuses all outgoing
UDP and resets direct connections to
the internet, so Unbound's walk from
the real root servers starts — the
log shows it reaching for the roots by
name and address — and is cut off
there. Real recursion on the public
internet, and DNSSEC validation of
public names, are therefore taught
from the documentation and labelled as
such wherever they appear.
`criteria.md` keeps the full ledger of
what was run and what was only read.

## What this guide covers

- [**What Unbound is**](what-unbound-is.md) —
  the mental model: a question in, an
  address out, and who sees the question
- [**The moving parts**](the-moving-parts.md) —
  the daemon, the cache, the iterator
  that walks the DNS, the validator
  that checks signatures, and the
  control channel
- [**Installing Unbound**](installing-unbound.md) —
  the package, the version check, and
  the config check that proves it can
  start
- [**The config file**](the-config-file.md) —
  one file, four kinds of clause,
  walked through line by line with the
  lab's working config
- [**Your first answers**](your-first-answers.md) —
  starting the daemon, reading a `dig`
  answer in detail, and the local
  names the lab defined
- [**Names for your network**](names-for-your-network.md) —
  serving a household: who may ask,
  choosing a private zone, and the
  warnings that come with it
- [**The cache at work**](the-cache-at-work.md) —
  TTLs counting down, a miss and a hit
  counted at the upstream, prefetch,
  and answers served past their expiry
- [**DNSSEC — checking the answers**](dnssec.md) —
  the chain of trust, the root anchor,
  and what a failed check looks like
- [**Forwarding on purpose**](forwarding-on-purpose.md) —
  when handing questions to another
  resolver is the right design, forward
  zones, stub zones, and encrypted
  upstreams
- [**Running it well**](running-it-well.md) —
  the control channel, reading the
  counters, and logging without
  drowning or spying
- [**Recipes**](recipes.md) — the
  Pi-hole pairing, one blocked name,
  a stub for the router's zone, and a
  starter set of house names
- [**The neighbours**](the-neighbours.md) —
  Pi-hole and AdGuard Home, dnsmasq,
  systemd-resolved, BIND, and the
  public resolvers: what each does
  that Unbound doesn't, and vice versa
- [**Limits**](limits.md) — no public
  zone hosting, no blocklists or web
  page of its own, and the failures it
  answers with one word
- [**Troubleshooting**](troubleshooting.md) —
  the config error with a line number,
  the special TLDs that never leave,
  the answer that will not die, and
  SERVFAIL's favourite cause
- [**Glossary**](glossary.md) — the
  terms, collected in one place

## What it doesn't cover

Hosting your public domain's DNS —
Unbound is a resolver, not an
authoritative server, and chapter 13
is plain about the difference.
Blocking adverts by itself: Unbound
has no blocklists; that is the
Pi-hole pairing in chapter 11, or the
single-name refuse in the recipes.
Running a resolver for the public
internet: chapter 1 explains why an
open resolver is a hazard, and this
guide never sets one up.

## How to use this guide

Read chapter 1 for the model and
chapter 2 before installing anything —
knowing which part does what turns
later confusion into a named problem.
Chapters 3 to 5 get you a running
resolver answering names you defined,
which is a complete result on its own.
Chapter 7 is the one to read slowly:
its method — count what the other end
saw — is how you check any resolver's
claims, including this guide's. The
lab's transcripts live in
`unbound-lab/transcripts/`; its config
is `unbound-lab/unbound.conf` and its
stand-in upstream is
`unbound-lab/fake-upstream.py`.

---

## Part of the series

This guide is one of the [For Mere Mortals](https://paulsullivan33-dev.github.io/mere-mortals/) guides: plain-language guides to the tools programmers and makers use.

Related guides:

- [DNS for Mere Mortals](https://paulsullivan33-dev.github.io/dns-for-mere-mortals/)
- [Pi-hole for Mere Mortals](https://paulsullivan33-dev.github.io/pi-hole-for-mere-mortals/)
- [Networking for Mere Mortals](https://paulsullivan33-dev.github.io/networking-for-mere-mortals/)

## License

The writing in this guide is licensed under [CC BY 4.0](https://github.com/paulsullivan33-dev/unbound-for-mere-mortals/blob/main/LICENSE). Code examples and lab scripts are licensed under the [MIT License](https://github.com/paulsullivan33-dev/unbound-for-mere-mortals/blob/main/LICENSE-CODE).
