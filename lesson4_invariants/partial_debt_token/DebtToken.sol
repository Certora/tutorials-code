// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @notice A partial debt token implementation
 * @dev The collateral of an account MUST cover its balance
 */
contract DebtToken {
  
  mapping(address => uint256) public balanceOf;
  mapping(address => uint256) private _collateralValue;
  uint256 public totalSupply;

  // The owner has additional privileges
  address private _owner;

  constructor(address owner) {
    _owner = owner;
  }

  modifier onlyOwner() {
      require(_owner == msg.sender);
      _;
  }

  function collateralOf(address account)
    public
    view
    returns (uint256)
  {
    return _collateralValue[account];
  }

  /// @notice Transfers the entire balance
  /// and collateral
  function transferDebt(address recipient)
    public
    returns (bool)
  {
    require(
      msg.sender != address(0),
      "Transfer from the zero address"
    );
    require(
      recipient != address(0),
      "Transfer to the zero address"
    );
    
    uint256 senderBalance = balanceOf[msg.sender];
    balanceOf[msg.sender] = 0;
    balanceOf[recipient] += senderBalance;

    // Transfer the collateral value as well
    uint256 senderCollateral = _collateralValue[msg.sender];
    _collateralValue[msg.sender] = 0;
    _collateralValue[recipient] += senderCollateral;
    return true;
  }

  function mint(address account, uint256 amount)
    onlyOwner()
    public
  {
    require(
      account != address(0),
      "Mint to the zero address"
    );
    require(
      balanceOf[account] + amount <= _collateralValue[account],
      "Minting uncovered by collateral"
    );

    totalSupply += amount;
    balanceOf[account] += amount;
  }

  function increaseCollateral(address account, uint256 amount)
    onlyOwner()
    public
  {
    require(
      account != address(0),
      "Add collateral to the zero address"
    );
    _collateralValue[account] += amount;
  }
}
