#!/usr/bin/env python3
import pandas as pd
import random
import json
import os
import copy
from collections import defaultdict
import time
from tabulate import tabulate

# Configuration - Update these paths as needed
PROCESSED_DATA_DIR = r"E:\Research Paper\Delivering\processed_data"
INITIAL_POP_PATH = r"E:\Research Paper\Delivering\initial_population.json"
OUTPUT_DIR = r"E:\Research Paper\Delivering\output"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Optimized PFOA Parameters
NUM_GENERATIONS = 50
POPULATION_SIZE = 60  # Reduced for faster execution
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.15
GENE_MUTATION_RATE = 0.1
PREDATION_RATE = 0.04
SCHOOLING_FACTOR = 0.7  # Higher for more exploitation

def load_data():
    """
    # تحميل البيانات
    # "هذه الدالة تقوم بتحميل جميع البيانات المطلوبة من الملفات وتجهيزها للاستخدام في الخوارزمية."
    """
    print("Loading data...")
    data = {}
    required_files = {
        "lectures": "lectures_to_schedule.csv",
        "timeslots": "valid_timeslots.csv",
        "classrooms": "processed_classrooms.csv",
        "enrollments": "student_enrollments.csv"
    }

    try:
        # Load each required file
        for key, filename in required_files.items():
            filepath = os.path.join(PROCESSED_DATA_DIR, filename)
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"Missing file: {filepath}")
            data[key] = pd.read_csv(filepath)

        # Create required dictionaries
        data["lecture_info"] = data["lectures"].set_index("lecture_id").to_dict("index")
        data["classroom_info"] = data["classrooms"].set_index("classroom_id").to_dict("index")
        data["timeslot_info"] = data["timeslots"].set_index("timeslot_id").to_dict("index")
        
        # Student-course relationships
        data["students_per_course"] = data["enrollments"].groupby("course_id")["student_id"].count().to_dict()
        
        # Available resources
        data["available_timeslots"] = list(data["timeslot_info"].keys())
        data["available_classrooms"] = list(data["classroom_info"].keys())

        print("All required data loaded successfully")
        return data

    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return None

def calculate_fitness(solution, all_data):
    """
    # حساب الملاءمة
    # "هذه الدالة تحسب قيمة الملاءمة (fitness) للحل بناءً على عدد المخالفات للقيود."
    """
    fitness = 0
    violations = {
        "instructor_conflict": 0,
        "room_conflict": 0,
        "capacity_violation": 0,
        "student_conflict": 0
    }
    
    instructor_schedule = defaultdict(set)
    room_schedule = defaultdict(set)
    student_schedules = defaultdict(set)

    for assignment in solution:
        try:
            lecture_id = assignment.get("lecture_id")
            timeslot_id = assignment.get("timeslot_id")
            classroom_id = assignment.get("classroom_id")
            
            if not all([lecture_id, timeslot_id, classroom_id]):
                continue

            lecture_details = all_data["lecture_info"].get(lecture_id, {})
            if not lecture_details:
                continue
                
            course_id = lecture_details.get("course_id")
            instructor_id = lecture_details.get("instructor_id")

            # Instructor conflicts
            if timeslot_id in instructor_schedule[instructor_id]:
                violations["instructor_conflict"] += 1
            else:
                instructor_schedule[instructor_id].add(timeslot_id)
            
            # Room conflicts
            if timeslot_id in room_schedule[classroom_id]:
                violations["room_conflict"] += 1
            else:
                room_schedule[classroom_id].add(timeslot_id)
            
            # Capacity violations
            room_capacity = all_data["classroom_info"].get(classroom_id, {}).get("capacity", 0)
            num_students = all_data["students_per_course"].get(course_id, 0)
            if num_students > room_capacity:
                violations["capacity_violation"] += 1
            
            # Student conflicts
            enrolled_students = all_data["enrollments"][all_data["enrollments"]["course_id"] == course_id]["student_id"]
            for student_id in enrolled_students:
                if timeslot_id in student_schedules[student_id]:
                    violations["student_conflict"] += 1
                else:
                    student_schedules[student_id].add(timeslot_id)

        except Exception as e:
            print(f"Error processing assignment: {str(e)}")
            continue

    total_penalty = (
        violations["instructor_conflict"] * 100 +
        violations["room_conflict"] * 100 +
        violations["capacity_violation"] * 50 +
        violations["student_conflict"] * 200
    )
    return -total_penalty, violations

def repair_solution(solution, all_data):
    """
    # إصلاح الحلول
    # "هذه الدالة تحاول إصلاح الحلول التي تحتوي على تعارضات أو مخالفات للقيود."
    """
    repaired_solution = copy.deepcopy(solution)
    changed = False
    
    # Track assignments
    instructor_assignments = defaultdict(list)
    room_assignments = defaultdict(list)
    
    # First pass to identify all assignments
    for i, assignment in enumerate(repaired_solution):
        try:
            lecture_id = assignment.get("lecture_id")
            timeslot_id = assignment.get("timeslot_id")
            classroom_id = assignment.get("classroom_id")
            
            if not all([lecture_id, timeslot_id, classroom_id]):
                continue

            lecture_details = all_data["lecture_info"].get(lecture_id, {})
            if not lecture_details:
                continue
                
            instructor_id = lecture_details.get("instructor_id")
            
            instructor_assignments[instructor_id].append((i, timeslot_id))
            room_assignments[classroom_id].append((i, timeslot_id))
        except Exception as e:
            print(f"Error tracking assignment: {str(e)}")
            continue
    
    # Second pass to repair conflicts - limited to 3 attempts per conflict
    for instructor, assignments in instructor_assignments.items():
        timeslot_groups = defaultdict(list)
        for idx, ts in assignments:
            timeslot_groups[ts].append(idx)
        
        for ts, indices in timeslot_groups.items():
            if len(indices) > 1:  # Conflict exists
                for i in indices[1:]:  # Keep first, repair others
                    for attempt in range(3):  # Try 3 times to find a solution
                        new_ts = random.choice(all_data["available_timeslots"])
                        new_room = random.choice(all_data["available_classrooms"])
                        
                        # Check if this alternative is valid
                        valid = True
                        
                        # Check instructor conflict
                        if new_ts in [t for idx, t in instructor_assignments[instructor] if idx != i]:
                            valid = False
                        
                        # Check room conflict if instructor check passed
                        if valid and new_ts in [t for idx, t in room_assignments[new_room] if idx != i]:
                            valid = False
                        
                        # Check capacity if other checks passed
                        if valid:
                            lecture_id = repaired_solution[i]["lecture_id"]
                            lecture_details = all_data["lecture_info"].get(lecture_id, {})
                            course_id = lecture_details.get("course_id", "")
                            num_students = all_data["students_per_course"].get(course_id, 0)
                            room_capacity = all_data["classroom_info"].get(new_room, {}).get("capacity", 0)
                            if num_students > room_capacity:
                                valid = False
                        
                        if valid:
                            repaired_solution[i]["timeslot_id"] = new_ts
                            repaired_solution[i]["classroom_id"] = new_room
                            changed = True
                            break
    
    return repaired_solution, changed

def selection(population_with_fitness):
    """
    # اختيار الوالدين
    # "هذه الدالة تختار الأفراد (الحلول) الأفضل لاستخدامهم في عمليات التزاوج (crossover)."
    """
    tournament_size = 3
    parents = []
    for _ in range(2):
        tournament = random.sample(population_with_fitness, tournament_size)
        tournament.sort(key=lambda x: x[1], reverse=True)
        parents.append(tournament[0][0])
    return parents[0], parents[1]

def crossover(parent1, parent2):
    """
    # التزاوج (Crossover)
    # "هذه الدالة تنفذ عملية التزاوج بين حلين لإنتاج حلول جديدة."
    """
    if random.random() > CROSSOVER_RATE or len(parent1) <= 1:
        return copy.deepcopy(parent1), copy.deepcopy(parent2)
    
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(solution, all_data):
    """
    # الطفرة (Mutation)
    # "هذه الدالة تقوم بتغيير عشوائي في بعض أجزاء الحل لزيادة التنوع."
    """
    if random.random() > MUTATION_RATE:
        return solution
    
    mutated_solution = copy.deepcopy(solution)
    for i in range(len(mutated_solution)):
        if random.random() < GENE_MUTATION_RATE:
            if random.random() < 0.5:
                mutated_solution[i]["timeslot_id"] = random.choice(all_data["available_timeslots"])
            else:
                mutated_solution[i]["classroom_id"] = random.choice(all_data["available_classrooms"])
    return mutated_solution

def predation(solution, all_data):
    """
    # الافتراس (Predation)
    # "هذه الدالة تحاكي سلوك الاستكشاف القوي عن طريق تغيير عدة جينات في الحل دفعة واحدة."
    """
    predated_solution = copy.deepcopy(solution)
    num_genes_to_predate = max(1, int(len(predated_solution) * 0.15))
    indices_to_predate = random.sample(range(len(predated_solution)), num_genes_to_predate)
    
    for i in indices_to_predate:
        predated_solution[i]["timeslot_id"] = random.choice(all_data["available_timeslots"])
        predated_solution[i]["classroom_id"] = random.choice(all_data["available_classrooms"])
    
    return predated_solution

def schooling_and_following(solution, best_solution_in_pop, all_data):
    """
    # التجمع واتباع القائد
    # "هذه الدالة تحاكي سلوك التجمع حيث يتحرك الحل نحو أفضل حل في الجيل الحالي."
    """
    schooled_solution = copy.deepcopy(solution)
    for i in range(len(schooled_solution)):
        if random.random() < SCHOOLING_FACTOR:
            if schooled_solution[i]["timeslot_id"] != best_solution_in_pop[i]["timeslot_id"]:
                schooled_solution[i]["timeslot_id"] = best_solution_in_pop[i]["timeslot_id"]
            if schooled_solution[i]["classroom_id"] != best_solution_in_pop[i]["classroom_id"]:
                schooled_solution[i]["classroom_id"] = best_solution_in_pop[i]["classroom_id"]
    return schooled_solution

def create_timetable(solution, all_data):
    """
    # إنشاء الجدول الزمني
    # "هذه الدالة تنشئ وتخزن الجدول الزمني النهائي بناءً على أفضل حل تم التوصل إليه."
    """
    table_data = []
    
    for assignment in solution:
        try:
            lecture_id = assignment.get("lecture_id")
            timeslot_id = assignment.get("timeslot_id")
            classroom_id = assignment.get("classroom_id")
            
            if not all([lecture_id, timeslot_id, classroom_id]):
                continue

            lecture_details = all_data["lecture_info"].get(lecture_id, {})
            if not lecture_details:
                continue
                
            course_id = lecture_details.get("course_id", "UNKNOWN")
            instructor_id = lecture_details.get("instructor_id", "UNKNOWN")
            
            timeslot = all_data["timeslot_info"].get(timeslot_id, {})
            classroom = all_data["classroom_info"].get(classroom_id, {})

            table_data.append({
                "Day": timeslot.get("day", "UNKNOWN"),
                "Start Time": timeslot.get("start_time", "00:00"),
                "End Time": timeslot.get("end_time", "00:00"),
                "Course": f"C-{course_id}",
                "Instructor": f"I-{instructor_id}",
                "Room": f"R-{classroom_id}",
                "Capacity": classroom.get("capacity", 0),
                "Lecture ID": lecture_id
            })
        except Exception as e:
            print(f"Error creating timetable entry: {str(e)}")
            continue

    # Save as CSV
    csv_path = os.path.join(OUTPUT_DIR, "timetable.csv")
    try:
        df = pd.DataFrame(table_data)
        df.to_csv(csv_path, index=False)
        print(f"Timetable saved as CSV: {csv_path}")
    except Exception as e:
        print(f"Error saving CSV: {str(e)}")
        csv_path = None

    # Generate formatted table for display
    display_data = []
    for row in table_data:
        display_data.append([
            row["Day"],
            row["Start Time"],
            row["End Time"],
            row["Course"],
            row["Instructor"],
            row["Room"],
            f"Cap: {row['Capacity']}"
        ])

    headers = ["Day", "Start", "End", "Course", "Instructor", "Room", "Capacity"]
    table = tabulate(display_data, headers=headers, tablefmt="grid")
    
    return table, csv_path

def run_pfoa(all_data):
    """
    # الحلقة الرئيسية لخوارزمية سمكة البخاخ
    # "هذه الدالة تنفذ جميع خطوات الخوارزمية من التهيئة حتى إيجاد أفضل حل."
    """
    print("\nStarting PFOA Timetable Optimization...")
    start_time = time.time()
    
    # Initialize population
    try:
        with open(INITIAL_POP_PATH, "r") as f:
            initial_solution = json.load(f)
        
        population = []
        for _ in range(POPULATION_SIZE):
            new_sol = copy.deepcopy(initial_solution)
            # Create initial diversity
            for assignment in new_sol:
                if random.random() < 0.2:
                    assignment["timeslot_id"] = random.choice(all_data["available_timeslots"])
                if random.random() < 0.2:
                    assignment["classroom_id"] = random.choice(all_data["available_classrooms"])
            population.append(new_sol)
        
        print(f"Initial population: {POPULATION_SIZE} solutions")
    except Exception as e:
        print(f"Error initializing population: {str(e)}")
        return None, []

    best_solution = None
    best_fitness = -float('inf')
    fitness_history = []

    for generation in range(1, NUM_GENERATIONS + 1):
        gen_start = time.time()
        
        # Evaluate population
        pop_with_fitness = []
        for sol in population:
            # Repair only every 2 generations for speed
            if generation % 2 == 0:
                repaired_sol, _ = repair_solution(sol, all_data)
            else:
                repaired_sol = sol
                
            fitness, violations = calculate_fitness(repaired_sol, all_data)
            pop_with_fitness.append((repaired_sol, fitness, violations))
        
        # Sort by fitness
        pop_with_fitness.sort(key=lambda x: x[1], reverse=True)
        
        # Track best solution
        current_best_sol, current_best_fit, current_violations = pop_with_fitness[0]
        if current_best_fit > best_fitness:
            best_fitness = current_best_fit
            best_solution = copy.deepcopy(current_best_sol)
        
        # Record history
        fitness_history.append({
            "generation": generation,
            "best_fitness": current_best_fit,
            "violations": current_violations,
            "time": time.time() - gen_start
        })

        # Create new population
        new_pop = []
        
        # Elitism - keep top 10%
        elite_count = max(1, int(POPULATION_SIZE * 0.1))
        new_pop.extend([sol for sol, _, _ in pop_with_fitness[:elite_count]])
        
        # Generate offspring
        while len(new_pop) < POPULATION_SIZE:
            parent1, parent2 = selection(pop_with_fitness)
            child1, child2 = crossover(parent1, parent2)
            
            for child in [child1, child2]:
                if len(new_pop) >= POPULATION_SIZE:
                    break
                    
                child = mutate(child, all_data)
                
                # Apply PFOA operators
                if random.random() < PREDATION_RATE:
                    child = predation(child, all_data)
                else:
                    child = schooling_and_following(child, current_best_sol, all_data)
                
                new_pop.append(child)

        population = new_pop
        gen_time = time.time() - gen_start
        
        # Print progress
        print(f"Gen {generation:02d}: Fitness={current_best_fit:>6} | "
              f"Instr={current_violations['instructor_conflict']} "
              f"Room={current_violations['room_conflict']} "
              f"Cap={current_violations['capacity_violation']} "
              f"Stud={current_violations['student_conflict']} | "
              f"Time={gen_time:.2f}s")

    total_time = time.time() - start_time
    
    # Final results
    print("\nOptimization Complete!")
    print("=====================")
    print(f"Generations: {NUM_GENERATIONS}")
    print(f"Total Time: {total_time:.2f} seconds")
    print(f"Best Fitness: {best_fitness}")
    
    if best_solution:
        _, final_violations = calculate_fitness(best_solution, all_data)
        print("\nViolations in Best Solution:")
        print(f"  Instructor Conflicts: {final_violations['instructor_conflict']}")
        print(f"  Room Conflicts: {final_violations['room_conflict']}")
        print(f"  Capacity Violations: {final_violations['capacity_violation']}")
        print(f"  Student Conflicts: {final_violations['student_conflict']}")
    
    return best_solution, fitness_history

def save_results(best_solution, history, all_data):
    """
    # حفظ النتائج
    # "هذه الدالة تحفظ أفضل حل، الجدول الزمني، وتاريخ الملاءمة في ملفات منفصلة."
    """
    results = {
        "best_solution": None,
        "timetable": None,
        "csv_path": None,
        "history": None
    }
    
    # Save best solution
    best_sol_path = os.path.join(OUTPUT_DIR, "best_solution.json")
    try:
        with open(best_sol_path, "w") as f:
            json.dump(best_solution, f, indent=4)
        results["best_solution"] = best_sol_path
        print(f"\nSaved best solution to: {best_sol_path}")
    except Exception as e:
        print(f"Error saving best solution: {str(e)}")
    
    # Save timetable
    timetable, csv_path = create_timetable(best_solution, all_data)
    timetable_path = os.path.join(OUTPUT_DIR, "timetable.txt")
    try:
        with open(timetable_path, "w") as f:
            f.write(timetable)
        results["timetable"] = timetable_path
        results["csv_path"] = csv_path
        print(f"Saved timetable to: {timetable_path}")
        if csv_path:
            print(f"Saved CSV to: {csv_path}")
    except Exception as e:
        print(f"Error saving timetable: {str(e)}")
    
    # Save history
    history_path = os.path.join(OUTPUT_DIR, "fitness_history.json")
    try:
        with open(history_path, "w") as f:
            json.dump(history, f, indent=4)
        results["history"] = history_path
        print(f"Saved fitness history to: {history_path}")
    except Exception as e:
        print(f"Error saving history: {str(e)}")
    
    return results

def main():
    """
    # الدالة الرئيسية
    # "هذه الدالة تنفذ جميع الخطوات: تحميل البيانات، تشغيل الخوارزمية، وحفظ النتائج."
    """
    print("University Timetable Optimization using PFOA")
    print("==========================================")
    
    # Load data
    all_data = load_data()
    if not all_data:
        print("Failed to load required data. Exiting.")
        return
    
    # Run optimization
    best_solution, history = run_pfoa(all_data)
    
    if best_solution:
        # Save results
        results = save_results(best_solution, history, all_data)
        
        # Display final timetable if available
        if results.get("timetable"):
            try:
                with open(results["timetable"], "r") as f:
                    print("\nFinal Timetable:\n")
                    print(f.read())
            except Exception as e:
                print(f"Error displaying timetable: {str(e)}")
    
    print("\nProgram completed.")

if __name__ == "__main__":
    main()