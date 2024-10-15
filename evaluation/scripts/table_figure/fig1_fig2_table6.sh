#!/bin/bash

# Define arrays for attributes and their corresponding datasets
gender_datasets="citypersons eurocity_day eurocity_night bdd100k"
age_datasets="citypersons eurocity_day eurocity_night bdd100k"
skin_datasets="bdd100k"

# Base paths
gt_base_path="./evaluation/labels/RQ1_overall/GT"
dt_base_path="./evaluation/labels/RQ1_overall/DT"

# Output file path
output_file="./evaluation/scripts/raw_results/fig_1_fig2_table6_results.txt"

# Clear the output file at the start
> "$output_file"

# Function to evaluate datasets for an attribute
evaluate_datasets() {
    local attribute=$1
    local datasets=$2

    for dataset in $datasets; do
        echo "Evaluating attribute: $attribute" >> "$output_file" 2>&1
        echo "Processing dataset: $dataset" >> "$output_file" 2>&1
        # Construct GT and DT paths
        gt_path="${gt_base_path}/${dataset}/${attribute}"
        dt_path="${dt_base_path}/${dataset}"
        # Execute the evaluation script and append output to file
        python ./evaluation/scripts/evaluation/evaluation.py --attribute $attribute --gt_path "$gt_path" --dt_path "$dt_path" >> "$output_file" 2>&1
    done
}

# Evaluate for each attribute
evaluate_datasets gender "$gender_datasets"
evaluate_datasets age "$age_datasets"
evaluate_datasets skin "$skin_datasets"

echo "Evaluations completed." >> "$output_file" 2>&1
