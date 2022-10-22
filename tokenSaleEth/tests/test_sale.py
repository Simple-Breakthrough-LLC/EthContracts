import pytest

from brownie import accounts, reverts

@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

def test_saleFail(sale, alice):

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

	sale.buy(1, {"from": alice.address, "value": sale.price()})
#  Pause
# pause contract
#  try buy
#  unpause
# / try buy

def test_buy(sale, tokenSale, alice):
	amount = 1
	price = sale.price()
	contractBal = sale.balance()
	aliceSale = tokenSale.balanceOf(alice)
	aliceBal = alice.balance()

	sale.buy(amount, {"from": alice.address, "value": price * amount})

	assert(tokenSale.balanceOf(alice) == aliceSale + amount)
	assert(alice.balance() == aliceBal - (amount * price))
	assert(sale.balance() == contractBal + (amount * price))

def test_withdraw(sale, deployer, alice):
	amount = 1
	deployerPay = deployer.balance()

	sale.buy(amount, {"from": alice.address, "value": sale.price()})

	sale.withdraw({"from": deployer})

	assert(sale.remainingSaleSupply() == 0)
	assert(sale.balance() == 0)
	assert(deployer.balance() == amount + deployerPay)





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
