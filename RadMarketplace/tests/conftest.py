import pytest
from brownie import GenericERC20, GenericERC721, MarketPlace, accounts


@pytest.fixture(scope="module")
def deployer():
    return accounts[0]


@pytest.fixture(scope="module")
def alice():
    return accounts[1]


@pytest.fixture(scope="module")
def bob():
    return accounts[2]


@pytest.fixture(scope="module")
def carol():
    return accounts[3]


@pytest.fixture(scope="module")
def royaltyRecipient():
    return accounts[4]

@pytest.fixture(scope="module")
def wallet():
    return accounts[5]


@pytest.fixture(scope="module", autouse=True)
def nft_contract(deployer, alice, bob, royaltyRecipient, marketplace):
    contract = deployer.deploy(GenericERC721)
    contract.mint(alice, 1)
    contract.mint(bob, 2)

    contract.setRoyalties(royaltyRecipient, 5000)
    contract.setApprovalForAll(marketplace, True, {"from": alice})
    contract.setApprovalForAll(marketplace, True, {"from": bob})
    return contract


@pytest.fixture(scope="module", autouse=True)
def marketplace(deployer, wallet):
    market_fee = 1
    waiver = 11
    contract = deployer.deploy(MarketPlace, deployer.address, wallet.address, market_fee, waiver)
    return contract


@pytest.fixture(scope="module", autouse=True)
def e20(deployer, alice, marketplace):
    contract = deployer.deploy(GenericERC20)
    contract.mint(alice, 10)
    marketplace.setARA(contract.address)
    return contract


def get_fees(id, price, market, nft, seller, ara):
    marketFee = 0
    _, royalties = nft.royaltyInfo(id, price)

    if ara.balanceOf(seller) < market.waiver():
        marketFee = (market.marketPlaceFee() * price) / 100

    adjustedPrice = price - marketFee - royalties

    return (adjustedPrice, marketFee, royalties)
