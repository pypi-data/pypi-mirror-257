import requests
import json
import inspect
from urllib.parse import urlencode
from requests.adapters import HTTPAdapter, Retry
import logging
from typing import List, Any
from .models.ticket import Ticket, TicketFeed, TicketType
from .models.attribute import AttributeChoice
from .models.asset import Asset, AssetModel
from .models.knowledge_article import KnowledgeArticle


class Tdx:
    """
    Interact with the TeamDynamix Rest API
    :param username: TDX service account username, could also be an admin service account BEID
    :param password: TDX service account password, could also be an admin service account key
    :param hostname: TDX hostname e.g. 'myorg.teamdynamix.com'
    :param environment: TDX environment, either 'sandbox' or 'production'
    :param asset_app_id: If interacting with the Asset APIs, provide the Asset Application ID
    :param client_portal_app_id: If interacting with the Client Portal APIs, provide the Client Portal Application ID
    :param ticketing_app_id: If interacting with the Ticket APIs, provide the Ticketing Application ID
    :param is_admin: True if using a TDX admin svc account to reach admin endpoints, defaults False
    """

    def __init__(
        self,
        username: str,
        password: str,
        hostname: str,
        environment: str,
        asset_app_id: int | bool = False,
        client_portal_app_id: int | bool = False,
        ticketing_app_id: int | bool = False,
        is_admin: bool = False,
    ) -> None:
        self.username = username
        self.password = password
        self.hostname = hostname
        self.environment = environment
        self.asset_app_id = asset_app_id
        self.client_portal_app_id = client_portal_app_id
        self.ticketing_app_id = ticketing_app_id
        self.is_admin = is_admin

        logging.basicConfig(level=logging.DEBUG)

        # Param checking
        if environment == "production":
            api_path = "TDWebAPI"
        elif environment == "sandbox":
            api_path = "SBTDWebAPI"
        else:
            raise Exception("Environment must be 'production' or 'sanbox'")

        # Define http adapter
        self.session = requests.Session()
        retries = Retry(
            total=5, backoff_factor=1, status_forcelist=[502, 503, 504, 429]
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

        # Define urls
        self.tdx_api_base_url = f"https://{self.hostname}/{api_path}"
        if self.ticketing_app_id:
            self.tickets_url = (
                f"{self.tdx_api_base_url}/api/{self.ticketing_app_id}/tickets"
            )
        if self.asset_app_id:
            self.assets_url = f"{self.tdx_api_base_url}/api/{self.asset_app_id}/assets"
        if self.client_portal_app_id:
            self.kb_url = (
                f"{self.tdx_api_base_url}/api/{self.client_portal_app_id}/knowledgebase"
            )

        self.bearer_token = self.__authenticate()

        self.default_header = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json",
        }

        self.valid_custom_classes = self.__valid_custom_classes()

    def __authenticate(self):
        """
        Some TDX endpoints require administrative privileges.
        This method handles admin accounts, which has a different auth endpoint and OAuth params

        """
        if self.is_admin:
            auth_url = self.tdx_api_base_url + "/api/auth/loginadmin"
            payload = json.dumps(
                {"BEID": self.username, "WebServicesKey": self.password}
            )

        else:
            auth_url = self.tdx_api_base_url + "/api/auth"
            payload = json.dumps({"username": self.username, "password": self.password})

        headers = {
            "Content-Type": "application/json",
        }

        response = self.session.post(auth_url, headers=headers, data=payload)

        self.token = response.text

        return self.token

    def __valid_custom_classes(self):
        # Valid classes sent to PUT, PATCH or POST payload
        return (
            Ticket,
            TicketFeed,
            TicketType,
            AttributeChoice,
            Asset,
            AssetModel,
            KnowledgeArticle,
        )

    def __to_patch_payload(
        self, data_dict: dict, op: str = "replace"
    ) -> List[dict[str, Any]]:
        """
        Convert the JSON representation of the model into a PATCH payload format with parameterized op and path
        """
        payload = []
        for attr_name, attr_value in data_dict.items():
            if attr_value is not None:
                payload.append({"op": op, "path": f"/{attr_name}", "value": attr_value})
        return payload

    def __request(self, method: str, url: str, data=False):
        """
        Base method for TDX API Requests
        """
        methods = ["GET", "PUT", "PATCH", "POST", "DELETE"]
        if method not in methods:
            raise ValueError("Method must be one of GET, PUT, PATCH, POST, or DELETE")

        # Parse data
        if not data:
            pass
        # If data is a arbitrary dict, just json.dump it
        elif isinstance(data, dict):
            json_data = json.dumps(data)
        # if a class is being passed and the method is NOT PATCH, change it to dict, then json
        elif isinstance(data, self.valid_custom_classes) and method != "PATCH":
            json_data = json.dumps(data.to_dict())
        # if a class is being passed and it is PATCH then, prep that data as a patch object
        elif isinstance(data, self.valid_custom_classes) and method == "PATCH":
            data_dict = data.to_dict()
            patch_data = self.__to_patch_payload(data_dict=data_dict)
            json_data = json.dumps(patch_data)
        else:
            raise Exception(
                "Unable to determine what to do with the data provided. Check its type."
            )

        try:
            match method:
                case "GET":
                    response = self.session.get(url, headers=self.default_header)
                case "PUT":
                    logging.info(json_data)
                    response = self.session.put(
                        url, headers=self.default_header, data=json_data
                    )
                case "PATCH":
                    logging.info(patch_data)
                    response = self.session.patch(
                        url, headers=self.default_header, data=json_data
                    )
                case "POST":
                    logging.info(json_data)
                    response = self.session.post(
                        url, headers=self.default_header, data=json_data
                    )
                case "DELETE":
                    response = self.session.delete(url, headers=self.default_header)
            response.raise_for_status()

        except requests.exceptions.HTTPError as err:
            raise Exception(
                "Http Error: " + str(err), "Response content:", err.response.text
            )
        # except requests.exceptions.ConnectionError as errc:
        #    raise Exception("Error Connecting: " + str(errc),"Response content:", err.response.text)
        # except requests.exceptions.Timeout as errt:
        #    raise Exception("Timeout Error: " + str(errt))
        # except requests.exceptions.RequestException as err:
        #    raise Exception("Error: " + str(err))

        try:
            content_length = int(response.headers.get("Content-Length", 0))
        except ValueError:
            content_length = 0

        if content_length > 0:
            try:
                return response.json()
            except json.JSONDecodeError:
                raise Exception(
                    "JSON decoding error: Unable to parse response body as JSON"
                )
        else:
            return {"status_code": response.status_code}

    #
    # TICKETS
    #
    def get_ticket(self, id: int) -> Ticket:
        url = f"{self.tickets_url}/{id}"
        response = self.__request("GET", url=url)
        return Ticket(**response)

    def update_ticket(self, id: int, data: Ticket) -> Ticket:
        url = f"{self.tickets_url}/{id}"
        response = self.__request("PATCH", url=url, data=data)
        return Ticket(**response)

    def create_ticket(
        self,
        data: Ticket,
        notify_responsible: bool = False,
        notify_requestor: bool = False,
    ) -> Ticket:
        params = {
            "NotifyRequestor": notify_requestor,
            "NotifyResponsible": notify_responsible,
        }
        encoded_params = urlencode(params)

        url = f"{self.tickets_url}?{encoded_params}"
        response = self.__request("POST", url=url, data=data)
        return Ticket(**response)

    def add_asset_to_ticket(self, ticket_id: int, asset_id: int):
        url = f"{self.tickets_url}/{ticket_id}/assets/{asset_id}"
        return self.__request("POST", url=url)

    def get_ticket_feed(self, id: int) -> List[TicketFeed]:
        url = f"{self.tickets_url}/{id}/feed"
        response = self.__request("GET", url=url)
        return [TicketFeed(**item) for item in response]

    def create_ticket_feed_entry(self, id: int, data: TicketFeed) -> TicketFeed:
        url = f"{self.tickets_url}/{self.id}/feed"
        response = self.__request("POST", url=url, data=data)
        return TicketFeed(**response)

    #
    # TICKET TYPES
    #
    def get_types(self, is_active: bool = True) -> List[TicketType]:
        """
        Get ticket types
        """
        params = {"IsActive": is_active}
        encoded_params = urlencode(params)

        url = f"{self.tickets_url}/types?{encoded_params}"
        response = self.__request("GET", url=url)
        return [TicketType(**item) for item in response]

    #
    # ATTRIBUTES
    #

    def get_attribute_choices(self, attribute_id: int) -> List[AttributeChoice]:
        """
        Get attribute choices

        Requires Admin svc account
        """

        url = self.tdx_api_base_url + f"/api/attributes/{attribute_id}/choices"
        response = self.__request("GET", url=url)
        return [AttributeChoice(**item) for item in response]

    def create_attribute_choice(
        self, attribute_id: int, choice_name: str, is_active: bool = True
    ) -> AttributeChoice:
        """
        Create attribute choices
        """

        url = self.tdx_api_base_url + f"/api/attributes/{attribute_id}/choices"

        payload = {"Name": choice_name, "IsActive": is_active}
        response = self.__request("POST", url=url, data=payload)
        return AttributeChoice(**response)

    def update_attribute_choice(
        self, attribute_id: int, choice_id: int, data: AttributeChoice
    ) -> AttributeChoice:
        """
        Update an attribute choice

        """
        url = (
            self.tdx_api_base_url
            + f"/api/attributes/{attribute_id}/choices/{choice_id}"
        )
        response = self.__request("PUT", url=url, data=data)
        return AttributeChoice(**response)

    #
    # ASSET
    #
    def get_asset(
        self,
        asset_id: int,
    ) -> Asset:
        """
        Get a single TDX Asset
        """
        url = f"{self.assets_url}/{asset_id}"
        response = self.__request(method="GET", url=url)
        return Asset(**response)

    def get_assets(
        self,
        search_payload: dict,
    ) -> List[Asset]:
        """
        Search for assets
        """
        url = f"{self.assets_url}/search"
        response = self.__request(method="POST", url=url, data=search_payload)
        return [Asset(**item) for item in response]

    def update_asset(
        self,
        asset_id: int,
        data: Asset,
    ) -> Asset:
        """
        Patch a single TDX Asset
        """
        url = f"{self.assets_url}/{asset_id}"
        response = self.__request(method="PATCH", url=url, data=data)
        return Asset(**response)

    def create_asset(
        self,
        data: Asset,
    ) -> Asset:
        """
        Create an Asset
        """
        url = self.assets_url
        response = self.__request(method="POST", url=url, data=data)
        return Asset(**response)

    def get_asset_id_by_serial(self, serial_number: str) -> dict:
        """
        Get an asset ID by searching for serial number
        """

        search_payload = {"SerialLike": serial_number}
        search_url = f"{self.assets_url}/search"

        search_response_json = self.__request(
            "POST", url=search_url, data=search_payload
        )

        if len(search_response_json) > 1:
            print(
                f"{serial_number}: more than 1 asset using this serial number in application {self.asset_app_id}"
            )

        try:
            result = search_response_json[0]["ID"]
        except Exception as e:
            print(f"{serial_number}: not in TDX")
            return {"error": f"Serial not in TDX {serial_number}"}

        return {"ID": result}

    # Asset Models
    def get_asset_models(self) -> List[AssetModel]:
        url = f"{self.assets_url}/models"
        response = self.__request("GET", url=url)
        return AssetModel(**response)

    def create_asset_model(self, asset_model, manufacturer, product_type) -> AssetModel:
        """
        Create an asset model if it doesn't already exist.

        manufacturer e.g. Dell
        product_type e.g. Laptop
        """
        # Get product type id
        product_type_id = self.get_asset_product_type_id(
            asset_product_type_name=product_type
        )

        # Get manufacturers
        manufacturer_id = self.get_asset_manufacturer_id(
            asset_manufacturer_name=manufacturer
        )

        # We have IDs for product types and manufactuers now. So we can see if the model exists
        search_models = self.get_asset_models()

        search_model_results = [m.ID for m in search_models if m.Name == asset_model]

        if len(search_model_results) > 0:
            return {
                "message": f"""Asset Model: {asset_model} already exists""",
                "ID": search_model_results[0],
            }
        else:
            # Create asset model
            print(
                f"Creating asset model: {asset_model}, manufacterer id: {manufacturer_id}, product type id: {product_type_id}"
            )
            create_url = f"{self.assets_url}/models"
            asset_model = AssetModel(
                Name=asset_model,
                ManufacturerID=manufacturer_id,
                ProductTypeID=product_type_id,
            )

            response = self.__request("POST", url=create_url, data=asset_model)
            return AssetModel(**response)

    # Asset Product Types
    def get_asset_product_type_id(
        self,
        asset_product_type_name: str,
    ) -> int:
        product_types_url = f"{self.assets_url}/models/types"

        product_types = self.__request("GET", product_types_url)

        if not any(p["Name"] == asset_product_type_name for p in product_types):
            raise Exception(f"Product type {asset_product_type_name} does not exist")
        else:
            return [
                p["ID"] for p in product_types if p["Name"] == asset_product_type_name
            ][0]

    # Asset Manufacturers
    def get_asset_manufacturer_id(
        self,
        asset_manufacturer_name: str,
    ) -> int:
        manufacturers_url = f"{self.asset_app_id}/vendors"

        manufacturers = self.__request("GET", url=manufacturers_url)

        if not any(m["Name"] == asset_manufacturer_name for m in manufacturers):
            raise Exception(
                f"Vendor/manufacturer {asset_manufacturer_name} does not exist"
            )
        else:
            return [
                m["ID"] for m in manufacturers if m["Name"] == asset_manufacturer_name
            ][0]

    #
    # KNOWLEDGE
    #
    def get_kb_article(
        self,
        kb_article_id: int,
    ) -> KnowledgeArticle:
        """
        Get a single KB article
        """
        url = f"{self.kb_url}/{kb_article_id}"

        response = self.__request("GET", url=url)
        return KnowledgeArticle(**response)

    def update_kb_article(
        self,
        kb_article_id: int,
        data: KnowledgeArticle,
    ) -> KnowledgeArticle:
        """
        Edit a KB article
        """
        url = f"{self.kb_url}/{kb_article_id}"
        response = self.__request("PUT", url=url, data=data)
        return KnowledgeArticle(**response)

    def create_kb_article(
        self,
        data: KnowledgeArticle,
    ) -> KnowledgeArticle:
        """
        Create a KB article
        """
        url = self.kb_url
        response = self.__request(method="POST", url=url, data=data)
        return KnowledgeArticle(**response)

    def search_kb_articles(
        self,
        search_payload: dict,
    ) -> List[KnowledgeArticle]:
        """
        Search KB Articles

        {
            "CategoryID": 24493,
        }
        """
        url = f"{self.kb_url}/search"

        response = self.__request("POST", url=url, data=search_payload)
        return [KnowledgeArticle(**item) for item in response]
