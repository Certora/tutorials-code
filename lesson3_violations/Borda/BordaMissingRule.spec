/*
 * Borda Missing Rule by Perito Flores
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



rule BordaMissingRule(env e,method m){

    require m.selector != sig:vote(address,address,address).selector;
    address winnerBefore = winner();
    calldataarg args; 
    m(e,args);
    address winnerAfter = winner();
    assert winnerAfter == winnerBefore ,  "The winner can be changed only after voting";
}
