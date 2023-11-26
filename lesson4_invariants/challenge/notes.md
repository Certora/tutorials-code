# Challenge notes

## Challenge rules
- No rules (only invariants, hooks, ghosts, axioms and functions)
- No harnessing
- `withdraw` and `deposit` will not be mutated

## Mutations to add
* Everyone has root as parent
* When joining child - cutting the grandfather off (before and after joining child?)
* Make child parent of root
* Make `contains` always return `true` or always `false`
* Make `getParent` or `getChild` always return root or zero
* Connect child to grandfather - can't be caught by invariant?
* Join a disconnected node! (should only be caught by reachability invariants)


## Do not mutate
- `withdraw` and `deposit`
