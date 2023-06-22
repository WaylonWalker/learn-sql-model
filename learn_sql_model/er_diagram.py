import sqlite3

from graphviz import Digraph

from learn_sql_model.config import get_config

config = get_config()


def generate_er_diagram(output_path):
    # Connect to the SQLite database
    database_path = config.database_url.replace("sqlite:///", "")
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Get the table names from the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Create a new Digraph
    dot = Digraph(format="png")
    dot.attr(rankdir="TD")

    # Iterate over the tables
    for table in tables:
        table_name = table[0]
        dot.node(table_name, shape="box")
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()

        # Add the columns to the table node
        for column in columns:
            column_name = column[1]
            dot.node(f"{table_name}.{column_name}", label=column_name, shape="oval")
            dot.edge(table_name, f"{table_name}.{column_name}")

        # Check for foreign key relationships
        cursor.execute(f"PRAGMA foreign_key_list({table_name});")
        foreign_keys = cursor.fetchall()

        # Add dotted lines for foreign key relationships
        for foreign_key in foreign_keys:
            from_column = foreign_key[3]
            to_table = foreign_key[2]
            to_column = foreign_key[4]
            dot.node(f"{to_table}.{to_column}", shape="oval")
            dot.edge(
                f"{table_name}.{from_column}", f"{to_table}.{to_column}", style="dotted"
            )

    # Render and save the diagram
    dot.render(output_path.replace(".png", ""), cleanup=True)

    # Close the database connection
    cursor.close()
    conn.close()


def generate_er_markdown(output_path, er_diagram_path):
    # Connect to the SQLite database
    database_path = config.database_url.replace("sqlite:///", "")
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Get the table names from the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    with open(output_path, "w") as f:
        # Write the ER Diagram image
        f.write(f"![ER Diagram]({er_diagram_path})\n\n---\n\n")

        # Iterate over the tables
        for table in tables:
            table_name = table[0]

            f.write(f"## Table: {table_name}\n\n")

            # Get the table columns
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()

            f.write("### First 5 rows\n\n")
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
            rows = cursor.fetchall()
            f.write(f'| {" | ".join([c[1] for c in columns])} |\n')
            f.write("|")
            for column in columns:
                # ---
                f.write(f'{"-"*(len(column[1]) + 2)}|')
            f.write("\n")
            for row in rows:
                f.write(f'| {" | ".join([str(r) for r in row])} |\n')
            f.write("\n")

            cursor.execute(f"PRAGMA foreign_key_list({table_name});")
            foreign_keys = cursor.fetchall()

            # Add dotted lines for foreign key relationships
            fkeys = {}
            for foreign_key in foreign_keys:
                from_column = foreign_key[3]
                to_table = foreign_key[2]
                to_column = foreign_key[4]
                fkeys[from_column] = f"{to_table}.{to_column}"

            # Replace 'description' with the actual column name in the table that contains the description, if applicable
            try:
                cursor.execute(f"SELECT description FROM {table_name} LIMIT 1;")
                description = cursor.fetchone()
                if description:
                    f.write(f"### Description\n\n{description[0]}\n\n")
            except:
                ...

            # Write the table columns
            f.write("### Columns\n\n")
            f.write("| Column Name | Type | Foreign Key | Example Value |\n")
            f.write("|-------------|------|-------------|---------------|\n")

            for column in columns:

                column_name = column[1]
                column_type = column[2]
                fkey = ""
                if column_name in fkeys:
                    fkey = fkeys[column_name]
                f.write(f"| {column_name} | {column_type} | {fkey} |  |  |\n")

            f.write("\n")

            # Get the count of records
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            records_count = cursor.fetchone()[0]
            f.write(
                f"### Records Count\n\nThe table {table_name} contains {records_count} records.\n\n---\n\n"
            )

    # Close the database connection
    cursor.close()
    conn.close()


if __name__ == "__main__":
    # Usage example
    database_path = "database.db"
    md_output_path = "database.md"
    er_output_path = "er_diagram.png"

    generate_er_diagram(database_path, er_output_path)
    generate_markdown(database_path, md_output_path, er_output_path)
