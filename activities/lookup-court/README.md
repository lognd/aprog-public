# Activity: Lookup Court

dunder-dungeon showed you the raw mechanism -- `__dict__`, `__mro__`,
bound methods -- by running code and predicting output. Lookup Court puts
that mechanism on trial with harder, more deliberate scenarios: given a
snippet, exactly where is an attribute actually found (an instance's own
dictionary, a class's dictionary, a base class further up the hierarchy,
or nowhere at all)? Which method does a call resolve to when two
unrelated base classes define the same method name? What does `super()`
actually consult when a class hierarchy branches and rejoins -- and why
is "call my parent's version" the wrong mental model the moment more than
one base class is involved? Does assigning to an instance ever change its
class? What is a bound method, mechanically? And does patching a class
after instances of it already exist change what those existing instances
do? Every explanation builds directly on dunder-dungeon's groundwork.

## Concepts covered

- tracing attribute lookup through `__dict__` and `__mro__` together, for
  scenarios more elaborate than dunder-dungeon's single examples
- method resolution in a multi-parent hierarchy, and the "leftmost base
  wins" rule when two unrelated bases define the same method name
- what `super()` actually consults -- the full `__mro__` of the running
  object, not simply "the parent class" -- demonstrated with a real
  diamond hierarchy and cooperative `super()` chaining
- confirming that assignment through an instance never modifies the
  class, even when a class attribute of the same name already exists
- what a bound method actually consists of, mechanically
- monkey-patching: reassigning a class's method from outside the class
  body, and why every existing instance immediately sees the change

## How it works

The launcher asks seven questions, one at a time, each with a short code
snippet and a hint. Type your answer in your own words (or as the exact
phrase, value, or line of code the question calls for) and press Enter. A
correct answer shows a full explanation and moves you to the next
question; a wrong answer -- if it matches a known misconception -- shows
why that specific answer is wrong, and otherwise asks you to reread the
snippet and try again.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly answered all seven questions and the launcher shows
you a passphrase.

## Hints

<details>
<summary>Hint 1 -- walk the __mro__ by hand before answering</summary>

For any question about which method actually runs, write out the class's
full `__mro__` first (the same left-to-right, each-class-once order
dunder-dungeon covers), then walk it in order and stop at the first class
that defines the name you are looking for.

</details>

<details>
<summary>Hint 2 -- super() means "next in the MRO," not "my parent"</summary>

For the diamond-hierarchy `super()` question, resist the urge to jump
straight to a class's direct parent. `super()` always means "whichever
class comes next after the CURRENTLY RUNNING class, in the __mro__ of the
object the whole chain started from" -- work through the chain one call
at a time.

</details>

<details>
<summary>Hint 3 -- lookup is never cached</summary>

For the monkey-patching question, remember that attribute and method
lookup happens fresh, every single time an attribute is accessed -- never
once at object-construction time. Nothing about an object's behavior is
ever "locked in" when it is created.

</details>

## Going further

- Write a three-level diamond (a hierarchy where the shared ancestor is
  reached through two different intermediate classes, each with their
  own further base) and predict its `__mro__` before checking it with
  `print(D.__mro__)`.
- Monkey-patch a method on a built-in type's subclass (for example,
  subclass `list` and patch a method on the subclass, not on `list`
  itself) and confirm which existing instances see the change.
- Look up `__getattr__` (a different, related mechanism from the ones in
  this activity) and explain, in your own words, how it changes what
  happens when normal attribute lookup would otherwise raise
  `AttributeError`.
