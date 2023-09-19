/**
 * # Simple voting invariant example
 *
 * A simple invariant example. Additionally there are two rules, one is a correct
 * translation of the invariant to a rule, and the other is a wrong translation.
 */

methods
{
    function votesInFavor() external returns (uint256) envfree;
    function votesAgainst() external returns (uint256) envfree;
    function totalVotes() external returns (uint256) envfree;
}


/// @title Sum of voter in favor and against equals total number of voted
invariant sumResultsEqualsTotalVotes()
    votesInFavor() + votesAgainst() == to_mathint(totalVotes());


/// @title This rule is a correct translation of the invariant
rule sumResultsEqualsTotalVotesAsRule(method f) {
    // Precondition
    require votesInFavor() + votesAgainst() == to_mathint(totalVotes());

    env e;
    calldataarg args;
    f(e, args);
    
    assert (
        votesInFavor() + votesAgainst() == to_mathint(totalVotes()),
        "Sum of votes should equal total votes"
    );
}


/// @title This rule is a wrong translation of the invariant
rule sumResultsEqualsTotalVotesWrong() {
    assert (
        votesInFavor() + votesAgainst() == to_mathint(totalVotes()),
        "Sum of votes should equal total votes"
    );
}
