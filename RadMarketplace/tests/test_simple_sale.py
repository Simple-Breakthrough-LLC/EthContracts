import pytest
from brownie import accounts, reverts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


##		 Simple Sale
# SUCCESS	Put NFT for sale(alice & bob)
# 		Check user balance
# 		Check receiver balance

def setAra(marketplace, nft):
	marketplace.setARA(nft.address)

def test_sale(marketplace, nft721, alice):
    token_id = 1
    price = 5

    assert nft721.ownerOf(token_id) == alice.address

    marketplace.createSimpleOffer(nft721, token_id, price, {"from": alice})

    assert nft721.ownerOf(token_id) != alice.address
    assert nft721.ownerOf(token_id) == marketplace.address


# FAIl		NFT you don't own for sale
# 		Check user balance
def test_invalid_sale(marketplace, nft721, alice):
    token_id = 2
    price = 5

    assert nft721.ownerOf(token_id) != alice.address
    with reverts("ERC721: transfer of token that is not own"):
        marketplace.createSimpleOffer(nft721, token_id, price, {"from": alice})
    assert nft721.ownerOf(token_id) != marketplace.address


# SUCCESS	Buy token
# 		Check buyer balance
# 		Check seller balance
def test_buy_token(marketplace, nft721, alice, bob):
    token_id = 1
    price = 5
    bobBalance = bob.balance()
    assert bobBalance >= price

    setAra(marketplace, nft721)
    s = marketplace.createSimpleOffer(nft721, token_id, price, {"from": alice})
    marketplace.buySimpleOffer(s.return_value, {"from": bob, "value": price})

    assert bob.balance() == bobBalance - price
    assert nft721.ownerOf(token_id) == bob.address


# FAIL		Remove bought NFT from sale
# 		Check seller NFT balance
def test_remove_offer(marketplace, nft721, alice):
    token_id = 1
    price = 1

    sale = marketplace.createSimpleOffer(nft721, token_id, price, {"from": alice})
    marketplace.removeSimpleOffer(sale.return_value, {"from": alice})

    assert nft721.ownerOf(token_id) == alice.address
    assert nft721.ownerOf(token_id) != marketplace.address


# FAIL		Remove not owned NFT from sale (NFT is in sale)
# 		Check seller NFT balance
def test_invalid_remove_offer(marketplace, nft721, alice, bob):
    token_id = 1
    price = 1

    sale = marketplace.createSimpleOffer(nft721, token_id, price, {"from": alice})
    with reverts("You are not the creator of this sale"):
        marketplace.removeSimpleOffer(sale.return_value, {"from": bob})

    assert nft721.ownerOf(token_id) != alice.address
    assert nft721.ownerOf(token_id) != bob.address
    assert nft721.ownerOf(token_id) == marketplace.address


# SUCCESS	Update NFT for sale
def test_update_sale(marketplace, nft721, alice):
    token_id = 1
    price = 5
    new_price = 50

    assert nft721.ownerOf(token_id) == alice.address
    sale = marketplace.createSimpleOffer(nft721, token_id, price, {"from": alice})
    assert nft721.ownerOf(token_id) != alice.address
    assert nft721.ownerOf(token_id) == marketplace.address

    marketplace.updateSimpleOffer(sale.return_value, new_price, {"from": alice})


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
