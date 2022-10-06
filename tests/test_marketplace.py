import pytest

from brownie import accounts, reverts

@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

def test_listFailing(alice, marketplace, token):
	with reverts():
		marketplace.createMarketItem(token, 1, 1, 0, {"from": alice})
	with reverts():
		marketplace.createMarketItem(token, 1, 1, 43,{"from": alice})
	with reverts():
		marketplace.createMarketItem(token, 1, 0, 1,{"from": alice})
	with reverts():
		marketplace.createMarketItem(token, 2, 1, 1,{"from": alice})
	assert(marketplace.fetchMarketItems() == ())


def test_listItems(alice, marketplace, token):
		marketplace.createMarketItem(token, 1, 1, 1, {"from": alice})
		assert(marketplace.fetchMarketItems() == ((1, 1, 1, 1, token.address, alice.address),))
		marketplace.createMarketItem(token, 1, 1, 3, {"from": alice})
		assert(token.balanceOf(alice, 1) == 38)

def test_buyItems(alice, bob, marketplace, token):
	nftPrice = 1
	amountBought = 3
	totalAmount = 5

	abalance = alice.balance()
	bbalance = bob.balance()

	marketplace.createMarketItem(token, 1, nftPrice, totalAmount, {"from": alice})
	assert(token.balanceOf(marketplace, 1) == 5)
	marketplace.createMarketSale(token, 1, amountBought, {"from":bob, "value": nftPrice * amountBought})
	assert(bob.balance() == (bbalance - (nftPrice * amountBought)))
	assert(token.balanceOf(bob, 1) == amountBought)
	assert(alice.balance() == (abalance + (nftPrice * amountBought)))

def test_buyAllItems(alice, bob, marketplace, token):
	nftPrice = 1
	totalAmount = 5
	amountBought = totalAmount

	marketplace.createMarketItem(token, 1, nftPrice, totalAmount, {"from": alice})
	assert(token.balanceOf(marketplace, 1) == 5)
	marketplace.createMarketSale(token, 1, amountBought, {"from":bob, "value": nftPrice * amountBought})
	assert(token.balanceOf(marketplace, 1) == 0)

	with reverts():
		marketplace.createMarketSale(token, 1, 1, {"from":bob, "value": nftPrice})
	assert(marketplace.fetchMarketItems() == ())


def test_buyFailing(alice, bob, marketplace, token):
	nftPriceLow = 1
	totalAmount = 5
	amountBought = totalAmount

	marketplace.createMarketItem(token, 1, nftPriceLow, totalAmount, {"from": alice})

	with reverts():
		marketplace.createMarketSale(token, 1, totalAmount * 3, {"from":bob, "value": totalAmount * 3})
	with reverts():
		marketplace.createMarketSale(token, 2, totalAmount * 3, {"from":bob, "value": totalAmount })
	with reverts():
		marketplace.createMarketSale(token, 1, 0, {"from":bob, "value": 0 })




