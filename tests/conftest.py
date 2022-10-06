import pytest
from brownie import marketPlaceBoilerPlate, GenericERC1155,  accounts


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
	return deployer.deploy(marketPlaceBoilerPlate)

@pytest.fixture(scope="module", autouse=True)
def token(deployer,marketplace, alice, bob):
	tok =  deployer.deploy(
		GenericERC1155
	)
	tok.mint(alice, 1, 42, "")
	tok.mint(bob, 2, 1, "")
	tok.setApprovalForAll(marketplace, True, {"from":alice})
	return tok

