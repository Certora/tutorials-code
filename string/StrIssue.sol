pragma solidity ^0.8.0;


/**
 * @title StrIssue - a contract exemplifying the issue with string storage
 * @dev The expression `structArray[index].y` is a string. The encoding of this string
 * can be ruined by the function `dirty(x, index)`. All other functions would maintain
 * correct encoding of the string.
 */
contract StrIssue {

  struct S {
    uint256 x;
    string y;
  }

  S[] internal structArray;

  string internal harnessedTestString;

  /// @notice Push a new struct.
  function push(uint256 xVal, string memory yVal) public {
    structArray.push(S({x: xVal, y: yVal}));
  }

  /// @notice Read a struct's values.
  function getData(uint256 index) public view returns (uint256, string memory) {
    return (structArray[index].x, structArray[index].y);
  }

  function arrayLength() public view returns (uint256) {
    return structArray.length;
  }

  /// @notice This function will "clean" the storage for the next push into `structArray`.
  function clear() public {
    S memory empty;
    structArray.push(empty);
    structArray.pop();
  }

  /// @notice We'll use this function to ensure the string encoding is correct.
  function getString(uint256 index) public view returns (string memory) {
    return structArray[index].y;
  }

  /// @notice This function exists solely to ruin the encoding of `structArray[index].y`.
  function dirty(uint256 z, uint256 index) public {
    bool isOdd = z % 2 == 1;
    uint256 evenLen = (z % 256) / 2;
    
    bool isIllegal = (z <= 64 && isOdd) || (evenLen > 31 && !isOdd);
    if (isIllegal) {
      string storage dirtyString = structArray[index].y;
      assembly {
        sstore(dirtyString.slot, z)
      }
    }
  }
}
