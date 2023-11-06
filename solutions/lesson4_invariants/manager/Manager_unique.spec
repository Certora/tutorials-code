/**
 * # Spec for funds manager `IManager.sol` showing manager is unique
 *
 * The purpose is to demonstrate the use of preserved block.
 */
methods {
    function getCurrentManager(uint256) external returns (address) envfree;
    function getPendingManager(uint256) external returns (address) envfree;
    function isActiveManager(address) external returns (bool) envfree;
}


/// A utility function
/// @return whether the fund exists
function isManaged(uint256 fundId) returns bool {
    return getCurrentManager(fundId) != 0;
}


/// @title A fund's manager is active
invariant managerIsActive(uint256 fundId)
    isManaged(fundId) <=> isActiveManager(getCurrentManager(fundId))
    {
        preserved claimManagement(uint256 fundId2) with (env e) {
            requireInvariant uniqueManager(fundId, fundId2);
        }
    }


/// @title A fund has a unique manager
invariant uniqueManager(uint256 fundId1, uint256 fundId2)
	((fundId1 != fundId2) && isManaged(fundId1)) => (
        getCurrentManager(fundId1) != getCurrentManager(fundId2)
    ) {
        preserved {
            requireInvariant managerIsActive(fundId1);
            requireInvariant managerIsActive(fundId2);
        }
    }
