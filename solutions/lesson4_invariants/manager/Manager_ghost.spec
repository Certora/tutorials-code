/**
 * # Spec for funds manager `IManager.sol`
 *
 * The purpose is to demonstrate the use of ghosts with invariants.
 */
methods {
    function getCurrentManager(uint256) external returns (address) envfree;
    function getPendingManager(uint256) external returns (address) envfree;
    function isActiveManager(address) external returns (bool) envfree;
}


/// @title The inverse mapping from managers to fund ids
ghost mapping(address => uint256) managersFunds;


hook Sstore funds[KEY uint256 fundId].(offset 0) address newManager {
    managersFunds[newManager] = fundId;
}


/// @title Adderess zero is never an active manager
invariant zeroIsNeverActive()
    !isActiveManager(0);


/// @title Every active manager has a fund they manage
invariant activeManagesAFund(address manager)
    isActiveManager(manager) => getCurrentManager(managersFunds[manager]) == manager
    {
        preserved {
            requireInvariant zeroIsNeverActive();
        }
    }
