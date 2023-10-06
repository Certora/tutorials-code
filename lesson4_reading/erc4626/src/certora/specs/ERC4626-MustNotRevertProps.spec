

import "./ERC4626-MonotonicityInvariant.spec";

//Had to change _ERC20 to ___ERC20 as of import that already declares __ERC20.
using ERC20 as __ERC20;

//This is counter-intuitive: why we need to import invariants that should be loaded when calling safeAssumptions()? 
use invariant totalAssetsZeroImpliesTotalSupplyZero;
use invariant sumOfBalancesEqualsTotalSupplyERC4626;
use invariant sumOfBalancesEqualsTotalSupplyERC20;
use invariant singleUserBalanceSmallerThanTotalSupplyERC20;
use invariant singleUserBalanceSmallerThanTotalSupplyERC4626;
use invariant mirrorIsCorrectERC20;
use invariant mirrorIsCorrectERC4626;



methods{
    function balanceOf(address) external returns uint256 envfree;
    function convertToAssets(uint256) external returns uint256 envfree;
    function convertToShares(uint256) external returns uint256 envfree;
    function maxDeposit(address) external returns uint256 envfree;
    function maxMint(address) external returns uint256 envfree;
    function maxRedeem(address) external returns uint256 envfree;
    function maxWithdraw(address) external returns uint256 envfree;
    function totalAssets() external returns uint256 envfree;
    function totalSupply() external returns uint256 envfree;
}


definition nonReveritngFunction(method f) returns bool = 
           f.selector == sig:convertToAssets(uint256).selector
        || f.selector == sig:convertToShares(uint256).selector
        || f.selector == sig:totalAssets().selector 
        || f.selector == sig:asset().selector
        || f.selector == sig:maxDeposit(address).selector
        || f.selector == sig:maxMint(address).selector
        || f.selector == sig:maxRedeem(address).selector
        || f.selector == sig:maxWithdraw(address).selector; 


rule mustNotRevertProps(method f) filtered {f -> nonReveritngFunction(f)}{
    env e;
    require(e.msg.value == 0);
    safeAssumptions();
    bool res = callMethodsWithParamenter(e, f);
    assert res == false, "Method ${f} reverted.";
}

function callMethodsWithParamenter(env e, method f)  returns bool {
    uint256 amount;
    address addr;
    if(f.selector == sig:convertToAssets(uint256).selector){
        /**OZ: 
        We'd need to ensure that totalAssets() + 1 does not overflow....totalSupply() + 10**__decimalsOffset() doesn't overflow and the mulDiv doesn't either
        function _convertToAssets(uint256 shares, Math.Rounding rounding) internal view virtual returns (uint256) {
            return shares.mulDiv(totalAssets() + 1, totalSupply() + 10 ** _decimalsOffset(), rounding);
        }
        */
        convertToAssets@withrevert(amount);
        return lastReverted;
    } else if(f.selector == sig:convertToShares(uint256).selector){
        convertToShares@withrevert(amount);
        return lastReverted;
    } else if(f.selector == sig:maxWithdraw(address).selector){
        maxWithdraw@withrevert(addr);
        return lastReverted;
    } else if(f.selector == sig:maxDeposit(address).selector){
        maxDeposit@withrevert(addr);
        return lastReverted;
    } else if(f.selector == sig:maxMint(address).selector){
        maxMint@withrevert(addr);
        return lastReverted;
    } else if(f.selector == sig:maxRedeem(address).selector){
        maxRedeem@withrevert(addr);
        return lastReverted;
    } else if(f.selector == sig:totalAssets().selector  || f.selector == sig:asset().selector){
        calldataarg args;
        f@withrevert(e, args);
        return lastReverted;
    }
    //Should be unreachable. 
    return true;
}
