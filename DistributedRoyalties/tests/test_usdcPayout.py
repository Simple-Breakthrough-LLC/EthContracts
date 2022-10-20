import pytest

from brownie import accounts, reverts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

# mint
# Check erc20 transfer works
# check user has nft

def test_E20mint(tok, nft, alice):
	amount = 3
	aliceBal = tok.balanceOf(alice)
	assert(aliceBal >= (nft.currentPrice() * amount))
	nft.mint(amount, {"from": alice})
	assert(tok.balanceOf(alice) == aliceBal - (nft.currentPrice() * amount))
	assert(nft.balanceOf(alice) == amount)



# Set payout FAIL
#  send more than 5
#  send none
#  send address len not same as percent len
#  send total shares over 100
#  send total shares under 100

def test_E20setPayout(nft, bob, carol, david):
	with reverts():
		nft.setPayout([bob, carol, david, bob, bob, bob, bob], [10, 10, 10, 10, 10, 10])
	with reverts():
		nft.setPayout([], [])
	with reverts():
		nft.setPayout([bob, carol, david], [50, 50])
	with reverts():
		nft.setPayout([bob, carol], [90, 20])
	with reverts():
		nft.setPayout([bob, carol], [50, 10])


# Set payout PASS
#  set bob, carol, david // 25 25 50
#  check payout valid

def test_E20payout(tok, nft, bob, carol, david):

	def calcShares(total, share):
		return ((share * total) / 100)

	balance = tok.balanceOf(nft.address)
	bobBalance = tok.balanceOf(bob.address)
	carolBalance = tok.balanceOf(carol.address)
	davidBalance = tok.balanceOf(david.address)

	nft.setPayout([bob, carol, david], [25, 25, 50])

	nft.withdraw()

	assert(tok.balanceOf(bob.address) == bobBalance + (calcShares(balance, 25)))
	assert(tok.balanceOf(carol.address) == carolBalance + (calcShares(balance, 25)))
	assert(tok.balanceOf(david.address) == davidBalance + (calcShares(balance, 50)))

def test_E20payout2(tok, nft, bob, carol, david):

	def calcShares(total, share):
		return ((share * total) / 100)

	balance = tok.balanceOf(nft.address)
	bobBalance = tok.balanceOf(bob.address)
	carolBalance = tok.balanceOf(carol.address)
	davidBalance = tok.balanceOf(david.address)

	nft.setPayout([bob, carol, david], [10, 60, 30])

	nft.withdraw()

	assert(tok.balanceOf(bob.address) == bobBalance + (calcShares(balance, 25)))
	assert(tok.balanceOf(carol.address) == carolBalance + (calcShares(balance, 25)))
	assert(tok.balanceOf(david.address) == davidBalance + (calcShares(balance, 50)))


# CONTRACT WITH ETH

def test_ETHmint(tok, eth, alice):
	amount = 3
	aliceBal = alice.balance()

	assert(aliceBal >= (eth.currentPrice() * amount))
	with reverts("Balance insufficient to complete purchase"):
		eth.mint(amount, {"from": alice.address, "value": 0})
	eth.mint(amount, {"from": alice.address, "value": eth.currentPrice() * amount})
	assert(alice.balance() == aliceBal - (eth.currentPrice() * amount))
	assert(eth.balanceOf(alice) == amount)



# Set payout FAIL
#  send more than 5
#  send none
#  send address len not same as percent len
#  send total shares over 100
#  send total shares under 100

def test_ETHsetPayout(eth, bob, carol, david):
	with reverts():
		eth.setPayout([bob, carol, david, bob, bob, bob, bob], [10, 10, 10, 10, 10, 10])
	with reverts():
		eth.setPayout([], [])
	with reverts():
		eth.setPayout([bob, carol, david], [50, 50])
	with reverts():
		eth.setPayout([bob, carol], [90, 20])
	with reverts():
		eth.setPayout([bob, carol], [50, 10])


# Set payout PASS
#  set bob, carol, david // 25 25 50
#  check payout valid

def test_ETHpayout(tok, eth, bob, carol, david):

	def calcShares(total, share):
		return ((share * total) / 100)

	balance = eth.balance()
	bobBalance = bob.balance()
	carolBalance = carol.balance()
	davidBalance = david.balance()

	eth.setPayout([bob, carol, david], [25, 25, 50])

	eth.withdraw()

	assert(bob.balance() == bobBalance + (calcShares(balance, 25)))
	assert(carol.balance() == carolBalance + (calcShares(balance, 25)))
	assert(david.balance() == davidBalance + (calcShares(balance, 50)))

def test_ETHpayout2(tok, eth, bob, carol, david):

	def calcShares(total, share):
		return ((share * total) / 100)

	balance = eth.balance()
	bobBalance = bob.balance()
	carolBalance = carol.balance()
	davidBalance = david.balance()

	eth.setPayout([bob, carol, david], [10, 60, 30])

	eth.withdraw()

	assert(bob.balance() == bobBalance + (calcShares(balance, 25)))
	assert(carol.balance() == carolBalance + (calcShares(balance, 25)))
	assert(david.balance() == davidBalance + (calcShares(balance, 50)))
