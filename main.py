import time

import pandas as pd

from app import Processor


def main():
    df = pd.read_csv("data/public/main1.csv", nrows=10000)
    start_time = time.time()
    df["name"] = df["full_name"]
    processor = Processor(df)
    processor.clean_data()
    # processor.df.to_csv("data/main1_clean.csv", index=False)
    duplicates = processor.find_duplicates()
    # duplicates.to_csv("data/duplicates.csv", index=False)
    print(len(duplicates))
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
