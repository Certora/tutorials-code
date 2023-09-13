import "./ERC4626-MonotonicityInvariant.spec";

//Had to change _ERC20 to ___ERC20 as of import that already declares __ERC20.
using ERC20 as __ERC20;

use invariant totalAssetsZeroImpliesTotalSupplyZero;
use invariant sumOfBalancesEqualsTotalSupplyERC4626;
use invariant sumOfBalancesEqualsTotalSupplyERC20;
use invariant singleUserBalanceSmallerThanTotalSupplyERC20;
use invariant singleUserBalanceSmallerThanTotalSupplyERC4626;



methods{
    function balanceOf(address) external returns uint256 envfree;
    function __ERC20.balanceOf(address) external returns uint256 envfree;
    function decimals() external returns uint8 envfree;
    function totalAssets() external returns uint256 envfree;
    function totalSupply() external returns uint256 envfree;
}

function assumeBalaneEqualSumManualERC4626_4(address addr1,address addr2,address addr3, address addr4){
    mathint totalSupply = totalSupply();
    mathint balanceOfAddr1 = balanceOf(addr1);
    mathint balanceOfAddr2 = balanceOf(addr2);
    mathint balanceOfAddr3 = balanceOf(addr3);
    mathint balanceOfAddr4 = balanceOf(addr4);

    require totalSupply == balanceOfAddr1 + balanceOfAddr2 + balanceOfAddr3 + balanceOfAddr4;
}

function assumeBalaneEqualSumManualERC20_4(address addr1,address addr2,address addr3, address addr4){
    mathint totalSupply = __ERC20.totalSupply();
    mathint balanceOfAddr1 = __ERC20.balanceOf(addr1);
    mathint balanceOfAddr2 = __ERC20.balanceOf(addr2);
    mathint balanceOfAddr3 = __ERC20.balanceOf(addr3);
    mathint balanceOfAddr4 = __ERC20.balanceOf(addr4);

    require totalSupply == balanceOfAddr1 + balanceOfAddr2 + balanceOfAddr3 + balanceOfAddr4;
}
    


rule inverseDepositRedeemInFavourForVault(uint256 assets, address deposit_receiver, address redeem_receiver, address redeem_owner){
    env e;
    safeAssumptions();
    assumeBalaneEqualSumManualERC4626_4(deposit_receiver, redeem_receiver, redeem_owner, e.msg.sender);
    assumeBalaneEqualSumManualERC20_4(deposit_receiver, redeem_receiver, redeem_owner, e.msg.sender);

    uint256 shares = deposit(e, assets, deposit_receiver);
    uint256 redeemedAssets = redeem(e, shares, redeem_receiver, redeem_owner);
    
    assert assets >= redeemedAssets, "User cannot gain assets using deposit / redeem combination.";
}

rule inverseRedeemDepositInFavourForVault(uint256 shares, address deposit_receiver, address redeem_receiver, address redeem_owner){
    env e;
    safeAssumptions();
    assumeBalaneEqualSumManualERC4626_4(deposit_receiver, redeem_receiver, redeem_owner, e.msg.sender);
    assumeBalaneEqualSumManualERC20_4(deposit_receiver, redeem_receiver, redeem_owner, e.msg.sender);
    

    uint256 redeemedAssets = redeem(e, shares, redeem_receiver, redeem_owner);
    uint256 depositedShares = deposit(e, redeemedAssets, deposit_receiver);
    
    assert shares >= depositedShares, "User cannot gain shares using deposit / redeem combination.";
}

rule inverseMintWithdrawInFavourForVault(uint256 shares, address mint_receiver, address withdraw_receiver, address withdraw_owner){
    env e;
    safeAssumptions();
    assumeBalaneEqualSumManualERC4626_4(mint_receiver, withdraw_receiver, withdraw_owner, e.msg.sender);
    assumeBalaneEqualSumManualERC20_4(mint_receiver, withdraw_receiver, withdraw_owner, e.msg.sender);

    uint256 assets = mint(e, shares, mint_receiver);
    uint256 withdrawnShares = withdraw(e, assets, withdraw_receiver, withdraw_owner);
    
    assert shares >= withdrawnShares, "User cannot gain assets using deposit / redeem combination.";
}

rule inverseWithdrawMintInFavourForVault(uint256 assets, address mint_receiver, address withdraw_receiver, address withdraw_owner){
    env e;
    safeAssumptions();
    assumeBalaneEqualSumManualERC4626_4(mint_receiver, withdraw_receiver, withdraw_owner, e.msg.sender);
    assumeBalaneEqualSumManualERC20_4(mint_receiver, withdraw_receiver, withdraw_owner, e.msg.sender);

    uint256 withdrawnShares = withdraw(e, assets, withdraw_receiver, withdraw_owner);
    uint256 mintedAssets = mint(e, withdrawnShares, mint_receiver);
    
    assert assets >= mintedAssets, "User cannot gain assets using deposit / redeem combination.";
}


//TODO: Not sure if this is even a valid property: The rule fails.
rule redeemInOneTransactionIsPreferable(address user, address receiver, uint256 s1, uint256 s2) {
    env e;

    safeAssumptions();
    uint256 shares = require_uint256(s1 + s2);

    //The below requires have been added to find more intuitive counter examples.
    require(e.msg.sender != currentContract);
    require(e.msg.sender != user);
    require(e.msg.sender != receiver);
    require(user != receiver);
    require(totalAssets() >= totalSupply());

    storage init = lastStorage;

    mathint redeemed1a = redeem(e, s1, receiver, user);
    mathint redeemed1b = redeem(e, s2, receiver, user);
    mathint redeemed2 = redeem(e, shares, receiver, user) at init;

    assert(redeemed2 <= redeemed1a + redeemed1b);
}

