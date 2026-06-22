methods {
    function count() external returns(uint256) envfree;
    function increment() external envfree;
    function decrement() external envfree;
}


rule checkIncrementCall() {

    //Precall Requirement
    require count() == 0;

    // Call OR Action
    increment();


    // Post-call Expectation
    assert count() == 1;

}
rule checkCounter() {

    //Retrieval of Pre-call value
    uint256 precallCountValue = count();

    // Call
    increment();
    decrement();

    //Retrieval of Post-call value
    uint256  postcallCountValue = count();

    //Post-call Expectation
    assert postcallCountValue == precallCountValue;
}
