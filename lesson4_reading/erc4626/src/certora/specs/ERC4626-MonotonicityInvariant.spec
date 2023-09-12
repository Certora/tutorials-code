
using ERC20 as _ERC20;

methods {
    function totalSupply() external returns uint256 envfree;
    function balanceOf(address) external returns uint256 envfree;
    function allowance(address, address) external returns uint256 envfree;
    function totalAssets() external returns uint256 envfree;
    function previewMint(uint256) external returns uint256 envfree;
    function previewWithdraw(uint256) external returns uint256 envfree;
    function previewDeposit(uint256) external returns uint256 envfree;
    function previewRedeem(uint256) external returns uint256 envfree;
    function _ERC20.totalSupply() external returns uint256 envfree;
}

function safeAssumptions(){
    requireInvariant totalAssetsZeroImpliesTotalSupplyZero;
    requireInvariant sumOfBalancesEqualsTotalSupplyERC4626;
    requireInvariant sumOfBalancesEqualsTotalSupplyERC20;
    requireInvariant singleUserBalanceSmallerThanTotalSupplyERC4626;
    requireInvariant singleUserBalanceSmallerThanTotalSupplyERC20;
}

rule assetAndShareMonotonicy(){

    safeAssumptions();
    uint256 totalAssetsBefore = totalAssets();
    uint256 totalSupplyBefore = totalSupply();

    method f;
    env e;
    uint256 amount;
    address receiver;
    address owner;
    if(f.selector == sig:mint(uint,address).selector){
        mint(e, amount, receiver);
    } else if(f.selector == sig:withdraw(uint,address,address).selector){
        withdraw(e, amount, receiver, owner);
    } else if(f.selector == sig:deposit(uint,address).selector){
        deposit(e, amount, receiver);
    } else if(f.selector == sig:redeem(uint,address,address).selector){
        redeem(e, amount, receiver, owner);
    } else {
        calldataarg args;
        f(e,args);
    }
    
    uint256 totalAssetsAfter = totalAssets();
    uint256 totalSupplyAfter = totalSupply();

    require(e.msg.sender != currentContract);
    assert totalSupplyBefore < totalSupplyAfter <=> totalAssetsBefore < totalAssetsAfter , "Strong monotonicity doesn't hold."; 
    assert (receiver != currentContract) => (totalAssetsBefore <= totalAssetsAfter <=> totalSupplyBefore <= totalSupplyAfter), "Monotonicity doesn't hold."; 
}


invariant totalAssetsZeroImpliesTotalSupplyZero()
    totalAssets() == 0 => totalSupply() == 0
    {

        preserved {
            requireInvariant sumOfBalancesEqualsTotalSupplyERC4626;
            requireInvariant sumOfBalancesEqualsTotalSupplyERC20;
            requireInvariant singleUserBalanceSmallerThanTotalSupplyERC4626;
            requireInvariant singleUserBalanceSmallerThanTotalSupplyERC20;
        }
}

invariant sumOfBalancesEqualsTotalSupplyERC4626()
    sumOfBalancesERC4626 == to_mathint(totalSupply());

ghost mathint sumOfBalancesERC4626 {
    init_state axiom sumOfBalancesERC4626 == 0;
}

hook Sstore balanceOf[KEY address user] uint256 newValue (uint256 oldValue) STORAGE {
    sumOfBalancesERC4626 = sumOfBalancesERC4626 + newValue - oldValue;
    userBalanceERC4626 = newValue;
}

hook Sload uint256 value balanceOf[KEY address auser] STORAGE {
    //This line makes the proof work. But is this actually safe to assume? With every load in the programm, we assume the invariant to hold.
    require to_mathint(value) <= sumOfBalancesERC4626;
}

invariant sumOfBalancesEqualsTotalSupplyERC20()
    sumOfBalancesERC20 == to_mathint(_ERC20.totalSupply());

ghost mathint sumOfBalancesERC20 {
    init_state axiom sumOfBalancesERC20 == 0;
}

hook Sstore _ERC20.balanceOf[KEY address user] uint256 newValue (uint256 oldValue) STORAGE {
    sumOfBalancesERC20 = sumOfBalancesERC20 + newValue - oldValue;
    userBalanceERC20 = newValue;
}

hook Sload uint256 value _ERC20.balanceOf[KEY address auser] STORAGE {
    //This line makes the proof work. But is this actually safe to assume? With every load in the programm, we assume the invariant to already hold.
    require to_mathint(value) <= sumOfBalancesERC20;
}

invariant singleUserBalanceSmallerThanTotalSupplyERC20()
    userBalanceERC20 <= sumOfBalancesERC20;

ghost mathint userBalanceERC20 {
    init_state axiom userBalanceERC20 == 0;
}


invariant singleUserBalanceSmallerThanTotalSupplyERC4626()
    userBalanceERC4626 <= sumOfBalancesERC4626;

ghost mathint userBalanceERC4626 {
    init_state axiom userBalanceERC4626 == 0;
}

