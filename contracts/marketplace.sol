// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/utils/Context.sol";
import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/interfaces/IERC1155Receiver.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract marketPlaceBoilerPlate is Context, ReentrancyGuard, IERC1155Receiver {
    using Counters for Counters.Counter;
    Counters.Counter private _itemIds;
    Counters.Counter private _itemsSold;

     address public owner;

     constructor() {
		owner = _msgSender();
     }

     struct MarketItem {
         uint256 itemId;
         uint256 tokenId;
         uint256 price;
         uint256 amount;
         address nftContract;
         address payable seller;
     }

     mapping(uint256 => MarketItem) private idToMarketItem;

     event MarketItemCreated (
        uint256 indexed itemId,
        uint256 indexed tokenId,
        uint256 price,
		uint256 amount,
        address indexed nftContract,
        address seller
     );

     event MarketItemSold (
         uint indexed itemId
         );

	function supportsInterface(bytes4 interfaceId) public pure override returns (bool) {
        return interfaceId == type(IERC165).interfaceId || interfaceId == type(IERC1155Receiver).interfaceId;
    }

    function onERC1155Received(
        address operator,
        address from,
        uint256 id,
        uint256 value,
        bytes calldata data
    ) external pure returns (bytes4) {
        return IERC1155Receiver.onERC1155Received.selector;
    }

    function onERC1155BatchReceived(
        address operator,
        address from,
        uint256[] calldata ids,
        uint256[] calldata values,
        bytes calldata data
    ) external pure returns (bytes4) {
        revert(); // this will never happen
    }

    function createMarketItem(
        address nftContract,
        uint256 tokenId,
        uint256 price,
		uint256 amount
        ) public payable nonReentrant {
            require(price > 0, "Price must be greater than 0");
            require(amount > 0, "Amount must be greater than 0");

            _itemIds.increment();

            uint256 itemId = _itemIds.current();

            idToMarketItem[itemId] =  MarketItem(
                itemId,
                tokenId,
                price,
				amount,
                nftContract,
                payable(_msgSender())
            );

            IERC1155(nftContract).safeTransferFrom(_msgSender(), address(this), tokenId, amount, "");
            // IERC1155(nftContract).transferFrom(_msgSender(), address(this), tokenId);

            emit MarketItemCreated(
                itemId,
                tokenId,
                price,
				amount,
                nftContract,
                _msgSender()
            );
        }

    function createMarketSale(
        address nftContract,
        uint256 itemId,
		uint256 amountBought
        ) public payable nonReentrant {
            uint256 price = idToMarketItem[itemId].price;
            uint256 tokenId = idToMarketItem[itemId].tokenId;
            uint256 remainingTokens = idToMarketItem[itemId].amount;
            // bool sold = idToMarketItem[itemId].sold;

            require(remainingTokens != 0, "This Sale has alredy finnished");
            require((amountBought > 0) && (amountBought <= remainingTokens), "Incorrect token amount");
            require(msg.value == (amountBought * price ), "Please submit the asking price in order to complete the purchase");

            emit MarketItemSold(
                itemId
                );

            idToMarketItem[itemId].seller.transfer(msg.value);

			IERC1155(nftContract).safeTransferFrom(address(this), _msgSender(), tokenId, amountBought, "");
            _itemsSold.increment();
            idToMarketItem[itemId].amount -= amountBought;
        }

    function fetchMarketItems() public view returns (MarketItem[] memory) {
        uint itemCount = _itemIds.current();
        uint unsoldItemCount = _itemIds.current() - _itemsSold.current();
        uint currentIndex = 0;

        MarketItem[] memory items = new MarketItem[](unsoldItemCount);
        for (uint i = 0; i < itemCount; i++) {
            if (idToMarketItem[i + 1].amount > 0) {
                uint currentId = i + 1;
                MarketItem storage currentItem = idToMarketItem[currentId];
                items[currentIndex] = currentItem;
                currentIndex += 1;
            }
        }
        return items;
    }
}
