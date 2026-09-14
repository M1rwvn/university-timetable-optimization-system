#!/usr/bin/env python3
import pandas as pd
import random
import json
import os

# Configuration
POPULATION_SIZE = 100  # Number of solutions in the initial population
PROCESSED_DATA_DIR = "/home/ubuntu/processed_data"
OUTPUT_DIR = "/home/ubuntu/pfoa_working_dir"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load processed data
print("Loading processed data...")
try:
    lectures_df = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "lectures_to_schedule.csv"))
    timeslots_df = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "valid_timeslots.csv"))
    classrooms_df = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "processed_classrooms.csv"))
    print(f"Loaded {len(lectures_df)} lectures, {len(timeslots_df)} timeslots, {len(classrooms_df)} classrooms.")
except Exception as e:
    print(f"Error loading processed data: {e}")
    exit(1)

if lectures_df.empty or timeslots_df.empty or classrooms_df.empty:
    print("One or more essential dataframes (lectures, timeslots, classrooms) are empty. Cannot proceed.")
    exit(1)

lecture_ids = lectures_df["lecture_id"].tolist()
timeslot_ids = timeslots_df["timeslot_id"].tolist()
classroom_ids = classrooms_df["classroom_id"].tolist()

# Function to create a single random solution (chromosome)
def create_random_solution(lecture_ids, timeslot_ids, classroom_ids):
    """Creates a random timetable solution (chromosome)."""
    solution = []
    for lecture_id in lecture_ids:
        assignment = {
            "lecture_id": lecture_id,
            "timeslot_id": random.choice(timeslot_ids),
            "classroom_id": random.choice(classroom_ids)
        }
        solution.append(assignment)
    return solution

# Generate initial population
print(f"\nGenerating initial population of {POPULATION_SIZE} solutions...")
initial_population = []
for i in range(POPULATION_SIZE):
    solution = create_random_solution(lecture_ids, timeslot_ids, classroom_ids)
    initial_population.append(solution)
    if (i + 1) % 10 == 0:
        print(f"Generated {i + 1}/{POPULATION_SIZE} solutions...")

print(f"Successfully generated {len(initial_population)} solutions.")

# Save the initial population to a JSON file
population_file_path = os.path.join(OUTPUT_DIR, "initial_population.json")
try:
    with open(population_file_path, "w") as f:
        json.dump(initial_population, f, indent=4)
    print(f"Initial population saved to {population_file_path}")
except Exception as e:
    print(f"Error saving initial population: {e}")

# Create the initial_population_generation.md file
description_content = f"""
# Initial Population Generation for PFOA

This document describes the generation of the initial population of timetable solutions for the Puffer Fish Optimization Algorithm (PFOA).

## 1. Objective

The goal is to create a diverse set of {POPULATION_SIZE} candidate timetables (chromosomes) to serve as the starting point for the PFOA optimization process. Each chromosome represents a complete potential timetable.

## 2. Data Used

The generation process utilizes the following processed data files:

*   `lectures_to_schedule.csv`: Contains {len(lectures_df)} unique lectures (course-instructor pairings) that need to be scheduled.
*   `valid_timeslots.csv`: Contains {len(timeslots_df)} valid timeslots available for scheduling.
*   `processed_classrooms.csv`: Contains {len(classrooms_df)} available classrooms.

## 3. Chromosome Structure

As defined in the problem encoding, a chromosome is a list of assignments. Each assignment is a dictionary mapping a `lecture_id` to a `timeslot_id` and a `classroom_id`:

```json
{{
    "lecture_id": int,
    "timeslot_id": int,
    "classroom_id": int
}}
```

A complete chromosome consists of {len(lectures_df)} such assignments, one for each lecture.

## 4. Generation Process

For each of the {POPULATION_SIZE} solutions in the initial population:

1.  Initialize an empty list for the new chromosome.
2.  For each `lecture_id` from the `lectures_to_schedule.csv` file:
    a.  Randomly select a `timeslot_id` from the list of all available `timeslot_id`s (from `valid_timeslots.csv`).
    b.  Randomly select a `classroom_id` from the list of all available `classroom_id`s (from `processed_classrooms.csv`).
    c.  Create an assignment dictionary with the `lecture_id`, selected `timeslot_id`, and selected `classroom_id`.
    d.  Add this assignment to the current chromosome.
3.  Once all lectures have been assigned a random timeslot and classroom, the chromosome is complete and added to the initial population.

This process ensures that every lecture is assigned in every generated timetable, and the assignments are made randomly to promote diversity in the initial population. No constraints (like clashes or capacity) are checked at this stage; that will be handled by the fitness function and repair mechanisms later in the PFOA process.

## 5. Output

The generated initial population, consisting of {len(initial_population)} solutions, is saved in JSON format to:
`{population_file_path}`

Each solution in the JSON file is a list of assignment dictionaries as described above.
"""

md_file_path = os.path.join(OUTPUT_DIR, "initial_population_generation.md")
try:
    with open(md_file_path, "w") as f:
        f.write(description_content)
    print(f"Initial population generation description saved to {md_file_path}")
except Exception as e:
    print(f"Error writing initial population generation description: {e}")

print("\nScript generate_initial_population.py finished.")

