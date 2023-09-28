methods {
    function points(address) external returns uint256  envfree;
    function vote(address,address,address) external;
    function voted(address) external returns bool  envfree;
    function winner() external returns address  envfree;
}

ghost bool accessed {
	init_state axiom !accessed;
}

hook Sstore _points[KEY address a] uint256 new_points (uint256 old_points) STORAGE {
	accessed = true;
}

hook Sstore _voted[KEY address a] bool val (bool old_val) STORAGE {
	accessed = true;
}

// require that !accessed in the initial state after the constructor concludes
invariant noConstructorSSTOREs() 
    !accessed
	{ preserved {
		require false; // this is purposely vacuous
	} }
