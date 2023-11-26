/**
 * Solution to string revert issue by using hooks
 * ==============================================
 *
 * In this solution we require that there are only legal string encoding in storage.
 * This is done using a hook that is called when the string's slot in read.
 * Note that this ignores the case where the `dirty` function was used to create
 * illegal string encoding in storage.
 */
 methods {
     function arrayLength() external returns (uint256) envfree;
 }


/// @title Checks that `encoded` is a valid encoding of a string's storage slot
function isLegalEncoding(uint256 encoded) returns bool {
    mathint strLen = (encoded % 256) / 2;  // The string length for short strings only
    bool isOdd = encoded % 2 == 1;
    return (encoded > 64 && isOdd) || (strLen <= 31 && !isOdd);
}


/// @title Hook activated when the string in field `y` is read - require strings are legal
hook Sload bytes32 str structArray[INDEX uint256 index].(offset 32) STORAGE {
    uint256 encoded;
    require to_bytes32(encoded) == str;
    require isLegalEncoding(encoded);  // All strings are legally encoded
}


/** @title Verify `push` only reverts due to `msg.value`
 *  @notice This rule assumes that strings `y` loaded are legally encoded.
 */
rule verifyPushUsingHook(uint256 xx, string yy) {
    env e;
    push@withrevert(e, xx, yy);

    assert lastReverted <=> (e.msg.value > 0);
}


/** @title Verifies `getData` reverts only if value is sent or bad index
 *  @notice This rule assumes that strings all `y` loaded are legally encoded.
 */
rule verifyGetDataUsingHook(uint256 index) {
    env e;
    getData@withrevert(e, index);
    assert lastReverted <=> (
        (e.msg.value != 0) ||
        (index >= arrayLength())
    );
}
