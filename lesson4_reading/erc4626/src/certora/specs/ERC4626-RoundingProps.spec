
//Had to change _ERC20 to ___ERC20 as of import that already declares __ERC20.
using ERC20Mock as __ERC20;



methods{
    function balanceOf(address) external returns uint256 envfree;
    function __ERC20.balanceOf(address) external returns uint256 envfree;
    function __ERC20.totalSupply() external returns uint256 envfree;
    function decimals() external returns uint8 envfree;
    function totalAssets() external returns uint256 envfree;
    function totalSupply() external returns uint256 envfree;
}

function mulDivSummary(uint256 x, uint256 y, uint256 denominator) returns uint256 {
    uint256 res;
   // require(res * denominator) <= x * y;
   // require((res + 1) * denominator) > x * y;

    require x <= denominator;  
    require res <= y;  
    
    return res;
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
    
    //Cases three are same
    require (addr1 == addr2 && addr2 == addr3 && addr1 != addr4) => totalSupply == balanceOfAddr1 + balanceOfAddr4; //4 differs
    require (addr1 == addr2 && addr2 == addr4 && addr1 != addr3) => totalSupply == balanceOfAddr1 + balanceOfAddr3; //3 differs
    require (addr1 == addr3 && addr3 == addr4 && addr1 != addr2) => totalSupply == balanceOfAddr1 + balanceOfAddr2; //2 differs
    require (addr2 == addr3 && addr3 == addr4 && addr1 != addr2) => totalSupply == balanceOfAddr2 + balanceOfAddr1; //1 differs
    
    require addr1 == addr2 && addr2 == addr3 && addr3 == addr4 => totalSupply == balanceOfAddr1;
}

function assumeBalanceEqualSumManualERC20_4(address addr1,address addr2,address addr3, address addr4){
    mathint totalSupply = __ERC20.totalSupply();
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
    
    //Cases three are same
    require (addr1 == addr2 && addr2 == addr3 && addr1 != addr4) => totalSupply == balanceOfAddr1 + balanceOfAddr4; //4 differs
    require (addr1 == addr2 && addr2 == addr4 && addr1 != addr3) => totalSupply == balanceOfAddr1 + balanceOfAddr3; //3 differs
    require (addr1 == addr3 && addr3 == addr4 && addr1 != addr2) => totalSupply == balanceOfAddr1 + balanceOfAddr2; //2 differs
    require (addr2 == addr3 && addr3 == addr4 && addr1 != addr2) => totalSupply == balanceOfAddr2 + balanceOfAddr1; //1 differs
    
    require addr1 == addr2 && addr2 == addr3 && addr3 == addr4 => totalSupply == balanceOfAddr1;
}
    
rule inverseMintWithdrawInFavourForVault_LessRestrictive(uint256 shares, address mint_receiver, address withdraw_receiver, address withdraw_owner){
    env e;
    assumeBalanceEqualSumManualERC20_4(mint_receiver,withdraw_receiver, withdraw_owner, e.msg.sender);
    assumeBalanceEqualSumManualERC4626_4(mint_receiver,withdraw_receiver, withdraw_owner, e.msg.sender);

    //Dismiss allowance case
    require(e.msg.sender == withdraw_owner);

    //Make all non zero to avoid unnecessary cases.
    require(e.msg.sender != 0);
    require(mint_receiver != 0);
    require(withdraw_owner != 0);
    require(withdraw_receiver != 0);


    require(e.msg.sender == withdraw_owner);

    uint256 assets = mint(e, shares, mint_receiver);
    uint256 withdrawnShares = withdraw(e, assets, withdraw_receiver, withdraw_owner);
    
    assert shares >= withdrawnShares, "User cannot gain assets using deposit / redeem combination.";
}
