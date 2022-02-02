"""
HTTP methods
"""
import json
import urllib
import requests

from .. import env
from ..exceptions.bitpay_exception import BitPayException


class RESTcli:
    __headers = {}
    __baseurl = ""

    def __init__(self, environment):
        self.__baseurl = env.TESTURL if environment == env.TEST else env.PRODURL
        self.init()

    def init(self):
        try:
            self.__headers = {
                "x-accept-version": env.BITPAYAPIVERSION,
                "x-bitpay-plugin-info": env.BITPAYPLUGININFO,
                "x-bitpay-api-frame": env.BITPAYAPIFRAME,
                "x-bitpay-api-frame-version": env.BITPAYAPIFRAMEVERSION,
                "content-type": "application/json",
                "X-accept-version": "2.0.0",
            }
        except BitPayException as e:
            print(e)

    def post(self, uri, form_data):
        """
        :param uri: Url at which user wants to post the data
        :param form_data: the data to be posted
        with the request body
        :return: json response
        """
        full_url = self.__baseurl + uri
        form_data = json.dumps(form_data)

        response = requests.post(full_url, data=form_data, headers=self.__headers)
        json_response = self.response_to_json_string(response)
        return json_response

    def get(self, uri, parameters=None):
        """

        :param uri: Url from which user wants to get the data
        :param parameters: These are query parameters
        :return: json response
        """
        full_url = self.__baseurl + uri
        if parameters is not None:
            full_url = "%s?%s" % (full_url, urllib.parse.urlencode(parameters))

        response = requests.get(full_url, headers=self.__headers)
        json_response = self.response_to_json_string(response)
        return json_response

    def response_to_json_string(self, response):
        if not response:
            raise BitPayException("Error: HTTP response is null")

        response_obj = response.json()
        if "status" in response_obj:
            if response_obj["status"] == "error":
                raise BitPayException(
                    "Error: " + response_obj["error"], response_obj["code"]
                )

        if "error" in response_obj:
            raise BitPayException(
                "Error: " + response_obj["error"], response_obj["code"]
            )
        elif "errors" in response_obj:
            message = ""
            for error in response_obj["errors"]:
                message += "\n" + str(error)
            raise BitPayException("Errors: " + message)

        if "success" in response_obj:
            return response_obj["success"]

        if "data" in response_obj:
            return response_obj["data"]

        return response_obj
