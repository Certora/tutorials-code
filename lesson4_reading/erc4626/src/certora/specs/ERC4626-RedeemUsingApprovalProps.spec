using ERC20Mock as _ERC20;

methods {
    function _ERC20.balanceOf(address) external returns uint256 envfree;
    function allowance(address, address) external returns uint256 envfree;
    function balanceOf(address) external returns uint256 envfree;
    function previewWithdraw(uint256) external returns uint256 envfree;
    function previewRedeem(uint256) external returns uint256 envfree;
    function totalAssets() external returns uint256 envfree;
}

/**
* Special case for when e.msg.sender == owner.
* 1. Third party `withdraw()` calls must update the msg.sender's allowance
* 2. withdraw() must allow proxies to withdraw tokens on behalf of the owner using share token approvals
* 3. Check that is doesn't revert. 
*/
rule ownerWithdrawal(uint256 assets, address receiver, address owner){
    env e; 
    require(e.msg.sender == owner);

    uint256 allowanceBefore = allowance(owner, e.msg.sender);
    withdraw@withrevert(e, assets, receiver, owner);
    uint256 allowanceAfter = allowance(owner, e.msg.sender);
    assert allowanceAfter == allowanceBefore;
    assert lastReverted == false;
}


//Third party `withdraw()` calls must update the msg.sender's allowance
//withdraw() must allow proxies to withdraw tokens on behalf of the owner using share token approvals
rule thirdPartyWithdrawal(uint256 assets, address receiver, address owner){
    env e; 
    require(e.msg.sender != owner);

    uint256 allowanceBefore = allowance(owner, e.msg.sender);
    uint256 shares = previewWithdraw(assets);

    withdraw(e, assets, receiver, owner);

    uint256 allowanceAfter = allowance(owner, e.msg.sender);
    assert allowanceAfter <= allowanceBefore;
    assert shares <= allowanceBefore;
}

//Third parties must not be able to withdraw() tokens on an owner's behalf without a token approval
rule thirdPartyWithdrawalRevertCase(uint256 assets, address receiver, address owner){
    env e; 
    uint256 allowanceBefore = allowance(owner, e.msg.sender);
    uint256 shares = previewWithdraw(assets);
    
    require shares > allowanceBefore;
    //If e.msg.sender is the owner, no allowance is required, see rule ownerWithdrawal
    require e.msg.sender != owner;
        
    withdraw@withrevert(e, assets, receiver, owner);
        
    bool withdrawReverted = lastReverted;

    assert withdrawReverted, "withdraw does not revert when no allowance provided.";
}



/**
* Special case for when e.msg.sender == owner.
* 1. Third party `redeem()` calls must update the msg.sender's allowance
* 2. redeem() must allow proxies to redeem shares on behalf of the owner using share token approvals
* 3. Check that is doesn't revert. 
*/
rule ownerRedeem(uint256 shares, address receiver, address owner){
    env e; 
    require(e.msg.sender == owner);

    uint256 allowanceBefore = allowance(owner, e.msg.sender);
    redeem@withrevert(e, shares, receiver, owner);
    uint256 allowanceAfter = allowance(owner, e.msg.sender);
    assert allowanceAfter == allowanceBefore;
    assert lastReverted == false;
}


//Third party `redeem()` calls must update the msg.sender's allowance
//redeem() must allow proxies to withdraw tokens on behalf of the owner using share token approvals
rule thirdPartyRedeem(uint256 shares, address receiver, address owner){
    env e; 
    require(e.msg.sender != owner);

    uint256 allowanceBefore = allowance(owner, e.msg.sender);
    uint256 assets = previewRedeem(shares);

    redeem(e, shares, receiver, owner);

    uint256 allowanceAfter = allowance(owner, e.msg.sender);
    assert allowanceAfter <= allowanceBefore;
    assert shares <= allowanceBefore;
}

//Third parties must not be able to redeem() tokens on an owner's behalf without a token approval
rule thirdPartyRedeemRevertCase(uint256 shares, address receiver, address owner){
    env e; 
    uint256 allowanceBefore = allowance(owner, e.msg.sender);
    uint256 assets = previewRedeem(shares);
    
    require shares > allowanceBefore;
    //If e.msg.sender is the owner, no allowance is required, see rule ownerWithdrawal
    require e.msg.sender != owner;
        
    redeem@withrevert(e, shares, receiver, owner);
        
    bool redeemReverted = lastReverted;

    assert redeemReverted, "redeem does not revert when no allowance provided.";
}


invariant balanceOfERC20EqualToTotalAsset()
    totalAssets() == _ERC20.balanceOf(currentContract);
