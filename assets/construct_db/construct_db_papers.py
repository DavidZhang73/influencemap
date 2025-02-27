import sqlite3, os
from datetime import datetime
from construct_db_func import build_coltype, construct_table, import_to_table, create_index
import construct_db_config as cfg

# Input data directory
data_dir = cfg.data_dir

# database path
db_path = cfg.db_path

# Table details
table_name = 'papers'
table_col = ['paper_id', 'conf_id', 'journ_id', 'pub_year']
table_type = ['text', 'text', 'text', 'int']
table_coltype = build_coltype(table_col, table_type)

# Data file details
data_file = 'Papers.txt'
data_ids = [0, 9, 8, 3]
data_path = os.path.join(data_dir, data_file)

def construct_papers():
    conn = sqlite3.connect(db_path)

    # Construct table
    construct_table(conn, table_name, table_coltype, override=True)

    # Import data to table
    import_to_table(conn, table_name, data_path, table_col, data_ids)

    # Index first column
    create_index(conn, table_name, table_col[0])
         
    # Save
    conn.commit()
    conn.close()

if __name__ == '__main__':
    construct_papers()
