// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";

/**
 * @title Free NFT Minter
 * @author Breakthrough Labs Inc.
 * @notice NFT, Free, ERC721
 * @custom:version 1.0.8
 * @custom:address 11
 * @custom:default-precision 0
 * @custom:simple-description Free NFT and Minter
 * @dev ERC721 NFT with the following features:
 *
 *  - NFT with mint function.
 *  - Fixed maximum supply.
 *
 */

contract NFT is ERC721Enumerable, Ownable {
    string private _baseURIextended;

    /**
     * @param _name NFT Name
     * @param _symbol NFT Symbol
     * @param _uri Token URI used for metadata
     */
    constructor(string memory name, string memory symbol)
        ERC721(name, symbol)
    {}

    function mint(address to) public {
        _safeMint(to, totalSupply());
    }

    /**
     * @dev An external method for users to purchase and mint NFTs. 
     * that the minted NFTs will not exceed the `MAX_SUPPLY`, and that a
     * @param amount The number of NFTs to mint.
     */
    function mint(address to, uint256 amount) public {
        uint256 start = totalSupply();
        uint256 end = start + amount;
        for (uint256 id = start; id < end; id++) _safeMint(to, id);
    }

    /**
     * @dev Updates the baseURI that will be used to retrieve NFT metadata.
     * @param baseURI_ The baseURI to be used.
     */
    function setBaseURI(string memory baseURI_) external onlyOwner {
        _baseURIextended = baseURI_;
    }

    function _baseURI() internal view virtual override returns (string memory) {
        return _baseURIextended;
    }
}
