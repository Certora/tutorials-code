methods {
    function clear() external envfree;
    function get(uint256) external returns (string) envfree;
}


/// @title Checks that `encoded` is a valid encoding of the first 32 bytes of a string
function isLegalEncoding(uint256 encoded) returns bool {
    mathint strLen = (encoded % 256) / 2;  // The string length for short strings only
    bool isOdd = encoded % 2 == 1;
    return (encoded > 64 && isOdd) || (strLen <= 31 && !isOdd);
}


/// @title Ghost updated by legality of string encoding is legal
ghost bool legalStr {
    init_state axiom legalStr;
}

/// @title Another ghost expressing the encoding is legal
ghost bool legalStr2;


/// @title Hook activated when the string in field `y` is read
hook Sload bytes32 str structArray[INDEX uint256 index].(offset 32) STORAGE {
    uint256 encoded;
    require to_bytes32(encoded) == str;
    bool isLegal = isLegalEncoding(encoded);
    legalStr = legalStr && isLegal;
    legalStr2 = isLegal;
}

/// @title Hook activated when the string in field `y` is written
hook Sstore structArray[INDEX uint256 index].(offset 32) bytes32 str STORAGE {
    uint256 encoded;
    require to_bytes32(encoded) == str;
    legalStr = legalStr && isLegalEncoding(encoded);
}


/** @title All reads and writes to string `y` are legal
 *  This invariant is violated by the function `dirty`.
 */
invariant alwaysLegalStorage()
    legalStr;


rule checkPushWithInvariant(uint256 xx, string yy) {
    requireInvariant alwaysLegalStorage();
    env e;

    push@withrevert(e, xx, yy);

    assert !lastReverted;
}


/// @title Checks when the `push` function reverts - but masks other revert causes
rule checkPushWithoutInvariant(uint256 xx, string yy) {
    // When a revert occurs, `legalStr2` will also revert back to false.
    // This might mask other causes for revert.
    legalStr2 = false;

    env e;
    // This require causes a revert unrelated to the string encoding.
    require e.msg.value != 0;

    push@withrevert(e, xx, yy);

    assert !lastReverted;// <=> !legalStr2;
}
