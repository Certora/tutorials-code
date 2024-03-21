/**
 * # Simple voting ghost invariant example
 */

methods
{
    function votesInFavor() external returns (uint256) envfree;
    function votesAgainst() external returns (uint256) envfree;
    function totalVotes() external returns (uint256) envfree;
}

ghost mathint numVoted {
    // No votes at start
    init_state axiom numVoted == 0;
}

hook Sstore _hasVoted[KEY address voter]
    bool newVal (bool oldVal) {
    numVoted = numVoted + 1;
}

/// @title Total voted intergrity
invariant sumResultsEqualsTotalVotes()
     to_mathint(totalVotes()) == numVoted;
