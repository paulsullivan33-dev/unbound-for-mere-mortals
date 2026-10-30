# DNSSEC — Checking the Answers

The outcome: you can say what
validation actually checks, where the
chain of trust is rooted, what a
failed check looks like from a chair
like yours — and which part of that
the lab could, and could not,
demonstrate.

Plain DNS takes answers on trust: a
reply that arrives with the right
return address is believed. DNSSEC
adds signatures. A signed zone
publishes, alongside its records, a
signature for each set of records
(**RRSIG**), the public key that made
it (**DNSKEY**), and — in its parent
zone — a hash of that key (**DS**).
Checking an answer means checking the
signature with the key, the key
against the parent's hash, the
parent's key against *its* parent's
hash, and so on up to the root. If
every link holds, the answer is what
its owner published. If any link
fails, the answer is **bogus**, and a
validating resolver — Unbound's
validator, chapter 2 — refuses it:
the client receives **SERVFAIL**, not
the lie.

Nothing is encrypted here. DNSSEC is
about *authenticity*, not privacy: it
proves the answer is genuine, and it
leaves the question visible, which is
why chapter 1's privacy story is
about who you ask, not about
signatures.

## The anchor: where trust starts

Every chain needs a first link you
hold yourself. Yours is the **root
trust anchor**: the hash of the root
zone's key-signing key, installed as
data, not fetched on faith. The lab
read its own:

```text
$ unbound-anchor -l
. IN DS 20326 8 2 E06D44B80B8F1D39A95C0B0D7C65D08458E880409BBC683457104237C7F8EC8D
```

and confirmed the same anchor arrived
with the distribution's `dns-root-data`
package, whose `root.key` holds the
root keys themselves:

```text
. IN DNSKEY 257 3 8 AwEAAaz/tAm8yTn4...  ; keytag 20326
```

(From `unbound-lab/transcripts/t02-anchor-and-checkconf.txt`.)
The root's key changes rarely and
ceremonially; when it does, resolvers
learn the successor automatically by
the RFC 5011 mechanism — the old key
signs the new one for a while, and
Unbound's `auto-trust-anchor-file`
tracks it, in a file Unbound itself
may rewrite. That is why the config
points at a writable `root.key` copy
rather than the package's read-only
one. `unbound-anchor` is the bootstrap
and repair tool for the same file: on
an internet-connected machine it can
rebuild a missing anchor from its
built-in copy plus an HTTPS fetch from
IANA. In the lab it printed its
verdict and stopped:

```text
$ unbound-anchor -a anchor-test.key -v
.../anchor-test.key has content
fail: the anchor is NOT ok and could not be fixed
```

— because fixing it needs the network
this sandbox will not give. The
package's anchor stood in, and was
genuine: it is the distribution's
signed data, identical to the tool's
built-in copy.

## What the lab could not show

Validation engages only when signed
answers arrive, and in the sandbox no
public answer arrives at all. Asking
for an ordinary public name, the log
shows the validator's partner — the
iterator — reaching for the roots by
their real addresses and being cut
off:

```text
$ dig +tcp ... example.com A
;; status: SERVFAIL ... ANSWER: 0

$ tail -6 unbound.log
error: read (in tcp s): Connection reset by peer for 192.5.5.241 port 53
error: read (in tcp s): Connection reset by peer for 198.41.0.4 port 53
...
```

(198.41.0.4 and 192.5.5.241 are
a.root-servers.net and b.root-servers.net;
the full record is `t05`.) So: the
anchor was read, the machinery
started, the walk began — and the
successful end-to-end validation of a
public name is **documented-only** in
this guide, from NLnet Labs'
documentation. On your network, the
way to see it work is one command:

```bash
dig @127.0.0.1 dnssec.works A
```

`dnssec.works` is a test zone kept for
this purpose: a good name there
answers with the **`ad` flag** set in
dig's header — *authenticated data*,
the validator vouching for the answer
— and its deliberately broken sibling
`fail.dnssec.works` answers SERVFAIL.
Those two replies, side by side, are
the whole chapter in miniature.

## The two sharp edges

**Clocks.** Signatures carry validity
windows, so a resolver with a wrong
clock calls good answers bogus and
fails everything at once. A sudden
total SERVFAIL storm is a clock
problem until proven otherwise
(chapter 14).

**Private zones.** Your own unsigned
names sit *below* a signed root, and
an unsigned delegation where the
parent expects a DS record reads as
forgery. That is why the lab's config
carries `domain-insecure: "lab"`, and
why your `home.arpa` and any forwarded
employer's zone will want the same
exemption or a local trust anchor.
Validation is on by default in
Unbound and this guide leaves it on;
the exemptions are surgical, named
zone by named zone.
