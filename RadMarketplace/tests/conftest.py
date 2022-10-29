import pytest
from brownie import RadMarketPlace, NFT1155, NFT721, accounts


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

@pytest.fixture(scope="module", autouse=True)
def marketplace(deployer):
	return deployer.deploy(RadMarketPlace)
@pytest.fixture(scope="module", autouse=True)

def nft1155(deployer, alice, bob):
	contract = deployer.deploy(NFT1155)
	contract.mint(alice, 1)
	contract.mint(bob, 3)

def nft721(deployer, alice, bob):
	contract = deployer.deploy(NFT721)
	contract.mint(alice, 0, 10)
	contract.mint(bob, 1, 10)
