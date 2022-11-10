import pytest
from brownie import GenericERC721, GenericERC20, MarketPlace, accounts


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
def marketplace(deployer):
    market_fee = 1
    waiver = 10
    return deployer.deploy(MarketPlace, deployer.address, market_fee, waiver)

@pytest.fixture(scope="module", autouse=True)
def e20(deployer, alice, marketplace):
	contract = deployer.deploy(GenericERC20)
	contract.mint(alice, 10)
	marketplace.setARA(contract.address)
	return contract
