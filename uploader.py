import requests
import os
import pprint


class SpreadsheetUploader:
    def __init__(
            self,
            base_url,
            username,
            password,
    ):
        """

        :param str base_url: Optional(default='test.com') - Application domain name
        :param str username: Optional(default='test+fakedev@fake.com') - account username
        :param str password: Optional(default='password') - Account password
        """
        self.base_url = base_url
        self.password = password
        self.username = username
        self.requests = None

    def login(self):
        """ Logs into a user account on shipwire

        :return None
        :rtype: None
        """
        url = 'https://' + self.base_url + '/login'
        print('Logging into url: ' + url)
        # print(self.username+':'+self.password)
        self.requests = requests.Session()
        response = self.requests.post(
            url,
            json={'user': self.username, 'pass': self.password},
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
            verify=False
        )
        response_data = response.json()
        pprint.pprint(response_data)

    def products(self):
        """ Requires ./results/products.csv
        Uploads a product spreadsheet via to an endpoint

        :return None
        :rtype: None
        :raises: File not found exception
        """
        exists = os.path.isfile('./results/products.csv')
        if not exists:
            raise Exception('products.csv not found, generate it first!')

        # Upload the spreadsheet to a server
        url = 'https://' + self.base_url + '/data/fileUpload/products'
        print('Upload products to : ' + url)
        file = {'file': open('./results/products.csv', 'rb')}
        response = self.requests.post(
            url,
            files=file,
            verify=False
        )

        response_data = response.json()
        pprint.pprint(response_data)

        name = response_data["result"]["data"][0]["name"]
        ext = response_data["result"]["data"][0]["extension"]
        submit_name = response_data["result"]["data"][0]["submitName"]
        errors = response_data["result"]["data"][0]["metadata"]["errors"]
        problem_products = response_data["result"]["data"][0]["metadata"]["problemProducts"]
        product_data = response_data["result"]["data"][0]["metadata"]["productData"]
        total = response_data["result"]["data"][0]["metadata"]["totalProducts"]

        data = {
            "errors": errors,
            "extension": ext,
            "fileData": [],
            "fileName": name,
            "problemProducts": problem_products,
            "processProducts": 1,
            "productData": product_data,
            "remoteFileName": submit_name,
            "totalEntries": total
        }

        # After the spreadsheet is parsed and validated submit the data for persistence
        # Submit the products from the uploaded spreadsheet
        url = 'https://' + self.base_url + '/data/productBulkSpreadsheet'
        print('Submit products to : ' + url)
        response = self.requests.post(
            url,
            json=data,
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
            verify=False
        )
        pprint.pprint(response)

    def orders(self):
        """ Requires ./results/orders.csv
        Uploads a order spreadsheet via upload to an endpoint

        :return None
        :rtype: None
        :raises: File not found exception
        """
        exists = os.path.isfile('./results/orders.csv')
        if not exists:
            raise Exception('orders.csv not found, generate it first!')

        file = {'file': open('./results/orders.csv', 'rb')}
        url = 'https://' + self.base_url + '/data/fileUpload/orders'
        print('Upload orders to : ' + url)
        response = self.requests.post(
            url,
            files=file,
            verify=False
        )

        response_data = response.json()
        pprint.pprint(response_data)

        submit_name = response_data["result"]["data"][0]["submitName"]

        data = {
            "email": self.username,
            "remoteFileName": submit_name
        }

        url = 'https://' + self.base_url + '/data/scheduleOrderUpload'
        print('Submit orders to : ' + url)
        response = self.requests.post(
            url,
            json=data,
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
            verify=False
        )
        pprint.pprint(response)

    def create_inventory_sql(self, quantity):
        """ Generates a ./results/stock.sql file for each product in the users account that will set stock to quantity

        :param int quantity: The number to set stock to
        :return None
        :rtype: None
        """
        if not os.path.exists('./results'):
            os.makedirs('./results')

        url = 'https://' + self.base_url + '/api/v3/products?limit=100'
        print('Fetching products from : ' + url)
        response = requests.get(
            url,
            auth=(self.username, self.password),
            verify=False
        )
        pprint.pprint(response)
        response_data = response.json()

        insert = 'INSERT INTO fulfillment_products_stock (product_id, warehouse_id, stock_good) VALUES'

        for product in response_data['resource']['items']:
            pid = product['resource']['id']
            insert += '(' + str(pid) + ',13,' + str(quantity) + '),'

        insert = insert[:-1]
        with open('./results/stock.sql', 'w') as file:
            file.write(insert)
