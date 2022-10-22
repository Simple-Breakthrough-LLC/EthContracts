import pytest
from brownie import TokenSaleToken, GenericERC20,  accounts


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
def tokenSale(deployer):
	return  deployer.deploy(GenericERC20)


@pytest.fixture(scope="module", autouse=True)
def sale(deployer, alice, tokenSale):
	contract =  deployer.deploy(TokenSaleToken, tokenSale, 10)
	contract.setSaleSupply(9)
	contract.setPrice(1)
	tokenSale.approve(contract.address, 10)
	return contract



