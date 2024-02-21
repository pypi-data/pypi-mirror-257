import requests
import logging
import random
import time
from uuid import UUID
from typing import Any, Dict, List, Optional
from .utils import hash_pass, hash_session, generate_client_hash
from .base_client import BaseClient


class INNClient(BaseClient):
    def __init__(self, host_url: str, api_key: Optional[UUID] = None):
        super().__init__(host_url, api_key)

    def do_login(self, user: str, password: str, require_success: bool = True):
        login_body = {
            "user": user,
            "pass": hash_pass(password, user),
            "apikey": self.api_key,
        }

        my_url = "/login"
        res_j = self._send_post_request(url=my_url, body=login_body)
        if not require_success:
            return res_j

        if "uuid" not in res_j:
            raise RuntimeError(f"Missing uuid in login response: {res_j}")

        self.email = res_j["email"]
        self.uuid = res_j["uuid"]
        self.username = user
        self.password = password
        self.pub = res_j["pub"]
        return res_j

    def passive_login(self, user: str, password: str):
        login_body = {
            "user": user,
            "pass": hash_pass(password, user),
            "apikey": self.api_key,
        }

        my_url = "/login"
        res_j = self._send_post_request(url=my_url, body=login_body)
        if new_uuid := res_j.get("uuid"):
            self.uuid = new_uuid
        return res_j

    def validate_session(self, user: str, session: str, api_key: str):
        body = {"user": user, "sessionHash": hash_session(session), "apiKey": api_key}
        my_url = "/core/session/validate"
        return self._send_post_request(my_url, body)

    def resend_verification(self, other_fields: dict = None):
        resend_body = {"email": self.email}
        if other_fields:
            resend_body.update(other_fields)

        my_url = "/auth/email/resend"
        return self._send_post_request(my_url, resend_body)

    def verify_by_code(self, verify_code: str):
        if not verify_code:
            return False
        verify_url = f"{self.host_url}/verify/{verify_code}"
        res = requests.get(verify_url)
        return res.text

    def request_password_reset(self, other_fields: dict = None):
        body = {"username": self.username, "apiKey": self.api_key}
        if other_fields:
            body.update(other_fields)

        my_url = "/auth/password/forgot"
        return self._send_post_request(my_url, body)

    def reset_password(self, reset_code: str, new_pass: str, other_fields: dict = None):
        body = {
            "username": self.username,
            "email": self.email,
            "resetCode": reset_code,
            "newPassword": hash_pass(new_pass, self.username),
            "newEmailHash": hash_pass(new_pass, self.email),
        }
        if other_fields:
            body.update(other_fields)
        verify_url = "/auth/password/reset"
        return self._send_post_request(verify_url, body)

    def request_username(self, other_fields: dict = None):
        body = {"email": self.email}
        if other_fields:
            body.update(other_fields)
        verify_url = "/auth/username/forgot"
        return self._send_post_request(verify_url, body)

    def change_password(self, old_pass: str, new_pass: str) -> dict:
        user_pass = hash_pass(new_pass, self.username)
        email_pass = hash_pass(new_pass, self.email)
        body = {
            "uuid": self.uuid,
            "user": self.username,
            "oldPass": hash_pass(old_pass, self.username),
            "newPass": user_pass,
            "email": self.email,
            "newEmailHash": email_pass,
        }
        return self._send_post_request("/auth/password/change", body)

    def waitfor_status(self, client_id):
        i_max = 30
        i = 0
        while True:
            time.sleep(1)
            i = i + 1
            res = self.do_check_status([client_id])
            if res.get("clientTxs")[0].get("status") == "Rejected":
                return True
            if res.get("clientTxs")[0].get("status") == "Final":
                return True
            if i >= i_max:
                return False

    def waitfor_possession(self, nft_uri):
        i_max = 30
        i = 0
        while True:
            time.sleep(1)
            i = i + 1
            nfts = self.list_nfts({"nftUris": nft_uri})
            if len(nfts) > 0:
                return True
            if i >= i_max:
                return False

    def get_nft_reports(self, coin_ids):
        body = {"uuid": self.uuid, "coinIds": coin_ids, "perPage": 1000}

        my_url = "/core/nft/reports"
        return self._send_post_request(url=my_url, body=body)

    def do_check_status(self, client_ids: list):
        body = {"uuid": self.uuid, "clientIds": client_ids}

        my_url = "/core/transactions/status"
        return self._send_post_request(url=my_url, body=body)

    def get_incomplete_txs(self):
        body = {"uuid": self.uuid}

        my_url = "/core/transactions/incomplete"
        return self._send_post_request(url=my_url, body=body)

    def register(self, body: dict, allow_login: bool = False):
        my_url = "/register"
        res_j = self._send_post_request(url=my_url, body=body)

        self.username = body["user"]

        if "uuid" not in res_j:
            return res_j

        self.email = res_j["email"]
        self.uuid = res_j["uuid"]
        self.pub = res_j["pub"]
        return res_j

    def list_nfts(self, body=None):
        inner_body = {"uuid": self.uuid, "perPage": 1000}
        if body:
            inner_body.update(body)
        my_url = "/core/nft/list"
        res_j = self._send_post_request(url=my_url, body=inner_body)
        if nfts := res_j.get("nfts"):
            return nfts
        return []

    def define_recipe(self, name: str, inputs: List, outputs: List):
        body = {"uuid": self.uuid, "name": name, "inputs": inputs, "outputs": outputs}
        my_url = "/recipe/define"
        return self._send_post_request(url=my_url, body=body)

    def list_recipes(self, owner_address: str):
        body = {"uuid": self.uuid, "owner": owner_address}
        my_url = "/recipe/list"
        return self._send_post_request(url=my_url, body=body)

    def use_recipe(self, recipe_uri, inputs, amount=1):
        body = {
            "uuid": self.uuid,
            "recipeUri": recipe_uri,
            "inputs": inputs,
            "amount": amount,
        }
        my_url = "/recipe/use"
        return self._send_post_request(url=my_url, body=body)

    def get_all_nfts(self, body=None):
        inner_body = {"uuid": self.uuid, "perPage": 1000}
        if body:
            inner_body.update(body)
        return self._send_post_request(url="/core/nft/all", body=inner_body)

    def get_nft_history(self, body=None):
        initial_body = {"uuid": self.uuid, "perPage": 1000}
        if body:
            initial_body.update(body)
        return self._send_post_request(url="/core/nft/history", body=initial_body)

    def get_nft_by_uri(self, nft_uri):
        body = {
            "uuid": self.uuid,
            "nftUris": [nft_uri],
        }

        my_url = "/core/nft/list"
        res_j = self._send_post_request(url=my_url, body=body)
        if not res_j.get("nfts"):
            return None
        return res_j.get("nfts")[0]

    def get_nft_balances(
        self,
        mint_ids: List[str] = None,
        nft_names: List[str] = None,
        version: str = None,
        per_page: int = None,
        page: int = None,
    ) -> Dict[str, Dict[str, Any]]:
        body = {"uuid": self.uuid}
        if mint_ids is not None:
            body["mintIds"] = mint_ids
        if nft_names is not None:
            body["nftNames"] = nft_names
        if per_page:
            body["perPage"] = per_page
        if page:
            body["page"] = page
        my_url = (
            "/core/nft/balances" if version is None else f"/{version}/core/nft/balances"
        )

        return self._send_post_request(url=my_url, body=body)

    def send_nft(self, nft_uri, receiver_addr, optionals=None):
        body = {"uuid": self.uuid, "nftUri": nft_uri, "recipientAddr": receiver_addr}
        if optionals:
            body.update(optionals)
        return self._send_post_request(url="/core/nft17/send", body=body)

    def check_balances(
        self, coins: List[int], block_height: int = -1, other_fields: dict = None
    ):
        body = {"uuid": self.uuid, "coinIds": [str(coin) for coin in coins]}
        if other_fields:
            body.update(other_fields)
        if block_height >= 0:
            body["endBlock"] = block_height
        my_url = "/core/wallet/balances"
        return self._send_post_request(url=my_url, body=body)

    def get_wallet_assets(self, coins: List[int] = None, asset_uris: List[str] = None):
        body = dict()
        if coins:
            body["coinIds"] = [str(coin) for coin in coins]
        if asset_uris:
            body["assetUris"] = asset_uris
        body["uuid"] = self.uuid
        my_url = "/core/wallet/assets"
        return self._send_post_request(url=my_url, body=body)

    def get_wallet_settings(self):
        body = {"uuid": self.uuid}
        my_url = "/core/wallet/settings"
        return self._send_post_request(url=my_url, body=body)

    def define_template(self, body: dict):
        body["uuid"] = self.uuid
        my_url = "/core/template/define"
        return self._send_post_request(url=my_url, body=body)

    def describe_template(self, body: dict):
        my_url = "/core/template/describe"
        return self._send_post_request(url=my_url, body=body)

    def list_template(self, body: dict):
        body["uuid"] = self.uuid
        return self._send_post_request(url="/core/template/list", body=body)

    def get_asset_history(self, asset_uri: str):
        body = {"uuid": self.uuid, "assetUri": asset_uri}
        my_url = "/core/asset/history"
        return self._send_post_request(url=my_url, body=body)

    def do_asset_create(
        self,
        coin_id: int,
        amount: int,
        client_id: str | None = None,
        properties: dict | None = None,
        comment: str | None = None,
        sync: bool = True,
    ):
        body = {"uuid": self.uuid, "coinId": str(coin_id), "amount": str(amount)}
        if client_id:
            body["clientId"] = client_id
            checksum = generate_client_hash(
                str(coin_id), str(self.api_key), amount, client_id
            )
            body["checksum"] = f"{checksum}"
        if properties:
            body["properties"] = properties
        if comment:
            body["comment"] = comment
        # if not sync:
        #    body["noBlock"] = True

        res = self._send_post_request(url="/core/asset/create", body=body)
        if sync:
            wait_res = self.waitfor_status(client_id=res.get("clientId"))
            assert wait_res, "[x] Create tx timed out"
        return res

    def register_callback(
        self,
        callback_url: str,
        condition: str,
        condition_value: str,
        method: str,
        auth_token: str,
        num_calls: int | None = None,
    ):
        body = {
            "uuid": self.uuid,
            "callbackUrl": callback_url,
            "condition": condition,
            "conditionValue": str(condition_value),
            "numCalls": num_calls,
            "method": method,
            "authToken": auth_token,
        }

        res = self._send_post_request(url="/callback/register", body=body)
        return res

    def delete_callback(
        self,
        callback_id: str,
    ):
        body = {
            "uuid": self.uuid,
            "callbackId": callback_id,
        }

        res = self._send_post_request(url="/callback/delete", body=body)
        return res

    def list_callbacks(
        self,
        callback_id: Optional[str] = None,
    ):
        body = {
            "uuid": self.uuid,
            "callbackId": callback_id,
        }

        res = self._send_post_request(url="/callback/list", body=body)
        return res

    def delete_asset(
        self,
        coin_id: int,
        amount: int,
        client_id: str | None = None,
        asset_uri: str | None = None,
        comment: str | None = None,
        other_fields: dict = None,
        sync: bool = True,
    ):
        body = {"uuid": self.uuid, "coinId": str(coin_id), "amount": str(amount)}
        if client_id:
            body["clientId"] = client_id
            checksum = generate_client_hash(
                str(coin_id), str(self.api_key), amount, client_id
            )
            body["checksum"] = f"{checksum}"
        if asset_uri:
            body["assetUri"] = asset_uri
        if comment:
            body["comment"] = comment
        if other_fields:
            body.update(other_fields)

        res = self._send_post_request(url="/core/asset/delete", body=body)
        if sync:
            wait_res = self.waitfor_status(client_id=res.get("clientId"))
            assert wait_res, "[x] Delete tx timed out"
        return res

    def modify_asset(
        self,
        coin_id: int,
        asset_uri: str,
        properties: dict,
        client_id: str,
        comment: str = None,
        checksum: str = None,
        devv_protect: bool = None,
        protect_time: int = None,
        sync: bool = True,
    ):
        body = {
            "uuid": self.uuid,
            "coinId": coin_id,
            "assetUri": asset_uri,
            "properties": properties,
            "clientId": client_id,
            "apiKey": self.api_key,
        }
        if comment is not None:
            body["comment"] = comment
        if checksum is None:
            checksum = generate_client_hash(
                str(coin_id), str(self.api_key), 1, client_id
            )
        body["checksum"] = checksum
        if devv_protect is not None:
            body["devvProtect"] = devv_protect
        if protect_time is not None:
            body["protectTime"] = protect_time

        res = self._send_post_request(url="/core/asset/modify", body=body)
        if sync:
            wait_res = self.waitfor_status(client_id=res.get("clientId"))
            assert wait_res, "[x] Modify tx timed out"
        return res

    def mint_nft(self, props: dict):
        props["uuid"] = self.uuid
        my_url = "/core/nft/mint"
        return self._send_post_request(url=my_url, body=props)

    def sell_nft(self, nft_uri: str, body=None):
        inner_body = {
            "uuid": self.uuid,
            "nftUri": nft_uri,
        }
        if body:
            inner_body.update(body)

        my_url = "/core/nft/sell"
        return self._send_post_request(url=my_url, body=inner_body)

    def retract_nft(self, nft_uri: str):
        body = {
            "uuid": self.uuid,
            "nftUri": nft_uri,
        }

        my_url = "/core/nft/retract"
        return self._send_post_request(url=my_url, body=body)

    def request_refund(self, description, body=None):
        if body is None:
            body = {}
        inner_body = {
            "uuid": self.uuid,
            "description": description,
        }
        inner_body.update(body)

        my_url = "/core/asset/return"
        return self._send_post_request(url=my_url, body=inner_body)

    def checkout_nft(self, buyer_address: str, nft_uri: str):
        body = {
            "uuid": self.uuid,
            "nftUri": nft_uri,
            "buyerAddress": buyer_address,
        }

        my_url = "/core/nft/checkout"
        return self._send_post_request(my_url, body)

    def fulfill_nft(
        self, buyer_address: str, nft_uri: str, checksum: Optional[str] = None
    ):
        body = {
            "uuid": self.uuid,
            "nftUri": nft_uri,
            "buyerAddress": buyer_address,
            "checksum": checksum,
        }

        my_url = "/core/nft/fulfill"
        return self._send_post_request(my_url, body)

    def unbundle_nft(self, nft_uri: str):
        body = {"uuid": self.uuid, "nftUri": nft_uri}

        my_url = "/core/nft/unbundle"
        return self._send_post_request(my_url, body)

    def escrow_unbundle_nft(self, nft_uri: str):
        body = {"uuid": self.uuid, "nftUri": nft_uri}

        my_url = "/core/escrow/unbundle"
        return self._send_post_request(my_url, body)

    def upload_content(
        self,
        content_name: str,
        content_type: str,
        field_schema: dict,
        content_raw: str,
        other_fields: dict = None,
    ):
        body = {
            "uuid": self.uuid,
            "content": {
                "raw": content_raw,
                "contentType": content_type,
                "fieldSchema": field_schema,
            },
            "name": content_name,
        }
        if other_fields:
            body.update(other_fields)

        my_url = "/core/content/upload"
        res_j = self._send_post_request(my_url, body)
        if content_ref := res_j.get("contentRef"):
            return content_ref
        return res_j

    def download_content(self, content_uri: str):
        body = {"contentRef": content_uri}

        my_url = "/core/content/download"
        res_j = self._send_post_request(my_url, body)

        if content := res_j.get("content"):
            return content
        return None

    def get_asset_by_uri(self, asset_uri: str):
        body = {"uuid": self.uuid, "assetUris": [asset_uri]}

        my_url = "/core/wallet/assets"
        res_j = self._send_post_request(my_url, body)
        if assets := res_j.get("assets"):
            return assets[0]
        return None

    def get_balance(self, coin_id: int):
        body = {"uuid": self.uuid, "coinIds": [str(coin_id)]}

        my_url = "/core/wallet/balances"
        res_j = self._send_post_request(my_url, body)
        if (balances := res_j.get("balances")) and (
            balance := balances[0].get("balance")
        ):
            return balance
        return 0

    def search_username(self, body: dict):
        init_body = {"uuid": self.uuid}
        init_body.update(body)

        my_url = "/core/search/username"
        res_j = self._send_post_request(url=my_url, body=init_body)

        return res_j

    def get_support_verification(self, user: str = None, email: str = None):
        body = {"uuid": self.uuid}
        if user:
            body["user"] = user
        if email:
            body["email"] = email
        my_url = "/tools/test/verification"
        return self._send_post_request(url=my_url, body=body)

    def get_wallet_addr(self):
        body = {
            "uuid": self.uuid,
            "name": self.username,
        }

        res_j = self.search_username(body)

        wallet_addr = res_j.get("wallets")
        if wallet_addr:
            return wallet_addr[0].get("addr")

        return wallet_addr

    def get_shard_info(self):
        """
        Send a request to retrieve information about the shard from the specified endpoint.
        :returns: A dictionary representing the JSON response received from the shard info endpoint.
        """
        my_url = "/core/shard/info"
        return self._send_get_request(url=my_url)

    def get_shard_configs(self):
        return self._send_get_request(url="/core/settings/configs")

    def get_settings_home(self):
        """
        Retrieve home settings from the user's shard.
        :return: A dictionary containing home settings retrieved from the shard.
        """
        body = {
            "uuid": self.uuid,
        }
        my_url = "/core/settings/home"
        return self._send_post_request(url=my_url, body=body)

    def get_transaction_info(self, body):
        """
        Send a request to retrieve information about the transaction from the specified endpoint.
        :param body: A dictionary containing the request body to be sent in JSON format.
        :returns: A dictionary representing the JSON response received from the transaction info endpoint.
        """
        my_url = "/core/transaction/info"
        return self._send_post_request(url=my_url, body=body)

    def get_block_info(self, body):
        my_url = "/core/block/info"
        return self._send_post_request(url=my_url, body=body)

    def get_block_chart(self, body):
        my_url = "/core/block/chart"
        return self._send_post_request(url=my_url, body=body)

    def create_chest_litpet(self):
        body = {
            "uuid": self.uuid,
        }

        my_url = "/litcraft/chest/litpet"
        return self._send_post_request(url=my_url, body=body)

    def make_litpet(self, mother_uri, father_uri, receiver_address, heptal_count=1000):
        body = {
            "uuid": self.uuid,
            "targetAddr": receiver_address,
            "motherUri": mother_uri,
            "fatherUri": father_uri,
            "heptalCount": heptal_count,
            "magicLevel": random.randint(1, 7),
        }

        my_url = "/litcraft/litpet/create"
        return self._send_post_request(url=my_url, body=body)

    def make_server_litpet(
        self,
        mother_species: str,
        father_species: str,
        target_addr: str,
        magic_level: int = None,
    ):
        body = {
            "uuid": self.uuid,
            "motherSpecies": mother_species,
            "fatherSpecies": father_species,
            "magicLevel": magic_level or random.randint(1, 7),
            "targetAddr": target_addr,
        }
        my_url = "/litcraft/litpet/servercreate"
        return self._send_post_request(url=my_url, body=body)

    def view_litpet(self, litpet_uri):
        body = {"uuid": self.uuid, "litpetUri": litpet_uri}

        my_url = "/litcraft/litpet/view"
        return self._send_post_request(url=my_url, body=body)

    def player_assets(self, pub: str):
        """
        Fetches the assets associated with a player's public key.
        :param pub: The public key of the player.
        :returns: A dictionary containing the player's assets information.
        """
        body = {"uuid": self.uuid, "pub": pub}
        my_url = "/litcraft/player/assets"
        return self._send_post_request(url=my_url, body=body)

    def player_balances(self, pub: str):
        """
        Retrieves the balances of a player's assets based on their public key.
        :param pub: The public key of the player.
        :returns: A dictionary containing the player's asset balances.
        """
        body = {"uuid": self.uuid, "pub": pub}
        my_url = "/litcraft/player/balances"
        return self._send_post_request(url=my_url, body=body)

    def send_transaction(
        self,
        coin_id: int,
        amount: int,
        receiver_address,
        asset_uri: str = None,
        comment: str = None,
        client_id: str = None,
        sync: bool = True,
    ):
        body = {
            "uuid": self.uuid,
            "wallet": self.get_wallet_addr(),
            "to": receiver_address,
            "coinId": str(coin_id),
            "amount": amount,
            "hex": "",
            "sig": "",
            "assetUri": asset_uri,
        }
        if asset_uri:
            body["assetUri"] = asset_uri
        if client_id:
            body["clientId"] = client_id
        if comment:
            body["comment"] = comment

        res = self._send_post_request(url="/core/transactions/send", body=body)
        if sync:
            wait_res = self.waitfor_status(client_id=res.get("clientId"))
            assert wait_res, "[x] Send tx timed out"
        return res

    def core_account_settings(self, body: dict):
        init_body = {"uuid": self.uuid}
        init_body.update(body)

        my_url = "/core/account/settings"
        res_j = self._send_post_request(url=my_url, body=init_body)

        return res_j

    def core_settings_modify(self, body: dict = None):
        init_body = {
            "uuid": self.uuid,
            "user": self.username,
            "pass": hash_pass(self.password, self.username),
        }
        if body:
            init_body.update(body)

        my_url = "/core/settings/modify"
        res_j = self._send_post_request(url=my_url, body=init_body)

        return res_j

    def core_account_assets(self, body: dict):
        init_body = {"uuid": self.uuid}
        init_body.update(body)

        my_url = "/core/account/assets"
        res_j = self._send_post_request(url=my_url, body=init_body)

        return res_j

    def core_account_balances(self, body: dict):
        init_body = {"uuid": self.uuid}
        init_body.update(body)

        my_url = "/core/account/balances"
        res_j = self._send_post_request(url=my_url, body=init_body)

        return res_j

    def core_account_transactions(self, body: dict):
        init_body = {"uuid": self.uuid}
        init_body.update(body)

        my_url = "/core/account/transactions"
        res_j = self._send_post_request(url=my_url, body=init_body)

        return res_j

    def core_escrow_bundle(self, body: dict, sync: bool = True):
        init_body = {"uuid": self.uuid}
        init_body.update(body)

        res = self._send_post_request(url="/core/escrow/bundle", body=init_body)
        if sync and "clientId" in res:
            wait_res = self.waitfor_status(client_id=res.get("clientId"))
            assert wait_res, "[x] Escrow bundle timed out"

        return res

    def core_escrow_unbundle(self, body: dict, sync: bool = True):
        init_body = {"uuid": self.uuid}
        init_body.update(body)

        res = self._send_post_request(url="/core/escrow/unbundle", body=init_body)
        if sync and "clientId" in res:
            wait_res = self.waitfor_status(client_id=res.get("clientId"))
            assert wait_res, "[x] Escrow unbundle timed out"

        return res

    def core_transactions_final(self, body: dict):
        init_body = {"uuid": self.uuid}
        init_body.update(body)

        my_url = "/core/transactions/final"
        res_j = self._send_post_request(url=my_url, body=init_body)
        return res_j

    def identity_presale_individual(self, body: dict):
        init_body = {"uuid": self.uuid}
        init_body.update(body)

        my_url = "/identity/presale/individual"
        res_j = self._send_post_request(url=my_url, body=init_body)
        return res_j

    def identity_kyc_view(self, body: dict):
        init_body = {"uuid": self.uuid}
        init_body.update(body)

        my_url = "/identity/kyc/view"
        res_j = self._send_post_request(url=my_url, body=init_body)
        return res_j

    def core_grant_role_permissions(self, body: dict):
        """
        Grant role permissions to the current user or entity.
        :param body: A dictionary containing the role assignment information. This should include details such as
        the target user or entity and the specific roles to be assigned.
        :returns: A dictionary that will contain information about the success or failure of the role assignment.
        """
        init_body = {"uuid": self.uuid}
        init_body.update(body)
        my_url = "/core/roles/assign"
        res_j = self._send_post_request(url=my_url, body=init_body)
        return res_j

    def core_revoke_role_permissions(self, body: dict):
        """
        Revoke role permissions from the current user or entity.
        :param body: A dictionary containing the role revocation information. This should include details such as
        the target user or entity and the specific roles to be revoked.
        :returns: A dictionary that will contain information about the success or failure of the role revocation.
        """
        init_body = {"uuid": self.uuid}
        init_body.update(body)
        my_url = "/core/roles/revoke"
        res_j = self._send_post_request(url=my_url, body=init_body)
        return res_j


class INNTestClient(INNClient):
    def __init__(self, host_url: str, api_key: Optional[UUID] = None):
        super().__init__(host_url, api_key)

    @staticmethod
    def register_users(host_url: str, n: int, offset: int) -> List[Dict]:
        """Register n users with the name test_{i} starting from i = offset."""
        users = []
        for i in range(n):
            user = {}
            acct_num = i + offset
            acct_pass = f"test{acct_num}"
            acct_name = f"test_{acct_num}"
            body = {
                "addr": "",
                "user": acct_name,
                "pass": hash_pass(acct_pass, acct_name),
                "fullName": f"Test {acct_num}",
                "email": f"test+{acct_num}@test.io",
                "phone": f"0301400{acct_num}",
            }
            myurl = f"{host_url}/register"
            res = requests.post(
                myurl,
                json=body,
                headers={"Content-Type": "application/json; charset=utf-8"},
                verify=True,
            ).json()
            user["user"] = body["user"]
            user["pass"] = acct_pass
            user["pub"] = res.get("pub")
            user["acctNum"] = acct_num
            user["username"] = f"test_{acct_num}"
            user["email"] = f"test+{acct_num}@test.io"
            user["phone"] = f"0301400{acct_num}"
            users.append(user)

        return users

    def test_bundle_mint(
        self, coin_id: int = None, amount: int = 1, asset_uris: list = None
    ):
        body = {
            "uuid": self.uuid,
            "assetName": "Test Bundle",
            "creator": "JustMe",
            "artist": "LitcraftB",
            "amount": "1",
            "nftType": "fungibleBundle",
            "assetDescription": "This is a test NFT-17 bundle.",
            "assetReferenceThumbnails": [
                "https://nftthumbnailsprod.s3.amazonaws.com/litcraft/chestbundles/Chest_TileLandChest.jpg"
            ],
            "assetReference": {
                "rawReference": ("https://nftassetsstaging.s3.amazonaws.com/devvio/\
                devvxuploads/d82b5a63-886a-49ee-ad99-cab9e3a3072e.jpg"),
                "hash": "663CA6F126F78802A8A84FFAF711149F69399335C445914DBC59F18EC32097EA",
                "fieldSchema": "",
            },
        }
        if coin_id:
            body.update(
                {"bundleAmount": str(amount), "bundleCoinId": f"{str(coin_id)}"}
            )
        if asset_uris:
            body.update({"bundleAssetUris": asset_uris})

        my_url = "/core/nft/mint"
        return self._send_post_request(url=my_url, body=body)

    def test_bundle(self, coin_id: int, amount: int = 1, other_fields: dict = None):
        body = {
            "uuid": self.uuid,
            "assetName": "Test Bundle",
            "creator": "JustMe",
            "artist": "LitcraftB",
            "bundleAmount": str(amount),
            "bundleCoinId": f"{str(coin_id)}",
            "assetDescription": "This is an NFT-17 bundle.",
            "saleLinkJson": {
                "rawReference": "https://somewhere",
                "hash": "663CA6F126F78802A8A84FFAF711149F69399335C445914DBC59F18EC32097EA",
                "fieldSchema": "",
            },
        }
        if other_fields:
            body.update(other_fields)

        my_url = "/core/escrow/bundle"
        return self._send_post_request(url=my_url, body=body)

    def register_user(self, lc_user: str, unhashed_pass: str):
        acct_num = random.randint(10000, 20000)
        body = {
            "user": lc_user,
            "pass": hash_pass(unhashed_pass, lc_user),
            "fullName": "Test",
            "email": f"test+{acct_num}@test.io",
            "phone": f"0301400{acct_num}"
        }
        try:
            self.register(body)
        except Exception:
            logging.debug("This user is already registered.")
        res = self.do_login(user=lc_user, password=unhashed_pass)
        return res
