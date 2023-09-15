// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ERC20} from "../../token/ERC20/ERC20.sol";

contract ERC20Mock is ERC20 {
    constructor() {}

    function mint(address account, uint256 amount) external {
        _mint(account, amount);
    }

    function burn(address account, uint256 amount) external {
        _burn(account, amount);
    }
}
