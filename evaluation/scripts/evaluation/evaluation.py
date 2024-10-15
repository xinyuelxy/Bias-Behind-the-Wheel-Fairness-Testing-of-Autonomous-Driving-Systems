import glob
import os
import numpy as np
from statsmodels.stats.proportion import proportions_ztest
import argparse

# Constants and mappings remain unchanged
PRED_THRES = 0.5
IOU_THRES = 0.5
ATTR_MAPPING = {
    'age': {0: 'Adults', 1: 'Children'},
    'gender': {0: 'Male', 1: 'Female'},
    'skin': {0: 'Light-Skin', 1: 'Dark-Skin'}
}
DT_TYPES = ['yolox', 'retinanet', 'faster_rcnn', 'cascade_rcnn', 'alfnet', 'csp', 'mgan', 'prnet']

# Calculate IoU
def cal_iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    interArea = abs(max((xB - xA, 0)) * max((yB - yA), 0))
    if interArea == 0:
        return 0

    boxAArea = abs((boxA[2] - boxA[0]) * (boxA[3] - boxA[1]))
    boxBArea = abs((boxB[2] - boxB[0]) * (boxB[3] - boxB[1]))

    iou = interArea / float(boxAArea + boxBArea - interArea)

    return iou

# Read the data from a file
def read_file(file_path):
    with open(file_path, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
    return lines

# Updated detection function
def detect(attribute, gt_path, dt_path):
    GT_files_list = glob.glob(gt_path + '/*.txt')
    overall_results = {}

    for dt_type in DT_TYPES:
        # Initialize arrays to hold counts for each run
        run_success_counts = np.zeros((10, 2))
        run_failure_counts = np.zeros((10, 2))
        num_runs = 0  # Counter for the number of runs

        for run in range(10):  # Iterate through all 10 results directories
            dt_type_path = os.path.join(dt_path, f"{dt_type}/results_{run}")

            for GT_txt_file in GT_files_list:
                file_id = GT_txt_file.split(".txt", 1)[0]
                file_name = os.path.basename(file_id)
                DT_filepath = os.path.join(dt_type_path, file_name + '.txt')

                if not os.path.exists(DT_filepath):
                    GT_lines = read_file(GT_txt_file)
                    for GT_line in GT_lines:
                        category = int(GT_line.split(' ')[0])
                        run_failure_counts[run][category] += 1
                else:
                    GT_lines = read_file(GT_txt_file)
                    DT_lines = read_file(DT_filepath)

                    for GT_line in GT_lines:
                        items = [float(item) for item in GT_line.split(' ')]
                        category, bb_GT = int(items[0]), items[1:]

                        iou_max = 0
                        conf_max = 0  # Added to track the highest confidence of a matched detection
                        for DT_line in DT_lines:
                            items = [float(item) for item in DT_line.split(' ')]
                            conf, bb_DT = items[0], items[1:]
                            iou = cal_iou(bb_GT, bb_DT)
                            if iou > iou_max:
                                iou_max = iou
                                conf_max = conf  # Update the max confidence when a new max iou is found

                        if iou_max > IOU_THRES and conf_max >= PRED_THRES:
                            run_success_counts[run][category] += 1
                        else:
                            run_failure_counts[run][category] += 1

        # After processing all runs, compute the averages
        success_counts_avg = np.mean(run_success_counts, axis=0)
        failure_counts_avg = np.mean(run_failure_counts, axis=0)

        # Store detailed run results and averages in overall_results
        overall_results[dt_type] = {
            'run_success_counts': run_success_counts,
            'run_failure_counts': run_failure_counts,
            'success_counts_avg': success_counts_avg,
            'failure_counts_avg': failure_counts_avg
        }

    return overall_results, ATTR_MAPPING[attribute]


# Main function with argument parsing and evaluation execution
def main():
    parser = argparse.ArgumentParser(description="Script for evaluating attributes")
    parser.add_argument('--attribute', type=str, required=True,
                        choices=['age', 'gender', 'skin'],
                        help='Attribute for evaluation: age, gender, or skin')
    parser.add_argument('--gt_path', type=str, required=True,
                        help='Path to ground truth files')
    parser.add_argument('--dt_path', type=str, required=True,
                        help='Path to detection result files')

    args = parser.parse_args()

    # Run detection evaluation
    overall_results, attribute_mapping = detect(args.attribute, args.gt_path, args.dt_path)

    # Print out the evaluation results
    print("\n========== Evaluation Results ==========\n")
    print(f"Current Testing Attribute: {args.attribute.capitalize()}")

    for dt_type, results in overall_results.items():
        print(f"\n========== DT Type: {dt_type} ==========\n")
        # Loop through each run and print out the results

        for run in range(10):
            success_counts = results['run_success_counts'][run]
            failure_counts = results['run_failure_counts'][run]
            total_counts = success_counts + failure_counts
            recall = success_counts / total_counts
            print(f"Run {run}:")
            for i in range(2):
                 print(f"{attribute_mapping[i]} - Total: {total_counts[i]}, Success: {success_counts[i]}, MR: {1 - recall[i]:.4f}")

        # Then print out the averages
        success_counts_avg = results['success_counts_avg']
        failure_counts_avg = results['failure_counts_avg']
        total_counts_avg = success_counts_avg + failure_counts_avg
        recall_avg = success_counts_avg / total_counts_avg
        EOD_avg = recall_avg[1] - recall_avg[0]
        print("\nAverage Results:")
        for i in range(2):
            print(f"{attribute_mapping[i]} - Avg Total: {total_counts_avg[i]}, Avg Success: {success_counts_avg[i]}, Avg MR: {1 - recall_avg[i]:.4f}")
        print(f"Avg EOD: {EOD_avg:.4f}\n")

        # Perform the z-test on the proportions based on averages
        z_score_avg, p_value_avg = proportions_ztest(success_counts_avg, total_counts_avg, alternative='two-sided')
        print(f"Avg Two Proportions Z-test (P-value): {p_value_avg:.4f}")

if __name__ == "__main__":
    main()


