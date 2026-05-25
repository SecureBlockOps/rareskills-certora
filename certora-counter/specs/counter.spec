methods {
    function count() external returns(uint256) envfree;
    function increment() external envfree;
}


rule checkCounter() {

    // Pre-Call State
    uint256 precallCount = count();

    // Method Call
    increment();

    // Post-call state
    uint256 postcallCount = count();

    // Assert that the post-call count is exactly one more than the pre-call count
    assert postcallCount == precallCount + 1;

}

rule checkCountValidity() {
    
    require count() == 0;
    
    // Grabbing the initial state of the count variable
    uint256 PrecallCountValue = count();

    // Call to increment()
    increment();
    increment();
    increment();

    // Grabbing the state of count after the increment() calls
    uint256 PostcallCountValue = count();

    // Assertions
    assert PrecallCountValue == 0;
    assert PostcallCountValue == PrecallCountValue + 3;
}
