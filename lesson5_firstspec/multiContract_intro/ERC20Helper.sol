// SPDX-License-Identifier: agpl-3.0
pragma solidity ^0.8.0;
import "./ERC20.sol";

contract ERC20Helper {

    function tokenBalanceOf(address token, address user) public returns (uint256) {
            return ERC20(token).balanceOf(user);
    }
}