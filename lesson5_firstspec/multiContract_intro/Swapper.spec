using ERC20Helper as helper;

methods  {
    function ERC20Helper.tokenBalanceOf(address token, address user) external returns (uint256) envfree;

    function _.transfer(address recipient, uint256 amount) external => DISPATCHER(true);
    function _.transferFrom(address sender, address recipient, uint256 amount) external => DISPATCHER(true); 
    function _.getPrice( address tokenFrom, address tokenTo) external => NONDET ;
}


rule swapPayment() {
    address tokenIn;
    address tokenOut;
    uint256 amount;

    env e;
    require e.msg.sender != currentContract ;

    mathint before = helper.tokenBalanceOf(tokenIn, e.msg.sender );
    swap(e, tokenIn, tokenOut, amount);
    mathint after = helper.tokenBalanceOf(tokenIn, e.msg.sender );
    assert tokenIn != tokenOut => after == before - amount;
}

rule check_uint256() {
    uint256 var;
    require var == require_uint256(2 ^ 256);
    assert var > max_uint256;
}

rule check1() {
    assert max_uint256 <= 2 ^ 256;
}

function getCVL() returns(uint256) {
    return 0;
}

rule check_mathint() {
    mathint var;
    require var == 2 ^ 256;
    assert (var > max_uint256);
}