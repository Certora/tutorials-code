/**
 * Example of the string revert issue
 * ==================================
 * The rules here assert that a revert in `push` and `getData` can only occur due to
 * value being sent, or bad index in the case of `getData`. Both rules fail because
 * of the string issue being another cause for revert.
 */
 methods {
     function arrayLength() external returns (uint256) envfree;
 }


/// @title Verifies the `push` function reverts only if value is sent
rule verifyPush(uint256 xx, string yy) {
    env e;
    push@withrevert(e, xx, yy);
    assert lastReverted <=> (e.msg.value != 0);
}


/// @title Verifies `getData` reverts only if value is sent or bad index
rule verifyGetData(uint256 index) {
    env e;
    getData@withrevert(e, index);
    assert lastReverted <=> (
        (e.msg.value != 0) ||
        (index >= arrayLength())
    );
}
