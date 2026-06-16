methods {

    function eqn(uint256, uint256) external returns (bool) envfree;
    function add(uint256 x, uint256 y) external returns(uint256) envfree;
    function divide(uint256,uint256) external returns(uint256) envfree;
    function average(uint256 x, uint256 y) external returns (uint256) envfree;
    function flawedCeilDiv(uint256 n, uint256 d) external returns (uint256) envfree;
}

rule flawedCeilDiv_overflow() {
    uint256 n;
    uint256 d;

    require d != 0;
    
    mathint returnVal = flawedCeilDiv(n, d);
    mathint expectedVal = (n + d - 1) / d;

    assert returnVal == expectedVal;   
}

rule average_overflowIgnored() {
    uint256 x;
    uint256 y;

    mathint returnVal = average(x, y);
    
    uint256 numerator = require_uint256(x + y);
    uint256 expectedVal = require_uint256(numerator / 2);

    assert returnVal == expectedVal;
}

rule average_overflow() {
    uint256 x;
    uint256 y;

    mathint returnVal = average(x, y);
    assert returnVal == (x + y) / 2;
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