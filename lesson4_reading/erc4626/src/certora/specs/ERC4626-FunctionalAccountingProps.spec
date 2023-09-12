import "./ERC4626-MonotonicityInvariant.spec";

//Had to change _ERC20 to __ERC20 as of import that already declares _ERC20. 
using ERC20Mock as __ERC20;

//This is counter-intuitive: why we need to import invariants that should be loaded when calling safeAssumptions()? 
use invariant totalAssetsZeroImpliesTotalSupplyZero;
use invariant sumOfBalancesEqualsTotalSupply;
use invariant sumOfBalancesEqualsTotalSupplyERC20;
use invariant singleUserBalanceSmallerThanTotalSupply;

methods {
    function __ERC20.balanceOf(address) external returns uint256 envfree;
    
    function balanceOf(address) external returns uint256 envfree;
    function previewDeposit(uint256) external returns uint256 envfree;
    function previewMint(uint256) external returns uint256 envfree;
    function previewRedeem(uint256) external returns uint256 envfree;
    function previewWithdraw(uint256) external returns uint256 envfree;
    function totalSupply() external returns uint256 envfree;
}

rule depositProperties(uint256 assets, address receiver, address owner){
    safeAssumptions();
    env e;
    //Not an assumption, but just creating an alias for e.msg.sender. Tryout if uint256 owver = e.msg.sender is a better choice here?
    require(e.msg.sender == owner);

    //The caller may not be the currentContract. Is that a fair assumption? 
    //Not sure if solidity allows a way to to fake e.msg.sender attribute. (Delegate call, reflection,...?)
    require(owner != currentContract);
   
        
    mathint ownerAssetsBefore = __ERC20.balanceOf(owner);
    mathint receiverSharesBefore = balanceOf(receiver);

    mathint previewShares = previewDeposit(assets);
    mathint shares = deposit(e, assets, receiver);

    mathint ownerAssetsAfter = __ERC20.balanceOf(owner);
    mathint receiverSharesAfter = balanceOf(receiver);
    
    assert ownerAssetsAfter + assets == ownerAssetsBefore;
    assert receiverSharesAfter - shares == receiverSharesBefore;
    assert shares >= previewShares;
}

rule mintProperties(uint256 shares, address receiver, address owner){
    safeAssumptions();
    env e;
    require(e.msg.sender == owner);

    //The caller may not be the currentContract. Is that a fair assumption? 
    //Not sure if solidity allows a way to to fake e.msg.sender attribute. (Delegate call, reflection,...?)
    require(owner != currentContract);
   
    
    mathint ownerAssetsBefore = __ERC20.balanceOf(owner);
    mathint receiverSharesBefore = balanceOf(receiver);

    mathint previewAssets = previewMint(shares);
    mathint assets = mint(e, shares, receiver);


    mathint ownerAssetsAfter = __ERC20.balanceOf(owner);
    mathint receiverSharesAfter = balanceOf(receiver);
    
    assert ownerAssetsAfter + assets == ownerAssetsBefore;
    assert receiverSharesAfter - shares == receiverSharesBefore;
    assert assets <= previewAssets;
}



rule withdrawProperties(uint256 assets, address receiver, address owner){
    safeAssumptions();
    env e;

    //The caller may not be the currentContract. Is that a fair assumption? 
    //Not sure if solidity allows a way to to fake e.msg.sender attribute. (Delegate call, reflection,...?)
    require(e.msg.sender != currentContract);

    mathint ownerSharesBefore = balanceOf(owner);
    mathint receiverAssetsBefore = __ERC20.balanceOf(receiver);

    mathint previewShares = previewWithdraw(assets);
    mathint shares = withdraw(e, assets, receiver, owner);


    mathint ownerSharesAfter = balanceOf(owner);
    mathint receiverAssetsAfter = __ERC20.balanceOf(receiver);

    assert ownerSharesAfter + shares == ownerSharesBefore;
    assert receiver != currentContract => receiverAssetsAfter - assets == receiverAssetsBefore;

    //Is this according to specifications or a bug? Couldn't find a clear answer to it. Probably yes, receiverAssets remain unchanged, at least don't increase.
    assert receiver == currentContract => receiverAssetsAfter == receiverAssetsBefore;

    assert shares <= previewShares;
}


rule redeemProperties(uint256 shares, address receiver, address owner){
    safeAssumptions();
    env e;

    //The caller may not be the currentContract. Is that a fair assumption? 
    //Not sure if solidity allows a way to to fake e.msg.sender attribute. (Delegate call, reflection,...?)
    require(e.msg.sender != currentContract);

    mathint ownerSharesBefore = balanceOf(owner);
    mathint receiverAssetsBefore = __ERC20.balanceOf(receiver);

    mathint previewAssets = previewRedeem(shares);
    mathint assets = redeem(e, shares, receiver, owner);


    mathint ownerSharesAfter = balanceOf(owner);
    mathint receiverAssetsAfter = __ERC20.balanceOf(receiver);
    
    assert ownerSharesAfter + shares == ownerSharesBefore;
    assert receiver != currentContract => receiverAssetsAfter - assets == receiverAssetsBefore;

    //Is this according to specifications or a bug? Couldn't find a clear answer to it. Probably yes, receiverAssets remain unchanged, at least don't increase.
    assert receiver == currentContract => receiverAssetsAfter == receiverAssetsBefore;

    assert assets >= previewAssets;
}

//Current results: https://prover.certora.com/output/53900/7538cffeb6f5475580378e6b3f25cefd?anonymousKey=a51328c86e7ebd55e0a9bab660fb6dc241ef0cbd//Current results: https://prover.certora.com/output/53900/9bff1a944136468fbd8ae1ec692542f2?anonymousKey=432f0b4234ca29fa80743d112d7579bf60c3440a
//Current results for Open Zeppelin: https://prover.certora.com/output/53900/82f230b8ac15469abeebc1dbcab64c80?anonymousKey=9cee98e777a96b8d5d26e4604b4a9ea1942d73b6