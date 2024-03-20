/**
 * Partial solution for ERC20 - Total supply is the sum of balances
 */
methods {
    function balanceOf(address) external returns (uint256) envfree;
    function totalSupply() external returns (uint256) envfree;

}

// ---- Ghosts and hooks -------------------------------------------------------

/// @title A ghost to mirror the balances
ghost mapping(address => uint256) balanceOfMirror {
    init_state axiom forall address a. balanceOfMirror[a] == 0;
}

/// @title A ghost representing the sum of all balances
ghost mathint sumBalances {
    init_state axiom sumBalances == 0;
    axiom forall address a. forall address b. (
        (a != b => sumBalances >= balanceOfMirror[a] + balanceOfMirror[b])
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
