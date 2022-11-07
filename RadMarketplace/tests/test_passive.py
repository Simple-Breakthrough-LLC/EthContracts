import pytest
from brownie import accounts, reverts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def setAra(marketplace, nft):
    marketplace.setARA(nft.address)


# TODO: Fails with "Only offer creator can cancel offer" but should not
def test_passive_offer(marketplace, nft_contract, bob):
    nft_id = 1
    price = 1
    bob_balance = bob.balance()
    market_balance = marketplace.balance()

    assert bob_balance >= price
    offer = marketplace.createPassiveOffer(nft_contract.address, nft_id, price, {"from": bob, "value": price})
    assert bob.balance() == bob_balance - price
    assert marketplace.balance() == market_balance + price

    v = marketplace.cancelOffer(offer.return_value, {"from": bob})
    # assert v.return_value == bob.address


def test_invalid_passive_offer(marketplace, nft_contract, bob):
    nft_id = 1
    bob_balance = bob.balance()
    price = bob_balance + 1

    with reverts("Insufficient funds"):
        marketplace.createPassiveOffer(nft_contract, nft_id, price, {"from": bob, "value": bob_balance})

    assert bob.balance() == bob_balance


# TODO: Fails with "rever" but should not
def test_reject_valid_offer(marketplace, nft_contract, bob, alice):
    nft_id = 1
    price = 1
    bob_balance = bob.balance()
    market_balance = marketplace.balance()

    assert bob_balance >= price
    offer = marketplace.createPassiveOffer(nft_contract, nft_id, price, {"from": bob, "value": price})
    assert bob.balance() == bob_balance - price
    assert marketplace.balance() == market_balance + price

    marketplace.rejectOffer(offer.return_value, {"from": alice})


# TODO: Fails with "rever" but should not
def test_accept_offer(marketplace, nft_contract, bob, alice):
    nft_id = 1
    price = 1

    setAra(marketplace, nft_contract)
    offer = marketplace.createPassiveOffer(nft_contract, nft_id, price, {"from": bob, "value": price})

    marketplace.acceptOffer(offer.return_value, {"from": alice})


###		Passive
# SUCCESS	List NFT
# 		Check buyer balance
# FAIL		List NFT already on sale
# FAIL		List own NFT (why would anyone do this though ?)
# SUCCESS	Accept offer
# 		Check balances and NFT owner
# SUCCESS	Reject offer
# 		Chck balances and NFT owner
# FAIL 		Accept inexistant offer
# FAIL 		Reject inexistant offer

### Safety tests ?
# Don't know about those, research ?
