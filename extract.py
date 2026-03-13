import os                                                                                                                 
import json                                                                                                               
import pandas as pd                                                                                                       
import psycopg2                                             
from datetime import datetime

# --- Config ---
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "erp_dev",
    "user": "erp_user",
    "password": "erp_pass"
}

TABLES = ["work_orders", "bom", "inventory", "vendors"]
STATE_FILE = "last_run.json"
OUTPUT_DIR = "raw"

# --- Load last run timestamp ---
def load_last_run():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)["last_run"]
    return "2000-01-01 00:00:00"

# --- Save last run timestamp ---
def save_last_run(timestamp):
    with open(STATE_FILE, "w") as f:
        json.dump({"last_run": timestamp}, f)

# --- Extract one table incrementally ---
def extract_table(cur, table, last_run):
    query = f"SELECT * FROM {table} WHERE updated_at > %s"
    cur.execute(query, (last_run,))
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    return pd.DataFrame(rows, columns=columns)

# --- Write to Parquet, partitioned by date ---
def write_parquet(df, table, date_str):
    folder = os.path.join(OUTPUT_DIR, table, date_str)
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{table}.parquet")
    df.to_parquet(path, index=False, engine="pyarrow")
    print(f"  Wrote {len(df)} rows to {path}")

# --- Main ---
def main():
    last_run = load_last_run()
    run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_str = datetime.now().strftime("%Y/%m/%d")

    print(f"Extracting data updated since: {last_run}")

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    for table in TABLES:
        print(f"Extracting {table}...")
        df = extract_table(cur, table, last_run)
        if df.empty:
            print(f"  No new data for {table}")
        else:
            write_parquet(df, table, date_str)

    cur.close()
    conn.close()

    save_last_run(run_time)
    print(f"Done. Last run saved as: {run_time}")

if __name__ == "__main__":
    main()