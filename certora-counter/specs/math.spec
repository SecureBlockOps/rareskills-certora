methods {

    function eqn(uint256, uint256) external returns (bool) envfree;
    function add(uint256 x, uint256 y) external returns(uint256) envfree;
    function divide(uint256,uint256) external returns(uint256) envfree;
    function average(uint256 x, uint256 y) external returns (uint256) envfree;
    function flawedCeilDiv(uint256 n, uint256 d) external returns (uint256) envfree;
    function add(uint256,uint256) external returns(uint256) envfree;
    function max(uint256 x, uint256 y) external returns (uint256) envfree;
    function mulDivUp(uint256 x,uint256 y,uint256 denominator) external returns (uint256) envfree;

}

/// CVL

rule mulDivUp_roundOrRevert() {
    uint256 x;
    uint256 y;
    uint256 denominator;

    if (denominator == 0) { // catches revert condition: if denominator is zero 
        mulDivUp@withrevert(x, y, denominator); 
        assert lastReverted;
    }
    else if (x * y > max_uint256) { // catches revert condition: multiplication overflows a max_uint256 value
        mulDivUp@withrevert(x, y, denominator);
        assert lastReverted;
    } 
    else { // catches all non-revert conditions
        if (x * y % denominator == 0) { // if there's no remainder after x * y and denominator division
            mathint result = mulDivUp@withrevert(x, y, denominator);
            
            assert !lastReverted;
            assert result == x * y / denominator;
        } 
        else { // if there's a remainder after x * y and denominator division
            mathint result = mulDivUp@withrevert(x, y, denominator); 
            
            assert !lastReverted;
            assert result == (x * y / denominator) + 1;
        }
    }
}


rule max_returnMax() {
    uint256 x;
    uint256 y;

    if (x >= y) {
        mathint max = max@withrevert(x, y);
        assert !lastReverted;
        assert max == x;
    }
    else {
        mathint max = max@withrevert(x, y);
        assert !lastReverted;
        assert max == y;
    }
}

rule add_sumWithOverflowRevert() {
    uint256 x;
    uint256 y;

    mathint _sum = x + y;
    
    if (_sum <= max_uint256) { // non-revert case
        mathint result = add@withrevert(x, y);
        assert !lastReverted;
        assert result == _sum;
    }
    else { // revert case
        add@withrevert(x, y);
        assert lastReverted; 
    }
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