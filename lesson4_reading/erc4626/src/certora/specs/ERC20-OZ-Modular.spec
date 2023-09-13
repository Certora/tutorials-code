
import "./ERC4626-MonotonicityInvariant.spec";

methods {
    function totalSupply() external returns uint256 envfree;
    function balanceOf(address) external returns uint256 envfree;
}

use invariant singleUserBalanceSmallerThanTotalSupplyERC20;
use invariant sumOfBalancesEqualsTotalSupplyERC20;

rule verifyAssumptionOnUpdate(){
    env e;
    address from;
    address to;
    uint256 amount;

    safeAssumptionsERC20();

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
