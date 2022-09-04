# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/1 18:27
@Author: Mr.lin
@Version: v1
@File: sub
"""
from ..requests import *
from ..module import *


@module
class Sub:

    def __init__(self, requests: Requests):
        self._req = requests

    def get_all(self) -> list:
        """
        Get all subscribes from this global

        :return:
        """
        params = {"$select": "skuPartNumber, skuId, id"}
        res = self._req.get(url="/subscribedSkus", params=params)
        return res.json()["value"]

    def get_info(self, sku_id: str) -> dict:
        """

        :param sku_id:
        :return:
        """
        params = {
            "$select": "capabilityStatus,consumedUnits,prepaidUnits,skuId,skuPartNumber"
        }
        res = self._req.get(url=f"/subscribedSkus/{sku_id}", params=params)
        data: dict = res.json()
        data.pop('@odata.context')
        return data
