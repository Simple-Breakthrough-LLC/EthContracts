import pytest

from brownie import RadMarketPlace, NFT1155, NFT721, accounts, reverts

@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

##		 Simple Sale
# SUCCESS	Put NFT for sale(alice & bob)
# 		Check user balance
#		Check receiver balance
# FAIl		NFT you don't own for sale
# 		Check user balance
# SUCCESS	Buy token
# 		Check buyer balance
#		Check seller balance
# FAIL		Remove bought NFT from sale
# 		Check seller NFT balance
# FAIL		Remove not owned NFT from sale (NFT is in sale)
# 		Check seller NFT balance


###		Auction
# SUCCESS	Place NFT for auction x 2
# 		Check all data + owner and contract balance
# FAIL		Place NFT you don't own in auction
# 		Check balances
# FAIL		Bid on sale that hasn't started
# FAIL		Bid lower than current price
# SUCCESS	Bid on sale x2
# 		Check highest bid is correct
# 		Check balances between each bid
# SUCCESS	Check end of auction (succeeded)
#		Check balance of contract , buyer
# SUCCESS	Check end of auction (succeeded)
#		Check balance of contract , buyer, seller

###		Passive
# SUCCESS	List NFT
#		Check buyer balance
# FAIL		List NFT already on sale
# FAIL		List own NFT (why would anyone do this though ?)
# SUCCESS	Accept offer
#		Check balances and NFT owner
# SUCCESS	Reject offer
#		Chck balances and NFT owner
# FAIL 		Accept inexistant offer
# FAIL 		Reject inexistant offer

### Safety tests ?
# Don't know about those, research ?
