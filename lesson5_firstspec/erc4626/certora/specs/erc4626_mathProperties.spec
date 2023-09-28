methods {
    function convertToShares(uint256) external returns (uint256) envfree;
    function convertToAssets(uint256) external returns (uint256) envfree;
}

/// @title The result of convertToShares/Assets of 0 is 0.
rule conversionOfZero {
    assert (convertToShares(0) == 0, "ConvertToShares does not convert 0 to 0");
    assert (convertToAssets(0) == 0, "ConvertToShares does not convert 0 to 0");
}

/// TODO More mathematical properties for convertToShares and convertToAssets 