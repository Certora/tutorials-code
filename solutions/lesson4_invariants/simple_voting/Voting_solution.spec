/**
 * # Simple voting contract complete spec
 *
 * To use gambit, run from the tutorials-code root folder the following command:
 * `certoraMutate --prover_conf solutions/lesson4_invariants/simple_voting/Voting_solution.conf --mutation_conf solutions/lesson4_invariants/simple_voting/mutate.json`
 */
methods
{
    function votesInFavor() external returns (uint256) envfree;
    function votesAgainst() external returns (uint256) envfree;
    function totalVotes() external returns (uint256) envfree;
    function hasVoted(address) external returns (bool) envfree;
}

// ---- Ghosts -----------------------------------------------------------------

/// @title Count the number of times `_hasVoted` been written to
ghost mathint numVoted {
    init_state axiom numVoted == 0;
}


/// @title For ensuring all changes to `_hasVoted` are legal
ghost bool illegalStore {
    init_state axiom !illegalStore;
}


/// @title Ghost indicating someone has voted
ghost bool someoneVoted;


// ---- Hooks ------------------------------------------------------------------

hook Sstore _hasVoted[KEY address voter] bool newVal (bool oldVal) {

    if (!oldVal && newVal) {
        numVoted = numVoted + 1;
    }

    someoneVoted = true;

    // Note once `illegalStore` is true, it remains true
    illegalStore = illegalStore || oldVal;
}


// ---- Rules ------------------------------------------------------------------

/// @title No illegal changes to `_hasVoted`
invariant onlyLegalVotedChanges()
    !illegalStore;


/// @title Total votes is the number of times `_hasVoted` been written to
invariant sumVotedEqualssTotalVotes()
     to_mathint(totalVotes()) == numVoted;


/// @title Sum of voter in favor and against equals total number of voted
invariant sumResultsEqualsTotalVotes()
    votesInFavor() + votesAgainst() == to_mathint(totalVotes());
    


/// @title Only the method `vote` can be used to vote
rule voteOnlyByCallingVote(method f) {
    require !someoneVoted;

    env e;
    calldataarg args;
    f(e, args);

    assert (
        someoneVoted => f.selector == sig:vote(bool).selector,
        "Voted only via vote"
    );
}


/// @title Votes in favor or against can only change by 1
rule votesChangeByOne(method f) {
    uint256 preFavor = votesInFavor();
    uint256 preAgainst = votesAgainst();

    env e;
    calldataarg args;
    f(e, args);

    mathint favorDiff = votesInFavor() - preFavor;
    mathint againstDiff = votesAgainst() - preAgainst;

    assert favorDiff >= 0 && favorDiff <= 1, "In favor may change by 0 or 1";
    assert againstDiff >= 0 && againstDiff <= 1, "Against may change by 0 or 1";
}


/// @title Voter determines if vote in favor or against
rule voterDecides(bool isInFavor) {
    uint256 preFavor = votesInFavor();
    uint256 preAgainst = votesAgainst();

    env e;
    vote(e, isInFavor);

    uint256 postFavor = votesInFavor();
    uint256 postAgainst = votesAgainst();

    assert (
        (isInFavor => (postFavor > preFavor)) &&
        (!isInFavor => (postAgainst > preAgainst))
    ), "Voter determines if vote is in favor or against";
}



/// @title Anyone can vote once
rule anyoneCanVote(address voter, bool isInFavor) {
    bool preHasVoted = hasVoted(voter);
    uint256 preTotal = totalVotes();

    env e;
    require e.msg.sender == voter;

    // Limit the overflow cases - this means we need only check `totalVotes`
    requireInvariant sumResultsEqualsTotalVotes();

    vote@withrevert(e, isInFavor);    

    assert (
        lastReverted <=> (
            preHasVoted  // Revert since voted before
            || e.msg.value > 0  // Sending ETH will cause revert
            || preTotal == max_uint256  // Revert due to overflow
        )
    ), "Can vote first time";
}
