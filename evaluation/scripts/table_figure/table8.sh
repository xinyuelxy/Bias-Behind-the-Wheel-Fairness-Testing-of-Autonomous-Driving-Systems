#!/bin/bash

# Attributes to evaluate
attributes=("gender" "age" "skin")

# Weather conditions
conditions=("non-rainy" "rainy")

# Output file for logging
output_file_weather="./evaluation/scripts/raw_results/table8_results.txt"

# Clear the output file at the start
> "$output_file_weather"

# Function to evaluate weather conditions
evaluate_weather() {
    local attribute=$1

    for condition in "${conditions[@]}"; do
        echo "Evaluating attribute: $attribute, Condition: $condition" | tee -a "$output_file_weather"
        gt_path="./evaluation/labels/RQ2_partitioned/weather/GT/${condition}/${attribute}"
        dt_path="./evaluation/labels/RQ2_partitioned/weather/DT/${condition}"
        python ./evaluation/scripts/evaluation/evaluation.py --attribute $attribute --gt_path "$gt_path" --dt_path "$dt_path" >> "$output_file_weather" 2>&1
    done
}

# Evaluate for each attribute
for attribute in "${attributes[@]}"; do
    evaluate_weather "$attribute"
done

echo "Weather evaluations completed." >> "$output_file_weather" 2>&1
