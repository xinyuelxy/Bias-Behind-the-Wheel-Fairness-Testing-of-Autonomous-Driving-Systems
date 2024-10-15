#!/bin/bash

# Define attributes
attributes=("gender" "age" "skin")

# Day and Night settings
conditions=("day" "night")

# Base paths for GT and DT, adjust the DT base path as per your directory structure
gt_base_path="./evaluation/labels/RQ2_partitioned/brightness/day_night/GT"
dt_base_path="/Users/xinyueli/Desktop/Research/fairness-testing/github/evaluation/labels/RQ2_partitioned/brightness/day_night/DT"

# Output file for logging
output_file="./evaluation/scripts/raw_results/table7_results.txt"

# Clear the output file at the start
> "$output_file"

# Loop through each attribute and condition
for attribute in "${attributes[@]}"; do
    for condition in "${conditions[@]}"; do
        echo "Evaluating $attribute for $condition" | tee -a "$output_file"
        gt_path="$gt_base_path/$condition/$attribute"
        dt_path="$dt_base_path/$condition"
        # Execute the evaluation script and append output to file
        python ./evaluation/scripts/evaluation/evaluation.py --attribute $attribute --gt_path "$gt_path" --dt_path "$dt_path" >> "$output_file" 2>&1
    done
done

echo "Evaluations completed." | tee -a "$output_file"
