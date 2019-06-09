import os
import csv
import random

from utils import random_string


def get_header_from_template(template_name):
    """
    Return the first row from a spreadsheet (.csv) to use as header row

    :param str template_name: The name of the spreadsheet to get header row from (looks in ./templates folder)
    :return strings
    :rtype: list(str)
    """
    # open file
    with open('./templates/%s.csv' % template_name, 'rt') as f:
        reader = csv.reader(f)

        # return the header row
        return next(reader)


class SpreadsheetGenerator:
    """
    Class that deals with the generation of spreadsheets (.csv)

    Attributes:
        out (str): The relative file dir to save the output spreadsheet
        skus (list(str)): list of skus to be used to generate orders
        ship_addrs (list(list)): list of US domestic addresses to be used for orders
    """
    def __init__(self, out):
        """

        :param str out: The relative file dir to save the output spreadsheet
        """
        self.out = out
        self.skus = []
        self.ship_addrs = [
            ["435 Indio Way", "Sunnyvale", "US", "Person1", "CA", "94085"],
            ["S 26th St", "West Des Moines", "US", "Person2", "IA", "50265"],
            ["3114 Glen Falls Road", "Highlands", "US", "Person3", "NC", "28741"],
            ["3033 Wilkinson Street", "Pea Ridge", "US", "Person4", "WV", "25705"]
        ]

    def write_products(self, quantity):
        """ Create a spreadsheet for use in product spreadsheet uploader (./results/products.csv)

        :param int quantity: The number of products to generate
        :return None
        :rtype: None
        """
        if not os.path.exists(self.out):
            os.makedirs(self.out)
        header_row = get_header_from_template('product')
        with open(self.out+'/products.csv', 'wt') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

            filewriter.writerow(header_row)

            i = 1
            while quantity > 0:
                sku = random_string()
                self.skus.append(sku)

                filewriter.writerow(
                    [
                        sku,  # sku
                        '',  # external_id
                        'Spreadsheet Test(%d)' % i,  # description
                        'TOYS_SPORTS_HOBBIES',  # category
                        14,  # length
                        2,  # width
                        4,  # height
                        1,  # weight
                        0,  # packaged_ready_to_ship
                        19.99,  # cost
                        39.99,  # wholesale
                        59.99,  # retail
                        '',  # UPC
                        '',  # EAN
                        'US',  # country_of_origin
                        950300  # HS_code
                    ])
                quantity -= 1
                i += 1

    def write_orders(self, quantity):
        """ Requires the products spreadsheet to exist
        Create a spreadsheet for use in order spreadsheet uploader (./results/orders.csv)

        :param int quantity: The number of orders to generate includes a random number of skus from sku spreadsheet
        :return None
        :rtype: None
        :raises: File not found exception
        """
        if not os.path.exists(self.out):
            os.makedirs(self.out)
        header_row = get_header_from_template('order')
        if not self.skus:
            exists = os.path.isfile(self.out+'/products.csv')
            if not exists:
                raise Exception('products.csv not found, generate it first!')
            with open(self.out+'/products.csv', 'rt') as f:
                reader = csv.reader(f)
                i = 0
                for row in reader:
                    if i != 0:
                        self.skus.append(row[0])
                    i += 1

        skus = self.skus
        with open(self.out+'/orders.csv', 'wt') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

            filewriter.writerow(header_row)

            while quantity > 0:
                order_no = random_string()
                address = self.ship_addrs[random.randrange(3)]
                random.shuffle(skus)
                sku = skus[0]

                sku_lines = random.randrange(10)

                filewriter.writerow(
                    [
                        order_no,  # order_no
                        '',  # external_id
                        '',  # order_date
                        address[3],  # name
                        address[0],  # address_1
                        '',  # address_2
                        '',  # address_3
                        address[1],  # city
                        address[4],  # state
                        address[5],  # zip
                        address[2],  # country
                        'fake@fake.com',  # email
                        '555-555-5555',  # phone
                        '',  # shipping_method
                        '',  # is_commercial
                        sku,  # sku
                        random.randrange(1, 5),  # quantity
                        'SpreadSheet Test'  # company_name
                    ])
                while sku_lines > 1:
                    random.shuffle(skus)
                    sku = skus[0]
                    filewriter.writerow(
                        [
                            order_no,  # order_no
                            '',  # external_id
                            '',  # order_date
                            address[3],  # name
                            address[0],  # address_1
                            '',  # address_2
                            '',  # address_3
                            address[1],  # city
                            address[4],  # state
                            address[5],  # zip
                            address[2],  # country
                            'fake@fake.com',  # email
                            '555-555-5555',  # phone
                            '',  # shipping_method
                            '',  # is_commercial
                            sku,  # sku
                            random.randrange(1, 5),  # quantity
                            'SpreadSheet Test'  # company_name
                        ])
                    sku_lines -= 1
                quantity -= 1
