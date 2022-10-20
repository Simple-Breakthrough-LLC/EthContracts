pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract GenericERC20 is ERC20 {
	constructor() ERC20("name", "symbol") {}

	function mint(
        address to,
        uint256 amount)
		public {
		_mint(to, amount);
	}
}
