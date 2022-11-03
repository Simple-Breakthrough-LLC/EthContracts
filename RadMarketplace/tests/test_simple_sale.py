import pytest
from brownie import accounts, reverts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


##		 Simple Sale
# SUCCESS	Put NFT for sale(alice & bob)
# 		Check user balance
# 		Check receiver balance

def setAra(marketplace, nft):
	marketplace.setARA(nft.address)

def test_sale(marketplace, nft721, alice):
    token_id = 1
    price = 5

    assert nft721.ownerOf(token_id) == alice.address

    marketplace.createSimpleOffer(nft721, token_id, price, {"from": alice})

    assert nft721.ownerOf(token_id) != alice.address
    assert nft721.ownerOf(token_id) == marketplace.address


# FAIl		NFT you don't own for sale
# 		Check user balance
def test_invalid_sale(marketplace, nft721, alice):
    token_id = 2
    price = 5

    assert nft721.ownerOf(token_id) != alice.address
    with reverts("ERC721: transfer of token that is not own"):
        marketplace.createSimpleOffer(nft721, token_id, price, {"from": alice})
    assert nft721.ownerOf(token_id) != marketplace.address


# SUCCESS	Buy token
# 		Check buyer balance
# 		Check seller balance
def test_buy_token(marketplace, nft721, alice, bob):
    token_id = 1
    price = 5
    assert bob.balance() >= price

    setAra(marketplace, nft721)
    s = marketplace.createSimpleOffer(nft721, token_id, price, {"from": alice})
    marketplace.buySimpleOffer(s.return_value, {"from": bob, "value": price})


# FAIL		Remove bought NFT from sale
# 		Check seller NFT balance
def test_remove_offer(marketplace, nft721, alice):
    token_id = 1
    price = 1

    sale = marketplace.createSimpleOffer(nft721, token_id, price, {"from": alice})
    marketplace.removeSimpleOffer(sale.return_value, {"from": alice})

    assert nft721.ownerOf(token_id) == alice.address
    assert nft721.ownerOf(token_id) != marketplace.address


# FAIL		Remove not owned NFT from sale (NFT is in sale)
# 		Check seller NFT balance
def test_invalid_remove_offer(marketplace, nft721, alice, bob):
    token_id = 1
    price = 1

    sale = marketplace.createSimpleOffer(nft721, token_id, price, {"from": alice})
    with reverts("You are not the creator of this sale"):
        marketplace.removeSimpleOffer(sale.return_value, {"from": bob})

    assert nft721.ownerOf(token_id) != alice.address
    assert nft721.ownerOf(token_id) != bob.address
    assert nft721.ownerOf(token_id) == marketplace.address


# SUCCESS	Update NFT for sale
def test_update_sale(marketplace, nft721, alice):
    token_id = 1
    price = 5
    new_price = 50

    assert nft721.ownerOf(token_id) == alice.address
    sale = marketplace.createSimpleOffer(nft721, token_id, price, {"from": alice})
    assert nft721.ownerOf(token_id) != alice.address
    assert nft721.ownerOf(token_id) == marketplace.address

    marketplace.updateSimpleOffer(sale.return_value, new_price, {"from": alice})
