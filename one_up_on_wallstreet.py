import argparse
from company import Company
from revision_checker import read_version_number

def print_program_version():
    print("="*30)
    print("One Up On Wallstreet v{}".format(read_version_number()))
    print("="*30)

def one_up_on_wallstreet(ticker):
    print_program_version()
    print("Ticker: {}".format(ticker))

    company = Company(ticker)

    top_selling_items = company.calculate_top_selling_items(ticker)

if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()

    # Add REQUIRED program cmd line arguments
    argument_parser_required = argument_parser.add_argument_group('REQUIRED')
    argument_parser_required.add_argument('-t', '--ticker', type=str, help='NYSE Ticker (ex. AMD or AAPL)', required=True)

    # Add OPTIONAL program cmd line arguments
    # argument_parser_required = argument_parser.add_argument_group('OPTIONAL')
    # argument_parser_required.add_argument('-e', '--example', type=str, help='Example optional argument', required=False)

    # Parse the command line arguments
    args = argument_parser.parse_args()

    one_up_on_wallstreet(args.ticker)