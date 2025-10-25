import csv
import sys

def filter_csv_columns(input_filename):
    """
    Filters columns specified by column_indicies from the specified CSV file.
    The filtered output is printed to standard output (sys.stdout).
    """
    ## TODO: DETERMINE AND SET UP COMMAND LINE PARAMETERS
    # Columns to keep (0-based indices):
    # $1 -> 0, $2 -> 1, $3 -> 2, $23 -> 22, $28 -> 27
    column_indicies = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 22, 27]

    try:
        # Open the specified file for reading.
        with open(input_filename, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile, delimiter=',')
            # Write output to the console (standard output)
            writer = csv.writer(sys.stdout, delimiter=',')

            for row in reader:
                # Ensure the row has enough columns (at least 28)
                if len(row) > max(column_indicies):
                    # Select the desired columns
                    filtered_row = [row[i] for i in column_indicies]
                    writer.writerow(filtered_row)

    except FileNotFoundError:
        sys.stderr.write(f"Error: Input file '{input_filename}' not found.\n")
    except Exception as e:
        sys.stderr.write(f"An error occurred: {e}\n")

if __name__ == "__main__":
    # Check if a filename argument was provided
    if len(sys.argv) < 2:
        # sys.argv[0] is the script name itself, so we need at least 2 elements.
        sys.stderr.write("Usage: python script_name.py <filename>\n")
        sys.exit(1) # Exit with an error code

    # The filename is the first command-line argument (sys.argv[1])
    filename = sys.argv[1]
    filter_csv_columns(filename)