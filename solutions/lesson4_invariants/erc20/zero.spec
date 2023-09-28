/**
 * ERC20 spec - invariant proving address zero has balance zero
 */
 methods {
     function balanceOf(address) external returns (uint256) envfree;
 }

/// @title Address zero has no balance
invariant zeroHasNoBalance()
    balanceOf(0) == 0;
