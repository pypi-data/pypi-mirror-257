import requests
from dataclasses import dataclass, field
import json

@dataclass
class AMS:
    env:str = "test"
    base_url:str = field(init=False)
    cookie_value:str = None
    cookie_string:str = field(init=False, default=None)
    read_only:bool = field(init=False, default=True)
    
    
    def __post_init__(self):
        self.base_url = f"https://ams.btcs{self.env}.net/api/AddressManagement"
        self.cookie_string = f".AspNetCore.Cookies={self.cookie_value}; Path=/; Secure; HttpOnly;" 
        if self.cookie_value:
            self.read_only = False

    def get_addresses(self, blockchain_id=None, include_balances=None, limit=99999999999999, account_ref=None, include_balance_groups=None, is_pay=None, is_active=None, is_contract=None, is_deposit=None, ownership=None, account_asset_id=None, customer_id=None, addresses=None, tags=None):
        page = 0
        page_size = 100
        total = 0
        take_now = page_size
        addresses = []

        while True:
            try:
                # respect the limit
                if limit - (total + page_size*page) <= 0:
                    break
                elif limit - (total + page_size*page) < page_size:
                    take_now = limit - (total + page_size*page)
                url = ""
                params = AMS.remove_none_fields({
                    "Skip": page*take_now,
                    "Take": take_now,
                    "AccountRef": account_ref,
                    "BlockchainId": blockchain_id,
                    "IncludeBalances": include_balances,
                    "IncludeBalanceGroups": include_balance_groups,
                    "IsPay": is_pay,
                    "IsActive": is_active,
                    "IsContract": is_contract,
                    "IsDeposit": is_deposit,
                    "Ownership": ownership,
                    "AccountAssetId": account_asset_id,
                    "CustomerId": customer_id,
                    "Addresses": addresses,
                    "Tags": tags
                })

                # if blockchain_id:
                #     url = "{}/addresses?Skip={}&Take={}&AccountRef={}&BlockchainId={}&IncludeBalances={}".format(self.base_url, page*take_now, take_now, account_ref, blockchain_id, include_balances)
                # else:
                #     url = "{}/addresses?Skip={}&Take={}&AccountRef={}&IncludeBalances={}".format(self.base_url, page*take_now, take_now, account_ref, include_balances)
                response = requests.request("GET", f"{self.base_url}/addresses", params=params)
                addresses_res = response.json()
                addresses.extend(addresses_res)
                page += 1
                total += take_now
                print(f"collected {total} addresses...")
                if len(addresses_res) == 0:
                    break

            except:
                print("Error with URL: {}".format(url))
        
        return addresses
    
    def tag_address(self, address, blockchain_id, tag):
        if self.read_only:
            raise Exception("No cookie provided.")

        data = json.dumps({
            "addresses": [
                {
                "blockchainId": blockchain_id,
                "address": address
                }
            ],
            "tags": [
                {
                "tagName": tag
                }
            ]
        })

        headers = {
            'cookie': self.cookie_string,
            'Content-Type': 'application/json'
        }

        return requests.patch(url=f"{self.base_url}/tag-address", data=data, headers=headers)

    def attach_address(self, address:str, blockchain_id:int, account_ref:str):
        if self.read_only:
            raise Exception("No cookie provided.")
        
        data = json.dumps({
            "blockchainId": blockchain_id,
            "accountRef": account_ref,
            "addresses": [
                address
            ]
        })

        headers = {
            'cookie': self.cookie_string,
            'Content-Type': 'application/json'
        }

        return requests.patch(url=f"{self.base_url}/attach-addresses", data=data, headers=headers)
    
    def detach_address(self, address:str, blockchain_id:int, account_ref:str):
        if self.read_only:
            raise Exception("No cookie provided.")
        
        data = json.dumps({
            "blockchainId": blockchain_id,
            "accountRef": account_ref,
            "address": address
        })

        headers = {
            'cookie': self.cookie_string,
            'Content-Type': 'application/json'
        }

        return requests.patch(url=f"{self.base_url}/detach-address", data=data, headers=headers)

    def upsert_address(self, blockchain_id:int, address:str, ownership:str=None, is_active:bool=None, is_deposit:bool=None, is_contract:bool=None, vault_account_ref:str=None, location:str=None, fee_booking_mode:str=None, fee_booking_height:bool=None, is_pay:bool=None, passphrase:str=None, account_ref:str=None, tags:[str]=None):
        if self.read_only:
            raise Exception("No cookie provided.")
        
        data_dict = {
            "ownership": ownership,
            "blockchainId": blockchain_id,
            "address": address,
            "isActive": is_active,
            "isDeposit": is_deposit,
            "isContract": is_contract,
            "vaultAccountRef": vault_account_ref,
            "location": location,
            "feeBookingMode": fee_booking_mode,
            "feeBookingStartHeight": fee_booking_height,
            "isPay": is_pay,
            "passPhrase": passphrase,
            "tags": tags,
            "accountRef": account_ref
        }

        # clear all fields where value is None
        data_dict = {k: v for k, v in data_dict.items() if v is not None}

        data = json.dumps(data_dict)

        print(data)

        headers = {
            'cookie': self.cookie_string,
            'Content-Type': 'application/json'
        }

        return requests.patch(url=f"{self.base_url}/address-detached", data=data, headers=headers)

    def remove_none_fields(my_dict):
        return {
            key: value for key, value in my_dict.items()
            if value is not None
        }
if __name__ == "__main__":
    COOKIE_VALUE = ""    
    ams = AMS("test", cookie_value=COOKIE_VALUE)
    # print(json.dumps(ams.get_addresses(is_deposit=True, include_balances=True, limit=10, tags=["siba"]), indent=2))

    # print(ams.upsert_address(
    #         blockchain_id=2, 
    #         address="addr1q8034em76n4qyhfrexv8j349gpcr5904cc4fm9vf7le59wxlrtnha482qfwj8jvc09r22srs8g2lt332nk2cnalng2uqnnqh77", 
    #         is_pay=True
    #         # tags=["siba_loves_python"]
    #     ).text)
    # print(ams.get_addresses(account="1065010", limit=10))
    # print(ams.tag_address(address="addr1q8034em76n4qyhfrexv8j349gpcr5904cc4fm9vf7le59wxlrtnha482qfwj8jvc09r22srs8g2lt332nk2cnalng2uqnnqh77", blockchain_id=2, tag="HW🔥").text)
    # print(ams.detach_address(address="addr1q8034em76n4qyhfrexv8j349gpcr5904cc4fm9vf7le59wxlrtnha482qfwj8jvc09r22srs8g2lt332nk2cnalng2uqnnqh77", blockchain_id=2, account_ref="200064921008").text)
    
    # addresses = [
    #     "0xa05b8dd67114bedac493c8e79b8de6bc09b43d126f39b2a9e5e64401d7ea8fa3f24f06a766f37893314e7a8d89eed3c9"
    # ]
    # for address in addresses:
    #     r = ams.tag_address(address=address, blockchain_id=19, tag="stk-slashed")
    #     print(r.text)


