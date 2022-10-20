import pytest
from brownie import DistributedRoyaltiesNFTDrop, GenericERC20, accounts


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
def david():
    return accounts[4]

@pytest.fixture(scope="module", autouse=True)
def tok(deployer, alice):
	contract = deployer.deploy(GenericERC20)
	contract.mint(alice, 50)
	return contract


@pytest.fixture(scope="module", autouse=True)
def nft(deployer, tok, alice):
	contract = deployer.deploy(BurnableLimitedNFT, "name", "symbol", "uri", 10, 10, 5, tok.address)
	tok.approve(contract.address, 1000, {"from": alice})
	return contract
