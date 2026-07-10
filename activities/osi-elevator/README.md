# Activity: OSI Elevator

Before touching HTTP, methods, or status codes, you need the picture
of what a "network" even is. When your browser talks to a server, the
data does not travel as one single blob understood by one single
piece of code -- it rides down through several LAYERS, each one
solving exactly one problem and trusting every layer below it to have
already solved its own, then rides back up through the same layers in
reverse on the other end. This activity is ten no-code scenarios and
definitions building that mental model from the physical wire all the
way up to HTTP itself, so that the next activity (`http-anatomy`) has
solid ground to stand on.

## Background

Picture the whole trip as an elevator ride through a building with
five floors, one problem solved per floor:

```
  Floor 7  APPLICATION   "what does this request MEAN?"        <- HTTP lives here
  Floor 4  TRANSPORT     "deliver it reliably, in order"        <- TCP lives here
  Floor 3  NETWORK       "find the right MACHINE"               <- IP lives here
  Floor 2  LINK          "get it across the local hop"          <- Ethernet/WiFi live here
  Floor 1  PHYSICAL      "turn it into an actual signal"        <- the cable or radio wave itself
```

(The traditional OSI model also names a session layer and a
presentation layer between transport and application -- floors 5 and
6. This activity is honest that, in day-to-day web development, those
two floors' jobs get absorbed into application-layer tools and
libraries rather than showing up as distinct concerns, so the
practical mental model most working developers actually use has five
floors, not seven.)

A request rides the elevator DOWN on the way out, getting a new
envelope taped around it at each floor -- ENCAPSULATION, wrapping data
in progressively more layers, like nesting envelopes. Your raw HTTP
request is the innermost letter. TCP (floor 4) wraps it first. IP
(floor 3) wraps that. Ethernet or WiFi (floor 2) wraps that last,
right before the signal actually leaves your machine as bits over a
wire or through the air:

```
  [ Ethernet frame [ IP packet [ TCP segment [ HTTP request ] ] ] ]
    (link, added        (network,   (transport,    (application,
     last, outermost)     3rd)        1st wrap)      innermost)
```

On the far end, the receiving machine rides the elevator back UP,
peeling off exactly one envelope per floor, in the exact reverse
order: Ethernet's wrapper comes off first (it was added last), then
IP's, then TCP's, leaving the original HTTP request completely intact
-- the same request that started the trip, untouched by any of the
wrapping and unwrapping in between.

Three different things get IDENTIFIED along the way, each at a
different level of precision: an IP address says which MACHINE (out
of a whole network); a port says which PROGRAM on that machine (out
of possibly many running at once); a MAC address says which network
CARD on the local segment (only relevant for the one local hop). DNS
(Domain Name System) is the translation step that happens before any
of this -- given a human-readable name like `example.com`, it hands
back the IP address to actually connect to. And TCP's entire job, in
one sentence, is reliable, ordered delivery: data arrives complete and
in the right order, or TCP fixes it before your code ever sees it --
unlike a bare "just send it" alternative, which makes no such
promises at all.

## Concepts covered

- Why networking is layered: each layer solves one problem and trusts
  every layer below it
- Encapsulation as nesting envelopes: wrapping on the way out, and
  unwrapping in exact reverse on the way in
- Which layer HTTP, TCP, IP, Ethernet/WiFi, and the physical medium
  each live at, using the practical five-layer model (with an honest
  note on where session/presentation actually go)
- What an IP address, a port, and a MAC address each identify
- DNS's one-sentence job: translating a name into an IP address
- TCP's one-sentence job -- reliable, ordered delivery -- contrasted
  with a "just send it" alternative that makes no such guarantee
- Which layer a web developer actually spends their working time at

## How it works

The launcher shows you ten questions, one at a time -- scenarios and
definitions, no code. Type your answer. A correct answer shows a
short explanation and moves you on; a wrong answer shows an
explanation of the specific misconception behind that guess. Read the
explanations even on questions you get right the first time -- this
activity builds directly on itself, floor by floor.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly answered all ten questions and the launcher shows
you a passphrase.

## Hints

<details>
<summary>Hint 1 -- work top to bottom, floor by floor</summary>

Application (what it means) is the top floor. Physical (the actual
signal) is the bottom floor. Every layer in between solves exactly one
problem on the way from one to the other -- transport for reliable
delivery, network for finding the right machine, link for the local
hop.

</details>

<details>
<summary>Hint 2 -- wrapping goes down, unwrapping goes up, and they mirror exactly</summary>

Whatever was wrapped LAST on the way out is unwrapped FIRST on the way
in. If you know the wrapping order, you already know the unwrapping
order -- just read it backwards.

</details>

<details>
<summary>Hint 3 -- match the identifier to what it has to distinguish</summary>

A MACHINE among a whole network needs an IP address. A PROGRAM among
several running on one machine needs a port. A network CARD on the
local segment needs a MAC address. Ask "among what set of things does
this need to be unique?"

</details>

## Going further

- Open a terminal and run `ping example.com` (or any site). Look at
  what it prints -- can you spot the IP address DNS resolved the name
  to?
- Look up what a "hop" means in networking, and read about
  `traceroute` (or `tracert` on Windows) -- it shows every intermediate
  machine your packet passes through on the network layer before
  reaching its destination.
- The next activity, `http-anatomy`, picks up exactly where this one
  ends: the application layer, where HTTP itself lives. The assignment
  after that, `typed-ledger-api`, is where you build a real program
  living at that top floor.
