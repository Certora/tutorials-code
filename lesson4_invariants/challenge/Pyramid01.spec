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
}


/// @title Right child
ghost mapping(address => address) rightChild {
    init_state axiom forall address member. rightChild[member] == 0;
}


/// @title Is reachable
ghost mapping(address => mapping(address => bool)) reachable {
    init_state axiom forall address from. forall address to. !reachable[from][to];

    // Non-members are never reachable
    axiom forall address a. forall address b. (
        !isMember[a] => (!reachable[a][b] && !reachable[b][a])
    );

    // Reflexivity
    axiom forall address a. (a != 0 && isMember[a]) => reachable[a][a];

    // Transitivity
    axiom forall address x. forall address y. forall address z. (
        (reachable[x][y] && reachable[y][z]) => reachable[x][z]
    );

    // Anti-commutativity
    axiom forall address a. forall address b. !reachable[a][b] || !reachable[b][a];

    // In a tree there is a unique path (also reflexivity)
    axiom forall address x. forall address y. forall address z. (
        (reachable[x][z] && reachable[y][z]) => (reachable[x][y] || reachable[y][x])
    );

    // Immediate children
    axiom forall address parent. forall address child. (
        isChildOf[parent][child] => reachable[parent][child]
    );
}


/// @title Reached from
ghost mapping(address => mapping(address => bool)) isReached {
    init_state axiom forall address from. forall address to. !isReached[from][to];

    // Non-members are never reachable
    axiom forall address a. forall address b. (
        !isMember[a] => (!isReached[a][b] && !isReached[b][a])
    );

    // Reflexivity
    axiom forall address a. (a != 0 && isMember[a]) => isReached[a][a];

    // Transitivity
    axiom forall address x. forall address y. forall address z. (
        (isReached[x][y] && isReached[y][z]) => isReached[x][z]
    );

    // Anti-commutativity
    axiom forall address a. forall address b. !isReached[a][b] || !isReached[b][a];

    // In a tree there is a unique path (also reflexivity)
    axiom forall address x. forall address y. forall address z. (
        (isReached[z][x] && isReached[z][y]) => (isReached[x][y] || isReached[y][x])
    );

    // Immediate children
    axiom forall address parent. forall address child. (
        isChildOf[parent][child] => isReached[child][parent]
    );
}


// ---- Hooks ------------------------------------------------------------------

hook Sstore currentContract.members[KEY address member].leftChild
    address newChild (address oldChild) STORAGE
{
    // leftChild[member] = newChild;
    isChildOf[member][newChild] = true;
    //isReached[newChild] = isReached[member];
    havoc reachable;
    // havoc reachable assuming reachable@new[member][newChild];
    // reachable[member] = reachable[newChild];

}

hook Sstore currentContract.members[KEY address member].rightChild
    address newChild (address oldChild) STORAGE
{
    // rightChild[member] = newChild;
    isChildOf[member][newChild] = true;
    //isReached[newChild] = isReached[member];
    havoc reachable;
    //havoc reachable assuming reachable@new[member][newChild];
    //reachable[member][newChild] = true;
}

hook Sstore currentContract.members[KEY address member].exists
    bool newVal (bool oldVal) STORAGE
{
    isMember[member] = newVal;
    // havoc reachable assuming reachable@new[member][member];
    // reachable[member][member] = true;
}


// ---- Invariants -------------------------------------------------------------

invariant membershipGhost(address a)
    isMember[a] == contains(a);


/// @title Root is a member
invariant rootIsAMember()
    contains(root());


/// @title Verifies the `isChildOf` ghost
invariant isChildOfIntegrity(address parent, address child, env e)
    (
        child != 0 && (
            getChild(e, parent, true) == child ||
            getChild(e, parent, false) == child
        )
    ) <=> isChildOf[parent][child];


/// @title Verifies that the root reaches all members
/*
invariant rootReachesAll(address a)
    contains(a) => isReached[a][root()]
    {
        preserved {
            requireInvariant membershipGhost(a);
            requireInvariant membershipGhost(root());
        }
        preserved join(address child, bool isRight) with (env e) {
            requireInvariant membershipGhost(e.msg.sender);
            requireInvariant rootReachesAll(e.msg.sender);
        }
    }
*/
invariant rootReachesAll(address a)
    contains(a) => reachable[root()][a]
    {
        preserved {
            requireInvariant membershipGhost(a);
            requireInvariant membershipGhost(root());
        }
        preserved join(address child, bool isRight) with (env e) {
            requireInvariant membershipGhost(e.msg.sender);
            requireInvariant rootReachesAll(e.msg.sender);
        }
    }
