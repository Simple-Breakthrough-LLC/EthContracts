import datetime

import pytest
from brownie import accounts, reverts, chain


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def setAra(marketplace, nft):
    marketplace.setARA(nft.address)


def test_create_auction(marketplace, nft_contract, alice, bob):
    nft_id, price, duration = 1, 1, 100
    start_time = chain.time()

    assert nft_contract.ownerOf(nft_id) == alice.address
    auction = marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})
    assert nft_contract.ownerOf(nft_id) == marketplace.address
    marketplace.bidAuction(auction.return_value, {"from": bob, "value": price})


def test_invalid_create_auction(marketplace, nft_contract, alice, bob):
    nft_id, price, duration = 2, 1, 100
    start_time = chain.time()

    assert nft_contract.ownerOf(nft_id) == bob.address

    with reverts("ERC721: transfer of token that is not own"):
        marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})

    assert nft_contract.ownerOf(nft_id) == bob.address

# Probably not a usuful test, there's not really a problem with starting an auction in the past

# def test_invalid_date_auction(marketplace, nft_contract, alice, bob):
#     nft_id, price, duration = 1, 1, 100
#     start_time = int((datetime.datetime.now() - datetime.timedelta(days=1)).timestamp())

#     with reverts("Duration must be greater than 0"):
#         marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})


def test_invalid_auction_bid(marketplace):
    auction_id = 10

    with reverts("Auction does not exist or has ended"):
        marketplace.bidAuction(auction_id)


def test_invalid_bid_auction(marketplace, nft_contract, alice, bob):
    nft_id, price, duration = 1, 1, 100
    start_time = chain.time()
    auction = marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})

    bob_balance = bob.balance()
    market_balance = marketplace.balance()
    with reverts("Auction does not exist or has ended"):
        marketplace.bidAuction(42, {"from": bob, "value": price - 1})
    with reverts("New bid should be higher than current one."):
        marketplace.bidAuction(auction.return_value, {"from": bob, "value": price - 1})
    assert bob_balance == bob.balance()
    assert market_balance == marketplace.balance()


# TODO: Should fail!
def test_bid_future_auction(marketplace, nft_contract, alice, bob):
    nft_id, price, duration = 1, 1, 100
    start_time = chain.time() + 7200  #7200 is 2 hours in seconds
    auction = marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})
    with reverts("Auction has not started"):
        marketplace.bidAuction(auction.return_value, {"from": bob, "value": price})


def test_bid_auction(marketplace, nft_contract, alice, bob, carol):
    nft_id, price, duration = 1, 1, 100
    start_time = chain.time()
    auction = marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})

    bob_balance = bob.balance()
    market_balance = marketplace.balance()

    marketplace.bidAuction(auction.return_value, {"from": bob, "value": price})
    assert bob.balance() == bob_balance - price
    assert marketplace.balance() == market_balance + price

    with reverts("New bid should be higher than current one."):
        marketplace.bidAuction(auction.return_value, {"from": carol, "value": price})


def test_redeem_auction(marketplace, nft_contract, alice, bob):
    nft_id, price, duration = 1, 1, 10
    start_time = chain.time()
    auction = marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})
    alice_balance = alice.balance()

    setAra(marketplace, nft_contract)
    marketplace.bidAuction(auction.return_value, {"from": bob, "value": price})
    market_balance = marketplace.balance()

    assert nft_contract.ownerOf(nft_id) == marketplace
    assert nft_contract.ownerOf(nft_id) != bob

    marketplace.redeemAuction(auction.return_value, {"from": bob})

    assert alice.balance() == alice_balance + price
    assert marketplace.balance() == market_balance - price
    assert nft_contract.ownerOf(nft_id) != marketplace
    assert nft_contract.ownerOf(nft_id) == bob


def test_redeem_auction_lower_bid(marketplace, nft_contract, alice, bob, carol):
    nft_id, price, duration = 1, 2, 10
    start_time = chain.time()
    auction = marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})
    bob_balance = bob.balance()
    carol_balance = carol.balance()

    setAra(marketplace, nft_contract)
    marketplace.bidAuction(auction.return_value, {"from": carol, "value": price - 1})
    marketplace.bidAuction(auction.return_value, {"from": bob, "value": price})

    with reverts("Only highest bidder can redeem NFT"):
        marketplace.redeemAuction(auction.return_value, {"from": carol})

    assert bob.balance() == bob_balance - price
    assert carol.balance() == carol_balance
    assert nft_contract.ownerOf(nft_id) != bob
    assert nft_contract.ownerOf(nft_id) != carol
    assert nft_contract.ownerOf(nft_id) == marketplace


def test_redeem_auction_lower_price(marketplace, nft_contract, alice, bob):
    nft_id, price, duration = 1, 2, 10
    start_time = chain.time()
    auction = marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})
    setAra(marketplace, nft_contract)

    marketplace.bidAuction(auction.return_value, {"from": bob, "value": price - 1})

    with reverts("Highest bid is lower than asking price"):
        marketplace.redeemAuction(auction.return_value, {"from": bob})


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
# 		Check balance of contract , buyer
# SUCCESS	Check end of auction (succeeded)
# 		Check balance of contract , buyer, seller
