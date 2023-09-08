/* Bank - methods block example
 * ----------------------------
 */
 

function preFunctionCall(env e) returns bool {
    uint256 userFunds = getFunds(e, e.msg.sender);
    uint256 total = getTotalFunds(e);
    return total >= userFunds;
}


/// @title Total funds should be at least as high as any user's funds
rule totalFundsAfterDepositWithPrecondition(uint256 amount) {
    env e; 
    
    require preFunctionCall(e);
    deposit(e, amount);

    uint256 userFundsAfter = getFunds(e, e.msg.sender);
    uint256 totalAfter = getTotalFunds(e);

    assert totalAfter >= userFundsAfter, "Total funds are less than a user's funds";
}


/// @title Depositing should increase total funds
rule integrityOfDeposit(uint256 amount) {
    env e; 

    uint256 fundsBefore = getFunds(e, e.msg.sender);
    deposit(e, amount); 
    uint256 fundsAfter = getFunds(e, e.msg.sender);

    assert (
        fundsBefore + amount == to_mathint(fundsAfter)
    ),
    "Deposit did not increase the funds as expected";
}
