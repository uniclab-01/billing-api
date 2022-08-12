from datetime import datetime
from typing import Optional, List, Dict, Tuple, Any
from uuid import UUID

import requests

from unicboard_billing_sdk.response_models import GetDeviceListInfoResponse, GetDeviceInfoResponse, GetDeviceValueResponse
from unicboard_billing_sdk.utils import get_device_value_structure, get_device_info_structure, get_device_list_info_structure


# It's a wrapper around the billing API
class BillingApiSdk:

    def __init__(self, api_billing_url: str, api_token: str) -> None:
        """
        This function initializes the class with the billing API URL and the API token.

        Args:
          api_billing_url (str): The URL of the API Billing endpoint.
          api_token (str): The API token you received from the billing system.
        """
        self._api_billing_url = api_billing_url
        self._api_token = api_token

    def get_device_list_info(
            self,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            filters: Optional[List[Dict[str, Any]]] = None,
            sorts: Optional[List[Tuple[str, str]]] = None,
    ) -> GetDeviceListInfoResponse:
        """
        It makes a GET request to the `/api/v1/devices/info` endpoint, and returns the response as a
        `GetDeviceListInfoResponse` object
        Args:
         limit (Optional[int]): The maximum number of devices to return.
         offset (Optional[int]): The offset of the first device to return.
         filters (Optional[List[Dict[str, Any]]]): A list of dictionaries, each of which contains a key and a value.
         The key is the name of the field to filter on, and the value is the value to filter on.
         sorts (Optional[List[Tuple[str, str]]]): A list of tuples, where each tuple is a field name and a sort direction.

        Returns:
            A list of devices.

        [GetDeviceListInfoResponse](GetDeviceListInfoResponse.md)
        """

        auth_header = {'Authorization': f'Bearer {self._api_token}'}
        query_params: Dict[str, Any] = {
            "filter": filters,
            "sort": sorts,
        }
        if limit is not None:
            query_params['limit'] = limit
        if offset is not None:
            query_params['offset'] = offset

        response = requests.get(
            f'{self._api_billing_url}/'
            f'api/v1/devices/info',
            params=query_params,
            headers=auth_header,
        )
        response.raise_for_status()
        return get_device_list_info_structure(response.json())

    def get_device_list_by_id_info(self, device_ids: List[UUID]) -> GetDeviceListInfoResponse:
        """
        It takes a list of device IDs and returns a list of device info objects

        Args:
          device_ids (List[UUID]): List[UUID]

        Returns:
          A list of devices.
        [GetDeviceListInfoResponse](GetDeviceListInfoResponse.md)
        """
        auth_header = {'Authorization': f'Bearer {self._api_token}'}

        device_ids_str = [str(device_id) for device_id in device_ids]
        response = requests.post(
            f'{self._api_billing_url}/'
            f'api/v1/devices/info',
            headers=auth_header,
            json={'device_ids': device_ids_str},
        )
        response.raise_for_status()
        return get_device_list_info_structure(response.json())

    def get_device_info(self, device_id: UUID) -> GetDeviceInfoResponse:
        """
        > This function takes a device ID and returns a `GetDeviceInfoResponse` object

        Args:
          device_id (UUID): The UUID of the device you want to get information about.

        Returns:
          A GetDeviceInfoResponse object. Status of payload information in device list)
        [GetDeviceInfoResponse](GetDeviceInfoResponse.md)
        """
        auth_header = {'Authorization': f'Bearer {self._api_token}'}

        response = requests.get(
            f'{self._api_billing_url}/'
            f'api/v1/devices/{str(device_id)}/info',
            headers=auth_header,
        )
        response.raise_for_status()
        return get_device_info_structure(response.json())

    def get_device_value(
            self,
            devices_id: List[UUID],
            period_from: datetime,
            period_to: datetime = None,
    ) -> GetDeviceValueResponse:
        """
        It gets the value of a device

        Args:
          devices_id (List[UUID]): List[UUID] - list of device IDs
          period_from (datetime): The start of the period for which you want to get the data.
          period_to (datetime): datetime = None

        Returns:
          GetDeviceValueResponse: response about device value
        [GetDeviceValueResponse](GetDeviceValueResponse.md)
        """
        auth_header = {'Authorization': f'Bearer {self._api_token}'}
        query_params: Dict[str, Any] = {
            "period_from": period_from,
            "period_to": period_to,
        }
        devices_id = [str(device_id) for device_id in devices_id]

        response = requests.post(
            f'{self._api_billing_url}/'
            f'/api/v1/devices/values',
            params=query_params,
            headers=auth_header,
            json={"devices_id": devices_id},
        )
        response.raise_for_status()
        return get_device_value_structure(response.json())
