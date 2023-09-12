import "./ERC4626-MonotonicityInvariant.spec";

//Had to change _ERC20 to ___ERC20 as of import that already declares __ERC20.
using ERC20 as __ERC20;

use invariant totalAssetsZeroImpliesTotalSupplyZero;
use invariant sumOfBalancesEqualsTotalSupply;
use invariant sumOfBalancesEqualsTotalSupplyERC20;
use invariant singleUserBalanceSmallerThanTotalSupply;


methods {
    function allowance(address, address) external returns uint256 envfree;
    function totalAssets() external returns uint256 envfree;
    function decimals() external returns uint8 envfree;
    function __ERC20.decimals() external returns uint8 envfree;
    function totalSupply() external returns uint256 envfree;
}


//deposit must increase totalSupply
rule depositMustIncreaseTotalSupply(uint256 assets, address user){
    safeAssumptions();

    uint256 totalSupplyBefore = totalSupply();
    env e; 
    deposit(e, assets, user);
    uint256 totalSupplyAfter = totalSupply();
    assert totalSupplyAfter >= totalSupplyBefore, "Total supply must increase when deposit is called."; 
}

//mint must increase totalAssets
rule mintMustIncreaseTotalAssets(uint256 shares, address user){
    safeAssumptions();

    uint256 totalAssetsBefore = totalAssets();
    env e;
    mint(e, shares, user);
    uint256 totalAssetsAfter = totalAssets();
    assert totalAssetsAfter >= totalAssetsBefore, "Total assets must increase when mint is called."; 
}

//withdraw must decrease totalAssets
rule withdrawMustDecreaseTotalSupply(uint256 assets, address receiver, address owner){
    safeAssumptions();
    
    uint256 totalSupplyBefore = totalSupply();
    env e; 

    withdraw(e, assets, receiver, owner);
    uint256 totalSupplyAfter = totalSupply();
    assert totalSupplyAfter <= totalSupplyBefore, "Total supply must decrease when withdraw is called."; 
}

//redeem must decrease totalAssets
rule redeemMustDecreaseTotalAssets(uint256 shares, address receiver, address owner){
    safeAssumptions();

    uint256 totalAssetsBefore = totalAssets();
    env e;
    redeem(e, shares, receiver, owner);
    uint256 totalAssetsAfter = totalAssets();
    assert totalAssetsAfter <= totalAssetsBefore, "Total assets must decrease when redeem is called."; 
}

//`decimals()` should be larger than or equal to `asset.decimals()`
rule decimalsOfUnderlyingVaultShouldBeLarger(uint256 shares, address receiver, address owner){
    //TODO: Rule fails. The method call to decimals returns a HAVOC'd value. Still the solver should be able to reason that ERC4626.decimals == ERC20.decimals as of the call to the super constructor.
    safeAssumptions();

    uint8 assetDecimals = __ERC20.decimals();
    uint8 decimals = decimals();
    
    assert decimals >= assetDecimals, "Decimals of underlying ERC20 should be larger than ERC4626 decimals."; 
}

//Current results:  https://prover.certora.com/output/53900/37a8a72cd1f6426383fa9d0d884dff39?anonymousKey=20d731f3d50ddececfa308670b0848ee616e4e58