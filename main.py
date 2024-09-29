import time

import pandas as pd

from app import Processor


def main():
    total_time = 0

    batch_size = 1000
    batch_count = 10
    for i in range(batch_count):
        df = pd.read_csv("data/public/main1.csv", nrows=batch_size * (i + 1))[batch_size * i :]
        start_time = time.time()
        df["name"] = df["full_name"]
        # df["name"] = df["last_name"] + " " + df["first_name"] + " " + df["middle_name"]
        processor = Processor(df)
        processor.clean_data()
        duplicates = processor.find_duplicates()
        # processor.df.to_csv("data/main1_clean.csv", index=False)
        # duplicates.to_csv("data/duplicates.csv", index=False)
        total_time += time.time() - start_time
        print(len(duplicates))
    print("--- %s seconds ---" % total_time)


if __name__ == "__main__":
    main()
