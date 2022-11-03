# Notes and specs

Google docs: https://docs.google.com/document/d/1bgQRy6FzgL3n6co1J5L6TY4XoUbfCKJtadXLS556_BE/edit#heading=h.dy0zn1rbvewu

Current MarketPlace: https://etherscan.io/address/0xA1F6868aC9D71984b296B209A9Bb4B7FC7f4bBA0

Rarible conttrcat : https://github.com/rarible/protocol-contracts/tree/master/exchange-v2

-------

NFT royalty standard: https://eips.ethereum.org/EIPS/eip-2981

Hashing standard: https://github.com/ethereum/EIPs/blob/master/EIPS/eip-712.md

--------------

ERC721 (for now)

1) One contract per type of sale , with one mediator contract to send the correct things to, that will decide what to do (would be multiple transactions maybe?)
OR
2) One contract to handle everything, but it would require several different data structures

 NFTs need to keep their original owner so it can be returned to them. Also need to origin contract. Hash these into a key for a mapping? hash : (info)

 struct nft {
	id,  contract, owner, data
 }

 Mapping : seuqntially, by sale id. backend will take care of the rest

 order : fill DS corresponding to order type (cimple, passive, auction) -> get key (hash) or id -> return order id, or hash
			- either require isgnature from wallet / contract
		-> transfer to contract / holding wallet

 ** ???? **

 Seems very inneficient that solidity doesn't free memory . How to deal with sales that have ended and take up space?
 How to retrieve info efficiently ?


** Questions **

- For 1155 sale, allow multiple to be put up for sale ? If so, price set per NFT or for all ? How would that work with auction ? Passive offers ?
		_ No 1155 for now
- How are we storing the sale info ? Will a database keep track of auctions (if so may not need hash)
	_ However rarible does it
- Escrow : contract or holding wallet? Can be set or not ?
	_ However rarible does it
- Marketplace fee for every transaction or only for buyer / seller ? Where does that fee go? Stored in contract or wallet?
	_ However rarible does it
- Delay start auction ?|
	_ Keep track of start / end time
- Cancel auction ?
	_Not clear ?


## Simple Sale
	User puts NFT for sale at a price.

### Write

- [X] Token for sale
- [X] Buy token from sale
- [X] Remove token from sale

### View
Token price
Owner ?

## Auction

Auction starts at 0. Users may place bets. Highest bidder gets NFT if reserve price is met. Highest bid in escrow. Winner pays gas and owner (potentially another transaction?)

Must keep start time and duration or start time and calc end time
Keep highest bidder

### Write

- [x] New auction (reserve price, ID, contract, start, duration)
- [x] Bid

### View
	Reserve price
	Start time
	End time or remaining time
	Bid count
	Highest bid
	Owner ?
	Highest bidder ?


## Passive offers

User sets price for an NFT they want. $$ to escrow. Owner can accept or reject offer

### Write

- [x] New offer (id, contract, price)

### View
	price
	buyer address
	offer to address
	offer form address


## Additional
- Royalties
- Marketplace fee (waived for owned of X ARA)
