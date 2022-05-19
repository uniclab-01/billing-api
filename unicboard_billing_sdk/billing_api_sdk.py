from datetime import datetime
from typing import Optional, List, Dict, Tuple, Any
from uuid import UUID

import requests

from unicboard_billing_sdk.response_models import GetDeviceListInfoResponse, GetDeviceInfoResponse, GetDeviceValueResponse
from unicboard_billing_sdk.utils import get_device_value_structure, get_device_info_structure, get_device_list_info_structure


class BillingApiSdk:

    def __init__(self, api_billing_url: str, api_token: str) -> None:
        self._api_billing_url = api_token
        self._api_token = api_billing_url

    def get_device_list_info(
            self,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            filters: Optional[List[Dict[str, Any]]] = None,
            sorts: Optional[List[Tuple[str, str]]] = None,
    ) -> GetDeviceListInfoResponse:
        auth_header = {'Authorization': f'Bearer {self._api_token}'}
        query_params: Dict[str, Any] = {
            "filters": filters,
            "sorts": sorts,
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

    def get_device_info(self, device_id: UUID) -> GetDeviceInfoResponse:
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
