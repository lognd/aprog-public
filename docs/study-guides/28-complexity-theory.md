# Study Guide 28: Complexity Theory

This module introduces Big-O notation and formalizes the growth-rate
intuition from Control & Functions: classifying real code into the five
common growth classes by counting how often the innermost line runs, and
then reasoning numerically with growth rates -- scaling a measured time,
comparing classes "eventually," and estimating logarithms.

## Know before you start

- The informal intuition that two correct functions can differ wildly in
  running time as input grows, and the "helper called in a loop"
  multiplication (without the formal notation, which is introduced here)
  [assumed: row 6 -- Control & Functions]
- `std::vector` size/capacity and reallocation copying every element
  [assumed: row 7 -- Standard Library Types]

## Taught here

Concept: the five growth classes
- Know that Big-O describes how running time grows as input size n grows,
  deliberately ignoring machine speed and constant amounts of extra work.
- Know the five classes: O(1) constant (input size changes nothing);
  O(log n) logarithmic (a large fraction of remaining work discarded each
  step -- doubling the input adds only ONE step); O(n) linear (doubling
  input doubles work); O(n log n) linearithmic (the signature of efficient
  sorting); O(n^2) quadratic (typically nested loops -- doubling input
  quadruples work).
- Be able to classify a function by counting how many times the innermost
  unit of work executes as a function of n.
- Know the composition rules: nested loops multiply their costs;
  sequential loops add them (and Big-O drops constant multipliers, so
  O(2n) is O(n)).
- Know that a triangular nested loop (`for j < i`) still runs n(n-1)/2
  inner iterations and is O(n^2) -- the 1/2 is a dropped constant.
- Know that a loop halving its remaining range each iteration is the
  O(log n) signature: ask "how many times can this be halved before
  reaching 1?"
- Know that indexed access into a contiguous array (`operator[]`) is a
  true O(1) operation.

Concept: worst case, best case, and amortized cost
- Know that an early-exit function's time depends on the specific input:
  the best case is the luckiest input, the worst case is the maximum
  possible work, and an unqualified complexity conventionally means the
  worst case -- the guarantee that holds for any input.
- Know amortized complexity: the provable average cost per operation over
  a long sequence, spreading rare expensive operations across the common
  cheap ones -- `std::vector::push_back` is usually O(1), occasionally an
  O(n) full resize, and amortized O(1) because capacity doubles.

Concept: numeric reasoning with growth rates
- Be able to scale a measured time: if input size is multiplied by k, time
  multiplies by k for O(n), by k^2 for O(n^2), and not at all for O(1) --
  the ratio between times at two sizes is determined by the growth rate
  alone.
- Know that Big-O hides a constant factor, so a "worse" class can be
  temporarily faster for small n (1000n beats n^2 below n = 1000), but the
  better growth rate always eventually wins and stays ahead -- constants
  delay the crossover, never change the winner.
- Be able to estimate `log2(x)` with the shortcut 2^10 = 1024 (roughly
  1000), and the rule log2(a*b) = log2(a) + log2(b) -- so log2(1,000,000)
  is about 20, which directly bounds binary-search step counts on
  realistic inputs.

## Study checklist

- [ ] Classify a single loop, sequential loops, nested loops, and a
      halving loop into their growth classes.
- [ ] Explain why a triangular loop is still O(n^2).
- [ ] Define amortized O(1) using push_back as the example.
- [ ] Given "2 ms at n=1000, O(n^2)", predict the time at n=10,000.
- [ ] Explain why 1000n vs n^2 has a crossover and who wins eventually.
- [ ] Estimate log2(1,000,000) without a calculator.

## Practiced in

`big-o-lineup`, `growth-witness`
