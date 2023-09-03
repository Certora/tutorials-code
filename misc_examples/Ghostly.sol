pragma solidity ^0.8.1;

contract Ghostly {

  mapping(uint256 => uint8) internal _map;

  uint8 internal _sumValues;

  function something() public view returns (uint8) {
    return _sumValues;
  }

  function update(uint256 index, uint8 value) public {
    require(_map[index] == 0);
    require(value > 0);
    _map[index] = value;
    _sumValues += value;
  }

  function passUpdate(uint256 index, uint8 value) public {
    require(_map[index] == 0);
    require(value > 0);

    _map[index + 1] = 1;  // This should still pass the rule

    _map[index] = value;
    _sumValues += value;
  }

  function failUpdate(uint256 index, uint8 value) public {
    require(_map[index] == 0);
    require(value > 0);
    _map[index] = value;
    _sumValues += value;
    
    _map[index + 1] = 1;  // This should fail the rule
  }
}
