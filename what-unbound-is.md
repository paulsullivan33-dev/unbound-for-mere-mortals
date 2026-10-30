# What Unbound Is

You type a name — a website, a mail
server, a printer down the hall — and
your computer needs a number: the IP
address where that name can be reached.
The system that turns names into
addresses is the **DNS**, and the
program that does the asking on your
behalf is called a **resolver**. Almost
every question your computer ever asks
is answered by a resolver somebody else
runs: your internet provider's, your
router's, or a public one such as
Google's 8.8.8.8 or Cloudflare's 1.1.1.1.

**Unbound is a resolver you run
yourself.** It is a program — written
by NLnet Labs, the Dutch non-profit
that also minds several DNS standards
— that listens for name questions on
your own machine or a small server on
your network, and answers them. It does
not keep a copy of the internet's phone
book; there isn't one to keep. Instead
it *walks*: starting from the root
servers at the top of the DNS, it asks
its way down, name part by name part,
until an authoritative server gives it
the answer. Then it checks the answer's
signature, remembers it for a while,
and hands it to you.

Three words describe it, and each one
earns its place. **Recursive**: it does
the whole walk itself, however many
servers that takes. **Validating**: it
checks DNSSEC signatures, so a forged
answer is recognised and refused rather
than passed on. **Caching**: every
answer carries a lifetime set by its
owner, and until that lifetime runs
out, the next identical question is
answered from memory — no walk at all.
Chapters 7 and 8 prove the second and
third of those as far as the lab's
network allowed, and say plainly where
that evidence stops.

## The privacy point, stated early

A resolver sees every name you look
up. Not the pages you read or the mail
you send — the *names*, which is most
of the story: names reveal the services
you use, the devices you own, and when
you are awake to use them. Sending
those questions to a provider means
trusting that provider's logging policy
and its legal jurisdiction. Running
Unbound does not make the questions
invisible — the servers Unbound asks
still see the tail end of each name it
walks (and Unbound's default *QNAME
minimisation* means each server is told
only the part it needs to answer). What
it changes is that no single company
collects the whole list. That trade —
a little more machinery at home, no
audience in the middle — is the reason
the tool exists.

The line this guide draws, early as
promised: a resolver is a listening
post by design, so **run one for
yourself and your household, never as
an open service for strangers**. An
open resolver on the internet gets
found and used to amplify attacks
within days, and its operator inherits
other people's question lists. Every
config in this guide listens on
private addresses and answers private
clients only.

## A first taste

After installing (chapter 3) and
configuring (chapter 4), asking is one
line — here using `dig`, the standard
DNS question tool, against the lab's
Unbound on its test port:

```bash
dig +tcp -p 18086 @127.0.0.1 printer.home.arpa A
```

```text
;; ANSWER SECTION:
printer.home.arpa.	3600	IN	A	192.168.1.50
```

The name goes in; the address comes
out, with its lifetime (3600 seconds)
attached. That name was one the lab
defined itself — chapter 5 reads a
full answer like this line by line —
but on a machine with internet access
the same question for a public name
would be walked, checked and cached by
exactly the same program.

## What it is not

Unbound is not an **authoritative
server**: it will not host your public
domain for the world to query (chapter
12). It is not a filter: it has no
advertising blocklists and no web
interface — those are Pi-hole's job,
and chapter 11 shows the two working
as a pair. It is not a full network
service stack: it hands out no
addresses (that is DHCP's job, usually
your router's). And it is not a
anonymity system: it removes the
middleman from your lookups; it does
not hide you from your provider, which
carries the traffic regardless.

## Who it is for

The household that wants its lookups
off a provider's books. The home-lab
builder who wants real names —
`nas.home.arpa`, not 192.168.1.60 —
for the machines down the hall. The
Pi-hole owner whose filter currently
forwards everything to a public
resolver, closing the loop the recipes
in chapter 11 close. The common thread
is one network, its own questions, and
a small machine that is already on.
