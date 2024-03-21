/**
 * Verification of ERC20 - proving that the sum of two distinct balances is not
 * greater than total supply.
 */
methods {
    function balanceOf(address) external returns (uint256) envfree;
    function totalSupply() external returns (uint256) envfree;

}

// ---- Ghosts and hooks -------------------------------------------------------

/** @title A ghost to mirror the balances
 *  This is needed for the axioms in `sumBalances`, since we cannot call solidity
 *  functions from the axioms.
 */
ghost mapping(address => uint256) balanceOfMirror {
    init_state axiom forall address a. balanceOfMirror[a] == 0;
}


/** @title A ghost representing the sum of all balances
 *  @notice We require that it would be at least the sum of three balances, since that
 *  is what is needed in the `preserved` blocks.
 *  @notice We use the `balanceOfMirror` mirror here, since we are not allowed to call
ghost mathint sumBalances {
    init_state axiom sumBalances == 0;
 *  contract functions from a ghost.
 */
ghost mathint sumBalances {
    init_state axiom sumBalances == 0;
    axiom forall address a. forall address b. (
        (a != b => sumBalances >= balanceOfMirror[a] + balanceOfMirror[b])
    );
    axiom forall address a. forall address b. forall address c. (
        (a != b && a != c && b != c) => 
        sumBalances >= balanceOfMirror[a] + balanceOfMirror[b] + balanceOfMirror[c]
    );
}


hook Sstore balanceOf[KEY address user] uint256 newBalance (uint256 oldBalance)
{
    sumBalances = sumBalances + newBalance - oldBalance;
    balanceOfMirror[user] = newBalance;
}


// ---- Invariants -------------------------------------------------------------

/// @title Formally prove that `balanceOfMirror` mirrors `balanceOf`
invariant mirrorIsTrue(address a)
    balanceOfMirror[a] == balanceOf(a);


/// @title Proves that `totalSupply` is `sumBalances`
invariant totalIsSumBalances()
    to_mathint(totalSupply()) == sumBalances
    {
        preserved transfer(address recipient, uint256 amount) with (env e1) {
            requireInvariant mirrorIsTrue(recipient);
            requireInvariant mirrorIsTrue(e1.msg.sender);
        }
        preserved transferFrom(
            address sender, address recipient, uint256 amount
        ) with (env e2) {
            requireInvariant mirrorIsTrue(sender);
            requireInvariant mirrorIsTrue(recipient);
            requireInvariant mirrorIsTrue(e2.msg.sender);
        }
    }


/// @title The sum of two balances is not greater than `sumBalances`
invariant sumOfTwo(address a, address b)
    (a != b) => (balanceOf(a) + balanceOf(b) <= sumBalances) {
        preserved transfer(address recipient, uint256 amt) with (env e1) {
            requireInvariant mirrorIsTrue(a);
            requireInvariant mirrorIsTrue(b);
            requireInvariant mirrorIsTrue(recipient);
        }
        preserved transferFrom(
            address sender, address recipient, uint256 amount
        ) with (env e2) {
            requireInvariant mirrorIsTrue(a);
            requireInvariant mirrorIsTrue(b);
            requireInvariant mirrorIsTrue(recipient);
        }
    }


/// @title The sum of two balances is not greater than `totalSupply`
invariant sumOfTwoTotalSupply(address a, address b)
    (a != b) => (balanceOf(a) + balanceOf(b) <= to_mathint(totalSupply())) {
        preserved transfer(address recipient, uint256 amt) with (env e1) {
            requireInvariant mirrorIsTrue(a);
            requireInvariant mirrorIsTrue(b);
            requireInvariant mirrorIsTrue(recipient);
            requireInvariant totalIsSumBalances();
        }
        preserved transferFrom(
            address sender, address recipient, uint256 amount
        ) with (env e2) {
            requireInvariant mirrorIsTrue(a);
            requireInvariant mirrorIsTrue(b);
            requireInvariant mirrorIsTrue(recipient);
            requireInvariant totalIsSumBalances();
        }
    }
