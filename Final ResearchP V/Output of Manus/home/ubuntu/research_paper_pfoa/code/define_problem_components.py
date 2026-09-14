#!/usr/bin/env python3
import pandas as pd
import os

# Create a directory for processed data
processed_data_dir = "/home/ubuntu/processed_data"
os.makedirs(processed_data_dir, exist_ok=True)

# File paths
base_path = "/home/ubuntu/upload"
files_info = {
    "timeslots": os.path.join(base_path, "timeslots.csv"),
    "students": os.path.join(base_path, "students.csv"),
    "schedule": os.path.join(base_path, "schedule.csv"),
    "instructors": os.path.join(base_path, "instructors.csv"),
    "courses": os.path.join(base_path, "courses.csv"),
    "classrooms": os.path.join(base_path, "classrooms.csv"),
}

# Load data
dfs = {}
print("Loading CSV files...")
for name, path in files_info.items():
    try:
        dfs[name] = pd.read_csv(path)
        print(f"Successfully loaded {name}.csv ({len(dfs[name])} rows)")
    except Exception as e:
        print(f"Error loading {name}.csv: {e}")
        # If a critical file is missing, we might need to stop or handle it
        if name in ["courses", "instructors", "timeslots", "classrooms", "schedule"]:
             raise # Reraise for critical files

# 1. Process Timeslots
print("\nProcessing timeslots.csv...")
timeslots_df = dfs["timeslots"].copy()

# Convert times to a comparable format (datetime.time or total minutes from midnight)
# Using total minutes from midnight for simplicity in duration calculation
problematic_time_rows = []
for index, row in timeslots_df.iterrows():
    try:
        start_dt = pd.to_datetime(row["start_time"], format="%H:%M")
        end_dt = pd.to_datetime(row["end_time"], format="%H:%M")
        timeslots_df.loc[index, "start_minutes"] = start_dt.hour * 60 + start_dt.minute
        timeslots_df.loc[index, "end_minutes"] = end_dt.hour * 60 + end_dt.minute
    except ValueError:
        problematic_time_rows.append(index)
        timeslots_df.loc[index, "start_minutes"] = pd.NaT
        timeslots_df.loc[index, "end_minutes"] = pd.NaT

if problematic_time_rows:
    print(f"Warning: Could not parse times for {len(problematic_time_rows)} rows in timeslots.csv. These rows will be dropped.")
    print(f"Problematic row indices: {problematic_time_rows[:10]} (first 10 if many)")
    timeslots_df.dropna(subset=["start_minutes", "end_minutes"], inplace=True)

original_rows = len(timeslots_df)
timeslots_df["duration_minutes"] = timeslots_df["end_minutes"] - timeslots_df["start_minutes"]
valid_timeslots_df = timeslots_df[timeslots_df["duration_minutes"] > 0].copy()
invalid_count = original_rows - len(valid_timeslots_df)
print(f"Timeslots: Original parsable rows: {original_rows}, Valid rows (duration > 0): {len(valid_timeslots_df)}, Invalid/Removed: {invalid_count}")
valid_timeslots_df.to_csv(os.path.join(processed_data_dir, "valid_timeslots.csv"), index=False)
print(f"Saved valid_timeslots.csv to {processed_data_dir}")
print(f"Valid timeslots summary (first 5 rows):\n{valid_timeslots_df.head().to_string()}")

# 2. Process other essential data files
courses_df = dfs["courses"].copy()
instructors_df = dfs["instructors"].copy()
classrooms_df = dfs["classrooms"].copy()
students_df = dfs["students"].copy()

print(f"\nCourses summary (first 5 rows):\n{courses_df.head().to_string()}")
courses_df.to_csv(os.path.join(processed_data_dir, "processed_courses.csv"), index=False)
print(f"Saved processed_courses.csv to {processed_data_dir}")

print(f"\nInstructors summary (first 5 rows):\n{instructors_df.head().to_string()}")
instructors_df.to_csv(os.path.join(processed_data_dir, "processed_instructors.csv"), index=False)
print(f"Saved processed_instructors.csv to {processed_data_dir}")

print(f"\nClassrooms summary (first 5 rows):\n{classrooms_df.head().to_string()}")
classrooms_df.to_csv(os.path.join(processed_data_dir, "processed_classrooms.csv"), index=False)
print(f"Saved processed_classrooms.csv to {processed_data_dir}")

print(f"\nStudents summary (first 5 rows):\n{students_df.head().to_string()}")
students_df.to_csv(os.path.join(processed_data_dir, "processed_students.csv"), index=False)
print(f"Saved processed_students.csv to {processed_data_dir}")


# 3. Define "Lectures" to be scheduled and Student Enrollments from schedule.csv
print("\nProcessing schedule.csv to define lectures and enrollments...")
schedule_df = dfs["schedule"].copy()

# A "lecture" is a (course_id, instructor_id) pair that needs a timeslot and classroom.
lectures_df = schedule_df[["course_id", "instructor_id"]].drop_duplicates().reset_index(drop=True)
lectures_df["lecture_id"] = lectures_df.index # Add a unique ID for each lecture

# Check consistency: if a course in schedule.csv is taught by multiple instructors
course_instructor_counts = schedule_df.groupby("course_id")["instructor_id"].nunique()
inconsistent_course_instructor_pairs = course_instructor_counts[course_instructor_counts > 1]
if not inconsistent_course_instructor_pairs.empty:
    print(f"Warning: The following courses from schedule.csv are associated with multiple instructors:")
    print(inconsistent_course_instructor_pairs.to_string())
    print("The 'lectures_to_schedule.csv' will treat each unique (course_id, instructor_id) pair as a distinct lecture unit.")
else:
    print("Each course_id in schedule.csv is consistently associated with a single instructor_id.")

print(f"\nDefined {len(lectures_df)} unique lectures (course_id, instructor_id pairs) to be scheduled.")
print(f"Lectures summary (first 5 rows):\n{lectures_df.head().to_string()}")
lectures_df.to_csv(os.path.join(processed_data_dir, "lectures_to_schedule.csv"), index=False)
print(f"Saved lectures_to_schedule.csv to {processed_data_dir}")

# Student enrollments: (student_id, course_id)
student_enrollments_df = schedule_df[["student_id", "course_id"]].drop_duplicates().reset_index(drop=True)
print(f"\nExtracted {len(student_enrollments_df)} unique student enrollments (student_id, course_id).")
print(f"Student enrollments summary (first 5 rows):\n{student_enrollments_df.head().to_string()}")
student_enrollments_df.to_csv(os.path.join(processed_data_dir, "student_enrollments.csv"), index=False)
print(f"Saved student_enrollments.csv to {processed_data_dir}")

# 4. Data Representation for a solution (Chromosome)
# This is a conceptual definition for the PFOA implementation.

print("\n--- Problem Encoding Definition Summary ---")
print("1. Entities for Timetabling:")
print(f"   - Courses: {len(courses_df)} (details in processed_courses.csv)")
print(f"   - Instructors: {len(instructors_df)} (details in processed_instructors.csv)")
print(f"   - Valid Timeslots: {len(valid_timeslots_df)} (details in valid_timeslots.csv)")
print(f"   - Classrooms: {len(classrooms_df)} (details in processed_classrooms.csv)")
print(f"   - Students: {len(students_df)} (details in processed_students.csv)")
print(f"   - Lectures to schedule: {len(lectures_df)} (defined as unique (course_id, instructor_id) pairs from schedule.csv, details in lectures_to_schedule.csv)")
print(f"   - Student enrollments: {len(student_enrollments_df)} (unique (student_id, course_id) pairs, details in student_enrollments.csv)")

print("\n2. Solution Representation (Chromosome for PFOA):")
print("   A chromosome (a single timetable solution) will be represented as a list of assignments.")
print("   Each assignment will link a 'lecture_id' (from lectures_to_schedule.csv) to a 'timeslot_id' (from valid_timeslots.csv) and a 'classroom_id' (from processed_classrooms.csv).")
print("   For example, an assignment could be a dictionary: {'lecture_id': L, 'timeslot_id': T, 'classroom_id': R}")
print("   The complete chromosome will be a list of such assignments, one for each lecture to be scheduled.")

print(f"\nAll processed data files have been saved in: {processed_data_dir}")

# Create the problem_encoding_description.md file
description_content = """
# Problem Encoding for Timetable Optimization using PFOA

This document outlines the encoding of the timetable problem for optimization using the Puffer Fish Optimization Algorithm (PFOA), based on the provided datasets.

## 1. Problem Definition

The university timetabling problem involves assigning a set of lectures (defined as course-instructor pairings) to specific timeslots and classrooms, subject to a variety of constraints. The goal is to find a feasible and high-quality timetable that minimizes conflicts and satisfies preferences.

## 2. Components to be Encoded

The primary components derived from the provided CSV files are:

*   **Courses**: Information about each course, including its ID, name, department, and credits (from `courses.csv`). Processed data is in `processed_data/processed_courses.csv`.
*   **Instructors**: Details of instructors, including their ID, name, and department (from `instructors.csv`). Processed data is in `processed_data/processed_instructors.csv`.
*   **Timeslots**: Available time periods for scheduling lectures, defined by day, start time, and end time (from `timeslots.csv`). Invalid timeslots (e.g., end time before or equal to start time, or unparseable times) have been filtered out. The processed list of valid timeslots is in `processed_data/valid_timeslots.csv`.
*   **Classrooms (Rooms)**: Information about available rooms, including ID, capacity, and type (from `classrooms.csv`). Processed data is in `processed_data/processed_classrooms.csv`.
*   **Students**: Information about students (from `students.csv`). This is primarily used in conjunction with enrollment data for conflict checking. Processed data is in `processed_data/processed_students.csv`.
*   **Lectures**: These are the actual events to be scheduled. A lecture is defined as a unique `(course_id, instructor_id)` pair. These pairs are derived from `schedule.csv`, assuming it indicates which instructor teaches which course. Each unique pair is assigned a `lecture_id`. The list of lectures to be scheduled is in `processed_data/lectures_to_schedule.csv`.
*   **Student Enrollments**: Data on which students are enrolled in which courses, derived from `schedule.csv` (specifically `student_id` and `course_id`). This is crucial for identifying student conflicts (e.g., a student scheduled for two different lectures at the same time). The processed list of unique enrollments is in `processed_data/student_enrollments.csv`.

## 3. Data Representation of a Solution (Chromosome)

A single candidate solution (a complete timetable, also referred to as a chromosome in PFOA) is represented as a list of assignments. Each element in the list corresponds to one of the defined "lectures" that need to be scheduled (identified by `lecture_id`).

Each assignment is typically a dictionary or object with the following structure:

```
{
    'lecture_id': int,    // Refers to an entry in lectures_to_schedule.csv
    'timeslot_id': int,   // Refers to an entry in valid_timeslots.csv
    'classroom_id': int   // Refers to an entry in processed_classrooms.csv
}
```

The entire chromosome is a list of these assignment structures. The length of the list is equal to the total number of unique lectures to be scheduled.

This representation allows the PFOA to generate and manipulate potential timetables. The fitness function will then evaluate each chromosome based on this structure to determine its quality by checking for constraint violations (e.g., instructor clashes, student clashes, room capacity violations, etc.).
"""
try:
    with open("/home/ubuntu/problem_encoding_description.md", "w") as f:
        f.write(description_content)
    print("\nSuccessfully created /home/ubuntu/problem_encoding_description.md")
except Exception as e:
    print(f"Error writing /home/ubuntu/problem_encoding_description.md: {e}")

print("\nScript define_problem_components.py finished.")

