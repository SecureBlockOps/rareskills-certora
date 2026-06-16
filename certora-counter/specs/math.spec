methods {

    function eqn(uint256, uint256) external returns (bool) envfree;
    function add(uint256 x, uint256 y) external returns(uint256) envfree;
    function divide(uint256,uint256) external returns(uint256) envfree;

}

rule checkEqn() {

    uint256 x; 
    uint256 y;

    satisfy eqn(x, y) == true;
}

rule checkAdd() {
    uint256 a;
    uint256 b;
    uint256 c = add@withrevert(a,b);
    assert a+b==c;
}


rule addShouldRevert() {

    uint256 a;
    uint256 b;

    require(a + b > max_uint256);
    
    add@withrevert(a,b);
    
    assert lastReverted; 
}

rule addShouldNotRevert() {

    uint256 a;
    uint256 b;

    require(a + b <= max_uint256);

    add@withrevert(a,b);

    assert !lastReverted;
}

rule checkMath() {

    uint256 a;
    
    divide@withrevert(a,0);
    bool divideCallStatus = lastReverted;

    add@withrevert(a,0);
    bool addCallStatus = lastReverted;

    assert divideCallStatus == true;
    assert addCallStatus == false;
}