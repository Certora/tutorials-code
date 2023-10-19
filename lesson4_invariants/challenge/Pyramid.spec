methods {
    function contains(bytes32) external returns (bool) envfree;
    function root() external returns (bytes32) envfree;
    function insert(bytes32, uint256) external envfree;
}

/* Ideas for rules
 * ---------------
 * Rightmost is maximal
 * Leftmost is minimal
 */

definition Zero() returns bytes32 = to_bytes32(0);


ghost mapping(bytes32 => bytes32) leftChild;
ghost mapping(bytes32 => bytes32) rightChild;

ghost mapping(bytes32 => mapping(bytes32 => bool)) isChildOf {
    init_state axiom forall bytes32 a. forall bytes32 b. !isChildOf[a][b];
}

ghost mapping(bytes32 => mapping(bytes32 => bool)) reachable {
    init_state axiom forall bytes32 from. forall bytes32 to. !reachable[from][to];
    //axiom forall bytes32 key. !reachable[key][Zero()] && !reachable[Zero()][key];

    // Reflexivity
    //axiom forall bytes32 key. (key != 0 && elementExists[key]) => reachable[key][key];

    // Transitivity
    axiom forall bytes32 x. forall bytes32 y. forall bytes32 z. (
        (reachable[x][y] && reachable[y][z]) => reachable[x][z]
    );

    // In a tree there is a unique path (also reflexivity)
    axiom forall bytes32 x. forall bytes32 y. forall bytes32 z. (
        (reachable[x][z] && reachable[y][z]) => (reachable[x][y] || reachable[y][x])
    );

    // Immediate children
    axiom forall bytes32 parent. forall bytes32 child. (
        isChildOf[parent][child] => reachable[parent][child]
    );
}

hook Sstore currentContract.tree.elements[KEY bytes32 key].leftChild 
    bytes32 newChild (bytes32 oldChild) STORAGE
{
        leftChild[key] = newChild;
        isChildOf[key][newChild] = true;
        if (rightChild[key] != oldChild) {
            isChildOf[key][oldChild] = false;
        }
}

hook Sstore currentContract.tree.elements[KEY bytes32 key].rightChild 
    bytes32 newChild (bytes32 oldChild) STORAGE
{
        rightChild[key] = newChild;
        isChildOf[key][newChild] = true;
        if (leftChild[key] != oldChild) {
            isChildOf[key][oldChild] = false;
        }
}

invariant rootReachesAll(bytes32 key)
    (contains(key) && key != root()) => reachable[root()][key];
