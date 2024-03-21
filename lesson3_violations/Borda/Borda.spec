/*
 * Borda Example
 * -------------
 *
 * Verification of a simple voting contract which uses a Borda election.
 * See https://en.wikipedia.org/wiki/Borda_count
 */



methods {
    function points(address) external returns uint256  envfree;
    function vote(address,address,address) external;
    function voted(address) external returns bool  envfree;
    function winner() external returns address  envfree;
}

/*
After voting, a user is marked as voted
    vote(e, f, s, t) => voted(e.msg.sender)
*/
rule integrityVote(address f, address s, address t) {
    env e;
    vote(e, f, s, t); //considering only non reverting cases 
    assert voted(e.msg.sender), "A user voted without being marked accordingly";
}

/*
Single vote per user
    A user cannot vote if he has voted before
    voted(e.msg.sender) => ㄱvote(e, f, s, t)
*/
rule singleVote(address f, address s, address t) {
    env e;
    bool has_voted_before = voted(e.msg.sender);
    vote@withrevert(e, f, s, t); //considering all cases
    assert has_voted_before => lastReverted, "Double voting is not allowed";
}

/*
Integrity of points:
    When voting, the points each candidate gets are updated as expected. 
    This rule also verifies that there are three distinct candidates.

    { points(f) = f_points ⋀ points(s) = s_points ⋀ points(t) = t_points }
    vote(e, f, s, t)
    { points(f) = f_points + 3 ⋀ points(s) = s_points + 2 ⋀ points(t) = t_points + 1 }
*/
rule integrityPoints(address f, address s, address t) {
    env e;
    uint256 f_points = points(f);
    uint256 s_points = points(s);
    uint256 t_points = points(t);
    vote(e, f, s, t);
    assert to_mathint(points(f)) == f_points + 3 &&
           to_mathint(points(s)) == s_points + 2 &&
           to_mathint(points(t)) == t_points + 1,   "unexpected change of points";
}

/*
Integrity of voted:
    Once a user casts their vote, they are marked as voted globally (for all future states).
    vote(e, f, s, t)  Globally voted(e.msg.sender)
*/
rule globallyVoted(address x, method f) {
    require voted(x);
    env eF;
    calldataarg arg;
    f(eF,arg); //taking into account all external function with all possible arguments 
    assert voted(x), "Once a user voted, he is marked as voted in all future states";
}

/*
 Integrity of winner
    The winner has the most points.
    winner() = forall ∀address c. points(c) ≤ points(w)


    Note: The Prover checks that the invariant is established after the constructor. In addition, Prover checks that the invariant holds after the execution of any contract method, assuming that it held before the method was executed.
    Note that c is an unconstrained variable therefore this invariant is checked against all possible values of c. 
*/
invariant integrityPointsOfWinner(address c)
            points(winner()) >= points(c);

/*
Vote is the only state-changing function. 
A vote can only affect the voter and the selected candidates, and has no effect on other addresses.
    ∀address c, c ≠ {f, s, t}.
    { c_points = points(c) ⋀ b = voted(c) }  vote(e, f, s, t)  { points(c) = c_points ⋀ ( voted(c) = b V c = e.msg.sender ) }
*/
rule noEffect(method m) {
    address c;
    env e;
    uint256 c_points = points(c);
    bool c_voted = voted(c);
    if (m.selector == sig:vote(address, address, address).selector) {
        address f;
        address s;
        address t;
        require( c != f  &&  c != s  &&  c != t );
        vote(e, f, s, t);
    }
    else {
        calldataarg args;
        m(e, args);
    }
    assert ( voted(c) == c_voted || c  == e.msg.sender ) &&
             points(c) == c_points, "unexpected change to others points or voted";
}


/*
Commutativity of votes.
    The order of votes is not important
    vote(e, f, s, t) ; vote(e’, f’, s’, t’)  ～  vote(e’, f’, s’, t’) ; vote(e, f, s, t)

    Note: This is a hyperproperty  as it compares the results of different executions. 
*/
rule voteCommutativity(address f1, address s1, address t1, address f2, address s2, address t2) {
    env e1;
    env e2;
    address c;
    address y;
    // A variable of type storage represents a snapshot of the EVM storage
    storage init = lastStorage;  
    

    // First 1 votes, then 2
    vote(e1, f1, s1, t1);
    vote(e2, f2, s2, t2);
    uint256 case1 = points(c);  

    // EVM storage is reset to the saved storage value
    vote(e2, f2, s2, t2) at init;
    vote(e1, f1, s1, t1);
    uint256 case2 = points(c);  
    // Assert commutativity with respect to points (but not winner...)
    assert case1 == case2, 
        "vote() is not commutative";
}


/*
Ability to vote
    If a user can vote, no other user can prevent him to do so by any operation.
    vote(e, f, s, t) ~ op; vote(e, f, s, t) (unless reached max_uint)
*/
rule allowVote(address f, address s, address t, method m) {
    env e;
    storage init = lastStorage;
    vote(e, f, s, t);  // Ensures the user can vote

    env eOther;
    require (e.msg.sender != eOther.msg.sender);
    calldataarg args;
    m(eOther, args) at init; //reset to the initial state

    require points(f) < max_uint256 - 3  &&  points(s)  < max_uint256 - 2  &&  points(t) < max_uint256 ; // No overflow

    vote@withrevert(e, f, s, t);

    assert !lastReverted, "a user can not be blocked from voting";
}


/*
Revert case of vote
    A user can vote, unless overflow in points or she has voted already 
*/
rule oneCanVote(address f, address s, address t) {
    env e;
    require e.msg.value == 0 ; //ignore revert on non payable
    bool overflowCheck = ( points(f) <= max_uint256 - 3  &&  points(s) <= max_uint256 - 2  &&  points(t) < max_uint256 );
    bool _voted = voted(e.msg.sender);
    vote@withrevert(e, f, s, t);
    bool reverted = lastReverted;

    assert (  overflowCheck && !_voted && f!=s && s!=t && f!=t ) 
            <=>  !reverted, "a user who hasn't yet voted should be able to do so unless there is an overflow for some candidate(s)";
}


/*
Participation criterion
    Abstaining from an election can not help a voter's preferred choice
    https://en.wikipedia.org/wiki/Participation_criterion

    { w1 = winner() }
        ( vote(e, f, s, t) )
    { winner() = f => (w1 = f) }
*/
rule participationCriterion(address f, address s, address t) {
    env e;
    address w1 = winner();
    require points(w1) >= points(f);
    require points(w1) >= points(s);
    require points(w1) >= points(t);
    vote(e, f, s, t);
    address w2 = winner();
    assert w1 == f => w2 == f, "winner changed unexpectedly";
}

/*
Resolvability criterion 
    Given a tie, there is a way for one added vote to make that winner unique.
    This property is proven by showing that given a tie , there is a vote that makes the winner unique.

    Note: This is implemented with the satisfy statement as the property require that exist a scenario and  not on every vote the tie must break.
    This property require uses quantifiers which works over ghost 
*/

// Ghosts are additional variables for use during verification,  and often used to communicate information between rules and hooks.
 

ghost mapping(address => uint256) points_mirror {
 init_state axiom forall address c. points_mirror[c] == 0;
} 

ghost mathint countVoters {
    init_state axiom countVoters == 0;
}
ghost mathint sumPoints {
    init_state axiom sumPoints == 0;
}

/* update ghost on changes to _points */
hook Sstore _points[KEY address a] uint256 new_points (uint256 old_points) {
  points_mirror[a] = new_points;
  sumPoints = sumPoints + new_points - old_points;
}

hook Sload uint256 curr_point _points[KEY address a] {
  require points_mirror[a] == curr_point;
}

hook Sstore _voted[KEY address a] bool val (bool old_val) {
  countVoters = countVoters +1;
}


rule resolvabilityCriterion(address f, address s, address t, address tie) {
    env e;
    address winnerBefore = winner(); 
    require (points(tie) == points(winner()));
    require forall address c. points_mirror[c] <= points_mirror[winnerBefore];
    vote(e, f, s, t);
    address winnerAfter = winner(); 
    satisfy forall address c. c != winnerAfter => points_mirror[c] < points_mirror[winnerAfter];
}

/*
  Each voter contribute a total of 6 points, so the sum of all points is six time the number of voters 
*/
invariant sumOfPoints() 
    sumPoints == countVoters * 6;
