import csv
import os
from datetime import datetime


def write_results_csv(output_tasks, new_output_tasks, input_file, output_directory):
    try:

        # Create a timestamp for uniqueness
        timestamp = datetime.now().strftime("M%S")

        if output_directory != None:
            output_base = output_directory
        else:
            output_base = "../output"

        # Get the parent directory name of the input file
        input_parent_dir = os.path.basename(os.path.dirname(input_file))

        # Create the output directory if it doesn't exist
        output_dir = os.path.join(output_base, input_parent_dir)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Define the output file paths with timestamp
        output_file_v1 = os.path.join(output_dir, f"{os.path.basename(input_file)}_smells_v1_{timestamp}.csv")
        output_file_v2 = os.path.join(output_dir, f"{os.path.basename(input_file)}_smells_v2_{timestamp}.csv")

        # Define the CSV column names
        csv_columns = ['Task name', 'Idempotency', 'Version specific installation', 'Outdated dependencies',
                       'Missing dependencies', 'Assumption about environment', 'Hardware specific commands',
                       'Broken Dependency']
        new_csv_columns = ['Repository Name', 'File Name', 'Line Number', 'Task Name', 'Smell Name',
                           'Smell Description']

        # Write task smells to CSV files
        with open(output_file_v1, 'a', newline='') as file_v1, open(output_file_v2, 'a', newline='') as file_v2:
            writer_v1 = csv.DictWriter(file_v1, fieldnames=new_csv_columns)
            writer_v1.writeheader()
            writer_v1.writerows(new_output_tasks)

            writer_v2 = csv.DictWriter(file_v2, fieldnames=csv_columns)
            writer_v2.writeheader()
            writer_v2.writerows(output_tasks)

    except Exception as e:
        print("Error occurred while writing CSV files:", str(e))
