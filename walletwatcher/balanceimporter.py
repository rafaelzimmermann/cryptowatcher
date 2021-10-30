import sys
from typing import List

from walletwatcher.parser import Parser, ExodusParser


class BalanceImporter:

    def __init__(self, parsers: List[Parser]):
        for importer in parsers:
            for transaction in importer.transactions():
                print(transaction)


if __name__ == '__main__':
    bi = BalanceImporter(parsers=[ExodusParser(sys.argv[1])])
