
import "./ERC4626-MonotonicityInvariant.spec";
//Had to change _ERC20 to ___ERC20 as of import that already declares __ERC20.
using ERC20Mock as __ERC20;
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
    function __ERC20.balanceOf(address) external returns uint256 envfree;
    function __ERC20.totalSupply() external returns uint256 envfree;
    function decimals() external returns uint8 envfree;
    function totalAssets() external returns uint256 envfree;
    function totalSupply() external returns uint256 envfree;
    function previewWithdraw(uint256 assets) external returns uint256 envfree;
    function previewRedeem(uint256 shares) external returns uint256 envfree;
}

function assumeBalanceEqualSumManualERC4626_4(address addr1,address addr2,address addr3, address addr4){
    mathint totalSupply = totalSupply();
    mathint balanceOfAddr1 = balanceOf(addr1);
    mathint balanceOfAddr2 = balanceOf(addr2);
    mathint balanceOfAddr3 = balanceOf(addr3);
    mathint balanceOfAddr4 = balanceOf(addr4);

    //Case all different
    require addr1 != addr2 && addr1 != addr3 && addr1 != addr4 && addr2 != addr3 && addr2 != addr4 && addr3 != addr4 => totalSupply == balanceOfAddr1 + balanceOfAddr2 + balanceOfAddr3 + balanceOfAddr4;

    //Case two are equal
    require (addr1 == addr2 && addr1 != addr3 && addr1 != addr4 && addr3 != addr4) => totalSupply == balanceOfAddr1 + balanceOfAddr3 + balanceOfAddr4;
    require (addr1 == addr3 && addr1 != addr2 && addr1 != addr4 && addr2 != addr4) => totalSupply == balanceOfAddr1 + balanceOfAddr2 + balanceOfAddr4;
    require (addr1 == addr4 && addr1 != addr2 && addr1 != addr3 && addr2 != addr3) => totalSupply == balanceOfAddr1 + balanceOfAddr2 + balanceOfAddr3;
    require (addr2 == addr3 && addr2 != addr1 && addr2 != addr4 && addr1 != addr4) => totalSupply == balanceOfAddr1 + balanceOfAddr2 + balanceOfAddr4;
    require (addr2 == addr4 && addr2 != addr1 && addr2 != addr3 && addr1 != addr3) => totalSupply == balanceOfAddr1 + balanceOfAddr2 + balanceOfAddr3;
    require (addr3 == addr4 && addr3 != addr1 && addr3 != addr2 && addr1 != addr2) => totalSupply == balanceOfAddr1 + balanceOfAddr2 + balanceOfAddr3;

    //Cases two are equal and the other two as well.
    require (addr1 == addr2 && addr3 == addr4) => totalSupply == balanceOfAddr1 + balanceOfAddr3;
    require (addr1 == addr3 && addr2 == addr4) => totalSupply == balanceOfAddr1 + balanceOfAddr2;
    require (addr2 == addr3 && addr1 == addr4) => totalSupply == balanceOfAddr1 + balanceOfAddr2;

    //Cases three are same
    require (addr1 == addr2 && addr2 == addr3 && addr1 != addr4) => totalSupply == balanceOfAddr1 + balanceOfAddr4; //4 differs
    require (addr1 == addr2 && addr2 == addr4 && addr1 != addr3) => totalSupply == balanceOfAddr1 + balanceOfAddr3; //3 differs
    require (addr1 == addr3 && addr3 == addr4 && addr1 != addr2) => totalSupply == balanceOfAddr1 + balanceOfAddr2; //2 differs
    require (addr2 == addr3 && addr3 == addr4 && addr1 != addr2) => totalSupply == balanceOfAddr2 + balanceOfAddr1; //1 differs
    
    require addr1 == addr2 && addr2 == addr3 && addr3 == addr4 => totalSupply == balanceOfAddr1;
}

function assumeBalanceEqualSumManualERC20_4(address addr1,address addr2,address addr3, address addr4){

    mathint totalSupply = __ERC20.totalSupply();

    if(addr1 != currentContract && addr2 != currentContract  && addr3 != currentContract && addr4 != currentContract){
        totalSupply = totalSupply - __ERC20.balanceOf(currentContract);
    }
    mathint balanceOfAddr1 = __ERC20.balanceOf(addr1);
    mathint balanceOfAddr2 = __ERC20.balanceOf(addr2);
    mathint balanceOfAddr3 = __ERC20.balanceOf(addr3);
    mathint balanceOfAddr4 = __ERC20.balanceOf(addr4);

    //Case all different
    require addr1 != addr2 && addr1 != addr3 && addr1 != addr4 && addr2 != addr3 && addr2 != addr4 && addr3 != addr4 => totalSupply == balanceOfAddr1 + balanceOfAddr2 + balanceOfAddr3 + balanceOfAddr4;

    //Case two are equal
    require (addr1 == addr2 && addr1 != addr3 && addr1 != addr4 && addr3 != addr4) => totalSupply == balanceOfAddr1 + balanceOfAddr3 + balanceOfAddr4;
    require (addr1 == addr3 && addr1 != addr2 && addr1 != addr4 && addr2 != addr4) => totalSupply == balanceOfAddr1 + balanceOfAddr2 + balanceOfAddr4;
    require (addr1 == addr4 && addr1 != addr2 && addr1 != addr3 && addr2 != addr3) => totalSupply == balanceOfAddr1 + balanceOfAddr2 + balanceOfAddr3;
    require (addr2 == addr3 && addr2 != addr1 && addr2 != addr4 && addr1 != addr4) => totalSupply == balanceOfAddr1 + balanceOfAddr2 + balanceOfAddr4;
    require (addr2 == addr4 && addr2 != addr1 && addr2 != addr3 && addr1 != addr3) => totalSupply == balanceOfAddr1 + balanceOfAddr2 + balanceOfAddr3;
    require (addr3 == addr4 && addr3 != addr1 && addr3 != addr2 && addr1 != addr2) => totalSupply == balanceOfAddr1 + balanceOfAddr2 + balanceOfAddr3;

    //Cases two are equal and the other two as well.
    require (addr1 == addr2 && addr3 == addr4) => totalSupply == balanceOfAddr1 + balanceOfAddr3;
    require (addr1 == addr3 && addr2 == addr4) => totalSupply == balanceOfAddr1 + balanceOfAddr2;
    require (addr2 == addr3 && addr1 == addr4) => totalSupply == balanceOfAddr1 + balanceOfAddr2;
    
    //Cases three are same
    require (addr1 == addr2 && addr2 == addr3 && addr1 != addr4) => totalSupply == balanceOfAddr1 + balanceOfAddr4; //4 differs
    require (addr1 == addr2 && addr2 == addr4 && addr1 != addr3) => totalSupply == balanceOfAddr1 + balanceOfAddr3; //3 differs
    require (addr1 == addr3 && addr3 == addr4 && addr1 != addr2) => totalSupply == balanceOfAddr1 + balanceOfAddr2; //2 differs
    require (addr2 == addr3 && addr3 == addr4 && addr1 != addr2) => totalSupply == balanceOfAddr2 + balanceOfAddr1; //1 differs
    
    require addr1 == addr2 && addr2 == addr3 && addr3 == addr4 => totalSupply == balanceOfAddr1;
}

rule inverseDepositRedeemInFavourForVault(uint256 assets, address deposit_receiver, address redeem_receiver, address redeem_owner){
    env e;
    safeAssumptions();

    assumeBalanceEqualSumManualERC20_4(deposit_receiver,redeem_receiver, redeem_owner, e.msg.sender);
    assumeBalanceEqualSumManualERC4626_4(deposit_receiver,redeem_receiver, redeem_owner, e.msg.sender);

    uint256 shares = deposit(e, assets, deposit_receiver);
    uint256 redeemedAssets = redeem(e, shares, redeem_receiver, redeem_owner);
    
    assert assets >= redeemedAssets, "User cannot gain assets using deposit / redeem combination.";
}

rule inverseRedeemDepositInFavourForVault(uint256 shares, address deposit_receiver, address redeem_receiver, address redeem_owner){
    env e;
    safeAssumptions();

    assumeBalanceEqualSumManualERC20_4(deposit_receiver,redeem_receiver, redeem_owner, e.msg.sender);
    assumeBalanceEqualSumManualERC4626_4(deposit_receiver,redeem_receiver, redeem_owner, e.msg.sender);

    uint256 redeemedAssets = redeem(e, shares, redeem_receiver, redeem_owner);
    uint256 depositedShares = deposit(e, redeemedAssets, deposit_receiver);
    
    assert shares >= depositedShares, "User cannot gain shares using redeem / deposit combination.";
}

rule inverseMintWithdrawInFavourForVault(uint256 shares, address mint_receiver, address withdraw_receiver, address withdraw_owner){
    env e;
    safeAssumptions();

    assumeBalanceEqualSumManualERC20_4(mint_receiver,withdraw_receiver, withdraw_owner, e.msg.sender);
    assumeBalanceEqualSumManualERC4626_4(mint_receiver,withdraw_receiver, withdraw_owner, e.msg.sender);

    uint256 assets = mint(e, shares, mint_receiver);
    uint256 withdrawnShares = withdraw(e, assets, withdraw_receiver, withdraw_owner);
    
    assert shares >= withdrawnShares, "User cannot gain assets using mint / withdraw combination.";
}

rule inverseWithdrawMintInFavourForVault(uint256 assets, address mint_receiver, address withdraw_receiver, address withdraw_owner){
    env e;
    safeAssumptions();

    assumeBalanceEqualSumManualERC20_4(mint_receiver,withdraw_receiver, withdraw_owner, e.msg.sender);
    assumeBalanceEqualSumManualERC4626_4(mint_receiver,withdraw_receiver, withdraw_owner, e.msg.sender);

    uint256 withdrawnShares = withdraw(e, assets, withdraw_receiver, withdraw_owner);
    uint256 mintedAssets = mint(e, withdrawnShares, mint_receiver);
    
    assert assets >= mintedAssets, "User cannot gain assets using withdraw / mint combination.";
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