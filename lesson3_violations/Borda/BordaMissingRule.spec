
methods {
    function points(address) external returns uint256  envfree;
    function vote(address,address,address) external;
    function voted(address) external returns bool  envfree;
    function winner() external returns address  envfree;
	function getWinnerPoints() external returns uint256 envfree optional;
}



invariant mod_integrityPointsOfWinner(address c)
            points(winner()) == getWinnerPoints();

