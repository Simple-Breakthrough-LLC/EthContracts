import pytest

from brownie import accounts, reverts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

# mint
# Check erc20 transfer works
# check user has nft

def test_mint(tok, nft, alice):
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

def test_setPayout(nft, bob, carol, david):
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

def test_payout(tok, nft, bob, carol, david):

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

def test_payout2(tok, nft, bob, carol, david):

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
