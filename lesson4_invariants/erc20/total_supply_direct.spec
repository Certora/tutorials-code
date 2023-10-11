/**
 * Failed attempt to prove that the sum of two distinct balances is not greater than
 * total supply, using a direct approach.
 */
methods {
    function balanceOf(address) external returns (uint256) envfree;
    function totalSupply() external returns (uint256) envfree;

}


invariant directSumOfTwo(address a, address b)
    (a != b) => (balanceOf(a) + balanceOf(b) <= to_mathint(totalSupply()));


invariant directSumOfThree(address a, address b, address c)
    (a != b) => (
        balanceOf(a) + balanceOf(b) + balanceOf(c) <= to_mathint(totalSupply())
    ) {
        preserved with (env e) {
            requireInvariant directSumOfThree(e.msg.sender, a, b);
            requireInvariant directSumOfThree(e.msg.sender, a, c);
            requireInvariant directSumOfThree(e.msg.sender, b, c);
        }
    }
