// SPDX-License-Identifier: MIT
pragma solidity 0.8.25;

contract Math {
    function eqn(uint256 x, uint256 y) external pure returns (bool) {
        return (2 * x + 3 * y == 22) && (4 * x - y == 2);
    }

    function add(uint256 x, uint256 y) public pure returns (uint256) {
        return x + y;
    }

    function divide(uint256 x, uint256 y) public pure returns (uint256) {
        return x / y;
    }

    function average(uint256 x, uint256 y) external pure returns (uint256) {
        unchecked {
            return (x + y) / 2;
        }
    }

    function flawedCeilDiv(
        uint256 n,
        uint256 d
    ) external pure returns (uint256 z) {
        assembly {
            z := div(sub(add(n, d), 1), d)
        }
    }

    function max(uint256 x, uint256 y) external pure returns (uint256 z) {
        assembly {
            z := xor(x, mul(xor(x, y), gt(y, x)))
        }
    }

    /// Solidity

    uint256 internal constant MAX_UINT256 = 2 ** 256 - 1;

    function mulDivUp(
        uint256 x,
        uint256 y,
        uint256 denominator
    ) external pure returns (uint256 z) {
        assembly {
            // Equivalent to require(denominator != 0 && (y == 0 || x <= type(uint256).max / y))
            if iszero(
                mul(denominator, iszero(mul(y, gt(x, div(MAX_UINT256, y)))))
            ) {
                revert(0, 0)
            }

            // If x * y modulo the denominator is strictly greater than 0,
            // 1 is added to round up the division of x * y by the denominator.
            z := add(
                gt(mod(mul(x, y), denominator), 0),
                div(mul(x, y), denominator)
            )
        }
    }
}
