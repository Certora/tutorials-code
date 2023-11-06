/* Specification for Pyramid Scheme contract
 *
 * TODO:
 * - Total balance unchanged except for ...
 */
methods {
    function contains(address) external returns (bool) envfree;
    function root() external returns (address) envfree;
}

ghost address _rootGhost;


/** @title Ghost `isChildOf[parent][child]`
 */
ghost mapping(address => mapping(address => bool)) isChildOf {
    init_state axiom forall address a. forall address b. !isChildOf[a][b];
}


ghost mapping(address => bool) isMember {
    init_state axiom forall address a. !isMember[a];
}


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

    // Root reaches all
    axiom forall address a. isMember[a] => reachable[_rootGhost][a];
}

hook Sstore currentContract.members[KEY address member].leftChild
    address newChild (address oldChild) STORAGE
{
    leftChild[member] = newChild;
    isChildOf[menber][newChild] = true;
}

hook Sstore currentContract.members[KEY address member].rightChild
    address newChild (address oldChild) STORAGE
{
    rightChild[member] = newChild;
    isChildOf[member][newChild] = true;
}

hook Sstore currentContract.members[KEY address member].exists
    bool newVal (bool oldVal) STORAGE
{
    isMember[member] = newVal;
}

invariant membershipGhost(address a)
    isMember[a] == contains(a);

invariant rootReachesAll(address a, address b)
    (
        isMember[a] == contains(a) && isMember[b] == contains[b]
