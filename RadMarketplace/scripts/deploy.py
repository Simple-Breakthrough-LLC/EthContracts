from brownie import MarketPlace, GenericERC20, GenericERC721 , accounts

def main():
    acct = accounts.load('MetamaskTest')
    token = GenericERC20.deploy({'from': acct}, publish_source=True)
    GenericERC721.deploy({'from': acct}, publish_source=True)
    MarketPlace.deploy("0xFe3929f0CE0f1Eda7D91Ce35bEf0BBb72D560ddd", 10, 5, {'from': acct}, publish_source=True)

