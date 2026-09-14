
# Initial Population Generation for PFOA

This document describes the generation of the initial population of timetable solutions for the Puffer Fish Optimization Algorithm (PFOA).

## 1. Objective

The goal is to create a diverse set of 100 candidate timetables (chromosomes) to serve as the starting point for the PFOA optimization process. Each chromosome represents a complete potential timetable.

## 2. Data Used

The generation process utilizes the following processed data files:

*   `lectures_to_schedule.csv`: Contains 1100 unique lectures (course-instructor pairings) that need to be scheduled.
*   `valid_timeslots.csv`: Contains 56 valid timeslots available for scheduling.
*   `processed_classrooms.csv`: Contains 30 available classrooms.

## 3. Chromosome Structure

As defined in the problem encoding, a chromosome is a list of assignments. Each assignment is a dictionary mapping a `lecture_id` to a `timeslot_id` and a `classroom_id`:

```json
{
    "lecture_id": int,
    "timeslot_id": int,
    "classroom_id": int
}
```

A complete chromosome consists of 1100 such assignments, one for each lecture.

## 4. Generation Process

For each of the 100 solutions in the initial population:

1.  Initialize an empty list for the new chromosome.
2.  For each `lecture_id` from the `lectures_to_schedule.csv` file:
    a.  Randomly select a `timeslot_id` from the list of all available `timeslot_id`s (from `valid_timeslots.csv`).
    b.  Randomly select a `classroom_id` from the list of all available `classroom_id`s (from `processed_classrooms.csv`).
    c.  Create an assignment dictionary with the `lecture_id`, selected `timeslot_id`, and selected `classroom_id`.
    d.  Add this assignment to the current chromosome.
3.  Once all lectures have been assigned a random timeslot and classroom, the chromosome is complete and added to the initial population.

This process ensures that every lecture is assigned in every generated timetable, and the assignments are made randomly to promote diversity in the initial population. No constraints (like clashes or capacity) are checked at this stage; that will be handled by the fitness function and repair mechanisms later in the PFOA process.

## 5. Output

The generated initial population, consisting of 100 solutions, is saved in JSON format to:
`/home/ubuntu/pfoa_working_dir/initial_population.json`

Each solution in the JSON file is a list of assignment dictionaries as described above.
