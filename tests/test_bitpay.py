"""
BitPay Unit Tests
"""
import unittest
from src.bitpay_light.client import Client
from src.bitpay_light.models.bill.bill import Bill
from src.bitpay_light.models.bill.item import Item
from src.bitpay_light.models.currency import Currency
from src.bitpay_light.models.invoice.buyer import Buyer
from src.bitpay_light.models.invoice.invoice import Invoice
from src.bitpay_light.models.bill.bill_status import BillStatus
from src.bitpay_light.env import TEST


class BitPayTest(unittest.TestCase):
    """
    Unit Test functions
    """

    __environment = TEST
    __token = "7STkLMsF5M98u5jCDLZrkN3Fv3wcRD956FQHWqv9biE"

    def setUp(self):
        self.client = Client(self.__token, self.__environment)

    def test_should_get_invoice_id(self):
        invoice = Invoice(2.16, "eur")
        invoice.set_order_id("98e572ea-910e-415d-b6de-65f5090680f6")
        invoice.set_full_notifications(True)
        invoice.set_extended_notifications(True)
        invoice.set_transaction_speed("medium")
        invoice.set_notification_url("https://hookbin.com/lJnJg9WW7MtG9GZlPVdj")
        invoice.set_redirect_u_r_l("https://hookbin.com/lJnJg9WW7MtG9GZlPVdj")
        invoice.set_pos_data("98e572ea35hj356xft8y8cgh56h5090680f6")
        invoice.set_item_desc("Ab tempora sed ut.")

        buyer = Buyer()
        buyer.set_name("Bily Matthews")
        buyer.set_email("sandbox@bitpay.com")
        buyer.set_address1("168 General Grove")
        buyer.set_address2("sandbox@bitpay.com")
        buyer.set_country("AD")
        buyer.set_locality("Port Horizon")
        buyer.set_notify(True)
        buyer.set_phone("+99477512690")
        buyer.set_postal_code("KY7 1TH")
        buyer.set_region("New Port")
        buyer.set_buyer_email("sandbox1@bitpay.com")
        invoice.set_buyer(buyer)

        basic_invoice = self.client.create_invoice(invoice)
        retrieve_invoice = self.client.get_invoice(basic_invoice.get_id())

        self.assertIsNotNone(basic_invoice.get_id())
        self.assertIsNotNone(retrieve_invoice.get_id())

    def test_should_create_invoice_btc(self):
        basic_invoice = self.client.create_invoice(Invoice(2.16, "btc"))
        self.assertIsNotNone(basic_invoice.get_id())

    def test_should_create_invoice_bch(self):
        basic_invoice = self.client.create_invoice(Invoice(2.16, "bch"))
        self.assertIsNotNone(basic_invoice.get_id())

    def test_should_create_invoice_eth(self):
        basic_invoice = self.client.create_invoice(Invoice(2.16, "eth"))
        self.assertIsNotNone(basic_invoice.get_id())

    def test_should_get_invoice_url(self):
        basic_invoice = self.client.create_invoice(Invoice(5.0, "usd"))
        self.assertIsNotNone(basic_invoice.get_url())

    def test_should_get_invoice_status(self):
        basic_invoice = self.client.create_invoice(Invoice(5.0, "usd"))
        self.assertEqual("new", basic_invoice.get_status())

    def test_should_create_invoice_one_tenth_btc(self):
        basic_invoice = self.client.create_invoice(Invoice(0.1, "btc"))
        self.assertEqual(0.1, basic_invoice.get_price())

    def test_should_create_invoice_100_usd(self):
        basic_invoice = self.client.create_invoice(Invoice(100.0, "usd"))
        self.assertEqual(100.0, basic_invoice.get_price())

    def test_should_create_invoice_100_eur(self):
        basic_invoice = self.client.create_invoice(Invoice(100.0, "eur"))
        self.assertEqual(100.0, basic_invoice.get_price())

    def test_should_get_invoice(self):
        basic_invoice = self.client.create_invoice(Invoice(5.0, "eur"))
        retrieved_invoice = self.client.get_invoice(basic_invoice.get_id())

        self.assertEqual(basic_invoice.get_id(), retrieved_invoice.get_id())

    def test_should_create_bill_usd(self):
        items = []

        item = Item()
        item.set_price(30.0)
        item.set_quantity(9)
        item.set_description("product-a")
        items.append(item)

        item = Item()
        item.set_price(14.0)
        item.set_quantity(16)
        item.set_description("product-b")
        items.append(item)

        item = Item()
        item.set_price(17.0)
        item.set_quantity(24)
        item.set_description("product-c")
        items.append(item)

        item = Item()
        item.set_price(4.0)
        item.set_quantity(46)
        item.set_description("product-d")
        items.append(item)

        bill = Bill("1001", Currency.USD, "sandbox@bitpay.com")
        bill.set_items(items)
        basic_bill = self.client.create_bill(bill)

        self.assertIsNotNone(basic_bill.get_id())
        self.assertIsNotNone(basic_bill.get_items()[0])

    def test_should_create_bill_eur(self):
        items = []

        item = Item()
        item.set_price(30.0)
        item.set_quantity(9)
        item.set_description("product-a")
        items.append(item)

        item = Item()
        item.set_price(14.0)
        item.set_quantity(16)
        item.set_description("product-b")
        items.append(item)

        item = Item()
        item.set_price(17.0)
        item.set_quantity(24)
        item.set_description("product-c")
        items.append(item)

        item = Item()
        item.set_price(4.0)
        item.set_quantity(46)
        item.set_description("product-d")
        items.append(item)

        bill = Bill("1002", Currency.EUR, "sandbox@bitpay.com")
        bill.set_items(items)
        basic_bill = self.client.create_bill(bill)

        self.assertIsNotNone(basic_bill.get_id())
        self.assertIsNotNone(basic_bill.get_items()[0])
        self.assertEqual(BillStatus.Draft, basic_bill.get_status())
        self.assertIsNotNone(basic_bill.get_url())

    def test_should_get_bill(self):
        items = []

        item = Item()
        item.set_price(30.0)
        item.set_quantity(9)
        item.set_description("product-a")
        items.append(item)

        item = Item()
        item.set_price(14.0)
        item.set_quantity(16)
        item.set_description("product-b")
        items.append(item)

        item = Item()
        item.set_price(17.0)
        item.set_quantity(24)
        item.set_description("product-c")
        items.append(item)

        item = Item()
        item.set_price(4.0)
        item.set_quantity(46)
        item.set_description("product-d")
        items.append(item)

        bill = Bill("1003", Currency.USD, "sandbox@bitpay.com")
        bill.set_items(items)
        basic_bill = self.client.create_bill(bill)
        retrieve_bill = self.client.get_bill(basic_bill.get_id())
        self.assertEqual(basic_bill.get_id(), retrieve_bill.get_id())
        self.assertEqual(len(basic_bill.get_items()), len(retrieve_bill.get_items()))

    def test_should_deliver_bill(self):
        items = []

        item = Item()
        item.set_price(30.0)
        item.set_quantity(9)
        item.set_description("product-a")
        items.append(item)

        item = Item()
        item.set_price(14.0)
        item.set_quantity(16)
        item.set_description("product-b")
        items.append(item)

        item = Item()
        item.set_price(17.0)
        item.set_quantity(24)
        item.set_description("product-c")
        items.append(item)

        item = Item()
        item.set_price(4.0)
        item.set_quantity(46)
        item.set_description("product-d")
        items.append(item)

        bill = Bill("1005", Currency.EUR, "sandbox@bitpay.com")
        bill.set_items(items)
        basic_bill = self.client.create_bill(bill)
        result = self.client.deliver_bill(basic_bill.get_id(), basic_bill.get_token())
        retrieve_bill = self.client.get_bill(basic_bill.get_id())

        self.assertEqual(basic_bill.get_id(), retrieve_bill.get_id())
        self.assertEqual(len(basic_bill.get_items()), len(retrieve_bill.get_items()))
        self.assertEqual("Success", result)
        self.assertEqual(BillStatus.Sent, retrieve_bill.get_status())

    def test_should_get_currencies(self):
        currency_list = self.client.get_currencies()
        self.assertIsNotNone(currency_list)

    def test_should_get_exchange_rates(self):
        rates = self.client.get_rates()
        rates_list = rates.get_rates()

        self.assertIsNotNone(rates_list)

    def test_should_get_eur_exchange_rate(self):
        rates = self.client.get_rates()
        rate = rates.get_rate(Currency.EUR)

        self.assertNotEqual(0, rate)

    def test_should_get_cny_exchange_rate(self):
        rates = self.client.get_rates()
        rate = rates.get_rate(Currency.CNY)

        self.assertNotEqual(0, rate)

    def test_should_update_exchange_rates(self):
        rates = self.client.get_currency_rates(Currency.ETH)
        rates.update()
        rates_list = rates.get_rates()

        self.assertIsNotNone(rates_list)

    def test_should_get_eth_to_usd_exchange_rate(self):
        rate = self.client.get_currency_pair_rate(Currency.ETH, Currency.USD)
        self.assertIsNotNone(rate)
