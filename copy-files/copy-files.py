# Files copy from <source_folder> to <destination_folder>. Possible args: ["all", "lastmonth"]

import os
import shutil
import datetime
import sys
import logging

# Set up logging to file and stdout
log_file_name = 'copy_files_' + datetime.date.today().strftime('%Y-%m-%d') + '.log'
logging.basicConfig(filename=log_file_name, filemode='a', format='%(asctime)s %(message)s', level=logging.INFO)
logger = logging.getLogger()
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

# Get the source and destination folders from the command line arguments
if len(sys.argv) < 3:
    logger.error("Usage: python script.py <source_folder> <destination_folder>")
    sys.exit()
source_folder = sys.argv[1]
destination_folder = sys.argv[2]

# Ask the user which period of files to copy
valid_periods = ["all", "lastmonth"]
while True:
    period = input(f"Which period of files to copy? ({'/'.join(valid_periods)}, default={valid_periods[1]}): ")
    if period == "":
        period = valid_periods[1]
        break
    if period in valid_periods:
        break
    print(f"Invalid period. Please enter {valid_periods}.")
    logger.error("Invalid period entered by user.")

# Calculate the date range for the specified period
if period == "all":
    first_day_of_period = datetime.date(1970, 1, 1)
    last_day_of_period = datetime.date.today()
elif period == "lastmonth":
    today = datetime.date.today()
    first_day_of_period = datetime.date(today.year, today.month-1, 1)
    last_day_of_period = first_day_of_period.replace(day=28) + datetime.timedelta(days=4)
    last_day_of_period = last_day_of_period - datetime.timedelta(days=last_day_of_period.day)

# Initialize the action for handling existing files
action = None

# Loop through all the files in the source folder
for filename in os.listdir(source_folder):
    file_path = os.path.join(source_folder, filename)
    # Check if the file was created during the specified period
    if first_day_of_period <= datetime.date.fromtimestamp(os.path.getctime(file_path)) <= last_day_of_period:
        # Copy the file to the destination folder
        destination_file_path = os.path.join(destination_folder, filename)
        if os.path.exists(destination_file_path):
            while True:
                if action is None:
                    action = input(f"A file with the name '{filename}' already exists in the destination folder. "
                                   "Do you want to (s)kip all existing files or (o)verwrite all existing files? (s/o): ")
                if action.lower() == "s":
                    logger.info(f"Skipped all existing files from '{source_folder}' to '{destination_folder}'.")
                    break
                elif action.lower() == "o":
                    break
                else:
                    print("Invalid action. Please enter 's' or 'o'.")
                    logger.error("Invalid action entered by user.")

        if action.lower() == "o" or not os.path.exists(destination_file_path):
            shutil.copy(file_path, destination_folder)
            logger.info(f"Copied file '{filename}' from '{source_folder}' to '{destination_folder}'.")
