import pytest
from brownie import SoulboundNFT, accounts


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
def soulbound(deployer, alice):
	contract = deployer.deploy(SoulboundNFT, "name", "symbol", "uri", 2)
	contract.mint(alice)
	contract.setApprovalForAll(alice, True)
	return contract
