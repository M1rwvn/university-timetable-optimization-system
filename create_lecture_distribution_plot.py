import json
import pandas as pd
import matplotlib.pyplot as plt
import os

BEST_SOLUTION_PATH = "/home/ubuntu/upload/pfoa_best_solution.json"
TIMESLOTS_PATH = "/home/ubuntu/upload/valid_timeslots.csv"
OUTPUT_PLOT_PATH = "/home/ubuntu/lecture_distribution_by_time.png"

def create_lecture_distribution_plot():
    print(f"Loading best solution from {BEST_SOLUTION_PATH}...")
    try:
        with open(BEST_SOLUTION_PATH, 'r') as f:
            best_solution_data = json.load(f)
        if not best_solution_data:
            print("Error: Best solution data is empty.")
            return False
        solution_df = pd.DataFrame(best_solution_data)
    except FileNotFoundError:
        print(f"Error: Best solution file not found at {BEST_SOLUTION_PATH}.")
        return False
    except Exception as e:
        print(f"Error loading best solution: {e}")
        return False

    print(f"Loading timeslots data from {TIMESLOTS_PATH}...")
    try:
        timeslots_df = pd.read_csv(TIMESLOTS_PATH)
        if timeslots_df.empty:
            print("Error: Timeslots data is empty.")
            return False
    except FileNotFoundError:
        print(f"Error: Timeslots file not found at {TIMESLOTS_PATH}.")
        return False
    except Exception as e:
        print(f"Error loading timeslots data: {e}")
        return False

    try:
        solution_df['timeslot_id'] = solution_df['timeslot_id'].astype(str)
        timeslots_df['timeslot_id'] = timeslots_df['timeslot_id'].astype(str)
        merged_df = pd.merge(solution_df, timeslots_df, on="timeslot_id", how="left")
    except Exception as e:
        print(f"Error merging dataframes: {e}")
        return False

    if merged_df['start_time'].isnull().any():
        print("Warning: Some lectures could not be matched with timeslot start times. Check timeslot_id consistency.")
        merged_df.dropna(subset=['start_time'], inplace=True)
        if merged_df.empty:
            print("Error: No lectures with valid start times after merge. Cannot create plot.")
            return False
            
    print("Generating lecture distribution plot by start time...")
    lecture_counts_by_time = merged_df.groupby("start_time").size().reset_index(name="lecture_count")
    
    try:
        lecture_counts_by_time['start_time_dt'] = pd.to_datetime(lecture_counts_by_time['start_time'], format='%H:%M').dt.time
        lecture_counts_by_time = lecture_counts_by_time.sort_values(by='start_time_dt')
    except Exception as e:
        print(f"Warning: Could not sort by start_time as time objects: {e}. Sorting as strings.")
        lecture_counts_by_time = lecture_counts_by_time.sort_values(by='start_time')

    plt.figure(figsize=(10, 6))
    plt.bar(lecture_counts_by_time["start_time"].astype(str), lecture_counts_by_time["lecture_count"], color="skyblue")
    plt.xlabel("Start Time of Lectures", fontsize=12)
    plt.ylabel("Number of Scheduled Lectures", fontsize=12)
    plt.title("Distribution of Scheduled Lectures by Start Time (PFOA Solution)", fontsize=14)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--')

    try:
        os.makedirs(os.path.dirname(OUTPUT_PLOT_PATH), exist_ok=True)
        plt.savefig(OUTPUT_PLOT_PATH)
        print(f"Lecture distribution plot saved to {OUTPUT_PLOT_PATH}")
        return True
    except Exception as e:
        print(f"Error saving plot: {e}")
        return False

if __name__ == "__main__":
    if not os.path.exists(TIMESLOTS_PATH):
        print(f"Prerequisite file {TIMESLOTS_PATH} not found. Please ensure 'define_problem_components.py' has been run successfully.")
    elif not os.path.exists(BEST_SOLUTION_PATH):
        print(f"Best solution file {BEST_SOLUTION_PATH} not found.")
    else:
        if create_lecture_distribution_plot():
            print("Plot generated successfully.")
        else:
            print("Plot generation failed.")
    print("Script create_lecture_distribution_plot.py finished.")

