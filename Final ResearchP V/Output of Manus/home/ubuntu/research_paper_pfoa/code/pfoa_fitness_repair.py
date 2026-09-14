#!/usr/bin/env python3
import pandas as pd
import random
import os
from collections import defaultdict

PROCESSED_DATA_DIR = "/home/ubuntu/processed_data"
OUTPUT_DIR = "/home/ubuntu/pfoa_working_dir"

# --- Load Data --- #
def load_data():
    print("Loading data for fitness and repair functions...")
    data = {}
    try:
        data["lectures"] = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "lectures_to_schedule.csv"))
        data["timeslots"] = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "valid_timeslots.csv"))
        data["classrooms"] = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "processed_classrooms.csv"))
        data["students"] = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "processed_students.csv"))
        data["courses"] = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "processed_courses.csv"))
        data["instructors"] = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "processed_instructors.csv"))
        data["enrollments"] = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "student_enrollments.csv"))
        print("All data loaded successfully.")
        
        data["lecture_info"] = data["lectures"].set_index("lecture_id").to_dict("index")
        data["course_info"] = data["courses"].set_index("course_id").to_dict("index")
        data["classroom_info"] = data["classrooms"].set_index("classroom_id").to_dict("index")
        data["timeslot_info"] = data["timeslots"].set_index("timeslot_id").to_dict("index")
        
        students_per_course = data["enrollments"].groupby("course_id")["student_id"].count().to_dict()
        data["students_per_course"] = students_per_course

        courses_per_student = data["enrollments"].groupby("student_id")["course_id"].apply(list).to_dict()
        data["courses_per_student"] = courses_per_student

    except Exception as e:
        print(f"Error loading data: {e}")
        return None
    return data

# --- Fitness Function --- #
def calculate_fitness(solution, all_data):
    fitness = 0
    violations = {
        "instructor_conflict": 0,
        "room_conflict": 0,
        "capacity_violation": 0,
        "student_conflict": 0
    }

    instructor_schedule = defaultdict(list)
    room_schedule = defaultdict(list)

    for assignment in solution:
        lecture_id = assignment["lecture_id"]
        timeslot_id = assignment["timeslot_id"]
        classroom_id = assignment["classroom_id"]

        lecture_details = all_data["lecture_info"].get(lecture_id)
        if not lecture_details: continue
        
        course_id = lecture_details["course_id"]
        instructor_id = lecture_details["instructor_id"]
        
        if timeslot_id in instructor_schedule[instructor_id]:
            violations["instructor_conflict"] += 1
        else:
            instructor_schedule[instructor_id].append(timeslot_id)

        if timeslot_id in room_schedule[classroom_id]:
            violations["room_conflict"] += 1
        else:
            room_schedule[classroom_id].append(timeslot_id)

        num_students_in_course = all_data["students_per_course"].get(course_id, 0)
        room_capacity = all_data["classroom_info"].get(classroom_id, {}).get("capacity", 0)
        if num_students_in_course > room_capacity:
            violations["capacity_violation"] += 1

    student_conflict_count = 0
    for student_id, enrolled_course_ids in all_data["courses_per_student"].items():
        student_timeslots_for_this_solution = []
        for assignment in solution:
            lecture_id = assignment["lecture_id"]
            assigned_course_id = all_data["lecture_info"].get(lecture_id, {}).get("course_id")
            if assigned_course_id in enrolled_course_ids:
                student_timeslots_for_this_solution.append(assignment["timeslot_id"])
        
        if len(student_timeslots_for_this_solution) != len(set(student_timeslots_for_this_solution)):
            student_conflict_count += (len(student_timeslots_for_this_solution) - len(set(student_timeslots_for_this_solution)))
    violations["student_conflict"] = student_conflict_count

    penalty_instructor = 100
    penalty_room = 100
    penalty_capacity = 50
    penalty_student = 200

    total_penalty = (
        violations["instructor_conflict"] * penalty_instructor +
        violations["room_conflict"] * penalty_room +
        violations["capacity_violation"] * penalty_capacity +
        violations["student_conflict"] * penalty_student
    )
    
    fitness = -total_penalty
    return fitness, violations

# --- Repair Function --- #
def repair_solution(solution, all_data):
    repaired_solution = [s.copy() for s in solution]
    changed = False
    available_timeslots = list(all_data["timeslot_info"].keys())
    available_classrooms = list(all_data["classroom_info"].keys())

    if not available_timeslots or not available_classrooms:
        print("Warning: No available timeslots or classrooms for repair.")
        return repaired_solution, False

    for i in range(len(repaired_solution)):
        assignment = repaired_solution[i]
        lecture_id = assignment["lecture_id"]
        original_timeslot_id = assignment["timeslot_id"]
        original_classroom_id = assignment["classroom_id"]

        lecture_details = all_data["lecture_info"].get(lecture_id)
        if not lecture_details: continue
        course_id = lecture_details["course_id"]
        instructor_id = lecture_details["instructor_id"]

        # Calculate current conflicts for THIS assignment `i` by THIS instructor
        instructor_slots_for_current_instructor = []
        for idx, other_assignment in enumerate(repaired_solution):
            if idx == i: continue
            other_lecture_details = all_data["lecture_info"].get(other_assignment["lecture_id"])
            if other_lecture_details and other_lecture_details["instructor_id"] == instructor_id:
                instructor_slots_for_current_instructor.append(other_assignment["timeslot_id"])
        
        if assignment["timeslot_id"] in instructor_slots_for_current_instructor:
            current_fix_changed = False
            for _ in range(10):
                new_timeslot = random.choice(available_timeslots)
                if new_timeslot not in instructor_slots_for_current_instructor:
                    assignment["timeslot_id"] = new_timeslot
                    changed = True
                    current_fix_changed = True
                    break
            if not current_fix_changed: assignment["timeslot_id"] = original_timeslot_id
        
        # Calculate current room conflicts for THIS assignment `i` in THIS classroom
        room_slots_for_current_room = []
        for idx, other_assignment in enumerate(repaired_solution):
            if idx == i: continue
            if other_assignment["classroom_id"] == assignment["classroom_id"]:
                room_slots_for_current_room.append(other_assignment["timeslot_id"])

        if assignment["timeslot_id"] in room_slots_for_current_room:
            fixed_by_timeslot_change_for_room_conflict = False
            for _ in range(10):
                new_timeslot = random.choice(available_timeslots)
                if new_timeslot not in room_slots_for_current_room and new_timeslot not in instructor_slots_for_current_instructor:
                    assignment["timeslot_id"] = new_timeslot
                    changed = True
                    fixed_by_timeslot_change_for_room_conflict = True
                    break
            
            if not fixed_by_timeslot_change_for_room_conflict:
                assignment["timeslot_id"] = original_timeslot_id # Revert timeslot change
                current_fix_changed_room = False
                for _ in range(10):
                    new_classroom = random.choice(available_classrooms)
                    # Check if this new_classroom is free at assignment["timeslot_id"]
                    new_room_conflict_flag = False
                    for other_idx, other_assignment_val in enumerate(repaired_solution):
                        if other_idx == i: continue
                        if other_assignment_val["classroom_id"] == new_classroom and other_assignment_val["timeslot_id"] == assignment["timeslot_id"]:
                            new_room_conflict_flag = True
                            break
                    if not new_room_conflict_flag:
                        assignment["classroom_id"] = new_classroom
                        changed = True
                        current_fix_changed_room = True
                        break
                if not current_fix_changed_room: assignment["classroom_id"] = original_classroom_id
        
        num_students_in_course = all_data["students_per_course"].get(course_id, 0)
        room_capacity = all_data["classroom_info"].get(assignment["classroom_id"], {}).get("capacity", 0)
        if num_students_in_course > room_capacity:
            current_fix_changed_cap = False
            for _ in range(10):
                new_classroom = random.choice(available_classrooms)
                new_room_capacity = all_data["classroom_info"].get(new_classroom, {}).get("capacity", 0)
                if num_students_in_course <= new_room_capacity:
                    new_room_conflict_flag = False
                    for other_idx, other_assignment_val in enumerate(repaired_solution):
                        if other_idx == i: continue
                        if other_assignment_val["classroom_id"] == new_classroom and other_assignment_val["timeslot_id"] == assignment["timeslot_id"]:
                            new_room_conflict_flag = True
                            break
                    if not new_room_conflict_flag:
                        assignment["classroom_id"] = new_classroom
                        changed = True
                        current_fix_changed_cap = True
                        break
            if not current_fix_changed_cap: assignment["classroom_id"] = original_classroom_id

    return repaired_solution, changed

if __name__ == "__main__":
    print("Fitness and Repair Functions Defined.")
    print("This script defines the functions but does not execute a full PFOA loop.")
    print("Attempting to load data and test with a dummy solution...")
    
    all_data = load_data()
    if all_data:
        print("\nGenerating a dummy solution for testing...")
        dummy_solution = []
        lecture_ids = list(all_data["lecture_info"].keys())
        timeslot_ids = list(all_data["timeslot_info"].keys())
        classroom_ids = list(all_data["classroom_info"].keys())

        if not lecture_ids or not timeslot_ids or not classroom_ids:
            print("Cannot create dummy solution: missing lectures, timeslots, or classrooms.")
        else:
            for i_lecture_id_idx, lecture_id_val in enumerate(lecture_ids):
                dummy_solution.append({
                    "lecture_id": lecture_id_val,
                    "timeslot_id": timeslot_ids[i_lecture_id_idx % len(timeslot_ids)],
                    "classroom_id": classroom_ids[i_lecture_id_idx % len(classroom_ids)]
                })
            
            print(f"Dummy solution generated with {len(dummy_solution)} assignments.")
            
            fitness, violations = calculate_fitness(dummy_solution, all_data)
            print(f"\nFitness of dummy solution: {fitness}")
            print(f"Violations in dummy solution: {violations}")
            
            repaired_dummy, repair_changed_flag = repair_solution(dummy_solution, all_data)
            if repair_changed_flag:
                print("\nDummy solution was modified by the repair function.")
                repaired_fitness, repaired_violations = calculate_fitness(repaired_dummy, all_data)
                print(f"Fitness of repaired dummy solution: {repaired_fitness}")
                print(f"Violations in repaired dummy solution: {repaired_violations}")
            else:
                print("\nRepair function did not modify the dummy solution (or no simple fixes found).")
    else:
        print("Could not load data, skipping tests.")

    print("\nScript pfoa_fitness_repair.py finished its test run.")

