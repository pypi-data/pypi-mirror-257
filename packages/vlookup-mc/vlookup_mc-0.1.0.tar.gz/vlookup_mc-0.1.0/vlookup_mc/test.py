import argparse
from VLookup import VLookup

"""

 python3 test.py --file1 ~/tmp/vlookup/f1.csv --file2 ~/tmp/vlookup/f2.csv --key-col1 ID --key-col2 ID --output-file ~/tmp/vlookup/f12.csv
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perform VLOOKUP operation on two CSV files.")
    parser.add_argument("--file1", help="Path to the first CSV file")
    parser.add_argument("--file2", help="Path to the second CSV file")
    parser.add_argument("--key-col1", help="Column name for the key in the first CSV file")
    parser.add_argument("--key-col2", help="Column name for the key in the second CSV file")
    parser.add_argument("--output-file", help="Path to the output CSV file")

    args = parser.parse_args()

    vlookup_processor = VLookup(args)
    vlookup_processor.vlookup()