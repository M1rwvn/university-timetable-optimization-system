
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
