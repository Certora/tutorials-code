/* Specification for Pyramid Scheme contract
 *
 * TODO:
 * - Total balance unchanged except for ...
 *
 * NOTE
 * The order of actions in the `join` method affects the possible hooks.
 * If we make child member (`members[child].exists = true;`) only after
 * changing
 */
methods {
    function root() external returns (address) envfree;
    function parentFrac() external returns (uint256) envfree;
    function joiningFee() external returns (uint256) envfree;
    function contains(address) external returns (bool) envfree;
}


// ---- Ghosts -----------------------------------------------------------------

/// @title Is a member
ghost mapping(address => bool) isMember {
    init_state axiom forall address a. !isMember[a];
}


/// @title Left child
ghost mapping(address => address) leftChild {
    init_state axiom forall address member. leftChild[member] == 0;
}


/// @title Ghost `isChildOf[parent][child]`
ghost mapping(address => mapping(address => bool)) isChildOf {
    init_state axiom forall address a. forall address b. !isChildOf[a][b];
    axiom forall address a. forall address b. isChildOf[a][b] || !isChildOf[a][b];
}


/// @title Ghost `isParentOf[parent][child]`
ghost mapping(address => mapping(address => bool)) isParentOf {
    init_state axiom forall address a. forall address b. !isParentOf[a][b];
}


/// @title Right child
ghost mapping(address => address) rightChild {
    init_state axiom forall address member. rightChild[member] == 0;
}


/// @title The root
ghost address rootMirror;


/// @title Reachable from root
ghost mapping(address => bool) rootReachable {
    init_state axiom forall address to. (to == rootMirror) || !rootReachable[to];

    // Root
    axiom rootReachable[rootMirror];

    // Immediate children
    axiom forall address parent. forall address child. (
        (isChildOf[parent][child] && rootReachable[parent]) => rootReachable[child]
    );
}



/// @title Root is ancestor
ghost mapping(address => bool) isRootAncestor {
    init_state axiom forall address a. (a == rootMirror) || !isRootAncestor[a];

    // Root
    axiom isRootAncestor[rootMirror];

    // Immediate children
    axiom forall address parent. forall address child. (
        (isParentOf[parent][child] && isRootAncestor[parent]) => isRootAncestor[child]
    );
}

/// @title Illegal child update
ghost bool illegalChildUpdate {
    init_state axiom !illegalChildUpdate;
}


/// @title Illegal parent update
ghost bool illegalParentUpdate {
    init_state axiom !illegalParentUpdate;
}


/// @title Illegal root change
ghost bool illegalRootChange {
    init_state axiom !illegalRootChange;
}


// ---- Hooks ------------------------------------------------------------------

hook Sstore currentContract.members[KEY address member].leftChild
    address newChild (address oldChild) STORAGE
{
    illegalChildUpdate = illegalChildUpdate || (oldChild != 0) || (newChild == 0);
    isChildOf[member][newChild] = true;
    rootReachable[newChild] = rootReachable[member];
}


hook Sstore currentContract.members[KEY address member].rightChild
    address newChild (address oldChild) STORAGE
{
    illegalChildUpdate = illegalChildUpdate || (oldChild != 0) || (newChild == 0);
    isChildOf[member][newChild] = true;
    rootReachable[newChild] = rootReachable[member];
}


hook Sstore currentContract.members[KEY address member].parent
    address newParent (address oldParent) STORAGE
{
    illegalParentUpdate = illegalParentUpdate || (oldParent != 0) || (newParent == 0);
    isParentOf[newParent][member] = true;
    isRootAncestor[member] = isRootAncestor[newParent];
}


hook Sstore currentContract.members[KEY address member].exists
    bool newVal (bool oldVal) STORAGE
{
    isMember[member] = newVal;
}


hook Sstore _root address newRoot (address oldRoot) STORAGE {
    rootMirror = newRoot;
    illegalRootChange = illegalRootChange || (newRoot == 0) || (oldRoot != 0);
}


// ---- Functions --------------------------------------------------------------
function safeIsChildOf(address parent, address child, env e) returns bool {
    // Bypass the requirement that parent be a member in `getChild`
    if (!contains(parent)) {
        return false;
    }
    return (getChild(e, parent, true) == child) || (getChild(e, parent, false) == child);
}


function safeIsParentOf(address parent, address child, env e) returns bool {
    // Bypass the requirement that child be a member in `getParent`
    if (!contains(child)) {
        return false;
    }
    return getParent(e, child) == parent;
}


// ---- Invariants -------------------------------------------------------------

invariant membershipGhost(address a)
    isMember[a] == contains(a);


/// @title Root is a member
invariant rootIsAMember()
    contains(root());


/// @title Root has no parent
invariant rootHasNoParent(env e)
    getParent(e, root()) == 0;


/// @title Root is no one's child
invariant rootIsNotChild(env e, address a)
    !safeIsChildOf(a, root(), e);


/// @title Zero is not a member
invariant zeroIsNotAMember()
    !contains(0);


invariant childlessIsZero(address parent, bool isRight, env e)
    !contains(getChild(e, parent, isRight)) => !hasChild(e, parent, isRight);

invariant childIsMember(address parent, bool isRight, env e)
    contains(parent) => (
        !hasChild(e, parent, isRight) || contains(getChild(e, parent, isRight))
    ) {
        preserved {
            requireInvariant zeroIsNotAMember();
        }
    }

invariant parentIsMember(address child, env e)
    (contains(child) && child != root()) => contains(getParent(e, child))
    {
        preserved {
            requireInvariant zeroIsNotAMember();
        }
    }

invariant parentlessIsZero(address child, env e)
    !contains(getParent(e, child)) => (getParent(e, child) == 0);


invariant parentlessIsRoot(address child, env e)
    !contains(getParent(e, child)) <=> (child == root())
    {
        preserved {
            requireInvariant parentlessIsZero(child, e);
        }
    }

/// @title Child and parent point at each other
invariant chiledOfParent(address parent, address child, env e)
    (contains(parent) && contains(child)) => (
        safeIsChildOf(parent, child, e) <=> safeIsParentOf(parent, child, e)
    ) {
        preserved {
            requireInvariant zeroIsNotAMember();
            requireInvariant childlessIsZero(parent, false, e);
            requireInvariant childlessIsZero(parent, true, e);
        }
    }


/// @title Child and parent are differrent
invariant childIsNotParent(address child, env e)
    contains(child) => (getParent(e, child) != child)
    {
        preserved {
            requireInvariant zeroIsNotAMember();
        }
    }


/// @title Verifies the `isChildOf` ghost
invariant isChildOfIntegrity(address parent, address child, env e)
    (
        child != 0 && safeIsChildOf(parent, child, e)
    ) <=> isChildOf[parent][child]
    {
        preserved {
            requireInvariant childIsMember(parent, true, e);
            requireInvariant childIsMember(parent, false, e);
            requireInvariant onlyLegalChildUpdates();
        }
    }



/// @title Every non-root member has a parent
invariant allChildrenHaveParents(env e, address child)
    (contains(child) && (child != root())) => contains(getParent(e, child));


/// @title Integrity of root mirror
invariant rootMirrorIsRoot()
    root() == rootMirror;


/// @title All memebrs are reachable from the root
invariant rootReachesAll(address a)
    contains(a) <=> rootReachable[a]
    {
        preserved {
            requireInvariant rootMirrorIsRoot();
        }
        preserved join(address child, bool isRight) with (env ejoin) {
            requireInvariant rootMirrorIsRoot();
            requireInvariant rootReachesAll(ejoin.msg.sender);
            requireInvariant isChildOfIntegrity(ejoin.msg.sender, child, ejoin);
        }
    }


/// @title Varifies `isParentOf` ghost
invariant isParentOfIntegrity(address parent, address child, env e)
    (parent != 0) => (isParentOf[parent][child] <=> safeIsParentOf(parent, child, e))
    {
        preserved {
            requireInvariant parentIsMember(child, e);
            requireInvariant onlyLegalParentUpdates();
        }
    }


/// @title Root is ancestor of all
invariant rootIsAncestor(address a)
    contains(a) <=> isRootAncestor[a]
    {
        preserved {
            requireInvariant rootMirrorIsRoot();
        }
        preserved join(address child, bool isRight) with (env ejoin) {
            requireInvariant rootMirrorIsRoot();
            requireInvariant rootIsAncestor(ejoin.msg.sender);
            requireInvariant isParentOfIntegrity(ejoin.msg.sender, child, ejoin);
        }
    }


invariant nonMembersAreParentless(address parent, address child, env e)
    ((parent != 0) && !contains(child)) => !isParentOf[parent][child]
    {
        preserved {
            requireInvariant isParentOfIntegrity(parent, child, e);
        }
    }


invariant hasParentIsMember(address parent, address child, env e)
    isParentOf[parent][child] => contains(child)
    {
        preserved {
            requireInvariant isParentOfIntegrity(parent, child, e);
        }
    }


invariant parentFracIsPositive()
    parentFrac() > 0;


invariant onlyLegalChildUpdates()
    !illegalChildUpdate;


invariant onlyLegalParentUpdates()
    !illegalParentUpdate
    {
        preserved join(address child, bool isRight) with (env ejoin) {
            requireInvariant zeroIsNotAMember();
            requireInvariant nonMembersAreParentless(ejoin.msg.sender, child, ejoin);
            requireInvariant hasParentIsMember(ejoin.msg.sender, child, ejoin);
        }
    }


invariant onlyLegalRootChanges()
    !illegalRootChange;


// ---- Rules ------------------------------------------------------------------
//rule withdrawIntegrity(address member, uint256 amount) {
//
//    env e;
//    require e.msg.sender == member;
//    requireInvariant parentFracIsPositive();
//    requireInvariant allChildrenHaveParents(e, member);
//    requireInvariant childIsNotParent(member, e);
//
//    address parent = getParent(e, member);
//    uint256 parentPreAmount = balanceOf(e, parent);
//
//    uint256 memberPreAmount = balanceOf(e, member);
//    uint256 memberPreBalance = nativeBalances[member];
//
//    withdraw(e, amount);
//
//    mathint amountDiff = memberPreAmount - balanceOf(e, member);
//    assert amountDiff >= 0;
//
//    mathint balanceDiff = nativeBalances[member] - memberPreBalance;
//    assert (member != currentContract) => balanceDiff == to_mathint(amount);
//
//    mathint parentDiff = balanceOf(e, parent) - parentPreAmount;
//    assert (member != root()) => (parentDiff == amount / parentFrac());
//}
