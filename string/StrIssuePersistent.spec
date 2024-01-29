/**
 * Using a persistent ghost to identify string revert
 * ==================================================
 */


/// @title Checks that `encoded` is a valid encoding of the first 32 bytes of a string
function isLegalEncoding(uint256 encoded) returns bool {
    mathint strLen = (encoded % 256) / 2;  // The string length for short strings only
    bool isOdd = encoded % 2 == 1;
    return (encoded > 64 && isOdd) || (strLen <= 31 && !isOdd);
}


/// @title Persistent ghost updated by legality of string encoding is legal
persistent ghost bool legalStr;


/// @title Hook activated when the string in field `y` is read
hook Sload bytes32 str structArray[INDEX uint256 index].(offset 32) STORAGE {
    uint256 encoded;
    require to_bytes32(encoded) == str;
    legalStr = isLegalEncoding(encoded) && legalStr;
}


/// @title Checks when the `push` function reverts
rule VerifyPush(uint256 xx, string yy) {
    // When a revert occurs, `legalStr` will not revert because it is `persistent`.
    legalStr = true;

    env e;

    push@withrevert(e, xx, yy);

    // Note that transferring funds to non-payable function can also cause revert.
    assert lastReverted <=> (!legalStr || e.msg.value != 0);
}


/// @title An example of `VerifyPush` where string
rule VerifyPushExample(uint256 xx, string yy) {
    legalStr = true;

    env e;
    // This require prevents a revert unrelated to the string encoding
    require e.msg.value == 0;

    push@withrevert(e, xx, yy);

    satisfy !legalStr;  // The example must have reverted
}
