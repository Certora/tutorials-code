methods {
    function convertToShares(uint256) external returns (uint256) envfree;
    function convertToAssets(uint256) external returns (uint256) envfree;

    function totalSupply() external returns (uint256) envfree;
    function totalAssets() external returns (uint256) envfree;

    
}

/// @title The result of convertToShares/Assets of 0 is 0.
rule conversionOfZero {
    assert (convertToShares(0) == 0, "ConvertToShares does not convert 0 to 0");
    assert (convertToAssets(0) == 0, "ConvertToShares does not convert 0 to 0");
}


/// @title convertToAssets is weakly additive.
rule convertToAssetsWeakAdditivity {

    uint256 num1;
    uint256 num2;
   
    assert (convertToAssets(num1) + convertToAssets(num2)) <= to_mathint(convertToAssets(require_uint256(num1 + num2))),
     "convertToAssets is not weakly additive";
}

/// @title convertToShares is weakly additive.
rule convertToSharesWeakAdditivity {

    uint256 num1;
    uint256 num2;
    
    assert (convertToShares(num1) + convertToShares(num2)) <= to_mathint(convertToShares(require_uint256(num1 + num2))),
     "convertToShares is not weakly additive";
}

/// @title convertToAssets is weakly monotonic
rule convertToAssetsWeakMonotonicity {
    uint256 num1;
    uint256 num2;
    
    assert ((num1 < num2) => (convertToAssets(num1) <= convertToAssets(num2)), "convertToAssets is not monotonic");
}

/// @title convertToAssets is weakly monotonic
rule convertToSharesWeakMonotonicity {
    uint256 num1;
    uint256 num2;
    
    assert ((num1 < num2) => (convertToShares(num1) <= convertToShares(num2)), "convertToShares is not monotonic");
}

/// @title convertToShares and convertToAssets are inverses of each other. rounding goes down, one can only
rule convertToCorrectness(){
    uint256 num;
    
    assert (num >= convertToAssets(convertToShares(num)), "convertToShares and convertToAssets are not decreasing as expected");
    assert (num >= convertToShares(convertToAssets(num)), "convertToShares and convertToAssets are not decreasing as expected");
}