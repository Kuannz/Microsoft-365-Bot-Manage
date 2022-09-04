# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/2 20:44
@Author: Mr.lin
@Version: v1
@File: role
"""
from ..requests import *
from ..module import *


@module
class Role:

    def __init__(self, requests: Requests):
        self._req = requests

    # def get_template(self):
    #     """
    #     Get the role template and format it as role.json
    #
    #     :return:{"displayName": "id", ...}
    #     """
    #     params = {"$select": "displayName, id, description"}
    #     res = self._req.get(url="/directoryRoleTemplates", params=params)
    #     data = res.json()["value"]
    #     print({ro.pop("displayName"): ro["id"] for ro in data})

    def get_all(self) -> dict[dict]:
        """
        List the directory roles that are activated in the tenant.

        :return: {"displayName": "id", ...}
        """
        params = {"$select": "displayName, id"}
        res = self._req.get(url="/directoryRoles", params=params)
        return res.json()["value"]

    def get_info(self, role_id: str) -> dict:
        """
        Get role's detailed information by id

        :param role_id:
        :return:{displayName:xxx, description:xxx}
        """
        url = f"/directoryRoles/roleTemplateId={role_id}"
        params = {"$select": "displayName, description"}
        res = self._req.get(url=url, params=params)
        info = res.json()
        info.pop("@odata.context")
        return info

    def get_member(self, role_id: str) -> list[dict]:
        """
        Retrieve the list of principals that are assigned to the directory role.

        :param role_id:
        :return: [{"userPrincipalName":xxx}, {""userPrincipalName":yyy}...]
        """
        url = f"/directoryRoles/roleTemplateId={role_id}/members/microsoft.graph.user"
        params = {"$select": "userPrincipalName"}
        res = self._req.get(url=url, params=params)
        return res.json()['value']

    def add_member(self, role_id: str, user_id: str):
        """
        Assign a role to a specified user

        :param role_id:
        :param user_id:
        :return:
        """
        url = f"/directoryRoles/roleTemplateId={role_id}/members/$ref"
        json = {
            "@odata.id": f"https://graph.microsoft.com/v1.0/directoryObjects/{user_id}"
        }
        self._req.post(url=url, json=json)

    def del_member(self, role_id, user_id):
        """
        Remove a member from a directoryRole.

        :param role_id:
        :param user_id:
        :return:
        """
        url = f"/directoryRoles/roleTemplateId={role_id}/members/{user_id}/$ref"
        self._req.delete(url)
