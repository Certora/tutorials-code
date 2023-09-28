rule othersThanCheaterCanVote(env e, calldataarg args){
  vote(e, args);

  satisfy e.msg.sender != 42;
}
