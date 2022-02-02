## Using the BitPay Python light client

This SDK provides a convenient abstraction of BitPay's [cryptographically-secure API](https://bitpay.com/api) and allows payment gateway developers to focus on payment flow/e-commerce integration rather than on the specific details of client-server interaction using the API.  This SDK optionally provides the flexibility for developers to have control over important details, including the handling of private tokens needed for client-server communication.

### Dependencies

You must have a BitPay merchant account to use this SDK.  It's free to [sign-up for a BitPay merchant account](https://bitpay.com/start).

If you need a test account, please visit https://test.bitpay.com/dashboard/signup and register for a BitPay merchant test account. Please fill in all questions, so you get a fully working test account.
If you are looking for a testnet bitcoin wallet to test with, please visit https://bitpay.com/wallet and
create a new wallet.
If you need testnet bitcoin please visit a testnet faucet, e.g. https://testnet.coinfaucet.eu/en/ or http://tpfaucet.appspot.com/

For more information about testing, please see https://bitpay.com/docs/testing

### Usage

This library was built and tested using the Intellij IDE; the source code tree is directly compatible with Other Java IDEs.
You can also look ar the full JavaDoc for reference [here](http://htmlpreview.github.io/?https://github.com/bitpay/java-bitpay-light-client/blob/master/docs/JavaDoc/index.html)

### Getting your client token

First of all, you need to generate a new POS token on your BitPay's account which will be required to securely connect to the BitPay's API.  
For testing purposes use:  
https://test.bitpay.com/dashboard/merchant/api-tokens

For production use:  
https://bitpay.com/dashboard/merchant/api-tokens

Click on 'Add New Token', give a name on the Token Label input, leave the 'Require Authentication' checkbox unchecked and click on 'Add Token'.
The new token will appear and ready to use.


### Initializing your BitPay client

Once you have the token, you can initialize the client for the desired environment:

```python
from bitpay_light.client import Client

bitpay = Client("token", "Test")
```

### Create an invoice

```python
// Setting mandatory parameters in invoice i.e price and currency.
Invoice invoice = new Invoice(100.0, "USD")

# Setting invoice optional parameters
invoice.setOrderId("98e572ea-910e-415d-b6de-65f5090680f6")
invoice.setFullNotifications(True)
invoice.setExtendedNotifications(True)
invoice.setTransactionSpeed("medium")
invoice.setNotificationURL("https://hookbin.com/lJnJg9WW7MtG9GZlPVdj")
invoice.setRedirectURL("https://hookbin.com/lJnJg9WW7MtG9GZlPVdj")
invoice.setPosData("98e572ea35hj356xft8y8cgh56h5090680f6")
invoice.setItemDesc("Ab tempora sed ut.")
invoice.setNotificationEmail("")

# Creating Invoice
invoice = Invoice(2.16, "eur")
invoice.set_order_id("98e572ea-910e-415d-b6de-65f5090680f6")
invoice.set_full_notifications(True)
invoice.set_extended_notifications(True)
invoice.set_transaction_speed("medium")
invoice.set_notification_url("https://hookbin.com/lJnJg9WW7MtG9GZlPVdj")
invoice.set_redirect_url("https://hookbin.com/lJnJg9WW7MtG9GZlPVdj")
invoice.set_pos_data("98e572ea35hj356xft8y8cgh56h5090680f6")
invoice.set_item_desc("Ab tempora sed ut.")

basic_invoice = bitpay.create_invoice(invoice)
```

### Create an invoice (extended)

You can add optional attributes to the invoice.  Atributes that are not set are ignored or given default values.
```python
invoice = Invoice(2.16, "eur")
invoice.set_order_id("98e572ea-910e-415d-b6de-65f5090680f6")
invoice.set_full_notifications(True)
invoice.set_extended_notifications(True)
invoice.set_transaction_speed("medium")
invoice.set_notification_url("https://hookbin.com/lJnJg9WW7MtG9GZlPVdj")
invoice.set_redirect_url("https://hookbin.com/lJnJg9WW7MtG9GZlPVdj")
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

invoice.set_buyer(buyer)

basic_invoice = bitpay.create_invoice(invoice)
```

### Retreive an invoice

```python
retrieve_invoice = bitpay.get_invoice(invoice_id)
```

### Get exchange rates

You can retrieve BitPay's [BBB exchange rates](https://bitpay.com/exchange-rates).

```python
rates = bitpay.get_rates()

rate = rates.get_rate("USD")

rates.update()
```

### Create a bill

```python
# Create a list of items to add in the bill
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


bill = Bill("1001", Currency.USD, "sandbox@bitpay.com")
bill.set_items(items)
create_bill = bitpay.create_bill(bill)
print(create_bill.get_id())
```

### Retreive a bill

```python
get_bill = bitpay.get_bill(bill_id)
```

### Deliver a bill

```python
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


bill = Bill("1001", Currency.USD, "sandbox@bitpay.com")
bill.set_items(items)
create_bill = bitpay.create_bill(bill)
deliver_bill = bitpay.deliver_bill(create_bill.get_id(), create_bill.get_token())
```


See also the tests project for more examples of API calls.