import pandas as pd
import sys

# Check if a file name is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python json_to_csv_list.py <JSON_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]  # Get the file path from the first argument

with open(json_file_path) as json_file:
    data = json.load(json_file)

df = pd.DataFrame(data)
csv_list = df.to_csv(index=False).splitlines()

print(csv_list)
