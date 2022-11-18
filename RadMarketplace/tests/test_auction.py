import time

import pytest
import math
from brownie import chain, reverts
from conftest import get_fees


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass



def test_create_auction(marketplace, nft_contract, alice, bob):
    nft_id, price, duration = 1, 1, 100
    start_time = chain.time() - 10

    assert nft_contract.ownerOf(nft_id) == alice.address
    auction = marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})

    assert nft_contract.ownerOf(nft_id) == marketplace.address
    marketplace.bidAuction(auction.return_value, {"from": bob, "value": price})


def test_invalid_create_auction(marketplace, nft_contract, alice, bob):
    nft_id, price, duration = 2, 1, 100
    start_time = chain.time()

    assert nft_contract.ownerOf(nft_id) == bob.address
    print(f"OWNER = {nft_contract.ownerOf(nft_id)} {nft_contract.ownerOf(nft_id) == bob.address}")

    with reverts("ERC721: transfer from incorrect owner"):
        marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})

    assert nft_contract.ownerOf(nft_id) == bob.address


def test_invalid_auction_bid(marketplace):
    auction_id = 10

    with reverts("Auction does not exist or has ended"):
        marketplace.bidAuction(auction_id)


def test_invalid_bid_auction(marketplace, nft_contract, alice, bob, carol):
    nft_id, price, duration = 1, 1, 100
    start_time = chain.time()
    auction = marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})

    bob_balance = bob.balance()
    market_balance = marketplace.balance()
    time.sleep(0.2)
    marketplace.bidAuction(auction.return_value, {"from": carol, "value": price})

    with reverts("New bid should be higher than current one."):
        marketplace.bidAuction(auction.return_value, {"from": bob, "value": price - 1})
    assert bob.balance() == bob_balance
    assert marketplace.balance() == market_balance + price


def test_bid_future_auction(marketplace, nft_contract, alice, bob):
    nft_id, price, duration = 1, 1, 100
    start_time = chain.time() + 7200  # 7200 is 2 hours in seconds
    auction = marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})
    with reverts("Auction has not started"):
        marketplace.bidAuction(auction.return_value, {"from": bob, "value": price})


def test_bid_ended_auction(marketplace, nft_contract, alice, bob):
    nft_id, price, duration = 1, 1, 1
    start_time = chain.time() - 7200  # 7200 is 2 hours in seconds
    auction = marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})

    with reverts("Auction has ended"):
        marketplace.bidAuction(auction.return_value, {"from": bob, "value": price})


def test_bid_auction(marketplace, nft_contract, alice, bob, carol):
    nft_id, price, duration = 1, 1, 100
    start_time = chain.time()
    auction = marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})

    bob_balance = bob.balance()
    market_balance = marketplace.balance()

    time.sleep(0.2)
    marketplace.bidAuction(auction.return_value, {"from": bob, "value": price})
    assert bob.balance() == bob_balance - price
    assert marketplace.balance() == market_balance + price

    with reverts("New bid should be higher than current one."):
        marketplace.bidAuction(auction.return_value, {"from": carol, "value": price})


def test_redeem_auction(marketplace, nft_contract, alice, bob, royaltyRecipient, e20, wallet):
    nft_id, price, duration = 1, 10, 2
    start_time = chain.time() - 1
    auction = marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})
    alice_balance = alice.balance()
    bob_balance = bob.balance()
    market_balance = marketplace.balance()
    wallet_balance = wallet.balance()
    royalty_balance = royaltyRecipient.balance()

    marketplace.bidAuction(auction.return_value, {"from": bob, "value": price})
    assert bob.balance() == bob_balance - price
    assert nft_contract.ownerOf(nft_id) == marketplace

    time.sleep(duration)
    marketplace.redeemAuction(auction.return_value, {"from": bob})
    adjustedPrice, marketFee, royalties = get_fees(nft_id, price, marketplace, nft_contract, alice, e20)
    print(f"original {price}, adjusted {adjustedPrice}, market fee {marketFee}, royalties {royalties}, alice balance {alice_balance}" )
    assert alice.balance() == alice_balance +  math.ceil(adjustedPrice)
    assert marketplace.balance() == market_balance
    assert wallet.balance() == wallet_balance + marketFee
    assert royaltyRecipient.balance() == royalty_balance + royalties
    assert nft_contract.ownerOf(nft_id) == bob


def test_redeem_auction_lower_bid(marketplace, nft_contract, alice, bob, carol):
    nft_id, price, duration = 1, 2, 2
    start_time = chain.time()
    auction = marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})
    bob_balance = bob.balance()
    carol_balance = carol.balance()

    marketplace.bidAuction(auction.return_value, {"from": carol, "value": price - 1})
    marketplace.bidAuction(auction.return_value, {"from": bob, "value": price})

    time.sleep(duration)
    with reverts("Only highest bidder can redeem NFT"):
        marketplace.redeemAuction(auction.return_value, {"from": carol})

    assert bob.balance() == bob_balance - price
    assert carol.balance() == carol_balance
    assert nft_contract.ownerOf(nft_id) == marketplace


def test_redeem_auction_lower_price(marketplace, nft_contract, alice, bob):
    nft_id, price, duration = 1, 2, 2
    start_time = chain.time()
    auction = marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})

    marketplace.bidAuction(auction.return_value, {"from": bob, "value": price - 1})

    time.sleep(duration)
    with reverts("Highest bid is lower than asking price"):
        marketplace.redeemAuction(auction.return_value, {"from": bob})


def test_redeem_ongoing_auction(marketplace, nft_contract, alice, bob):
    nft_id, price, duration = 1, 1, 3600
    start_time = chain.time() - 2600
    auction = marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})

    marketplace.bidAuction(auction.return_value, {"from": bob, "value": price + 1})
    marketplace_balance = marketplace.balance()

    with reverts("Auction still in progress"):
        marketplace.redeemAuction(auction.return_value, {"from": bob})

    assert marketplace.balance() == marketplace_balance
    assert nft_contract.ownerOf(nft_id) == marketplace


def test_redeem_invalid_auction(marketplace, nft_contract, alice, bob):
    nft_id, price, duration = 1, 1, 10
    start_time = chain.time()
    marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})

    with reverts("Auction does not exist or has ended"):
        marketplace.redeemAuction(123, {"from": bob})

    assert nft_contract.ownerOf(nft_id) == marketplace

def test_end_auction_fail(marketplace, nft_contract, alice, bob, carol):
    nft_id, price, duration = 1, 10, 5
    start_time = chain.time() - 1
    auction = marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})
    bob_balance = bob.balance()

    marketplace.bidAuction(auction.return_value, {"from": bob, "value": price // 2})
    assert bob.balance() == (bob_balance - (price // 2))
    assert nft_contract.ownerOf(nft_id) == marketplace

    with reverts("Auction does not exist"):
        marketplace.endAuction(12)
    with reverts("Auction still in progress"):
        marketplace.endAuction(auction.return_value, {"from": alice})
    with reverts("Only nft owner, contract owner or bidder can end the auction"):
        marketplace.endAuction(auction.return_value, {"from": carol})

    marketplace.bidAuction(auction.return_value, {"from": bob, "value": price})
    assert bob.balance() == bob_balance - price

    time.sleep(duration)

    with reverts("Cannot end auction whose bid has met the asking price"):
        marketplace.endAuction(auction.return_value, {"from": alice})




def test_end_auction(marketplace, nft_contract, alice, bob):
    nft_id, price, duration = 1, 10, 2
    start_time = chain.time() - 1
    auction = marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})
    bob_balance = bob.balance()

    marketplace.bidAuction(auction.return_value, {"from": bob, "value": price // 2})
    assert bob.balance() == (bob_balance - (price // 2))
    assert nft_contract.ownerOf(nft_id) == marketplace

    time.sleep(duration)

    marketplace.endAuction(auction.return_value, {"from": alice})
    assert nft_contract.ownerOf(nft_id) == alice
    assert bob.balance() == bob_balance
