/**
 * Bad solution to string revert issue
 * ===================================
 *
 * The rule `badVerifyPush` uses a ghost and a hook to ensure that a revert occurs
 * when the storage of the string is badly encoded. But this can mask other
 * revert causes. For example, in `badVerifyPushExample` we force a revert
 * by passing non-zero `msg.value` to `push`.
 */


/// @title Checks that `encoded` is a valid encoding of the first 32 bytes of a string
function isLegalEncoding(uint256 encoded) returns bool {
    mathint strLen = (encoded % 256) / 2;  // The string length for short strings only
    bool isOdd = encoded % 2 == 1;
    return (encoded > 64 && isOdd) || (strLen <= 31 && !isOdd);
}


/// @title Ghost updated by legality of string encoding is legal
ghost bool legalStr;


/// @title Hook activated when the string in field `y` is read
hook Sload bytes32 str structArray[INDEX uint256 index].(offset 32) STORAGE {
    uint256 encoded;
    require to_bytes32(encoded) == str;
    legalStr = isLegalEncoding(encoded);
}


/// @title Checks when the `push` function reverts - but masks other revert causes
rule badVerifyPush(uint256 xx, string yy) {
    // When a revert occurs, `legalStr2` will also revert back to false.
    // This might mask other causes for revert.
    legalStr = false;

    env e;

    push@withrevert(e, xx, yy);

    assert lastReverted <=> !legalStr;
}


/// @title Example that `badVerifyPush` can have other revert causes
rule badVerifyPushExample(uint256 xx, string yy) {
    legalStr = false;

    env e;
    // This require causes a revert unrelated to the string encoding.
    require e.msg.value != 0;

    push@withrevert(e, xx, yy);

    // This example cannot occur, since `msg.value` being nonzero will cause a revert.
    satisfy !lastReverted;
}
