# [Day 1: Sonar Sweep](https://adventofcode.com/2021/day/1)

### Description

Implementation as an ERC20-token `AOC01` on the Ethereum Ropsten Test Network.
Calling the smart contracts `part1` or `part2` with your input will at first burn all
the `AOC01` tokens in your wallet, and then mint new ones representing the solution.

You will need some ETH in your test wallet to cover gas fees.

[Deployed contract - 0xcfd1A2202aBaeb14a6a96D56E4283d1Cf9F8472e](https://ropsten.etherscan.io/address/0xcfd1A2202aBaeb14a6a96D56E4283d1Cf9F8472e#writeContract)

### How to use it

1. Create a wallet on metamask and connect to the Etheruem Ropsten Test Network.
   [Tutorial - Step 3](https://docs.alchemy.com/alchemy/tutorials/hello-world-smart-contract#step-3-create-an-ethereum-account-address)

2. Load up your wallet with some Ropsten-ETH via a faucet.
   [Tutorial - Step 4](https://docs.alchemy.com/alchemy/tutorials/hello-world-smart-contract#step-4-add-ether-from-a-faucet)

3. [Open contract on Etherscan](https://ropsten.etherscan.io/address/0xcfd1A2202aBaeb14a6a96D56E4283d1Cf9F8472e#writeContract)

4. Add `0xcfd1A2202aBaeb14a6a96D56E4283d1Cf9F8472e` as a custom token in Metamask, so you can check your balance.

5. Connect with Metamask (and make sure you are connected to Ropsten)

6. Use the `part1` or `part2` method by entering your input as an array in this format:

    [199,200,208,210,200,207,240,269,260,263]

7. Confirm the transaction and wait until it is completed.

8. The balance of the `AOC01` token in your wallet will reflect the solution, previously held tokens will be burned :)


### Dev Instructions

Follow [this tutorial](https://docs.alchemy.com/alchemy/tutorials/hello-world-smart-contract)
on how to setup an development environment for the Ethereum Ropsten Test Network with Hardhat
and Alchemy.

You will need an `.env` file with the following values:

    API_URL = "https://eth-ropsten.alchemyapi.io/v2/{YOUR ALCHEMY API KEY}"
    API_KEY = "{YOUR ALCHEMY API KEY}"
    PRIVATE_KEY = "{YOUR METAMASK PRIVATE KEY}"
    ETHERSCAN_API_KEY = "{YOUR ETHERSCAN API KEY}"
    CONTRACT_ADDRESS = "{FILL AFTER DEPLOY}


Compile the contract:

    npx hardhat compile

Test the contract:

    npx hardhat test

Deploy the contract:

    npx hardhat run scripts/deploy.js --network ropsten

Store contract address in .env as `CONTRACT_ADDRESS` after deploy

Run scripts:

    npx hardhat run scripts/x.js [--network ropsten]

Verify contract:

    npx hardhat verify --network ropsten DEPLOYED_CONTRACT_ADDRESS 1
