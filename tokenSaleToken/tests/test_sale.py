import pytest

from brownie import accounts, reverts

@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

def test_saleFail(sale, tokenPayment, tokenSale, alice):

	with reverts( "Insufficient funds"):
		sale.buy(7, {"from": alice.address})
	with reverts( "Not enough tokens remaining"):
		sale.buy(15, {"from": alice.address})

#  Invalid sale
# Buy too much
#  Not enough funds

def test_Pause(sale, deployer, alice):
	sale.pause({"from": deployer})
	with reverts():
		sale.buy(1, {"from": alice.address})
	sale.unpause({"from": deployer})

	sale.buy(1, {"from": alice.address})
#  Pause
# pause contract
#  try buy
#  unpause
# / try buy

def test_buy(sale, tokenPayment, tokenSale, alice):
	amount = 1
	price = sale.price()
	contractSale = tokenSale.balanceOf(sale)
	aliceSale = tokenSale.balanceOf(alice)
	alicePay = tokenPayment.balanceOf(alice)

	sale.buy(amount, {"from": alice.address})

	assert(tokenSale.balanceOf(alice) == aliceSale + amount)

	assert(tokenPayment.balanceOf(sale) == contractSale + (amount * price))
	assert(tokenPayment.balanceOf(alice) == alicePay - (amount * price))


def test_withdraw(sale, tokenPayment, tokenSale, deployer, alice):
	amount = 1
	deployerPay = tokenPayment.balanceOf(deployer)

	sale.buy(amount, {"from": alice.address})

	sale.withdraw({"from": deployer})

	assert(sale.remainingSaleSupply() == 0)
	assert(tokenPayment.balanceOf(sale) == 0)
	assert(tokenPayment.balanceOf(deployer) == amount + deployerPay)





#  valid sale
# buy
# check contrcat balance
#  check sender balance
#  withdraw a
#  iwthdraw b

#  valide sa;e 2
# buy again
#  check again
#  withdraw all
