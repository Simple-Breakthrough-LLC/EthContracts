# Notes and specs

Google docs: https://docs.google.com/document/d/1bgQRy6FzgL3n6co1J5L6TY4XoUbfCKJtadXLS556_BE/edit#heading=h.dy0zn1rbvewu

--------------

Both ERC1155 and ERC721

- One contract per type of sale , with one mediator contract to send the correct things to, that will decide what to do (would be multiple transactions maybe?)
- OR
- One contract to handle everything, but it would require several different data structures

 NFTs need to keep their original owner so it can be returned to them. Also need to origin contract. Hash these into a key for a mapping? hash : (info)

** Questions **

 - For 1155 sale, allow multiple to be put up for sale ? If so, price set per NFT or for all ? How would that work with auction ? Passive offers ?
 - How are we storing the sale info ? Will a database keep track of auctions (if so may not need hash)
 - Escrow : contract or holding wallet? Can be set or not ?
 - Marketplace fee for every transaction or only for buyer / seller ? Where does that fee go? Stored in contract or wallet?
 - Delay start auction ?
 - Cancel auction ?

## Simple Sale
	User puts NFT for sale at a price.

### Write
	- [ ] Token for sale
	- [ ] Buy token from sale
	- [ ] Remove token from sale

### View
	Token price
	Owner ?

## Auction

	Auction starts at 0. Users may place bets. Highest bidder gets NFT if reserve price is met. Highest bid in escrow. Winner pays gas and owner (potentially another transaction?)


### Write

	- [ ] New auction (reserve price, ID, contract, start, duration)

	- [ ] Bid
	- [ ] Set remaining time

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

	- [ ] New offer (id, contract, price)

### View



## Additional

	- Marketplace fee (waived for owned of X ARA)
