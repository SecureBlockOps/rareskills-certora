methods {

    function eqn(uint256, uint256) external returns (bool) envfree;
}

rule checkEqn() {

    uint256 x; 
    uint256 y;

    satisfy eqn(x, y) == true;
}
