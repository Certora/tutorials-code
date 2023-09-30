methods {
    function points(address) external returns uint256  envfree;
    function vote(address,address,address) external;
    function voted(address) external returns bool  envfree;
    function winner() external returns address  envfree;
}

rule viewNeverRevert() {
    address _points;
    address _voted;

    winner@withrevert();
    assert !lastReverted;
    points@withrevert(_points);
    assert !lastReverted;
    voted@withrevert(_voted);
    assert !lastReverted;
}
