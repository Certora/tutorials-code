
using ERC20Mock as _ERC20;

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
    function ERC20._update(address from, address to, uint256 value) internal => updateStub(from, to, value);
}

function updateStub(address from,  address to ,uint256 amount) {
    uint256 balanceOfTo = balanceOf(to);
    uint256 balanceOfFrom = balanceOf(from);
    uint256 totalSupply = totalSupply();
    //TODO: verify the assumptions by writing a rule for it.
    if(to != from){
        require (balanceOf(to) == require_uint256(balanceOfTo + amount));
        require (balanceOf(from) == require_uint256(balanceOfFrom - amount));
        require (require_uint256(totalSupply + amount) == totalSupply());
    }
}

function safeAssumptions(){
    requireInvariant totalAssetsZeroImpliesTotalSupplyZero;
    requireInvariant sumOfBalancesEqualsTotalSupply;
    requireInvariant sumOfBalancesEqualsTotalSupplyERC20;
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

/**
* This invariant does not hold for OpenZeppelin. There is a public function mint that allows to increase totalSupply without increasing totalAssets! 
*/
invariant totalAssetsZeroImpliesTotalSupplyZero()
    totalAssets() == 0 => totalSupply() == 0
    {

        preserved {
            requireInvariant sumOfBalancesEqualsTotalSupply;
            requireInvariant sumOfBalancesEqualsTotalSupplyERC20;
            requireInvariant singleUserBalanceSmallerThanTotalSupply;
        }
}

invariant sumOfBalancesEqualsTotalSupply()
    sumOfBalances == to_mathint(totalSupply());

ghost mathint sumOfBalances {
    init_state axiom sumOfBalances == 0;
}

hook Sstore _balances[KEY address user] uint256 newValue (uint256 oldValue) STORAGE {
    sumOfBalances = sumOfBalances + newValue - oldValue;
}
hook Sload uint256 value _balances[KEY address auser] STORAGE {
    //This line makes the proof work. But is this actually safe to assume? With every load in the programm, we assume the invariant to hold.
    require to_mathint(value) <= sumOfBalances;
}

invariant sumOfBalancesEqualsTotalSupplyERC20()
    sumOfBalancesERC20 == to_mathint(_ERC20.totalSupply());

ghost mathint sumOfBalancesERC20 {
    init_state axiom sumOfBalancesERC20 == 0;
}

hook Sstore _ERC20._balances[KEY address user] uint256 newValue (uint256 oldValue) STORAGE {
    sumOfBalancesERC20 = sumOfBalancesERC20 + newValue - oldValue;
    userBalance = newValue;
}

hook Sload uint256 value _ERC20._balances[KEY address auser] STORAGE {
    //This line makes the proof work. But is this actually safe to assume? With every load in the programm, we assume the invariant to already hold.
    require to_mathint(value) <= sumOfBalancesERC20;
}

invariant singleUserBalanceSmallerThanTotalSupply()
    userBalance <= sumOfBalancesERC20;

ghost mathint userBalance {
    init_state axiom userBalance == 0;
}

//Current results: https://prover.certora.com/output/53900/1c908f0eff9c42518fc6206e42152cd8/?anonymousKey=435376258db9ce72101337c61da0d6e95b45d02f