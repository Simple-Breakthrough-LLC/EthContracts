import pytest

from brownie import accounts, reverts

@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

def test_mint(alice, soulbound):
	soulbound.mint(alice)
	assert(soulbound.ownerOf(0) == alice)
	with reverts():
		soulbound.mint(alice)
	assert(soulbound.balanceOf(alice) == 2)

def test_transfer(alice, bob, soulbound):
	with reverts():
		soulbound.transferFrom(alice, bob, 0, {"from" : alice})
	with reverts():
		soulbound.safeTransferFrom(alice, bob, 0, {"from" : alice})
