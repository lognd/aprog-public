# Activity: OS Mental Models

Every activity in this row has had you calling `open()`, `read()`,
`write()`, and `close()` -- but none of them stopped to ask the more basic
question: what are you actually talking to when you make one of those
calls? This activity is that missing conversation. No code, no shell, no
compiler -- just the mental model every other activity in this row quietly
assumes you already have.

Think of the operating system (OS) as a hotel manager. Hundreds of guests
(your running programs) share one building (the computer): one kitchen
(the CPU), one set of storage rooms (the disk), one supply of towels
(memory). No guest gets to walk into the kitchen and start cooking
themselves, and no guest gets to wander into another guest's room. Instead,
every guest requests things through the manager's staff at the front desk:
"I need a towel," "please bring my bag up from storage." The manager
decides who gets the kitchen next, keeps each guest's room private from
every other guest, and lets a guest just say "bring me a towel" without
ever needing to know which shelf it came from. That manager is the
operating system, and the front desk is the interface your program uses to
ask for anything privileged at all.

## Concepts covered

- What an operating system actually is: a resource manager, an abstraction
  layer, and a referee between every running program and the hardware
- The difference between a kernel (the privileged core) and an OS
  distribution (the kernel plus shells, utilities, and libraries)
- User mode vs. kernel mode, and why the CPU itself -- not a setting, not a
  convention -- stops your program from touching hardware directly
- A syscall as the one controlled doorway between user mode and kernel mode
- The three problems every OS solves: sharing, isolation, and abstraction
- What a process is, and how it relates to the fd table from
  `posix-file-tour`
- Where `errno` (covered in `file-io-contracts`) actually comes from

## How it works

Eleven questions, each with a hint, keyed wrong-answer explanations, and a
full explanation shown after you answer. Type your answer exactly as
prompted (case-sensitive, no surrounding spaces). A wrong answer shows why
it's wrong and re-prompts; it does not move you forward. All eleven
correct unlocks the passphrase.

## Getting started

```bash
python3 launch.py
```

## The two-mode picture

Every question in this activity keeps coming back to one line: the
boundary between what your code is allowed to do and what only the kernel
is allowed to do. Here it is as a picture. "Above the line" is user mode,
where your compiled program runs; "below the line" is kernel mode, where
the kernel runs and where the hardware actually lives.

```text
   your program (user mode)
   ------------------------------------------------
       open() / read() / write() / close()
                     |
                     |  <-- syscall: the doorbell.
                     |      Ring it, and the CPU itself
                     |      switches privilege levels.
                     v
   ==================================================
   kernel (kernel mode) -- the only code allowed to
   touch hardware directly: disk, memory, network card
   ==================================================
                     |
                     v
              [ physical hardware ]
```

Your program never reaches through that line itself. It rings the
doorbell (a syscall), the CPU switches to kernel mode, the kernel does the
privileged work, and control comes back to you in user mode -- exactly
like a hotel guest never walking into the kitchen themselves, only ever
asking the front desk to bring something out.

## Kernel vs. distribution

"Linux" and "Ubuntu" get used almost interchangeably, but they name two
different things. Linux is a kernel: the privileged core program that
directly manages the CPU, memory, and hardware. Ubuntu is a distribution:
that same Linux kernel, bundled with a shell, command-line utilities, a
package manager, and (usually) a desktop, into one installable product.
Fedora and Debian are different distributions built around the same
Linux kernel. The same split exists on other platforms: macOS is built
around a kernel called XNU, and Windows is built around a kernel called
NT -- in both cases, the product name you know is the distribution, and
the kernel underneath has its own, much less famous, name.

## Why this activity comes first in this row

Every other activity you'll do in Basic OS Theory -- `posix-file-tour`,
`file-io-contracts`, `write-your-first-syscalls`, `hex-dump` -- is you
talking through the doorbell in the diagram above. `posix-file-tour` walks
the stack that request travels through. `file-io-contracts` drills the
precise promises the kernel makes (and doesn't make) once it answers.
`write-your-first-syscalls` has you actually ring the doorbell yourself.
`hex-dump` has you build a real program out of nothing but those rings.
None of them stop to explain what's on the other side of the door, or why
a door is needed at all -- that's what this activity is for.

## You will know you are done when...

After the eleventh question, the terminal prints your passphrase between
two horizontal lines.

## Hints

<details>
<summary>Hint 1 -- kernel vs. distribution</summary>

Ask yourself: could two different products (Ubuntu and Fedora, say) be
built around the exact same underlying core? If yes, that core is the
kernel, and each product wrapping it is a distribution.

</details>

<details>
<summary>Hint 2 -- user mode vs. kernel mode</summary>

This isn't a permission you could grant yourself with a config file. It's
enforced by the CPU chip itself, the same way a locked door is enforced by
the lock, not by a sign asking you not to enter.

</details>

<details>
<summary>Hint 3 -- the three problems</summary>

Sharing is about many programs wanting the same one thing (one CPU, one
disk) at once. Isolation is about one program's mistake not becoming
everyone's problem. Abstraction is about your program getting to say what
it wants ("open this file") without knowing how the hardware underneath
actually does it.

</details>

## Going further

- Run `uname -s -r` in your terminal. The first field names the kernel
  you're running; look up which distribution you're actually using and
  confirm it's built around that same kernel.
- `strace` traces every syscall a program makes. This only works on Linux
  (macOS and Windows use different tools -- `dtruss` and Process Monitor,
  respectively). If you're on Linux, try `strace ls 2>&1 | head -20` and
  see how many syscalls a program as simple as `ls` actually makes before
  it prints anything.
- Look up what a microkernel is, and how it differs from the kind of
  kernel (a monolithic kernel) that Linux, XNU, and NT all are. What
  moves out of kernel mode in a microkernel design, and why would anyone
  want that?
