

import "./ERC4626-MonotonicityInvariant.spec";
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

//ERC4626-Monotonicity declares safeAssumptions(), why is it required to activeley declare the invariants used in safeAssumptions in this file?
use invariant totalAssetsZeroImpliesTotalSupplyZero;
use invariant sumOfBalancesEqualsTotalSupply;
use invariant sumOfBalancesEqualsTotalSupplyERC20;
use invariant singleUserBalanceSmallerThanTotalSupply;



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

//Current Results: https://prover.certora.com/output/53900/d309d19804ea430da22bfed21fa3dab2?anonymousKey=c8dc63e28bb1d5f2161f021b0332cbd4cbdfc442
//Current results on Open Zeppelin https://prover.certora.com/output/53900/56ba04402c354671948812c6b58c59ec?anonymousKey=bf80f4cd10de6aebf76c0bea70f6c47e80278290