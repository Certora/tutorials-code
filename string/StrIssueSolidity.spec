/**
 * Solution to string revert issue by harnessing Solidity functions
 * ================================================================
 *
 * Here we use two "harnessed" functions `clear()` and `getString(index)`. Calling
 * `clear()` from CVL (without `@withrevert`) will ensure that the next call to `push`
 * will have well encoded storage. Similarly, calling `getString(index)` before
 * `getData(index)` will ensure the string we shall read is well-encoded.
 *
 * The downside to this solution is that it assumes that the storage can not
 * contain a badly encoded string. But for the `StrIssue` contract this is wrong,
 * since we can use the function `dirty` to create a badly encoded string.
 * We show this in `badStringExample`.
 *
 * However, the benefit of this solution is that it is not affected by the Solidity
 * version. Because it does not depend on the details of the encoding.
 */
methods {
    function clear() external envfree;
    function getString(uint256) external returns (string memory) envfree;
}


/// @title Verify that only bad storage or `msg.value` can cause `push` to revert
rule verifyPushWithHarnessing(uint256 xx, string yy) {
    // Using the harnessed `clear()` to ensure the storage for the next
    // push is OK.
    clear();

    env e;
    push@withrevert(e, xx, yy);

    assert lastReverted <=> (e.msg.value > 0);
}


/// @title Verify that only bad storage or `msg.value` can cause `getData` to revert
rule verifyGetDataWithHarnessing(uint256 index) {
    // Using the harnessed `getString()` to ensure the string `structArray[index].y`
    // is well encoded.
    getString(index);

    env e;
    getData@withrevert(e, index);

    assert lastReverted <=> (e.msg.value > 0);
}


/// @title Example of creating a badly encoded string
rule badStringExample(uint256 index) {
    // Using the harnessed `getString()` to ensure the string `structArray[index].y`
    // is well encoded.
    getString(index);

    env e;
    require e.msg.value == 0;  // Prevent revert due to non-zero value

    uint256 z = 1;  // A bad value for the first 32 bytes of the string
    dirty(e, z, index);  // Force bad string encoding

    getData@withrevert(e, index);

    satisfy lastReverted;
}
