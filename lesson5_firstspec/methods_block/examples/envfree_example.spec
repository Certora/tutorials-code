/* Methods block example
 * ---------------------
 */

methods{
    // `getFunds` implementation does not require any context to be executed
    function getFunds(address) external returns (uint256) envfree;
}


rule integrityOfDeposit(uint256 amount) {
    env e; 

    uint256 fundsBefore = getFunds(e.msg.sender);
    deposit(e, amount); 
    uint256 fundsAfter = getFunds(e.msg.sender);

    assert (
        fundsBefore + amount == to_mathint(fundsAfter)
    ),
    "Deposit did not increase the funds as expected";
}
