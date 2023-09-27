methods {
    function points(address) external returns uint256  envfree;
    function vote(address,address,address) external;
    function voted(address) external returns bool  envfree;
    function winner() external returns address  envfree;
}

ghost mapping(address => bool) voted_tracker {
	init_state axiom forall address c. voted_tracker[c] == false;
}

hook Sstore _voted[KEY address a] bool val (bool old_val) STORAGE {
	voted_tracker[a] = val;
}

invariant BordaMissingRule()
	forall address c. voted_tracker[c] == voted(c);