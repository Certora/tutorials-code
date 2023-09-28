methods {
    function points(address) external returns uint256  envfree;
    function vote(address,address,address) external;
    function voted(address) external returns bool  envfree;
    function winner() external returns address  envfree;
}

// Needed to prove the rule
invariant integrityPointsOfWinner(address c)
            points(winner()) >= points(c);


