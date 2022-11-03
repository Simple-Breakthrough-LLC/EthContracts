// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/interfaces/IERC721Receiver.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";


contract MarketPlace is Ownable, IERC721Receiver {

	struct sale {
		address contractAddress;
		address payable owner;
		uint256 id;
		uint256 price;
	}

	struct auction {
		sale data;
		uint256 startTime;
		uint256 duration;
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
	uint256 _auctionId;
	uint256 _offerId;

	mapping (uint256 => sale) internal _sales;
	mapping (uint256 => auction) internal _auctions;
	mapping (uint256 => offer) internal _offer;

	constructor (
		address _ara,
		uint256 _marketFee,
		uint256 _waiver
	) {
		araToken = _ara;
		marketPlaceFee = _marketFee;
		_salesId = 1;
		_auctionId = 1;
		_offerId = 1;
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

	function getSimpleSale(uint256 saleId) external view returns (uint256) {
		return _sales[saleId].price;
	}

	function getAuction(uint256 auctionId) external view returns (address, uint256) {
		return (_auctions[auctionId].bidder, _auctions[auctionId].bid);
	}


	function onERC721Received(address,address,uint256,bytes calldata) external pure returns (bytes4) {
		return IERC721Receiver.onERC721Received.selector;
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

		require(_sales[saleId].contractAddress != address(0x0), "This sale does not exist or has ended");
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

	function createAuction (address nftContract, uint256 nftId, uint256 price, uint256 startTime, uint256 duration) external returns (uint256) {
		// expecting time between when user submits to time when transaction is ran to be different
		require(startTime + 60 >= block.timestamp, "Duration must be greater than 0");

		ERC721 nft = ERC721(nftContract);

		nft.transferFrom(msg.sender, address(this), nftId);
		_auctions[_auctionId] = auction(sale(nftContract, payable(msg.sender), nftId, price), startTime, duration, address(0x0), 0);


		_auctionId++;
		return _auctionId - 1;
	}


	function bidAuction(uint256 auctionId) external payable {
		require (_auctions[auctionId].data.owner != address(0x0), "Auction does not exist or has ended");
		require(block.timestamp < (_auctions[auctionId].startTime + _auctions[auctionId].duration));
		require(msg.value > _auctions[auctionId].bid);

		if (_auctions[auctionId].bidder != address(0x0))
			payable(_auctions[auctionId].bidder).transfer(_auctions[auctionId].bid);

		_auctions[auctionId].bid = msg.value;
		_auctions[auctionId].bidder = msg.sender;
	}

	function redeemAuction(uint256 auctionId) external {

		require (_auctions[auctionId].data.owner != address(0x0), "Auction does not exist or has ended");
		require(msg.sender == _auctions[auctionId].bidder);

		ERC721 nft = ERC721(_auctions[auctionId].data.contractAddress);
		ERC20 ARA = ERC20(araToken);

		nft.transferFrom(address(this), msg.sender, _auctions[auctionId].data.id);


		if (ARA.balanceOf(_auctions[auctionId].data.owner) < waiver)
			_auctions[auctionId].data.owner.transfer(_auctions[auctionId].data.price - ((_auctions[auctionId].data.price * marketPlaceFee) / 100));
		else
			_auctions[auctionId].data.owner.transfer(_auctions[auctionId].data.price);

		delete _auctions[auctionId];
	}

	function createPassiveOffer(address nftContract, uint256 nftId, uint256 price) external payable returns(uint256) {

		ERC721 nft = ERC721(nftContract);

		require(price == msg.value, "Insufficient funds");
		_offer[_offerId] = offer(sale(nftContract, payable(nft.ownerOf(nftId)), nftId, price), msg.sender);


		_offerId++;
		return _offerId;
	}

	function rejectOffer(uint256 offerId)	external {
		require (_offer[offerId].data.owner != address(0x0), "Offer does not exist or has ended");

		ERC721 nft = ERC721(_offer[_offerId].data.contractAddress);

		require(msg.sender == nft.ownerOf(_offer[_offerId].data.id), "Only nft owner can cancel offer");
		payable(_offer[_offerId].buyer).transfer(_offer[_offerId].data.price);

		delete _offer[_offerId];
	}


	function acceptOffer(uint256 offerId) external {
		require (_offer[offerId].data.owner != address(0x0), "Offer does not exist or has ended");

		ERC721 nft = ERC721(_offer[_offerId].data.contractAddress);

		address owner =  nft.ownerOf(_offer[_offerId].data.id);

		require(msg.sender == owner, "Only nft owner can accept offer");
		payable(owner).transfer(_offer[_offerId].data.price);
		nft.safeTransferFrom(owner, _offer[_offerId].buyer, _offer[_offerId].data.id);

		delete _offer[_offerId];
	}

	function cancelOffer(uint256 offerId) external {
		require (_offer[offerId].data.owner != address(0x0), "Offer does not exist or has ended");

		require(msg.sender == _offer[_offerId].buyer, "Only offer creator can cancel offer");
		payable(msg.sender).transfer(_offer[_offerId].data.price);

		delete _offer[_offerId];
	}
}
