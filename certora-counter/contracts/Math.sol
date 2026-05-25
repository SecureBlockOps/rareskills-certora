// SPDX-License-Identifier: MIT
pragma solidity 0.8.25;

contract Math {
    function eqn(uint256 x, uint256 y) external pure returns (bool) {
        return (2 * x + 3 * y == 22) && (4 * x - y == 2);
    }
}
