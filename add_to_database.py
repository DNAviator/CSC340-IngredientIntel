import csv


class CsvToSql:
  """
  Class to convert data from a CSV file to SQL INSERT statements.
  """

  def __init__(self, filename, table_name, uniqueKey, output_file_path=""):
    """
    Initializes the class with filename and target table name.

    Args:
        filename: Path to the CSV file.
        table_name: Name of the target table in the database.
    """
    self.filename = filename
    self.table_name = table_name
    self.headers = None
    self.data_types = None
    self.uniqueKey = uniqueKey


  def generate_insert_statements(self):
    """
    Reads data from the CSV file and generates individual INSERT statements.

    Writes the statements to a file named 'data_import.sql'.
    """
    with open(self.filename, "r") as csvfile:
      reader = csv.reader(csvfile)
      self.headers = next(reader)       # Get headers from the first row

      self.headers = [_.replace(' ', '_') for _ in self.headers]    # replace spaces with underscores
      self.columns = ", ".join(f'"{_}"' for _ in self.headers)      # join all headers with proper formatting for sql
      placeholders = ", ".join(["'%s'" for _ in self.headers])      # create a placeholder script for easy insertion of values later
      placeholders = f"({placeholders})"                            # wrap placeholders with () for sql
      self.base_sql = f"""INSERT INTO "{self.table_name}" ({self.columns}) VALUES """       # finish formatting first row of sql statement


      # Open file for writing SQL statements
      with open("data_import.sql", "w") as sqlfile:

        # Write first row of sql to file
        sqlfile.write(self.base_sql + "\n")
        # Loop through remaining data rows and write INSERT statements
        for row in reader:
          # Format data based on data types
          formatted_data = [0 if value == "" or value == "#N/A" else value for value in row]

          # Substitute data into base template
          individual_sql = placeholders % tuple(formatted_data)
          sqlfile.write(individual_sql + ",\n")

        # deal with the ending and prevent duplicate results
        sqlfile.seek(sqlfile.tell() - 3) # moves back to delete extra , and \n
        sqlfile.write(f'\nON CONFLICT ("{self.uniqueKey}") DO UPDATE SET ({self.columns}) = ({", ".join(f'excluded."{_}"' for _ in self.headers)});') # formats and adds final sql line


  def run(self):
    """
    Runs the entire process of getting data types and generating SQL statements.
    """
    self.generate_insert_statements()
    print(f"SQL INSERT statements created and saved to 'data_import.sql'")


if __name__ == "__main__":
  filename = input("Enter filename (CSV only): ")
  table_name = input("Enter target table name: ")
  uniqueKey = input("Enter the unique key for the table (IntLibID): ")
  # output_file_path = input("Enter path for the output file: ")
  converter = CsvToSql(filename, table_name, uniqueKey)
  converter.run()
