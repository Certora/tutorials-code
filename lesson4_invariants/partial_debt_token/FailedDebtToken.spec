/**
 * Failed attempt for a debt token invariant
 *
 * An invariant claiming the collateral of
 * an account is never less than the balance.
 */
methods {
    function balanceOf(address) external returns (uint256) envfree;
    function collateralOf(address) external returns (uint256) envfree;
}


/// @title Collateral is never less than the balance
invariant collateralCoversBalance(address account)
    collateralOf(account) >= balanceOf(account);
