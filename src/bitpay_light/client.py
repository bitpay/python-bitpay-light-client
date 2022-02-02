"""
Class Client
package Bitpay light
author  Antonio Buedo
version 1.0.2201
See bitpay.com/api for more information.
"""

from . import env
from .models.bill.bill import Bill
from .models.rate.rate import Rate
from .utils.rest_cli import RESTcli
from .models.rate.rates import Rates
from .models.currency import Currency
from .models.invoice.invoice import Invoice
from .exceptions.bitpay_exception import BitPayException
from .exceptions.bill_query_exception import BillQueryException
from .exceptions.rate_query_exception import RateQueryException
from .exceptions.bill_creation_exception import BillCreationException
from .exceptions.invoice_query_exception import InvoiceQueryException
from .exceptions.bill_delivery_exception import BillDeliveryException
from .exceptions.currency_query_exception import CurrencyQueryException
from .exceptions.invoice_creation_exception import InvoiceCreationException


class Client:
    """
    * Class Client
    * @package Bitpay
    * @author  Antonio Buedo
    * @version 1.0.2201
    * See bitpay.com/api for more information.
    """

    __env = None
    __token = None
    __restcli = None

    def __init__(self, token: str, environment: str):
        try:
            self.__token = token
            self.__env = env.TEST if environment.lower() == "test" else env.PROD
            self.init()
        except Exception as exe:
            raise BitPayException(
                "failed to initialize BitPay Light Client (Config) " + str(exe)
            )

    def init(self):
        try:
            self.__restcli = RESTcli(self.__env)
        except Exception as exe:
            raise BitPayException("failed to build configuration : " + str(exe))

    # //////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////////////////////

    def create_invoice(self, invoice: Invoice) -> Invoice:
        """
        Create a BitPay invoice

        :param Invoice invoice: An Invoice object with request parameters defined
        :return: A BitPay generated Invoice object
        :rtype: Invoice
        :raises BitPayException
        :raises InvoiceCreationException
        """
        try:
            invoice.set_token(self.__token)
            response_json = self.__restcli.post("invoices", invoice.to_json())
        except BitPayException as exe:
            raise InvoiceCreationException(
                "failed to serialize Invoice object : " "%s" % str(exe),
                exe.get_api_code(),
            )
        except Exception as exe:
            raise InvoiceCreationException(
                "failed to serialize Invoice object : %s" % str(exe)
            )

        try:
            invoice = Invoice(**response_json)
        except Exception as exe:
            raise InvoiceCreationException(
                "failed to deserialize BitPay server response "
                "(Invoice) : %s" % str(exe)
            )

        return invoice

    def get_invoice(self, invoice_id: str) -> Invoice:
        """
        Retrieve a BitPay invoice by invoice id using the specified facade.
        The client must have been previously authorized for the specified
        facade (the public facade requires no authorization)

        :param str invoice_id: The id of the invoice to retrieve
        :return: A BitPay Invoice object
        :rtype: Invoice
        :raises BitPayException
        :raises InvoiceQueryException
        """
        try:
            params = {"token": self.__token}
            response_json = self.__restcli.get("invoices/%s" % invoice_id, params)
        except BitPayException as exe:
            raise InvoiceQueryException(
                "failed to serialize Invoice object : " "%s" % str(exe),
                exe.get_api_code(),
            )
        except Exception as exe:
            raise InvoiceQueryException(
                "failed to serialize Invoice object :" " %s" % str(exe)
            )

        try:
            invoice = Invoice(**response_json)
        except Exception as exe:
            raise InvoiceQueryException(
                "failed to deserialize BitPay server response"
                " (Invoice) : %s" % str(exe)
            )

        return invoice

    def create_bill(self, bill: Bill) -> Bill:
        """
        Create a BitPay Bill.

        :param Bill bill: A Bill object with request parameters defined.
        :return: A BitPay generated Bill object.
        :rtype: Bill
        :raises BitPayException
        :raises BillCreationException
        """
        try:
            bill.set_token(self.__token)
            response_json = self.__restcli.post("bills", bill.to_json())
        except BitPayException as exe:
            raise BillCreationException(
                "failed to serialize bill object :  %s" % str(exe), exe.get_api_code()
            )

        try:
            bill = Bill(**response_json)
        except Exception as exe:
            raise BillCreationException(
                "failed to deserialize BitPay server response (Bill) : %s" % str(exe)
            )

        return bill

    def get_bill(self, bill_id: str) -> Bill:
        """
        Retrieve a BitPay bill by bill id using the specified facade.

        :param str bill_id: The id of the bill to retrieve.
        :return: A BitPay Bill object.
        :rtype: Bill
        :raises BitPayException
        :raises BillQueryException
        """
        try:
            params = {"token": self.__token}
            response_json = self.__restcli.get("bills/%s" % bill_id, params)
        except BitPayException as exe:
            raise BillQueryException(
                "failed to serialize bill object :  %s" % str(exe), exe.get_api_code()
            )

        try:
            bill = Bill(**response_json)
        except Exception as exe:
            raise BillQueryException(
                "failed to deserialize BitPay server response" " (Bill) : %s" % str(exe)
            )
        return bill

    def deliver_bill(self, bill_id: str, bill_token: str) -> bool:
        """
        Deliver a BitPay Bill.

        :param str bill_id: The id of the requested bill.
        :param str bill_token: The token of the requested bill.
        :return: A response status returned from the API.
        :rtype: bool
        :raises BitPayException
        :raises BillDeliveryException
        """
        try:
            params = {"token": bill_token}
            response_json = self.__restcli.post(
                "bills/%s" % bill_id + "/deliveries", params
            )
        except BitPayException as exe:
            raise BillDeliveryException(
                "failed to serialize bill object :  %s" % str(exe), exe.get_api_code()
            )

        try:
            result = response_json
        except Exception as exe:
            raise BillDeliveryException(
                "failed to deserialize BitPay server response" " (Bill) : %s" % str(exe)
            )
        return result

    def get_currencies(self) -> [Currency]:
        """
        Fetch the supported currencies.

        :return: A list of BitPay Invoice objects.
        :rtype: [Currency]
        :raises BitPayException
        :raises CurrencyQueryException
        """
        try:
            response_json = self.__restcli.get("currencies", None)
        except BitPayException as exe:
            raise CurrencyQueryException(
                "failed to serialize Currency object :  %s" % str(exe),
                exe.get_api_code(),
            )

        try:
            currencies = []
            for currency in response_json:
                currencies.append(Currency(**currency))
        except Exception as exe:
            raise CurrencyQueryException(
                "failed to deserialize BitPay server response "
                " (Currency) : %s" % str(exe)
            )
        return currencies

    def get_rates(self) -> [Rates]:
        """
        Retrieve the exchange rate table maintained by BitPay.  See https://bitpay.com/bitcoin-exchange-rates.

        :return: A Rates object populated with the BitPay exchange rate table.
        :rtype: [Rates]
        :raises BitPayException
        :raises RateQueryException
        """
        try:
            response_json = self.__restcli.get("rates", None)
        except BitPayException as exe:
            raise RateQueryException(
                "failed to serialize Rates object :  %s" % str(exe), exe.get_api_code()
            )

        try:
            rates = []
            for rate in response_json:
                rates.append(Rate(**rate))
            rates = Rates(rates, self)
        except Exception as exe:
            raise RateQueryException(
                "failed to deserialize BitPay server response "
                " (Rates) : %s" % str(exe)
            )
        return rates

    def get_currency_rates(self, base_currency: str) -> [Rates]:
        """
        Retrieve all the rates for a given cryptocurrency

        :param str base_currency: The cryptocurrency for which you want to fetch the rates.
        Current supported values are BTC, BCH, ETH, XRP, DOGE and LTC
        :return: A Rates object populated with the currency rates for the requested baseCurrency.
        :rtype: [Rates]
        :raises BitPayException
        :raises RateQueryException
        """
        try:
            response_json = self.__restcli.get("rates/%s" % base_currency, None)
        except BitPayException as exe:
            raise RateQueryException(
                "failed to serialize Rates object :  %s" % str(exe), exe.get_api_code()
            )

        try:
            rates = []
            for rate in response_json:
                rates.append(Rate(**rate))
            rates = Rates(rates, self)
        except Exception as exe:
            raise RateQueryException(
                "failed to deserialize BitPay server response "
                " (Rates) : %s" % str(exe)
            )
        return rates

    def get_currency_pair_rate(self, base_currency: str, currency: str) -> Rate:
        """
        Retrieve the rate for a cryptocurrency / fiat pair

        :param str base_currency: The cryptocurrency for which you want to fetch the fiat-equivalent rate.
        Current supported values are BTC, BCH, ETH, XRP, DOGE and LTC
        :param str currency: The fiat currency for which you want to fetch the baseCurrency rate
        :return: A Rate object populated with the currency rate for the requested baseCurrency.
        :rtype: Rate
        :raises BitPayException
        :raises RateQueryException
        """
        try:
            response_json = self.__restcli.get(
                "rates/%s" % base_currency + "/%s" % currency, None
            )
        except BitPayException as exe:
            raise RateQueryException(
                "failed to serialize Rates object :  %s" % str(exe), exe.get_api_code()
            )

        try:
            rate = Rate(**response_json)
        except Exception as exe:
            raise RateQueryException(
                "failed to deserialize BitPay server response "
                " (Rate) : %s" % str(exe)
            )
        return rate
