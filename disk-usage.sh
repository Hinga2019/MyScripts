#!/bin/bash

# This script will measure the disk usage of the different folders in your hosting
# Usage:
# $ bash disk-usage > disk-usage_report

# Get the list of folders
folders=$(ls -1)

# Declare an associative array to store folder sizes
declare -A folder_sizes

# Loop through the folders
for folder in $folders; do

  # Get the size of the folder in kilobytes
  size=$(du -sk "$folder" | awk '{print $1}')

  # Store the size in the associative array with the folder name as the key
  folder_sizes["$folder"]=$size

done

# Function to convert size to human-readable format
function convert_to_readable() {
  local size=$1
  if (( size >= 1024 * 1024 )); then
    echo "$(( size / 1024 / 1024 ))G"
  elif (( size >= 1024 )); then
    echo "$(( size / 1024 ))M"
  else
    echo "${size}K"
  fi
}

# Sort folders by size
sorted_folders=$(for folder in "${!folder_sizes[@]}"; do
  echo "${folder_sizes[$folder]} $folder"
done | sort -n -r | cut -d ' ' -f 2)

# Print the size of the folders in human-readable format
for folder in $sorted_folders; do
  size=${folder_sizes["$folder"]}
  echo "The size of the folder '$folder' is $(convert_to_readable $size)"
done

