// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./TokenContract.sol";

contract MarketplaceContract {
    TokenContract public tokenContract;
    
    constructor(address _tokenContract) {
        tokenContract = TokenContract(_tokenContract);
    }
    
    function buyToken(uint256 amount) public {
        // Simplified: assume 1 token costs 1 ether
        require(msg.value >= amount, "Insufficient payment");
        tokenContract.mint(msg.sender, amount);
    }
    
    function sellToken(uint256 amount) public {
        tokenContract.transfer(address(this), amount);
        payable(msg.sender).transfer(amount);
    }
}