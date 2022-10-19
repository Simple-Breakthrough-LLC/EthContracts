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

//  mint

//  MC4V3WX
//  MV4C3WX
//  MVC43WX
//  MCV43WX
//  MV34CWX
//  MV43CWX
//  MC43VWX
//  MC34VWX
//  MV3C4WX
//  MVC34WX
//  MCV34WX
//  MC3V4WX
