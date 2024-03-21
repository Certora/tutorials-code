
/**
* A combination of all acknoweldged missing bugs 
**/

methods {
    function points(address) external returns uint256  envfree;
    function vote(address,address,address) external;
    function voted(address) external returns bool  envfree;
    function winner() external returns address  envfree;
}
/**
 * @author https://github.com/Czar102 
 * @dev  integrity of voted()
 * @notice reported in https://github.com/Certora/tutorials-code/issues/5
 * @dev catches buggy version BordaNewBug1.sol
**/
ghost mapping(address => bool) voted_mirror {
	init_state axiom forall address c. !voted_mirror[c];
}

hook Sstore _voted[KEY address a] bool val (bool old_val) {
	voted_mirror[a] = val;
}

/*BordaMissingRule() */
invariant integrityOfVoted()
	forall address a. voted_mirror[a] == voted(a);


/**
 * @author https://github.com/imsrybr0 
 * @dev  draw favor winner
 * @notice https://github.com/Certora/tutorials-code/issues/7
 * @dev catches buggy version BordaNewBug2.sol
**/
rule drawFavorsWinner(env e, address f, address s, address t) {
    address w1 = winner(e);

    require w1 != f;
    require w1 != s;
    require w1 != t;
    
    uint256 w1Points = points(e, w1);
    
    vote(e, f, s, t);
    
    address w2 = winner(e);

    assert w1 != w2 <=> points(e, f) > w1Points || points(e, s) > w1Points || points(e, t) > w1Points;
}


/**
 * @author https://github.com/Czar102 
 * @dev  prefers last voted high
 * @notice reported in https://github.com/Certora/tutorials-code/issues/13
 * @dev catches buggy version BordaNewBug3.sol
**/

rule preferLastVotedHigh(address f, address s, address t) {
	env e;
    uint prev_points = points(winner());
	vote(e, f, s, t);
	address w = winner();
	assert (points(w) == points(f) => points(w) == prev_points || w == f);
	assert (points(w) == points(s) => points(w) == prev_points || w == f || w == s);
	assert (points(w) == points(t) => points(w) == prev_points || w == f || w == s || w == t);
}

/**
 * @author https://github.com/peritoflores 
 * @dev  winner can only change by vote
 * @notice reported in https://github.com/Certora/tutorials-code/issues/14
 * @dev catches buggy version BordaNewBug4.sol
**/
rule changeToWinner(env e,method m){

    require m.selector != sig:vote(address,address,address).selector;
    address winnerBefore = winner();
    calldataarg args; 
    m(e,args);
    address winnerAfter = winner();
    assert winnerAfter == winnerBefore ,  "The winner can be changed only after voting";
}

/**
 * @author https://github.com/Czar102 
 * @dev  prefers last voted high
 * @notice reported in https://github.com/Certora/tutorials-code/issues/17
 * @dev catches buggy version BordaNewBug5.sol
**/

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
