// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;


/// @title A simple "funds managers" example for exercising the use of invariants
/// The `IManager` keeps track of the funds managers, and ensures that each fund has
/// a unique manager.
/// To change managers:
/// - the current manager must set their successor as the pending manager
/// - the pending manager must claim management
interface IManager {

  /// Encapsulates the data of a managed fund
  struct ManagedFund {
    address currentManager;  // Current fund manager
    address pendingManager;  // Pending manager
    uint256 amount;  // Amount managed
  }

  /// @return whether `manager` currently manages a fund
  function isActiveManager(address manager) external view returns (bool);

  /// @notice Create a new managed fund setting message sender as its manager
  /// @dev The message sender may not manage another fund
  /// @param fundId the id number of the new fund
  function createFund(uint256 fundId) external;

  /// @notice Set the pending manager for a fund
  /// @dev Only the fund's manager may set the pending manager
  function setPendingManager(uint256 fundId, address pending) external;

  /// @notice Claim management of the fund
  /// @dev Only the pending manager may claim management
  /// @dev The pending manager will become the new current manager of the fund
  function claimManagement(uint256 fundId) external;

  /// @return The current manager of the fund
  function getCurrentManager(uint256 fundId) external view returns (address);

  /// @return The fund's pending manager
  function getPendingManager(uint256 fundId) external view returns (address);
}
