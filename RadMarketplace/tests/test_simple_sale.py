import pytest
from brownie import accounts, reverts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def setAra(marketplace, nft):
    marketplace.setARA(nft.address)


##		 Simple Sale
# SUCCESS	Put NFT for sale(alice & bob)
# 		Check user balance
# 		Check receiver balance
def test_sale(marketplace, nft_contract, alice):
    nft_id = 1
    price = 5

    assert nft_contract.ownerOf(nft_id) == alice.address

    marketplace.createSimpleOffer(nft_contract, nft_id, price, {"from": alice})

    assert nft_contract.ownerOf(nft_id) != alice.address
    assert nft_contract.ownerOf(nft_id) == marketplace.address


# FAIl		NFT you don't own for sale
# 		Check user balance
def test_invalid_sale(marketplace, nft_contract, alice):
    nft_id = 2
    price = 5

    assert nft_contract.ownerOf(nft_id) != alice.address
    with reverts("ERC721: transfer of token that is not own"):
        marketplace.createSimpleOffer(nft_contract, nft_id, price, {"from": alice})
    assert nft_contract.ownerOf(nft_id) != marketplace.address


# SUCCESS	Buy token
# 		Check buyer balance
# 		Check seller balance
def test_buy_token(marketplace, nft_contract, alice, bob):
    nft_id = 1
    price = 5
    alice_balance = alice.balance()
    bob_balance = bob.balance()
    assert bob_balance >= price

    setAra(marketplace, nft_contract)
    sale = marketplace.createSimpleOffer(nft_contract, nft_id, price, {"from": alice})
    marketplace.buySimpleOffer(sale.return_value, {"from": bob, "value": price})

    assert bob.balance() == bob_balance - price
    assert alice.balance() == alice_balance + price
    assert nft_contract.ownerOf(nft_id) == bob.address


def test_invalid_buy_token(marketplace, nft_contract, alice, bob):
    nft_id = 1
    price = 5
    invalid_sale_id = 123
    bob_balance = bob.balance()
    alice_balance = alice.balance()
    assert bob_balance >= price

    setAra(marketplace, nft_contract)
    marketplace.createSimpleOffer(nft_contract, nft_id, price, {"from": alice})
    with reverts("This sale does not exist or has ended"):
        marketplace.buySimpleOffer(invalid_sale_id, {"from": bob, "value": price})

    assert bob.balance() == bob_balance
    assert alice.balance() == alice_balance
    assert nft_contract.ownerOf(nft_id) != bob.address
    assert nft_contract.ownerOf(nft_id) == marketplace.address


def test_invalid_value_buy(marketplace, nft_contract, alice, bob):
    nft_id, price = 1, 1
    bob_balance = bob.balance()
    alice_balance = alice.balance()

    setAra(marketplace, nft_contract)
    sale = marketplace.createSimpleOffer(nft_contract, nft_id, price, {"from": alice})
    with reverts("Insufficient funds"):
        marketplace.buySimpleOffer(sale.return_value, {"from": bob, "value": price - 1})

    assert bob.balance() == bob_balance
    assert alice.balance() == alice_balance
    assert nft_contract.ownerOf(nft_id) != bob.address
    assert nft_contract.ownerOf(nft_id) == marketplace.address


# FAIL		Remove bought NFT from sale
# 		Check seller NFT balance
def test_remove_offer(marketplace, nft_contract, alice):
    nft_id = 1
    price = 1

    sale = marketplace.createSimpleOffer(nft_contract, nft_id, price, {"from": alice})
    marketplace.removeSimpleOffer(sale.return_value, {"from": alice})

    assert nft_contract.ownerOf(nft_id) == alice.address
    assert nft_contract.ownerOf(nft_id) != marketplace.address


# FAIL		Remove not owned NFT from sale (NFT is in sale)
# 		Check seller NFT balance
def test_invalid_remove_offer(marketplace, nft_contract, alice, bob):
    nft_id = 1
    price = 1

    sale = marketplace.createSimpleOffer(nft_contract, nft_id, price, {"from": alice})
    with reverts("You are not the creator of this sale"):
        marketplace.removeSimpleOffer(sale.return_value, {"from": bob})

    assert nft_contract.ownerOf(nft_id) != alice.address
    assert nft_contract.ownerOf(nft_id) != bob.address
    assert nft_contract.ownerOf(nft_id) == marketplace.address


# SUCCESS	Update NFT for sale
def test_update_sale(marketplace, nft_contract, alice):
    nft_id = 1
    price = 5
    new_price = 50

    assert nft_contract.ownerOf(nft_id) == alice.address
    sale = marketplace.createSimpleOffer(nft_contract, nft_id, price, {"from": alice})
    assert nft_contract.ownerOf(nft_id) != alice.address
    assert nft_contract.ownerOf(nft_id) == marketplace.address

    marketplace.updateSimpleOffer(sale.return_value, new_price, {"from": alice})


def test_invalid_update_sale(marketplace, nft_contract, alice, bob):
    nft_id = 1
    price = 5
    new_price = 50

    assert nft_contract.ownerOf(nft_id) == alice.address
    sale = marketplace.createSimpleOffer(nft_contract, nft_id, price, {"from": alice})
    assert nft_contract.ownerOf(nft_id) != alice.address
    assert nft_contract.ownerOf(nft_id) == marketplace.address

    with reverts("You are not the creator of this sale"):
        marketplace.updateSimpleOffer(sale.return_value, new_price, {"from": bob})
