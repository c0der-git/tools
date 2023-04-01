#!/bin/bash

# Set the default verbose flag to false
verbose=false

# Parse the command-line arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    -v|--verbose)
      verbose=true
      shift
      ;;
    all|last\ month)
      copy_type="$1"
      shift
      ;;
    *)
      echo "Invalid argument: $1"
      echo "Usage: $0 {all|last month} [-v|--verbose] source_dir destination_dir"
      exit 1
      ;;
  esac
done

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 {all|last month} [-v|--verbose] source_dir destination_dir"
  exit 1
fi

# Set the source and destination directories
source_dir="$1"
destination_dir="$2"

# Set the log file with a date stamp
log_file="copy_log_$(date +%Y-%m-%d-%H-%M-%S).txt"

# Set the copy command with or without verbose flag
if [ "$verbose" = true ]; then
  copy_cmd="cp -rv"
else
  copy_cmd="cp -r"
fi

# Copy all files from folder1 to folder2
if [ "$copy_type" == "all" ]; then
  # Copy all files and save the result to the log file
  $copy_cmd "$source_dir"/* "$destination_dir" &> "$log_file"

  # Check if there were any errors and print a warning message to stdout
  if [ "$?" -ne 0 ]; then
    echo "WARNING: Some files failed to copy."
    grep -i "error" "$log_file" | cut -d ":" -f 1 | uniq
  else
    echo "All files copied successfully."
  fi

# Copy files from folder1 that were created during the previous month
elif [ "$copy_type" == "last month" ]; then
  # Set the start and end dates for the previous month
  start_date=$(date -v-1m +%Y-%m-01)
  end_date=$(date -v-1m +%Y-%m-%d)

  # Copy files from folder1 to folder2 that were created during the previous month and save the result to the log file
  find "$source_dir" -type f -newermt "$start_date" ! -newermt "$end_date" -exec $copy_cmd {} "$destination_dir" \; &> "$log_file"

  # Check if there were any errors and print a warning message to stdout
  if [ "$?" -ne 0 ]; then
    echo "WARNING: Some files failed to copy."
    grep -i "error" "$log_file" | cut -d ":" -f 1 | uniq
  else
    echo "Files created during the previous month copied successfully."
  fi

else
  echo "Invalid argument. Usage: $0 {all|last month} [-v|--verbose] source_dir destination_dir"
  exit 1
fi

