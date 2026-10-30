# Installing Unbound

The outcome: Unbound installed, its
version read back, and its config
checker passing — the proof that the
program on your disk can start before
you ask it to.

Unbound is in every mainstream Linux
distribution's packages, and that is
the route to take: your distribution
keeps it updated and wires it into its
service manager. On Debian and Ubuntu:

```bash
sudo apt update
sudo apt install unbound
```

That one package brings the daemon, the
config checker, the control tool, and
the anchor tool's partner data — the
`dns-root-data` package, which carries
the root hints and the root trust
anchor as ordinary files in
`/usr/share/dns/`. On Fedora the same
job is `sudo dnf install unbound`;
on FreeBSD, `pkg install unbound`.

## The version check

```bash
$ unbound -V
Version 1.19.2
...
Linked modules: dns64 python cachedb subnetcache respip validator iterator
```

The first line is the number to quote
when asking for help. The last line is
worth a glance: it lists the modules
compiled in, and **validator** and
**iterator** should both be there —
they are the checker and the walker
from chapter 2. (This guide's 1.19.2
was current for Ubuntu 24.04 in
October 2026; your number will differ,
and nothing in the guide depends on
the difference.)

## Before it ever runs: check the config

The package installs a default setup
under `/etc/unbound/`: a thin
`unbound.conf` that mostly *includes*
the drop-in directory
`/etc/unbound/unbound.conf.d/`, so your
own file can live there without
fighting the package's. Whatever you
end up with, this command is the gate:

```bash
$ unbound-checkconf
unbound-checkconf: no errors in /etc/unbound/unbound.conf
```

Run it after every edit, before every
restart. A resolver that cannot start
fails silently for every client that
depends on it, and `unbound-checkconf`
turns that class of failure into a
line number on your screen instead.
Chapter 4 shows its error messages for
a misspelled option and a bad value;
they are exact and they name the line.

## Starting it as a service

On a distribution install, the service
is simply:

```bash
sudo systemctl enable --now unbound
```

and the distribution's default already
listens on localhost. Your machine's
own lookups may or may not use it —
on many desktops a stub listener
(`systemd-resolved`) sits in front and
can itself be pointed at Unbound; the
neighbours chapter untangles that.
Chapter 5 starts the lab's instance by
hand, on a test port, so its behaviour
can be watched in isolation.

## How the lab installed it, honestly

The lab machine is a shared sandbox,
and when the lab ran, its package
manager's lock was held by another
user's work:

```text
E: Could not get lock /var/lib/dpkg/lock-frontend. It is held by process 62745 (apt-get)
```

So the lab took the fallback other
guides in this series have used: it
downloaded the **identical distribution
packages** (`apt-get download unbound
libunbound8 unbound-anchor dns-root-data`,
plus two small libraries the package
needs) and unpacked them, unmodified,
into a scratch tree with `dpkg -x`,
running the binaries from there. Same
publisher, same version, same files —
the only difference is the prefix, and
the transcripts note the wrapper that
arranges it. On your machine the
ordinary `apt install` above is the
right route, and nothing in the
transcripts depends on the difference.
The full record is
`unbound-lab/transcripts/t00-install.txt`.
