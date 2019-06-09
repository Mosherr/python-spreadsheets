import argparse

from generator import SpreadsheetGenerator
from uploader import SpreadsheetUploader


def main():
    text = 'Tool for generating product & order spreadsheets, can also curl them to a server.'
    parser = argparse.ArgumentParser(description=text)
    parser.add_argument("-u", "--url", help="Base url for curl (sample.com)")
    parser.add_argument("-e", "--email", help="Email username for auth (test@test.com)")
    parser.add_argument("-p", "--password", help="Password for auth (abc123)")

    parser.add_argument("-gp", "--gproducts", help="Generate product spreadsheet of quantity (-gp=1000)")
    parser.add_argument("-go", "--gorders", help="Generate order spreadsheet of quantity (-go=1000)")
    parser.add_argument("-up", "--uproducts", help="Upload the product spreadsheet", action="store_true")
    parser.add_argument("-uo", "--uorders", help="Upload the order spreadsheet", action="store_true")

    parser.add_argument("-gs", "--gstock", help="Generate stock sql for previously generated product spreadsheet")
    parser.add_argument("-o", "--out", help="The relative file dir to save the output spreadsheet")

    # read arguments from the command line
    args = parser.parse_args()

    base_url = 'developer.corp.shipwire.com'
    username = 'test+fakedev@shipwire.com'
    password = 'password'
    out = './results'
    if args.url:
        base_url = args.url
    if args.email:
        username = args.email
    if args.password:
        password = args.password
    if args.out:
        out = args.out

    generator = SpreadsheetGenerator(out=out)
    uploader = SpreadsheetUploader(base_url=base_url, username=username, password=password)

    if args.gproducts:
        generator.write_products(quantity=int(args.gproducts))
    if args.gorders:
        generator.write_orders(quantity=int(args.gorders))
    if args.uproducts:
        uploader.login()
        uploader.products()
    if args.uorders:
        uploader.login()
        uploader.orders()
    if args.gstock:
        uploader.create_inventory_sql(quantity=int(args.gstock))


if __name__ == '__main__':
    main()
