methods {
    function points(address) external returns uint256  envfree;
    function vote(address,address,address) external;
    function voted(address) external returns bool  envfree;
    function winner() external returns address  envfree;
}

rule drawFavorsWinner(env e, address f, address s, address t) {
    address w1 = winner(e);
    
    uint256 w1Points = points(e, w1);
    
    vote(e, f, s, t);
    
    address w2 = winner(e);

    assert w1 != w2 => points(e, f) > w1Points || points(e, s) > w1Points || points(e, t) > w1Points;
}

