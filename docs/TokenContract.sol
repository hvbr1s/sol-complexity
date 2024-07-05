// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TokenContract {
    mapping(address => uint256) public balances;
    
    function mint(address to, uint256 amount) public {
        balances[to] += amount;
    }
    
    function transfer(address to, uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }
}