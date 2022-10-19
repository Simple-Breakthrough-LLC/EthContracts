
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
	address public paymentToken;
	address public saleToken;

	constructor (
		address _paymentToken,
		address _saleToken,
		uint256 saleSupply
	) {
		paymentToken = _paymentToken;
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

	function setPaymentToken (address token) external onlyOwner {
		paymentToken = token;
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

	function buy (uint256 amount) whenNotPaused nonReentrant external {
		ERC20 payment = ERC20(paymentToken);
		ERC20 sale = ERC20(saleToken);

		require(remainingSaleSupply >= amount, "Not enough tokens remaining");
		require(payment.balanceOf(msg.sender) >= amount * price, "Insufficient funds");


		payment.transferFrom(msg.sender, address(this), amount * price);
		sale.mint(msg.sender, amount);

		totalSupply += amount;
		remainingSaleSupply -= amount;
	}

    function withdraw() external onlyOwner {
		ERC20 payment = ERC20(paymentToken);

		payment.transfer(msg.sender, payment.balanceOf(address(this)));

		remainingSaleSupply = 0;
    }

}
