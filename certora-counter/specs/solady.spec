methods {
        function min(uint256 x, uint256 y) external returns (uint256) envfree;
}

rule min(){
    uint256 a;
    uint256 b;

    if(a<b){
        uint256 c = min@withrevert(a,b);
        assert !lastReverted;
        assert c == a;
    }
    else {
        uint256 c = min@withrevert(a,b);
        assert !lastReverted;
        assert c == b;
    } 
}