MustNotRevertProps
---
* `convertToAssets()` must not revert for reasonable values
* `convertToShares()` must not revert for reasonable values

> Comment Johannes: What's meant by reasonable values here? There are ways to make both revert, when `totalSupply * shares|assets` overflows. 

* `asset()` must not revert
* `totalAssets()` must not revert
* `maxDeposit()` must not revert
* `maxMint()` must not revert
* `maxRedeem()` must not revert
* `maxWithdraw()` must not revert

> Comment Johannes: `maxWithdraw` reverts in an integer overflow case as it depends on `convertToAssets()`. If that spec is correct, it's a bug.

FunctionalAccountingProps
---
> Implementation see rule depositProperties
* `deposit()` must deduct assets from the owner
* `deposit()` must credit shares to the receiver
* `deposit()` must mint greater than or equal to the number of shares predicted by `previewDeposit()`
> Implementation see rule mintProperties
* `mint()` must deduct assets from the owner
* `mint()` must credit shares to the receiver
* `mint()` must consume less than or equal to the number of assets predicted by `previewMint()`
> Implementation see rule withdrawProperties
* `withdraw()` must deduct shares from the owner
* `withdraw()` must credit assets to the receiver
* `withdraw()` must deduct less than or equal to the number of shares predicted by `previewWithdraw()`
> Implementation see rule redeemProperties
* `redeem()` must deduct shares from the owner
* `redeem()` must credit assets to the receiver
* `redeem()` must credit greater than or equal to the number of assets predicted by `previewRedeem()`

RedeemUsingApprovalProps
---
> All properties with withdraw and redeem implemented.
* `withdraw()` must allow proxies to withdraw tokens on behalf of the owner using share token approvals
* `redeem()` must allow proxies to redeem shares on behalf of the owner using share token approvals
* Third party `withdraw()` calls must update the msg.sender's allowance
* Third party `redeem()` calls must update the msg.sender's allowance
* Third parties must not be able to `withdraw()` tokens on an owner's behalf without a token approval
* Third parties must not be able to `redeem()` shares on an owner's behalf without a token approval

SenderIndependentProps
---
> declaring methods env free checks this automatically for us. Otherwise one _could_ take two different env e1, env e2 and show that the return value of the function calls is equal for any environment.
* `maxDeposit()` must assume the receiver/sender has infinite assets
* `maxMint()` must assume the receiver/sender has infinite assets
* `previewMint()` must not account for msg.sender asset balance
* `previewDeposit()` must not account for msg.sender asset balance
* `previewWithdraw()` must not account for msg.sender share balance
* `previewRedeem()` must not account for msg.sender share balance



RoundingProps
---
> Show that storage doesn't change when using these function. (i.e. check that all view function are actually view)
* Shares may never be minted for free using:
  * `previewDeposit()`
  * `previewMint()`
  * `convertToShares()`

* Tokens may never be withdrawn for free using:
  * `previewWithdraw()`
  * `previewRedeem()`
  * `convertToAssets()`

> Solve a rule totalMonotonicty
* Shares may never be minted for free using:
  * `deposit()`
  * `mint()`

* Tokens may never be withdrawn for free using:
  * `withdraw()`
  * `redeem()`

SecurityProps
---
* `decimals()` should be larger than or equal to `asset.decimals()`

> Added specification in file `ERC4626-InflationAttack.spec``
* Accounting system must not be vulnerable to share price inflation attacks

> Johannes: Added 4 rules to show the below.
* `deposit/mint` must increase `totalSupply/totalAssets`
* `withdraw/redeem` must decrease `totalSupply/totalAssets`


* `previewDeposit()` must not account for vault specific/user/global limits
* `previewMint()` must not account for vault specific/user/global limits
* `previewWithdraw()` must not account for vault specific/user/global limits
* `previewRedeem()` must not account for vault specific/user/global limits


Properties that may not be testable
---
* Note that any unfavorable discrepancy between `convertToShares` and `previewDeposit` SHOULD be considered slippage in share price or some other type of condition, meaning the depositor will lose assets by depositing.
* Whether a given method is inclusive of withdraw/deposit fees




Other Properties
------
* `withdraw` and `redeem` are semantically equivalent when the inputs are converted using the respective `convert` method.
* `mint` and `deposit` are semantically equivalent when the inputs are converted using the respective `convert` method.
* Deposit increases the number of shares by mint. Shares minted should be proportional to the increase of the balance of the vault. 
  ```
  a: amount to deposit
  B: Balance of vault before deposit
  s: shares to mint 
  T: Total shares before minting
  Then it holds: (a+B)/B = (s+T)/T => s = aT/B
  ```
  Source https://www.youtube.com/watch?v=k7WNibJOBXE

* When withdrawing, the shares burned must be proportional to the total balance of the vault
  ```
  a: amount to withdraw
  B: Balance of vault before deposit
  s: shares to burn
  T: Total shares before burning
  Then it holds: (B-a)/B = (T-s)/T => s = aT/B
  ```
  Source https://www.youtube.com/watch?v=k7WNibJOBXE
* ERC-4626 Inflation attack: Can we model a rule that "executes" the inflation attack? What happens if we change the analyzed contract to use standard division instead of `FixedPointMathLib.sol`? Does the rule detect it? 

  Source https://tienshaoku.medium.com/eip-4626-inflation-sandwich-attack-deep-dive-and-how-to-solve-it-9e3e320cc3f1