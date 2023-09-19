
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
    function __ERC20.allowance(address,address) external returns uint256 envfree;
    function __ERC20.balanceOf(address) external returns uint256 envfree;
    function __ERC20.decimals() external returns uint8 envfree;
    function __ERC20.totalSupply() external returns uint256 envfree;
    
    function balanceOf(address) external returns uint256 envfree;
    function convertToAssets(uint256) external returns uint256 envfree;
    function convertToShares(uint256) external returns uint256 envfree;
    function decimals() external returns uint8 envfree;
    function previewDeposit(uint256) external returns uint256 envfree;
    function previewMint(uint256) external returns uint256 envfree;
    function previewWithdraw(uint256) external returns uint256 envfree;
    function totalAssets() external returns uint256 envfree;
    function totalSupply() external returns uint256 envfree;
}



rule simpleVersionOfVulnerableAttack(uint256 assets, address deposit_receiver, address redeem_receiver, address redeem_ownver) {
    env e;
    safeAssumptions();
    address attacker = e.msg.sender;

    require(balanceOf(attacker) == 0);
    require(balanceOf(deposit_receiver) == 0);
    require(balanceOf(redeem_receiver) == 0);
    require(balanceOf(redeem_ownver) == 0);

    require(attacker != currentContract);

    uint256 shares = deposit(e, assets, deposit_receiver);

    //In the inflationAttack there are 2 steps that we don't model here! 

    uint256 receivedAssets = redeem(e, shares, redeem_receiver, redeem_ownver);
    assert(receivedAssets <= assets);
}




//Source: Medium Article by Shao https://tienshaoku.medium.com/eip-4626-inflation-sandwich-attack-deep-dive-and-how-to-solve-it-9e3e320cc3f1
rule vulnerableToInflationAttack(address attacker, address victim, address deposit1_receiver, address deposit2_victim_receiver,address redeem_receiver,address redeem_ownver ){

    //Doesn't work properly...Retry later.
    /*requireInvariant sumOfBalancesEqualsTotalSupplyERC4626;
    requireInvariant sumOfBalancesEqualsTotalSupplyERC20;
    requireInvariant singleUserBalanceSmallerThanTotalSupplyERC4626;
    requireInvariant singleUserBalanceSmallerThanTotalSupplyERC20;*/
    //Doesn't work
    //require forall address x. balanceOf(x) <= totalSupply();
    //Doesn't work
    //require forall address y. __ERC20.balanceOf(y) <= __ERC20.totalSupply();
    safeAssumptions();
    uint256 oneEther;
    uint256 oneWei;

    require(oneWei > 0);
    require(oneEther > 0);

    mathint assetsAttackerPreAttack = to_mathint(oneEther) + to_mathint(oneWei);
    uint8 ERC4626decimals = decimals();
    uint8 ERC20decimals = __ERC20.decimals();
    
    require(attacker != currentContract);
    require(attacker != __ERC20);
    require(attacker != 0);
    require(victim != currentContract);
    require(victim != __ERC20);
    require(victim != 0);
    require(victim != attacker);

    //Following the pattern "First Deposit" of the article.
    require(totalSupply() == 0);
    require(totalAssets() == 0);

    //Duplicated all requireInvariants
    //Doesn't work either....
    require(balanceOf(attacker) == 0);
    require(balanceOf(victim) == 0);
    require(balanceOf(deposit1_receiver) == 0);
    require(balanceOf(deposit2_victim_receiver) == 0);
    require(balanceOf(redeem_receiver) == 0);
    require(balanceOf(redeem_ownver) == 0);
        
    uint256 before_step_1_totalSupply = totalSupply();
    uint256 before_step_1_totalAssets = totalAssets();

    /**
    * Step 1: the attacker front-runs the depositor and deposits 1 wei WETH and gets 1 share: since totalSupply is 0, shares = 1 * 10**18 / 10**18 = 1
    */
    env e1;
    require(e1.msg.sender == attacker);
    uint256 firstShares = deposit(e1, oneEther, deposit1_receiver);
    
    uint256 before_step_2_totalSupply = totalSupply();
    uint256 before_step_2_totalAssets = totalAssets();

    env e2;
    require(e2.msg.sender == attacker);
    require(e2.block.timestamp > e1.block.timestamp);

    require(__ERC20.balanceOf(attacker) >= oneWei);

    /**
    * Step 2: the attacker also transfers 1 * 1e18 weiWETH, making the totalAssets() WETH balance of the vault become 1e18 + 1 wei
    */
    __ERC20.transferFrom(e2, attacker, currentContract, oneWei);
    require(__ERC20.balanceOf(currentContract) > 0);
    
    uint256 before_step_3_totalSupply = totalSupply();
    uint256 before_step_3_totalAssets = totalAssets();

    //assert before_step_3_totalSupply > 0;

    
    /** 
    * Step 3: 
    * The spied-on depositor deposits 1e18 wei WETH. However, the depositor gets 0 shares: 1e18 * 1 (totalSupply) / (1e18 + 1) = 1e18 / (1e18 + 1) = 0. 
    * Since the depositor gets 0 shares, totalSupply() remains at 1
    */
    env e3;
    require(e3.msg.sender == victim);
    require(e3.block.timestamp > e2.block.timestamp);
    uint256 previweAssets = previewDeposit(oneWei);
    uint256 victimShares = deposit(e3, oneWei, deposit2_victim_receiver);
    
    /**
    * Step 4: the attacker still has the 1 only share ever minted and thus the withdrawal of
    * that 1 share takes away everything in the vault, including the depositor’s 1e18 weiWETH
    */
    
    uint256 before_step_4_totalSupply = totalSupply();
    uint256 before_step_4_totalAssets = totalAssets();
    uint256 random; 
    env e4;
    require(e4.msg.sender == attacker);
    require(e4.block.timestamp > e3.block.timestamp);
    //TODO: can attacker actually withdraw `convertToAssets(before_step_4_totalSupply)` or only `assetsAttackerPreAttack`
    mathint assetsAttackerPostAttack = redeem(e4, before_step_4_totalSupply, redeem_receiver, redeem_ownver);

    uint256 finalTotalAssets = totalAssets();
    uint256 finalTotalSupply = totalSupply();
    mathint assetsAttackerGained = assetsAttackerPostAttack - assetsAttackerPreAttack;
    
    assert assetsAttackerPreAttack >= assetsAttackerPostAttack, "The attacker gained assets.";
}
