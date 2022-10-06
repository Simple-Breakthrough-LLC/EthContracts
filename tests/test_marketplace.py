import pytest

from brownie import accounts, reverts

@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

def test_listFailing(alice, marketplace, token):
	# marketplace.createMarketItem(token, id, price, amount)
	with reverts():
		marketplace.createMarketItem(token, 1, 1, 0, {"from": alice})
	with reverts():
		marketplace.createMarketItem(token, 1, 1, 43,{"from": alice})
	with reverts():
		marketplace.createMarketItem(token, 1, 0, 1,{"from": alice})
	assert(marketplace.fetchMarketItems() == ())

# buy more than available
# buy 0
# buy more than you can afford


# Passing tests

def test_listItems(alice, marketplace, token):
		marketplace.createMarketItem(token, 1, 1, 1, {"from": alice})
		assert(marketplace.fetchMarketItems() == ((1, 1, 1, 1, token.address, alice.address),))
		marketplace.createMarketItem(token, 1, 1, 3, {"from": alice})
		assert(token.balanceOf(alice, 1) == 38)

# correct listing 1 / 1
#  Check fetch items

# correct listing 1/ X
#  Check fetch items

# correct listing X / X
#  Check fetch items

# buy 1
# buy all
# check fetch items
# def test_buyItems(alice, bob, marketplace, token):
# 	nftPrice = 1
# 	amoutnBought = 3
# 	totalAmount = 5

# 	marketplace.createMarketItem(token, 1, nftPrice, totalAmount, {"from": alice})

# 	abalance = alice.balance
# 	bbalance = bob.balance

# 	marketplace.createMarketSale(token, 1, amoutnBought, {"from":bob})
# 	assert(marketplace.fetchMarketItems() == ())
# 	assert(token.balanceOf(bob, 1) == 2)
# 	assert(alice.balance() == (abalance + (nftPrice * amoutnBought)) )
# 	assert(bob.balance() == (bbalance - (nftPrice * amoutnBought)) )










