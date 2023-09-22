---
marp: true
---

# Inflation Attack on ERC4626 

Goal: Use Certora to verify that OpenZeppelin's implementation of ERC4626 is _not_ vulnerable to [the inflation attack](https://tienshaoku.medium.com/eip-4626-inflation-sandwich-attack-deep-dive-and-how-to-solve-it-9e3e320cc3f1). 

---

## First Step

Expressed a [CVL rule](https://github.com/johspaeth/tutorials-code/blob/johannes/openzeppelin/lesson4_reading/erc4626/src/certora/specs/ERC4626-InflationAttack.spec) describing the inflation attack. Rule [`vulnerableToInflationAttack`](https://prover.certora.com/output/53900/0bf85896db274ffaa69423bb9aee18a3?anonymousKey=0c379fab28b2c842757f5dc9ea0d80e8fe524fe0) shows a counter-example on an ERC4626 implementation (not the OpenZeppelin one), that is vulnerable to the inflation attack. 

Running the same rule on the OpenZeppelin implementation of ERC4626 [results in a timeout](https://prover.certora.com/output/53900/e5626ff6be1c42a6be6e3165b9e019b0?anonymousKey=5de6d6561925486182b6676849f546d19b180a4c).

---

## Approach for Mitigation of Timeouts
* Issue: rule for the inflation attack is quite complicated.
* Idea: simplify the process by trying to fix a timeout on another rule and get back to rule for the inflation attack and hope that timeout has been resolved there as well.
* New rule chosen: `inverseMintWithdrawInFavourForVault`. Using the rule the solver finds a [CEX on the implementation not from OpenZeppelin](https://prover.certora.com/output/53900/644362c3b13b40ac9a2591261f47da73?anonymousKey=fc4c4d05380fd0a603b52841daff53be4bc1e96d) but [times out](https://prover.certora.com/output/53900/8490846494044992848c1133995bea66?anonymousKey=8f65f17f2f781c8c705b3ba03041848b600e7213) when verifying the OpenZeppelin implementation. 
* Below is a set of trials to resolve the timeouts. All tests have been performed independently, i.e., state has been reset between runs to see individual impact. 
* The order the trials are presented is not the order in which I tested them. Initially, I followed the dump page output and the coloring scheme to understand which methods are affecting the timeouts. `withdraw` and `mint` were labeled as complex due to the branching structure of `_update`. `mulDiv` and the underlying non-linear math wasn't the first candidate I looked at. 

---
## Summarization (1 of 2)

The function [`mulDiv`](https://github.com/johspaeth/tutorials-code/blob/johannes/openzeppelin/lesson4_reading/erc4626/src/openzeppelin-9ef69c0/contracts/utils/math/Math.sol#L122) of the Math library uses a lot of assembly code. Assumption, if we can support prover in reasoning about it, we hope to get rid of timeouts. 

* Replace the entire function by `return require_uint256(x*y/denominator)` &rarr; [No Timeout](https://prover.certora.com/output/53900/d27c1b91c1124a2a94ab218a786ad663?anonymousKey=1025554e844dde70385a9e77e4e01e32747d69a6)
* Replace by upper and lower limits, it holds that `x*y/denominator <= res && x*y/denominator > res - 1` &rarr;  [No Timeout](https://prover.certora.com/output/53900/8532175924fa45ebbf0ffc5169be33a4?anonymousKey=e978c048cb901d0580f456f6f94b118cb911147f)
* Further relaxation of `require_uint256(x*y/denominator)` as `x == 0 => res == 0  && x <= denominator` (using domain knowledge: `shares <= totalSupply()` or `assets <= totalAssets()`) &rarr; [No timeout, but CEX not valid, as rule too imprecise.](https://prover.certora.com/output/53900/7ea1e2d3e730424a86039175967d109e?anonymousKey=c3be7ae883f01a12845d619da481e7364e6839d2)


---
## Summarization (2 of 2)

* Summarize `_update` Function of ERC20. The complexity of the `_update` function (>3 diamonds and many calls from `transfer`, `mint`, `burn` and `transferFrom`). The function modifies storage (transformation on `balances` mapping) but does not return any result. &rarr; [Timeout](https://prover.certora.com/output/53900/ccba8ccd72d948398b664653026b6506?anonymousKey=2be223f7795547c09daf65b18afbba1af022a225)

---
## Using Ghosts

* For the rule we are expressing, we know that `convertToAssets` and `convertToShares` are both called exactly once. Using a ghost we can store the parameters to the first call and summarize the result of the second call using the stored value. We know that the following equation holds `assets >= convertToAssets(convertToShares(assets))`, i.e., when the second call is made we can use the ghosted first call's result to define an upper limit. This way we assume to avoid calling `mulDiv` in general, as the calls are intercepted. &rarr; [No timeout, but CEX not valid.](https://prover.certora.com/output/53900/9061f8f699f44f25ba82e107700c53f3?anonymousKey=6a49b2d92ba1e5aae72963fb12c768aa4d468479)

---
## Concretizing Inputs

* Hardcode values for addresses. &rarr; [Timeout](https://prover.certora.com/output/53900/9a658882ff0546ada41483dddad87e43?anonymousKey=2df94692716083070411c00b761f4b96ca7d3bbd)
* Hardcode `shares` to one specific concrete value. &rarr;  [Timeout](https://prover.certora.com/output/53900/be834272042a486bb1af4920959b972d?anonymousKey=4f24aaefdae632cdb09d3879ff8fe0fbc338025e)

---
## Munging


* Observation: The `_update` Function of ERC20 is central to the code and complex. It has 3+ diamonds and combines logic from `transfer`, `mint`, `burn` and `transferFrom` in one function. By in-lining the code, one can reduce code complexity for the solver. For instance, branches `if(from == address(0))` can be eliminated as of knowledge that `from != 0`. This requires inter-procedural (but not cross-contract) reasoning over path conditions. Does the static analysis eliminate these cases? &rarr; (Led to a Timeout. No link available - I can reproduce if required)
* Replacing [`safeTransfer`](src/openzeppelin-9ef69c0/contracts/token/ERC20/extensions/ERC4626.sol):278 calls by `transfer`. `safeTransfer` is a method from library `SafeTransferLib` and uses assembly code to perform the operations. &rarr; (Led to a Timeout. No link available - I can reproduce if required)

---

## Experimenting with solver options

Using options
```
-smt_hashingScheme plainInjectivity -solvers [yices,z3]
```

&rarr; [Timeout](https://prover.certora.com/output/53900/a7adb6e2c62846789c830f76b8765785?anonymousKey=58dca0bb32f089ee2b4cc23abf115c48d2d63d8c)

&rarr; In the end, the summary `require_uint256(x*y/denominator)` solved the issue. The additional SMT option wasn't required anymore. 

---

# Non-timeout related comments

---

## Limited expressiveness of CVL

* Expressiveness for summation is restricted. For ERC 4626, the equation `sumOfBalance == totalSupply` is not expressible. A [complicated rule](https://github.com/johspaeth/tutorials-code/blob/johannes/openzeppelin/lesson4_reading/erc4626/src/certora/specs-openzeppelin/ERC4626-RoundingProps.spec#L61) is needed to express the formula

$$
totalSupply = \sum_{a \in uniqueAddresses} balanceOf(a)
$$

where $uniqueAddresses$ is the set of addresses participating in the transaction.

Is it possible to express a set and containment in CVL? 

---

## Learnings on rule writing process

* Setting up [a GitHub Action](https://github.com/Certora/CertoraInit/blob/master/.github/workflows/certora.yml) significantly helps to keep track of changes in the process: One commit equals one Certora run.
* _Improvement to the GitHub Action_: Certora could report back to GitHub. Then it'll be easier to reason which commit led to an error (failed verfication/timeout). Could be easily done, for instance, using [SARIF](https://sarifweb.azurewebsites.net/). 


---

## Open Questions / Other comments
* How does a good structure of the rule writing process look like? 
&rarr; _Will probably learn it in the the project, I'll be starting this week._
* During the process I frequently applied combinations of the above trials. My assumption was that it could have easily been the case, that only _in combination_ they solve the timeout issue. During the process of rule writing, how can one judge the best approach to take to not waste time? 
* When using summaries that are too weak, how to avoid counter-examples of non-interest? &rarr; _...most certainly hard to guide the solver into a certain direction._

---


TODO: Get back to inflation attack. [Run](https://prover.certora.com/output/53900/9c2969d79a5a4873988750f7625e9e66?anonymousKey=be24280a64b9a374ea1d76a8b4f38b52169d24e6) with basic `mulDivSummary` doesn't timeout. Inspect results. If the CEX is correct, open Zeppelin would be vulnerable to the attack.
First observation (needs second inspection): The CEX doesn't work, the global setup is incorrect as property `ERC20.totalsupply == sumOfBalances` is violated. Must be hard-coded as it's not possible to use a `requireInvariant`. 

----
## Improvement to the rule writing process
When writing and testing specs I had several versions of the spec and code at the same time and submitted those to the server. Because I had wait several minutes for the results, frequently, I  already initiated a job for another idea to test in parallel. The code and spec were maintained using git and tracking changes of the code diffs are easy, but mapping back Certora results to the actual commit is difficult, especially as one had to remember which link of a Certora job belongs to which commit. 

I [found a GitHub Action](https://github.com/Certora/CertoraInit/blob/master/.github/workflows/certora.yml) that I added to my repository. However, this GitHub action also only triggers the actual run - **no indication on GitHub is given if the verification actually terminates successfully or not**. The feedback one gets on GitHub is limited to the successful _submission_ of the job in Certora. I wish I could quickly see the list of commits and the actual results of the Certora execution, such that one quickly see which changes introduced / eliminated the timeout for a rule.  

Certora should report back to GitHub as part of the GitHub action. See SARIF. 

---
