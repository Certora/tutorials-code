/* Both examples below imply that:
 * `pre != post  =>  exists uint256 i s.t. _map@old[i] == 0 && map@new[i] > 0`
 * where `_map` has type `mapping(uint256 => uint8)`.
 */

/* First example ===============================================================
 * This example proves that if `pre != post` then:
 * 1. During `f` there was a store operation to `_map[i]` for some `i` where
 *    the old value was zero and the new value was non-zero, and
 * 2. During `f` the *last* store operation to `_map` was as above, i.e.
 *    a non-zero value replaced a zero value
 */

ghost imp() returns bool;

hook Sstore _map[KEY uint256 i] uint8 newVal (uint8 oldVal) {
    havoc imp assuming (oldVal == 0 && newVal > 0) => imp@new();
}

rule someRule(method f) {
    assert sig:something().isView;

    uint256 pre = something();

    env e;
    calldataarg args;
    f(e, args);

    uint256 post = something();

    assert (pre != post) => imp();
}


/* Second example ==============================================================
 * This example proves that if `pre != post` then:
 * As above - during `f` there was a store operation to `_map[i]` for some `i` where
 * the old value was zero and the new value was non-zero. However, unlike the first
 * example it is not required that the last store during `f` would be of this form.
 */
ghost imp() returns bool {
    init_state axiom !imp();
}

hook Sstore _map[KEY uint256 i] uint8 newVal (uint8 oldVal) {
    havoc imp assuming (
        ( (oldVal == 0 && newVal > 0) => imp@new() ) &&
        (!(oldVal == 0 && newVal > 0) => imp@old() == imp@new() )
    );
}

rule someRule(method f) {
    assert sig:something().isView;

    require !imp();
    uint256 pre = something();

    env e;
    calldataarg args;
    f(e, args);

    uint256 post = something();

    assert (pre != post) => imp();
}

// -----------------------------------------------------------------------------

/* More complicated setup. Both examples below show that:
 * `pre != post  =>  exists uint128 j s.t. _map@old[i][j] == 0 && map@new[i][j] > 0`
 * where `_map` has type `mapping(uint256 => mapping(uint128 => uint8))`.
 */

// First example ===============================================================
ghost imp(uint256) returns bool;

hook Sstore _map[KEY uint256 i][KEY uint128 j] uint8 newVal (uint8 oldVal) {
    havoc imp assuming (oldVal == 0 && newVal > 0) => imp@new(i);
}

rule someRule(method f, uint256 i) {
    assert sig:something(uint256).isView;

    uint256 pre = something(i);

    env e;
    calldataarg args;
    f(e, args);

    uint256 post = something(i);

    assert (pre != post) => imp(i);
}


// Second example ==============================================================
ghost imp(uint256) returns bool {
    init_state axiom forall uint256 i. !imp(i);
}

hook Sstore _map[KEY uint256 i][KEY uint128 j] uint8 newVal (uint8 oldVal) {
    havoc imp assuming (
        ( (oldVal == 0 && newVal > 0) <=> imp@new(i) ) &&
        ( forall uint256 k. k != i => !imp@new(k) )
    );
}

rule someRule(method f, uint256 i) {
    assert sig:something(uint256).isView;

    require !imp(i);
    uint256 pre = something(i);

    env e;
    calldataarg args;
    f(e, args);

    uint256 post = something(i);

    assert (pre != post) => imp(i);
}
