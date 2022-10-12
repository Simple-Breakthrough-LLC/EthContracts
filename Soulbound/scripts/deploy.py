from brownie import SoulboundNFT, accounts

def main():
    acct = accounts.load('MetamaskTest')
    SoulboundNFT.deploy("Test", "TST", "", 10, {'from': acct}, publish_source=True)

