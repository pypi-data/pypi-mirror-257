import pandas as pd


class VLookup:
    def __init__(self, args):
        self.file1 = args.file1
        self.file2 = args.file2
        self.key_col1 = args.key_col1
        self.key_col2 = args.key_col2
        self.output_file = args.output_file

    def vlookup(self):
        # Read CSV files into DataFrames
        df1 = pd.read_csv(self.file1)
        df2 = pd.read_csv(self.file2)

        # Perform VLOOKUP
        merged_df = pd.merge(df1, df2, how='left', left_on=self.key_col1, right_on=self.key_col2)

        # Write the merged DataFrame to CSV
        merged_df.to_csv(self.output_file, index=False)


