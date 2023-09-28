rule othersThanCheaterCanVote(env e, calldataarg args){
  vote(e, args);

  satisfy e.msg.sender != 42;
}

rule twoCanVote(env e1, env e2, calldataarg args1, calldataarg args2){
  vote(e1, args1);
  vote(e2, args2);

  satisfy true;
}
