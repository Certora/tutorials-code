/**
 * Solution to string revert issue by using hooks
 * ==============================================
 *
 */
methods {
    function clear() external envfree;
    function getString(uint256) external returns (string memory) envfree;
}


/// @title Checks that `encoded` is a valid encoding of the first 32 bytes of a string
function isLegalEncoding(uint256 encoded) returns bool {
    mathint strLen = (encoded % 256) / 2;  // The string length for short strings only
    bool isOdd = encoded % 2 == 1;
    return (encoded > 64 && isOdd) || (strLen <= 31 && !isOdd);
}


/// @title Ghost updated by legality of string encoding is legal
ghost bool isLegalStr {
    init_state axiom isLegalStr;
}

/** @title Ghost determining whether to require any string read is legally encoded
 *  @notice We would not need this ghost if we separated this spec into two specs
 */
ghost bool isRequiredLegal {
    init_state axiom !isRequiredLegal;
}


/// @title Hook activated when the string in field `y` is read
hook Sload bytes32 str structArray[INDEX uint256 index].(offset 32) STORAGE {
    uint256 encoded;
    require to_bytes32(encoded) == str;

    if (isRequiredLegal) {
        require isLegalEncoding(encoded);  // All strings are legally encoded
    } else {
        isLegalStr = isLegalStr && isLegalEncoding(encoded);  // Check the value
    }
}

/// @title Hook activated when the string in field `y` is written
hook Sstore structArray[INDEX uint256 index].(offset 32) bytes32 str STORAGE {
    uint256 encoded;
    require to_bytes32(encoded) == str;
    isLegalStr = isLegalStr && isLegalEncoding(encoded);
}


/** @title All reads and writes to string `y` are legal
 *  @notice This invariant is violated by the function `dirty`.
 */
invariant alwaysLegalStorage()
    isLegalStr;


/** @title Verify `push` only reverts due to `msg.value`
 *  @notice This rule assumes that strings `y` loaded are legally encoded.
 */
rule verifyPushRelyingOnInvariant(uint256 xx, string yy) {
    // Set the flag to require strings `y` loaded are legally encoded.
    isRequiredLegal = true;

    env e;
    push@withrevert(e, xx, yy);

    assert lastReverted <=> (e.msg.value > 0);
}
