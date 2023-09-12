
methods {
    function totalSupply() external returns uint256 envfree;
    function balanceOf(address) external returns uint256 envfree;
}


function safeAssumptions() {
    requireInvariant sumOfBalancesEqualsTotalSupplyERC20;
    requireInvariant singleUserBalanceSmallerThanTotalSupplyERC20;
    requireInvariant singleUserBalanceSmallerThanTotalSupplyERC20;
}

rule verifyAssumptionOnUpdate(){
    env e;
    address from;
    address to;
    uint256 amount;

    safeAssumptions();

    mathint balanceOfToBefore = balanceOf(to);
    mathint balanceOfFromBefore = balanceOf(from);
    mathint totalSupplyBefore = totalSupply();

    wrapperUpdate(e, from, to, amount);


    mathint balanceOfToAfter = balanceOf(to);
    mathint balanceOfFromAfter = balanceOf(from);
    mathint totalSupplyAfter = totalSupply();
    
    assert to != 0 && from != to => balanceOfToAfter == balanceOfToBefore + amount;
    assert from != 0 && from != to => balanceOfFromAfter == balanceOfFromBefore - amount;
    assert from == to => balanceOfFromAfter == balanceOfFromBefore;

    assert to == 0 && from != 0 => totalSupplyAfter == totalSupplyBefore - amount;
    assert from == 0 && to != 0 => totalSupplyAfter == totalSupplyBefore + amount;
    assert to != 0 && from != 0 => totalSupplyAfter == totalSupplyBefore;
}


rule noneSense(){
    address x;
    uint256 amount;
    uint256 val = balanceOf(x);

    require balanceOf(x) + amount == val;
    assert amount > 0;
}



invariant sumOfBalancesEqualsTotalSupplyERC20()
    sumOfBalancesERC20 == to_mathint(totalSupply());

ghost mathint sumOfBalancesERC20 {
    init_state axiom sumOfBalancesERC20 == 0;
}

hook Sstore _balances[KEY address user] uint256 newValue (uint256 oldValue) STORAGE {
    sumOfBalancesERC20 = sumOfBalancesERC20 + newValue - oldValue;
    userBalanceERC20 = newValue;
}

hook Sload uint256 value _balances[KEY address auser] STORAGE {
    //This line makes the proof work. But is this actually safe to assume? With every load in the programm, we assume the invariant to already hold.
    require to_mathint(value) <= sumOfBalancesERC20;
}

invariant singleUserBalanceSmallerThanTotalSupplyERC20()
    userBalanceERC20 <= sumOfBalancesERC20;

ghost mathint userBalanceERC20 {
    init_state axiom userBalanceERC20 == 0;
}


//Current results: https://prover.certora.com/output/53900/1c908f0eff9c42518fc6206e42152cd8/?anonymousKey=435376258db9ce72101337c61da0d6e95b45d02f