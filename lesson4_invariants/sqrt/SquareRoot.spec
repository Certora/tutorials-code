/**
 * Spec for square root approximation
 */
methods {
    function FIXEDPOINT() external returns (uint256) envfree;
    function sqrt(uint256 x) internal returns (uint256) with (env e) => sqrtSummary(x);
}


/// @title This ghost mirrors `FIXEDPOINT`
ghost uint256 fixedpoint;


/// @title A macro defining the desired precision
definition PRECISION() returns mathint = 1 * fixedpoint;


/// @title Ghost function for square root
ghost sqrtSummary(uint256) returns uint256 {
    axiom forall uint256 x. (
        sqrtSummary(x) * sqrtSummary(x) - x * fixedpoint <= PRECISION() &&
        sqrtSummary(x) * sqrtSummary(x) - x * fixedpoint >= 0 - PRECISION()
    );
}

/// @title This rule simply tests the summary `sqrtSummary`
rule sqrtTest(uint256 x, env e) {
    requireInvariant fixedPointValue();
    require fixedpoint == FIXEDPOINT();
    assert sqrt(e, x) * sqrt(e, x) - x * FIXEDPOINT() <= PRECISION();
    assert sqrt(e, x) * sqrt(e, x) - x * FIXEDPOINT() >= -PRECISION();
}


invariant fixedPointValue()
    FIXEDPOINT() == 10000;
