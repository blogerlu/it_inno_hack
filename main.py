import re
import time
from uuid import UUID

import pandas as pd
from clickhouse_driver import Client

from app import Processor

mode = "fast"


def check_table_exists(client, table_name):
    query = f"EXISTS TABLE {table_name}"
    try:
        return client.execute(query)[0][0]  # Возвращает True или False
    except:
        print(f"Error checking table")
        return False

table_name = 'table_dataset1'
client = Client(host='clickhouse', port=9000, user='default', password='', database='default')

# Проверяем доступность таблицы с интервалом в 5 секунд
while True:
    if check_table_exists(client, table_name):
        print(f"Таблица {table_name} доступна.")
        break
    else:
        print(f"Таблица {table_name} недоступна, пробую снова через 5 секунд...")
        time.sleep(5)

columns_1 = [column[0] for column in client.execute("DESCRIBE TABLE table_dataset1")]
columns_2 = [column[0] for column in client.execute("DESCRIBE TABLE table_dataset2")]
columns_3 = [column[0] for column in client.execute("DESCRIBE TABLE table_dataset3")]

for code in range(1040, 1040 + 32):
    letter = chr(code)  # Преобразуем код в символ
    print(letter)
    for code2 in range(1040, 1040 + 32):
        letter2 = chr(code2)
        for code3 in range(1040, 1040 + 32):
            letter3 = chr(code3)

        start_time = time.time()
        query_table_1 = f"SELECT * FROM table_dataset1 WHERE UPPER(full_name) LIKE '{letter}{letter2}{letter3}%';"
        query_table_2 = f"SELECT * FROM table_dataset2 WHERE UPPER(last_name) LIKE '{letter}{letter2}{letter3}%';"
        query_table_3 = (
            f"SELECT * FROM table_dataset3 WHERE splitByChar(' ', name)[2] LIKE '{letter}{letter2}{letter3}%';"
        )

        result1 = client.execute(query_table_1)
        result2 = client.execute(query_table_2)
        result3 = client.execute(query_table_3)

        df1 = pd.DataFrame(result1, columns=columns_1)
        df2 = pd.DataFrame(result2, columns=columns_2)
        df3 = pd.DataFrame(result3, columns=columns_3)

        df1.to_csv("df1.csv", index=False)
        df2.to_csv("df2.csv", index=False)
        df3.to_csv("df3.csv", index=False)

        # df1['uid_table1'] = df1['uid']
        df1["uid"] = df1["uid"].map(lambda x: "tb1 " + str(x))
        df1["name"] = df1["full_name"]

        # df2['uid_table2'] = df2['uid']
        df2["uid"] = df2["uid"].map(lambda x: "tb2 " + str(x))

        df2["name"] = df2["last_name"] + " " + df2["first_name"] + " " + df2["middle_name"]

        # df3['uid_table3'] = df3['uid']
        df3["uid"] = df3["uid"].map(lambda x: "tb3 " + str(x))

        df3["name"] = df3["name"].map(lambda x: x.split(" ")[1]) + " " + df3["name"].map(lambda x: x.split(" ")[0])

        df = pd.concat([df1, df2, df3])
        df.fillna("", inplace=True)

        print(time.time() - start_time)
        print(df.shape)
        # print(df)
        # df.to_csv("test.csv", index=False)

        processor = Processor(df)
        processor.clean_data()
        duplicates = processor.find_duplicates(mode=mode)
        # processor.df.to_csv("data/main1_clean.csv", index=False)
        # duplicates.to_csv("duplicates.csv", index=False)
        # print(time.time() - start_time)
        # total_duplicates_count += len(duplicates)

        k = duplicates.groupby("uid1")["uid2"].apply(lambda x: ", ".join(x)).reset_index()
        use_id = []
        for _, row in k.iterrows():
            cl1 = row["uid1"]
            cl2 = row["uid2"]
            cl = cl1 + cl2
            pattern = r"(tb[1-3])\s+([0-9a-fA-F-]+)"
            matches = re.findall(pattern, cl)

            data = {"tb1": [], "tb2": [], "tb3": []}
            flag = True
            for label, uid in matches:
                if UUID(uid) in use_id:
                    flag = False
                    break
                data[label].append(UUID(uid))
                use_id.append(UUID(uid))
            # print(data)
            # break
            if flag:
                client.execute(
                    "INSERT INTO table_results (id_is1, id_is2, id_is3) VALUES",
                    [(data["tb1"], data["tb2"], data["tb3"])],
                )
            #     break
        # break
        # break
    # break
