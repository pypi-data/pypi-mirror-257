import requests
import xian_tools.utils as utl
import xian_tools.transactions as tr

from xian_tools.wallet import Wallet
from typing import Dict, Any


class Xian:
    def __init__(self, node_url: str, wallet: Wallet = None):
        self.wallet = wallet if wallet else Wallet()
        self.node_url = node_url

    def get_tx(self, tx_hash: str) -> Dict[str, Any]:
        """ Return transaction data """
        return tr.get_tx(self.node_url, tx_hash)

    def get_balance(
            self,
            address: str = None,
            contract: str = 'currency') -> int | float:
        """ Return balance for given address and token contract """

        address = address if address else self.wallet.public_key

        with requests.get(f'{self.node_url}/abci_query?path="/get/{contract}.balances:{address}"') as r:
            balance_byte_string = r.json()['result']['response']['value']

            # Decodes to 'None'
            if balance_byte_string == 'AA==':
                return 0

            try:
                balance = utl.decode_int(balance_byte_string)
                return int(balance)
            except:
                balance = utl.decode_float(balance_byte_string)
                return balance

    def send_tx(
            self,
            contract: str,
            function: str,
            kwargs: dict,
            stamps: int = 500,
            chain_id: str = None) -> Dict[str, Any]:
        """
        Send a transaction to the network
        :returns:
        - success - Boolean. True if successful
        - data - String. Transaction hash
        """

        tx = tr.create_tx(
            contract=contract,
            function=function,
            kwargs=kwargs,
            stamps=stamps,
            chain_id=chain_id,
            private_key=self.wallet.private_key,
            nonce=tr.get_nonce(
                self.node_url,
                self.wallet.public_key
            )
        )

        data = tr.broadcast_tx(self.node_url, tx)

        result = {
            'success': True,
            'tx_hash': data['data']['result']['hash'],
            'result': None,
            'data': data
        }

        if 'error' in data:
            result['success'] = False
            result['result'] = data['error']['data']

        elif data['result']['check_tx']['code'] == 1:
            result['success'] = False
            result['result'] = 'Transaction check not successful'

        elif data['result']['deliver_tx']['code'] == 1:
            result['success'] = False
            result['result'] = 'Transaction delivery not successful'

        elif data['result']['deliver_tx']['data']['status'] == 1:
            result['success'] = False
            result['result'] = data['result']['deliver_tx']['data']['result']

        return result

    def send(
            self,
            amount: int | float | str,
            to_address: str,
            token: str = "currency",
            stamps: int = 100,
            chain_id: str = None) -> Dict[str, Any]:
        """
        Send a token to a given address
        :returns:
        - success - Boolean. True if successful
        - data - String. Transaction hash
        """

        kwargs = {"amount": float(amount), "to": to_address}
        return self.send_tx(token, "transfer", kwargs, stamps, chain_id)

    def get_contract_data(
            self,
            contract: str,
            variable: str,
            *keys: str) -> None | int | float:
        """ Retrieve contract data and decode it """

        path = f'/get/{contract}.{variable}'
        path = f'{path}:{":".join(keys)}' if keys else path

        with requests.get(f'{self.node_url}/abci_query?path="{path}"') as r:
            byte_string = r.json()['result']['response']['value']

            # Decodes to 'None'
            if byte_string == 'AA==':
                return None

            try:
                data = utl.decode_int(byte_string)
            except:
                data = utl.decode_float(byte_string)
                data = int(data) if data.is_integer() else data

            return data

    def get_approved_amount(
            self,
            contract: str,
            address: str = None,
            token: str = 'currency') -> None | int | float:
        """ Retrieve approved token amount for a contract """

        address = address if address else self.wallet.public_key

        value = self.get_contract_data(token, 'balances', address, contract)
        value = 0 if value is None else value

        return value

    def approve(
            self,
            contract: str,
            token: str = "currency",
            amount: int | float | str = 900000000000,
            chain_id: str = None) -> Dict[str, Any]:
        """ Approve smart contract to spend max token amount """

        kwargs = {"amount": float(amount), "to": contract}
        return self.send_tx(token, "approve", kwargs, 50, chain_id)

    def deploy_contract(
            self,
            name: str,
            code: str,
            stamps: int = 1000,
            chain_id: str = None) -> Dict[str, Any]:
        """
        Deploy a contract to the network
        :returns:
        - success - Boolean. True if successful
        - data - String. Transaction hash
        """

        kwargs = {"name": name, "code": code}
        return self.send_tx('submission', 'submit_contract', kwargs, stamps, chain_id)
