pragma solidity ^0.8.0;

/**
 * @title Square root approximation
 * Approximates the square root, assuming numbers use FIXEDPOINT value,
 * So the number x = 123456 represents 123456 / FIXEDPOINT which is
 * 1.23456 if FIXEDPOINT is 10000.
 */
contract SquareRoot {
  uint256 public immutable FIXEDPOINT = 10000;
  uint256 public immutable ITERATIONS = 10;

  function sqrt(uint256 x) public pure returns (uint256) {
    uint256 r = 1 * FIXEDPOINT;  // initial guess

    for (uint256 i = 0; i < ITERATIONS; i++) {
      r = (r + (x / r) * FIXEDPOINT) / 2;
    }
    return r;
  }
}
