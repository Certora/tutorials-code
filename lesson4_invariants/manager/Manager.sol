// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import {IManager} from "./IManager.sol";

/// @title Correct implementation of `IManager`
contract Manager is IManager {

  // Maps a fundId to the fund's data
  mapping (uint256 => ManagedFund) public funds; 

  // A flag indicating if an address is a current manager of some fund
  mapping (address => bool) private _isActiveManager; 
  
  /// @inheritdoc IManager
  function isActiveManager(address manager) public view returns (bool) {
    return _isActiveManager[manager];
  }

  /// @inheritdoc IManager
  function createFund(uint256 fundId) public {
    require(msg.sender != address(0));
    require(funds[fundId].currentManager == address(0));
    require(!isActiveManager(msg.sender));
    funds[fundId].currentManager = msg.sender;
    _isActiveManager[msg.sender] = true;
  }

  /// @inheritdoc IManager
  function setPendingManager(uint256 fundId, address pending) public {
    require(funds[fundId].currentManager == msg.sender);
    funds[fundId].pendingManager = pending;
  }

  /// @inheritdoc IManager
  function claimManagement(uint256 fundId) public {
    require(msg.sender != address(0) && funds[fundId].currentManager != address(0));
    require(funds[fundId].pendingManager == msg.sender);
    require(!isActiveManager(msg.sender));
    _isActiveManager[funds[fundId].currentManager] = false;
    funds[fundId].currentManager = msg.sender;
    funds[fundId].pendingManager = address(0);
    _isActiveManager[msg.sender] = true;
  }

  /// @inheritdoc IManager
  function getCurrentManager(uint256 fundId) public view returns (address) {
    return funds[fundId].currentManager;
  }

  /// @inheritdoc IManager
  function getPendingManager(uint256 fundId) public view returns (address) {
    return funds[fundId].pendingManager;
  }
}
