import datetime
import time

import pytest
from brownie import accounts, chain, reverts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def setAra(marketplace, nft):
    marketplace.setARA(nft.address)


def test_create_auction(marketplace, nft_contract, alice, bob):
    nft_id, price, duration = 1, 1, 100
    start_time = chain.time() - 10

    print(f"start_time = {start_time}")
    assert nft_contract.ownerOf(nft_id) == alice.address
    auction = marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})
    auction_start, dur, ts = auction.return_value

    print(f"Auction_start = {auction_start}")
    print(f"Auction dur = {dur}")
    print(f"block.timestamp = {ts}")
    # print(f"block.timestamp = {auction.return_value}")
    # print(f"{start_time > auction.return_value}")

    assert nft_contract.ownerOf(nft_id) == marketplace.address
    bid = marketplace.bidAuction(1, {"from": bob, "value": price})
    print(f"bid_time = {bid.return_value}")


# def test_invalid_create_auction(marketplace, nft_contract, alice, bob):
#     nft_id, price, duration = 2, 1, 100
#     start_time = chain.time()

#     assert nft_contract.ownerOf(nft_id) == bob.address

#     with reverts("ERC721: transfer of token that is not own"):
#         marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})

#     assert nft_contract.ownerOf(nft_id) == bob.address


# def test_invalid_auction_bid(marketplace):
#     auction_id = 10

#     with reverts("Auction does not exist or has ended"):
#         marketplace.bidAuction(auction_id)


# def test_invalid_bid_auction(marketplace, nft_contract, alice, bob):
#     nft_id, price, duration = 1, 1, 100
#     start_time = chain.time()
#     auction = marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})

#     bob_balance = bob.balance()
#     market_balance = marketplace.balance()
#     with reverts("Auction does not exist or has ended"):
#         marketplace.bidAuction(42, {"from": bob, "value": price - 1})
#     with reverts("New bid should be higher than current one."):
#         marketplace.bidAuction(auction.return_value, {"from": bob, "value": price - 1})
#     assert bob_balance == bob.balance()
#     assert market_balance == marketplace.balance()


# def test_bid_future_auction(marketplace, nft_contract, alice, bob):
#     nft_id, price, duration = 1, 1, 100
#     start_time = chain.time() + 7200  #7200 is 2 hours in seconds
#     auction = marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})
#     with reverts("Auction has not started"):
#         marketplace.bidAuction(auction.return_value, {"from": bob, "value": price})


# def test_bid_ended_auction(marketplace, nft_contract, alice, bob):
#     nft_id, price, duration = 1, 1, 1
#     start_time = chain.time() - 7200  #7200 is 2 hours in seconds
#     auction = marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})

#     with reverts("Auction has ended"):
#         marketplace.bidAuction(auction.return_value, {"from": bob, "value": price})


# def test_bid_auction(marketplace, nft_contract, alice, bob, carol):
#     nft_id, price, duration = 1, 1, 100
#     start_time = chain.time()
#     auction = marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})

#     bob_balance = bob.balance()
#     market_balance = marketplace.balance()

#     marketplace.bidAuction(auction.return_value, {"from": bob, "value": price})
#     assert bob.balance() == bob_balance - price
#     assert marketplace.balance() == market_balance + price

#     with reverts("New bid should be higher than current one."):
#         marketplace.bidAuction(auction.return_value, {"from": carol, "value": price})


# def test_redeem_auction(marketplace, nft_contract, alice, bob):
#     nft_id, price, duration = 1, 1, 10
#     start_time = chain.time()
#     auction = marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})
#     alice_balance = alice.balance()

#     setAra(marketplace, nft_contract)
#     marketplace.bidAuction(auction.return_value, {"from": bob, "value": price})
#     market_balance = marketplace.balance()

#     assert nft_contract.ownerOf(nft_id) == marketplace
#     assert nft_contract.ownerOf(nft_id) != bob

#     marketplace.redeemAuction(auction.return_value, {"from": bob})

#     assert alice.balance() == alice_balance + price
#     assert marketplace.balance() == market_balance - price
#     assert nft_contract.ownerOf(nft_id) != marketplace
#     assert nft_contract.ownerOf(nft_id) == bob


# def test_redeem_auction_lower_bid(marketplace, nft_contract, alice, bob, carol):
#     nft_id, price, duration = 1, 2, 10
#     start_time = chain.time()
#     auction = marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})
#     bob_balance = bob.balance()
#     carol_balance = carol.balance()

#     setAra(marketplace, nft_contract)
#     marketplace.bidAuction(auction.return_value, {"from": carol, "value": price - 1})
#     marketplace.bidAuction(auction.return_value, {"from": bob, "value": price})

#     with reverts("Only highest bidder can redeem NFT"):
#         marketplace.redeemAuction(auction.return_value, {"from": carol})

#     assert bob.balance() == bob_balance - price
#     assert carol.balance() == carol_balance
#     assert nft_contract.ownerOf(nft_id) != bob
#     assert nft_contract.ownerOf(nft_id) != carol
#     assert nft_contract.ownerOf(nft_id) == marketplace


# def test_redeem_auction_lower_price(marketplace, nft_contract, alice, bob):
#     nft_id, price, duration = 1, 2, 10
#     start_time = chain.time()
#     auction = marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})
#     setAra(marketplace, nft_contract)

#     marketplace.bidAuction(auction.return_value, {"from": bob, "value": price - 1})

#     with reverts("Highest bid is lower than asking price"):
#         marketplace.redeemAuction(auction.return_value, {"from": bob})

# # def test_redeem_ongoing_auction(marketplace, nft_contract, alice, bob):
# #     nft_id, price, duration = 1, 1, 100
# #     start_time = chain.time() - 600
# #     print(f"CHAIN TIME {start_time}")
# #     auction = marketplace.createAuction(nft_contract, nft_id, price, start_time, duration, {"from": alice})
# #     setAra(marketplace, nft_contract)

# #     bid = marketplace.bidAuction(auction.return_value, {"from": bob, "value": price + 1})
# #     time.sleep(duration)
# #     print(f"HERE! BID  {bid.return_value} auctionId = {auction.return_value}")

# #     with reverts("Auction still in progress"):
# #         val = marketplace.redeemAuction(auction.return_value, {"from": bob})
# #         print(f"HERE! BID  {val.return_value} auctionId = {auction.return_value}")
# #     assert 1 == 2

# ###		Auction
# # SUCCESS	Place NFT for auction x 2
# # 		Check all data + owner and contract balance
# # FAIL		Place NFT you don't own in auction
# # 		Check balances
# # FAIL		Bid on sale that hasn't started
# # FAIL		Bid lower than current price
# # SUCCESS	Bid on sale x2
# # 		Check highest bid is correct
# # 		Check balances between each bid
# # SUCCESS	Check end of auction (succeeded)
# # 		Check balance of contract , buyer
# # SUCCESS	Check end of auction (succeeded)
# # 		Check balance of contract , buyer, seller
