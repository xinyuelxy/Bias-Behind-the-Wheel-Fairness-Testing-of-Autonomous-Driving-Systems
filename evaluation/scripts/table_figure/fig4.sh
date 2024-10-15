#!/bin/bash

# Base paths for ground truth (GT) and detection (DT)
gt_base_path="./evaluation/labels/RQ2_partitioned/contrast/3_contrast_levels/GT"
dt_base_path="./evaluation/labels/RQ2_partitioned/contrast/3_contrast_levels/DT"

# Function to evaluate for a single attribute across three contrast levels
evaluate_attribute_levels() {
    local attribute=$1
    
    for level in {1..3}; do
        echo "Evaluating attribute: $attribute, Contrast Level: $level"
        # Construct GT and DT paths for the current level
        local gt_path="$gt_base_path/level$level/$attribute"
        local dt_path="$dt_base_path/level$level"
        # Execute the evaluation script
        python ./evaluation/scripts/evaluation/evaluation.py --attribute $attribute --gt_path "$gt_path" --dt_path "$dt_path"
    done
}

# Evaluate for each attribute across all contrast levels
echo "===================================="
echo "Starting evaluation for Gender..."
evaluate_attribute_levels gender

echo "===================================="
echo "Starting evaluation for Age..."
evaluate_attribute_levels age

echo "===================================="
echo "Starting evaluation for Skin..."
evaluate_attribute_levels skin

echo "===================================="
echo "Evaluations completed."
#!/bin/bash

# Define the attributes and their corresponding contrast levels
declare -a attributes=("gender" "age" "skin")
declare -a contrast_levels=("level1" "level2" "level3")

# Base paths for ground truth (GT) and detection (DT)
gt_base_path="./evaluation/labels/RQ2_partitioned/contrast/3_contrast_levels/GT"
dt_base_path="./evaluation/labels/RQ2_partitioned/contrast/3_contrast_levels/DT"

# Output file for storing the results
output_file="./evaluation/scripts/raw_results/fig4_results.txt"

# Ensure the output file is empty
> "$output_file"

# Function to evaluate attributes across contrast levels
evaluate_contrasts() {
    local attribute=$1
    local level=$2

    echo "Evaluating attribute: $attribute, Contrast Level: $level" | tee -a "$output_file"
    local gt_path="${gt_base_path}/${level}/${attribute}"
    local dt_path="${dt_base_path}/${level}"
    # Execute the evaluation script and append results to the output file
    python ./evaluation/scripts/evaluation/evaluation.py --attribute "$attribute" --gt_path "$gt_path" --dt_path "$dt_path" 2>&1 | tee -a "$output_file"
}

# Loop through each attribute and contrast level to perform evaluations
for attribute in "${attributes[@]}"; do
    for level in "${contrast_levels[@]}"; do
        evaluate_contrasts "$attribute" "$level"
    done
done

echo "Evaluations completed." | tee -a "$output_file"
