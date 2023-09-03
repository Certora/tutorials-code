/*
 * ERC20 Example
 * -------------
 */

 methods {
    // envfree functions 
    function totalSupply() external returns uint256 envfree;
    function balanceOf(address) external returns uint256 envfree;
    function allowance(address,address) external returns uint256 envfree;
    function _owner() external returns address envfree;
}


// @title Checks that `transferFrom()`  decreases allowance of `e.msg.sender`
rule integrityOfTransferFrom(address sender, address recipient, uint256 amount) {
    env e;
    
    require sender != recipient;
    require amount != 0;


    uint256 allowanceBefore = allowance(sender, e.msg.sender);
    transferFrom(e, sender, recipient, amount);
    uint256 allowanceAfter = allowance(sender, e.msg.sender);
    
    assert (
        allowanceBefore > allowanceAfter
        ),
        "allowance must decrease after using the allowance to pay on behalf of somebody else";
}

/*
    The function below just calls (dispatch) all methods (an arbitrary one) from the contract, 
    using given [env e], [address from] and [address to].
    We use this function in several rules. The usecase is typically to show that 
    the call of the function does not affect a "property" of a third party (i.e. != e.msg.sender, from, to),
    such as the balance or allowance.  

*/
function callFunctionWithParams(env e, method f, address from, address to) {
    uint256 amount;

    if (f.selector == sig:transfer(address, uint256).selector) {
        require e.msg.sender == from;
        transfer(e, to, amount);
    } else if (f.selector == sig:allowance(address, address).selector) {
        allowance(e, from, to);
    } else if (f.selector == sig:approve(address, uint256).selector) {
        approve(e, to, amount);
    } else if (f.selector == sig:transferFrom(address, address, uint256).selector) {
        transferFrom(e, from, to, amount);
    } else if (f.selector == sig:increaseAllowance(address, uint256).selector) {
        increaseAllowance(e, to, amount);
    } else if (f.selector == sig:decreaseAllowance(address, uint256).selector) {
        decreaseAllowance(e, to, amount);
    } else if (f.selector == sig:mint(address, uint256).selector) {
        mint(e, to, amount);
    } else if (f.selector == sig:burn(address, uint256).selector) {
        burn(e, from, amount);
    } else {
        calldataarg args;
        f(e, args);
    }
}

/*
    Given addresses [e.msg.sender], [from], [to] and [thirdParty], we check that 
    there is no method [f] that would:
    1] not take [thirdParty] as an input argument, and
    2] yet changed the balance of [thirdParty].
    Intuitively, we target the case where a transfer of tokens [from] -> [to]
    changes the balance of [thirdParty]. 
*/
rule doesNotAffectAThirdPartyBalance(method f) {
    env e;  
    address from;
    address to;
    address thirdParty;

    require (thirdParty != from) && (thirdParty != to);

    uint256 thirdBalanceBefore = balanceOf(thirdParty);
    
    callFunctionWithParams(e, f, from, to);

    assert balanceOf(thirdParty) == thirdBalanceBefore;
}




/** @title Users' balance can only be changed as a result of `transfer()`,
 * `transferFrom()`,`mint()`, and `burn()`.
 *
 * @notice The use of `f.selector` in this rule is very similar to its use in solidity.
 * Since f is a parametric method that can be any function in the contract, we use
 * `f.selector` to specify the functions that may change the balance.
 */
rule balanceChangesFromCertainFunctions(method f, address user){
    env e;
    calldataarg args;
    uint256 userBalanceBefore = balanceOf(user);
    f(e, args);
    uint256 userBalanceAfter = balanceOf(user);

    assert (
        userBalanceBefore != userBalanceAfter => 
        (
            f.selector == sig:transfer(address, uint256).selector ||
            f.selector == sig:transferFrom(address, address, uint256).selector ||
            f.selector == sig:mint(address, uint256).selector ||
            f.selector == sig:burn(address, uint256).selector)
        ),
        "user's balance changed as a result function other than transfer(), transferFrom(), mint() or burn()";
}


rule onlyOwnersMayChangeTotalSupply(method f) {
    env e;
    uint256 totalSupplyBefore = totalSupply();
    calldataarg args;
    f(e,args);
    uint256 totalSupplyAfter = totalSupply();
    assert totalSupplyAfter != totalSupplyBefore => e.msg.sender == _owner() ;
}