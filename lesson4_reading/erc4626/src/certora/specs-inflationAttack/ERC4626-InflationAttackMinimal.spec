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
    function _ERC20.balanceOf(address) external returns uint256 envfree;

    //Summarizing complicated math logic by a simple version. 
    function Math.mulDiv(uint256 x, uint256 y, uint256 denominator) internal returns uint256 => mulDivSummary(x,y,denominator);
} 

//////////////////////////////////////////////////////
//                                                  //
//           CVL summary functions below            //
//                                                  //
//////////////////////////////////////////////////////

function mulDivSummary(uint256 x, uint256 y, uint256 denominator) returns uint256 {
    return require_uint256(x*y/denominator);
}

//////////////////////////////////////////////////////
//                                                  //
//                 CVL rules below                  //
//                                                  //
//////////////////////////////////////////////////////

/**
* This rule performs a deposit followed by a redeem. The property to check is that the step of actions, 
* a user (attacker) cannot gain any assets
*/
rule simpleVersionOfInflationAttack(uint256 assets, address deposit_receiver, address redeem_receiver, address redeem_ownver) {
    env e;
    safeAssumptionsERC4626();
    address attacker = e.msg.sender;

    //The following 4 lines are not required, but are used to get a simpler counter-example. For a full proof they must be removed.
    require(balanceOf(attacker) == 0);
    require(balanceOf(deposit_receiver) == 0);
    require(balanceOf(redeem_receiver) == 0);
    require(balanceOf(redeem_ownver) == 0);

    require(attacker != currentContract);

    uint256 shares = deposit(e, assets, deposit_receiver);
    uint256 receivedAssets = redeem(e, shares, redeem_receiver, redeem_ownver);

    assert(receivedAssets <= assets, "The attacker gained more assets than deposited.");
}

//////////////////////////////////////////////////////
//                                                  //
//              Helper functions below              //
//                                                  //
//////////////////////////////////////////////////////

//A helper function that can be use to require all invariants proven for ERC4626.
function safeAssumptionsERC4626(){
    requireInvariant sumOfBalancesEqualsTotalSupplyERC4626;
    requireInvariant singleUserBalanceSmallerThanTotalSupplyERC4626;
    safeAssumptionsERC20();
}

//A helper function that can be use to require all invariants proven for ERC20.
function safeAssumptionsERC20() {
    requireInvariant sumOfBalancesEqualsTotalSupplyERC20;
    requireInvariant singleUserBalanceSmallerThanTotalSupplyERC20;
}

//A helper function that can be use to ensure that the mirror of balances for ERC20 and ERC4626 are correct.
function balaceMirrorsAreCorrect(address x) {
    requireInvariant mirrorIsCorrectERC20(x);
    requireInvariant mirrorIsCorrectERC4626(x);
}

//////////////////////////////////////////////////////
//                                                  //
//             Ghost definitions below              //
//                                                  //
//////////////////////////////////////////////////////

ghost mathint sumOfBalancesERC20 {
    init_state axiom sumOfBalancesERC20 == 0;
}

ghost mathint sumOfBalancesERC4626 {
    init_state axiom sumOfBalancesERC4626 == 0;
}

//A mirror of all balances for ERC20
ghost mapping(address => uint256) balanceOfMirroredERC20 {
    init_state axiom forall address a. (balanceOfMirroredERC20[a] == 0);
}

//A mirror of all balances for ERC4626
ghost mapping(address => uint256) balanceOfMirroredERC4626 {
    init_state axiom forall address a. (balanceOfMirroredERC4626[a] == 0);
}

ghost mathint userBalanceERC20 {
    init_state axiom userBalanceERC20 == 0;
}

ghost mathint userBalanceERC4626 {
    init_state axiom userBalanceERC4626 == 0;
}

//////////////////////////////////////////////////////
//                                                  //
//             Hooks definitions below              //
//                                                  //
//////////////////////////////////////////////////////

hook Sstore _ERC20._balances[KEY address user] uint256 newValue (uint256 oldValue) STORAGE {
    sumOfBalancesERC20 = sumOfBalancesERC20 + newValue - oldValue;
    userBalanceERC20 = newValue;
    balanceOfMirroredERC20[user] = newValue;
}

hook Sload uint256 value _ERC20._balances[KEY address user] STORAGE {
    //This line makes the proof work. But is this actually safe to assume? With every load in the programm, we assume the invariant to already hold.
    require to_mathint(value) <= sumOfBalancesERC20;
    require value == balanceOfMirroredERC20[user];
}

hook Sstore ERC4626Mock._balances[KEY address user] uint256 newValue (uint256 oldValue) STORAGE {
    sumOfBalancesERC4626 = sumOfBalancesERC4626 + newValue - oldValue;
    userBalanceERC4626 = newValue;
    balanceOfMirroredERC4626[user] = newValue;
}

hook Sload uint256 value ERC4626Mock._balances[KEY address user] STORAGE {
    //This line makes the proof work. But is this actually safe to assume? With every load in the programm, we assume the invariant to hold.
    require to_mathint(value) <= sumOfBalancesERC4626;
    require value == balanceOfMirroredERC4626[user];
}

//////////////////////////////////////////////////////
//                                                  //
//           Invariants definitions below           //
//                                                  //
//////////////////////////////////////////////////////

invariant sumOfBalancesEqualsTotalSupplyERC20()
    sumOfBalancesERC20 == to_mathint(_ERC20.totalSupply());

invariant sumOfBalancesEqualsTotalSupplyERC4626()
    sumOfBalancesERC4626 == to_mathint(totalSupply());

invariant singleUserBalanceSmallerThanTotalSupplyERC20()
    userBalanceERC20 <= sumOfBalancesERC20;

invariant singleUserBalanceSmallerThanTotalSupplyERC4626()
    userBalanceERC4626 <= sumOfBalancesERC4626;

invariant mirrorIsCorrectERC20(address x)
    balanceOfMirroredERC20[x] == _ERC20.balanceOf(x);

invariant mirrorIsCorrectERC4626(address x)
    balanceOfMirroredERC4626[x] == balanceOf(x);


