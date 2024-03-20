/**
 * Partial solution for ERC20 - Adding a ghost
 */
methods {
    function balanceOf(address) external returns (uint256) envfree;
    function totalSupply() external returns (uint256) envfree;

}

// ---- Ghosts and hooks -------------------------------------------------------

ghost mathint sumBalances {
    init_state axiom sumBalances == 0;
}

hook Sstore balanceOf[KEY address user] uint256 newBalance (uint256 oldBalance)
{
    sumBalances = sumBalances + newBalance - oldBalance;
}
