import os
from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    deploy_mocks,
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from web3 import Web3


def deploy_fund_me():
    # 3 ways of accesing account:
    # 1. local accounts from ganache
    # account = accounts[0]
    # 2. add to brownie account (encrypted account): brownie accounts new xxxxxxxxx
    # account = accounts.load("metamask_test-account")
    # 3. save as PRIVATE KEY in .env or brownie-config.yaml
    # account = accounts.add(os.getenv("PRIVATE_KEY"))
    # account = accounts.add(config["wallets"]["from_key"])

    account = get_account()
    # pass the price feed address to our fundme contract

    # if we are on a persistent network like rinkeby, use the associated address
    # otherwise, deploy mocks

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me

    # how many block to wait
    # transaction.wait(1)


def main():
    deploy_fund_me()
