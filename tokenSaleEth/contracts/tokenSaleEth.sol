
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

// import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "./ERC20Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

contract TokenSaleToken is

	Ownable,
	Pausable
{
	uint256 maxSupply;

	uint256 private _guard;

	uint256 public price;
	uint256 public remainingSaleSupply;
	uint256 public totalSupply;
	address public saleToken;

	constructor (
		address _saleToken,
		uint256 saleSupply
	) payable {
		saleToken = _saleToken;
		remainingSaleSupply = saleSupply;
		totalSupply = 0;
		_guard = 1;
	}

	modifier nonReentrant() {
		uint256 local;

		_guard += 1;
		local = _guard;
        _;
        require(local == _guard);
	}

	function setPrice(uint256 _price) external onlyOwner {
		price = _price;
	}

	function setSaleToken (address token) external onlyOwner {
		saleToken = token;
	}

	function setSaleSupply (uint256 amount) external onlyOwner {
		remainingSaleSupply = amount;
	}

	function pause() external onlyOwner {
		_pause();
	}

	function unpause() external onlyOwner {
		_unpause();
	}

	function buy (uint256 amount) payable whenNotPaused nonReentrant external {
		ERC20 sale = ERC20(saleToken);

		require(remainingSaleSupply >= amount, "Not enough tokens remaining");
		require(msg.value == amount * price, "Insufficient funds");

		sale.mint(msg.sender, amount);

		totalSupply += amount;
		remainingSaleSupply -= amount;
	}

    function withdraw() payable external onlyOwner {

		msg.sender.transfer(address(this).balance);

		remainingSaleSupply = 0;
    }

}
