/**
 * Vacuous rules examples
 */
methods {
    function amounts(address) external returns (uint256) envfree;
    function maximalAmount() external returns (uint256) envfree;
    function add(address, uint256) external returns (uint256) envfree;
    function sub(address, uint256) external returns (uint256) envfree;
}


rule simpleVacuousRule(uint256 x, uint256 y) {
    // Contradictory requirement
    require (x > y) && (y > x);
    assert false;  // Should always fail
}


rule subtleVacuousRule(address user, uint256 amount) {
    uint256 userAmount = amounts(user);
    require amount > userAmount;
    sub(user, amount);
    assert false;  // Should always fail
}


rule revertingRule(address user, uint256 amount) {
    uint256 userAmount = amounts(user);
    require amount > userAmount;
    sub@withrevert(user, amount);
    assert lastReverted;
}
