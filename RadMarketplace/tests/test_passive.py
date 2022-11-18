import pytest
import  math
from brownie import reverts
from conftest import get_fees


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def setAra(marketplace, nft):
    marketplace.setARA(nft.address)


def test_passive_offer(marketplace, nft_contract, bob):
    nft_id = 1
    price = 1
    bob_balance = bob.balance()
    market_balance = marketplace.balance()

    assert bob_balance >= price
    offer = marketplace.createPassiveOffer(nft_contract.address, nft_id, price, {"from": bob, "value": price})
    assert bob.balance() == bob_balance - price
    assert marketplace.balance() == market_balance + price

    marketplace.cancelOffer(offer.return_value, {"from": bob})
    with reverts("Offer does not exist or has ended"):
        marketplace.cancelOffer(offer.return_value, {"from": bob})


def test_invalid_passive_offer(marketplace, nft_contract, bob):
    nft_id = 1
    bob_balance = bob.balance()
    price = bob_balance + 1

    with reverts("Insufficient funds"):
        marketplace.createPassiveOffer(nft_contract, nft_id, price, {"from": bob, "value": bob_balance})

    assert bob.balance() == bob_balance


def test_reject_valid_offer(marketplace, nft_contract, bob, alice):
    nft_id, price = 1, 1
    bob_balance = bob.balance()
    market_balance = marketplace.balance()

    assert bob_balance >= price
    offer = marketplace.createPassiveOffer(nft_contract, nft_id, price, {"from": bob, "value": price})
    assert bob.balance() == bob_balance - price
    assert marketplace.balance() == market_balance + price

    marketplace.rejectOffer(offer.return_value, {"from": alice})
    with reverts("Offer does not exist or has ended"):
        marketplace.rejectOffer(offer.return_value, {"from": alice})


def test_accept_offer(marketplace, nft_contract, bob, alice, royaltyRecipient, e20, wallet):
    nft_id, price = 1, 10
    alice_balance = alice.balance()
    bob_balance = bob.balance()
    market_balance = marketplace.balance()
    royalty_balance = royaltyRecipient.balance()
    wallet_balance = wallet.balance()


    setAra(marketplace, nft_contract)
    offer = marketplace.createPassiveOffer(nft_contract, nft_id, price, {"from": bob, "value": price})

    assert bob.balance() == bob_balance - price

    marketplace.acceptOffer(offer.return_value, {"from": alice})
    adjustedPrice, marketFee, royalties = get_fees(nft_id, price, marketplace, nft_contract, alice, e20)
    assert marketplace.balance() == market_balance + marketFee
    assert wallet.balance() == wallet_balance + marketFee
    assert royaltyRecipient.balance() == royalty_balance + royalties
    assert nft_contract.ownerOf(nft_id) == bob.address
    assert alice.balance() == alice_balance +  math.ceil(adjustedPrice)


def test_accept_invalid_offer(marketplace, nft_contract, bob, alice):
    nft_id, price = 1, 1

    marketplace.createPassiveOffer(nft_contract, nft_id, price, {"from": bob, "value": price})

    with reverts("Offer does not exist or has ended"):
        marketplace.acceptOffer(123, {"from": alice})

    assert nft_contract.ownerOf(nft_id) == alice


def test_accept_others_offer(marketplace, nft_contract, bob, alice, carol):
    nft_id, price = 1, 1

    offer = marketplace.createPassiveOffer(nft_contract, nft_id, price, {"from": bob, "value": price})

    with reverts("Only nft owner can accept offer"):
        marketplace.acceptOffer(offer.return_value, {"from": carol})
    assert nft_contract.ownerOf(nft_id) == alice.address


def test_reject_other_offer(marketplace, nft_contract, bob, alice):
    nft_id, price = 1, 1
    bob_balance = bob.balance()
    market_balance = marketplace.balance()

    offer = marketplace.createPassiveOffer(nft_contract, nft_id, price, {"from": bob, "value": price})

    with reverts("Only nft owner can cancel offer"):
        marketplace.rejectOffer(offer.return_value, {"from": bob})

    assert bob.balance() == bob_balance - 1
    assert marketplace.balance() == market_balance + price
    assert nft_contract.ownerOf(nft_id) == alice


def test_reject_invalid_offer(marketplace, nft_contract, bob, alice):
    nft_id, price = 1, 1

    marketplace.createPassiveOffer(nft_contract, nft_id, price, {"from": bob, "value": price})

    with reverts("Offer does not exist or has ended"):
        marketplace.rejectOffer(123, {"from": alice})


def test_cancel_offer(marketplace, nft_contract, bob):
    nft_id, price = 1, 1
    bob_balance = bob.balance()
    market_balance = marketplace.balance()

    offer = marketplace.createPassiveOffer(nft_contract.address, nft_id, price, {"from": bob, "value": price})

    assert bob.balance() == bob_balance - price
    assert marketplace.balance() == market_balance + price

    marketplace.cancelOffer(offer.return_value, {"from": bob})
    with reverts("Offer does not exist or has ended"):
        marketplace.cancelOffer(offer.return_value, {"from": bob})

    assert bob.balance() == bob_balance
    assert marketplace.balance() == market_balance


def test_cancel_others_offer(marketplace, nft_contract, bob, carol):
    nft_id, price = 1, 1

    offer = marketplace.createPassiveOffer(nft_contract.address, nft_id, price, {"from": bob, "value": price})

    with reverts("Only offer creator can cancel offer"):
        marketplace.cancelOffer(offer.return_value, {"from": carol})


def test_cancel_invalid_offer(marketplace, nft_contract, bob):
    nft_id, price = 1, 1

    marketplace.createPassiveOffer(nft_contract.address, nft_id, price, {"from": bob, "value": price})

    with reverts("Offer does not exist or has ended"):
        marketplace.cancelOffer(123, {"from": bob})
