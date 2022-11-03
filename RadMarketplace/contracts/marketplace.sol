// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";


contract MarketPlace is Ownable {

	struct sale {
		address contractAddress;
		address payable owner;
		uint256 id;
		uint256 price;
	}

	struct auction {
		sale data;
		address bidder;
		uint256 bid;
	}

	struct offer {
		sale data;
		address buyer;
	}

	address public araToken;
	uint256 marketPlaceFee;
	uint256 waiver;

	uint256 _salesId;

	mapping (uint256 => sale) internal _sales;

	constructor (
		address _ara,
		uint256 _marketFee,
		uint256 _waiver
	) {
		araToken = _ara;
		marketPlaceFee = _marketFee;
		_salesId = 1;
		waiver = _waiver;
	}

	function setARA(address _ara) external onlyOwner {
		araToken = _ara;
	}

	function setFee(uint256 _marketFee) external onlyOwner {
		marketPlaceFee = _marketFee;
	}

	function setWaiver(uint256 _waiver) external onlyOwner {
		waiver = _waiver;
	}


	function createSimpleOffer(address nftContract, uint256 nftId, uint256 price) external returns (uint256) {

		ERC721 nft = ERC721(nftContract);

		nft.safeTransferFrom(msg.sender, address(this), nftId);
		_sales[_salesId] = sale(nftContract, payable(msg.sender), nftId, price);
		_salesId++;

		return _salesId - 1;
	}

	function removeSimpleOffer (uint256 saleId) external {
		require(_sales[saleId].owner == msg.sender, "You are not the creator of this sale");

		ERC721 nft = ERC721(_sales[saleId].contractAddress);

		nft.safeTransferFrom(address(this), msg.sender, _sales[saleId].id);
		delete _sales[saleId];
	}

	function updateSimpleOffer (uint256 saleId, uint256 newPrice) external {
		require(_sales[saleId].owner == msg.sender, "You are not the creator of this sale");

		_sales[saleId].price = newPrice;
	}

	function buySimpleOffer (uint256 saleId) external payable{

		require(_sales[saleId].contractAddress == address(0x0), "This sale does not exist or has ended");
		require(msg.value == _sales[saleId].price, "Insufficient funds");

		// Transfer money to seller, need to see whats up with market fee
		ERC721 nft = ERC721(_sales[saleId].contractAddress);
		ERC20 ARA = ERC20(araToken);

		if (ARA.balanceOf(_sales[saleId].owner) < waiver)
			_sales[saleId].owner.transfer(_sales[saleId].price - ((_sales[saleId].price * marketPlaceFee) / 100));
		else
			_sales[saleId].owner.transfer(_sales[saleId].price);

		nft.safeTransferFrom(address(this), msg.sender, _sales[saleId].id);

		delete _sales[saleId];
	}

	function createAuction (address nftContract, uint256 nftId, uint256 price, uint256 startTime, uint256 duration) external {

	}

}
