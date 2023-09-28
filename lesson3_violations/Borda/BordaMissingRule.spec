methods {
    function points(address) external returns uint256  envfree;
    function vote(address,address,address) external;
    function voted(address) external returns bool  envfree;
    function winner() external returns address  envfree;
}

// Needed to prove the rule
invariant integrityPointsOfWinner(address c)
            points(winner()) >= points(c);

rule preferLastVotedHigh(address f, address s, address t) {
	env e;
    uint prev_points = points(winner());
	vote(e, f, s, t);
	address w = winner();
	assert (points(w) == points(f) => points(w) == prev_points || w == f);
	assert (points(w) == points(s) => points(w) == prev_points || w == f || w == s);
	assert (points(w) == points(t) => points(w) == prev_points || w == f || w == s || w == t);
}
