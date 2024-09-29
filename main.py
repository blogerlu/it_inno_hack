import time

import pandas as pd
from tqdm import tqdm

from app import Processor


def main():
    total_time = 0
    total_duplicates_count = 0

    batch_size = 10000
    batch_count = 1
    mode = "fast"

    print(f"Total rows count: {batch_size * batch_count}")
    for i in tqdm(range(batch_count)):
        df = pd.read_csv("data/public/main1.csv", nrows=batch_size * (i + 1))[batch_size * i :]
        start_time = time.time()
        df["name"] = df["full_name"]
        # df["name"] = df["last_name"] + " " + df["first_name"] + " " + df["middle_name"]
        processor = Processor(df)
        processor.clean_data()
        duplicates = processor.find_duplicates(mode=mode)
        processor.df.to_csv("data/main1_clean.csv", index=False)
        duplicates.to_csv("data/duplicates.csv", index=False)
        total_time += time.time() - start_time
        total_duplicates_count += len(duplicates)
    print(f"Found duplicates: {total_duplicates_count}")
    print("--- %s seconds ---" % total_time)


if __name__ == "__main__":
    main()
