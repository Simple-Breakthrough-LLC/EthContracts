
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

contract TokenSaleToken is
	Ownable,
	Pausable
{
	uint256 maxSupply;

	uint256 private _guard;

	uint256 public price;
	uint256 public remainingSaleTokens;
	uint256 public totalSupply;
	address public paymentToken;
	address public saleToken;

	constructor (
		address _paymentToken,
		address _saleToken,
		uint256 _maxSupply
	) {
		paymentToken = _paymentToken;
		saleToken = _saleToken;
		maxSupply = _maxSupply;
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

	function setPaymentToken (address token) external onlyOwner {
		paymentToken = token;
	}

	function setSaleToken (address token) external onlyOwner {
		saleToken = token;
	}

	function pauseContract() external onlyOwner {
		_pause();
	}

	function unpauseContract() external onlyOwner {
		_unpause();
	}

	function Buy (uint256 amount) whenNotPaused nonReentrant external {
		IERC20 payment = IERC20(paymentToken);
		IERC20 sale = IERC20(saleToken);

		require (payment.balanceOf(msg.sender) >= amount * price, "Insufficient funds");

		payment.transferFrom(msg.sender, address(this), amount * price);
		sale.mint(msg.sender, amount);

	}
}
