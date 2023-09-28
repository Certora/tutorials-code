methods {
    function points(address) external returns uint256  envfree;
    function vote(address,address,address) external;
    function voted(address) external returns bool  envfree;
    function winner() external returns address  envfree;
}

ghost mathint countVoters {
	init_state axiom countVoters == 0;
}

ghost mathint sumPoints {
	init_state axiom sumPoints == 0;
}

hook Sstore _points[KEY address a] uint256 new_points (uint256 old_points) STORAGE {
	sumPoints = sumPoints + new_points - old_points;
}

hook Sstore _voted[KEY address a] bool val (bool old_val) STORAGE {
	countVoters = countVoters + (val ? 1 : 0) - (old_val ? 1 : 0);
}

invariant sumOfPoints() 
    sumPoints == countVoters * 6;



