#!/usr/bin/env python3
import pandas as pd
import random
import json
import os
import copy
from collections import defaultdict
import time

PROCESSED_DATA_DIR = "/home/ubuntu/processed_data"
INITIAL_POP_PATH = "/home/ubuntu/pfoa_working_dir/initial_population.json"
OUTPUT_DIR = "/home/ubuntu/pfoa_working_dir"

# --- PFOA Configuration ---
NUM_GENERATIONS = 50  # Number of generations to run the PFOA
POPULATION_SIZE = 100 # Should match the size of the initial population
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.2 # Per-solution mutation rate
GENE_MUTATION_RATE = 0.1 # Per-gene (assignment) mutation rate if solution is selected for mutation

# PFOA specific parameters (placeholders, to be refined based on PFOA literature)
PREDATION_RATE = 0.1 # Probability of a solution undergoing predation (strong exploration)
SCHOOLING_FACTOR = 0.5 # Influence factor for schooling/following behavior

# --- Load Data (Copied from pfoa_fitness_repair.py for self-containment) --- #
def load_data():
    print("Loading data for PFOA core...")
    data = {}
    try:
        data["lectures"] = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "lectures_to_schedule.csv"))
        data["timeslots"] = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "valid_timeslots.csv"))
        data["classrooms"] = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "processed_classrooms.csv"))
        data["students"] = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "processed_students.csv"))
        data["courses"] = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "processed_courses.csv"))
        data["instructors"] = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "processed_instructors.csv"))
        data["enrollments"] = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "student_enrollments.csv"))
        print("All data loaded successfully for PFOA core.")
        
        data["lecture_info"] = data["lectures"].set_index("lecture_id").to_dict("index")
        data["course_info"] = data["courses"].set_index("course_id").to_dict("index")
        data["classroom_info"] = data["classrooms"].set_index("classroom_id").to_dict("index")
        data["timeslot_info"] = data["timeslots"].set_index("timeslot_id").to_dict("index")
        
        students_per_course = data["enrollments"].groupby("course_id")["student_id"].count().to_dict()
        data["students_per_course"] = students_per_course

        courses_per_student = data["enrollments"].groupby("student_id")["course_id"].apply(list).to_dict()
        data["courses_per_student"] = courses_per_student
        
        data["available_timeslots"] = list(data["timeslot_info"].keys())
        data["available_classrooms"] = list(data["classroom_info"].keys())

    except Exception as e:
        print(f"Error loading data in PFOA core: {e}")
        return None
    return data

# --- Fitness Function (Copied from pfoa_fitness_repair.py) --- #
def calculate_fitness(solution, all_data):
    fitness = 0
    violations = {
        "instructor_conflict": 0, "room_conflict": 0,
        "capacity_violation": 0, "student_conflict": 0
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
        if timeslot_id in instructor_schedule[instructor_id]: violations["instructor_conflict"] += 1
        else: instructor_schedule[instructor_id].append(timeslot_id)
        if timeslot_id in room_schedule[classroom_id]: violations["room_conflict"] += 1
        else: room_schedule[classroom_id].append(timeslot_id)
        num_students = all_data["students_per_course"].get(course_id, 0)
        room_capacity = all_data["classroom_info"].get(classroom_id, {}).get("capacity", 0)
        if num_students > room_capacity: violations["capacity_violation"] += 1

    student_conflict_count = 0
    for student_id, enrolled_ids in all_data["courses_per_student"].items():
        student_ts = []
        for assign in solution:
            lec_id = assign["lecture_id"]
            assigned_cid = all_data["lecture_info"].get(lec_id, {}).get("course_id")
            if assigned_cid in enrolled_ids: student_ts.append(assign["timeslot_id"])
        if len(student_ts) != len(set(student_ts)): student_conflict_count += (len(student_ts) - len(set(student_ts)))
    violations["student_conflict"] = student_conflict_count

    total_penalty = (violations["instructor_conflict"] * 100 + violations["room_conflict"] * 100 +
                     violations["capacity_violation"] * 50 + violations["student_conflict"] * 200)
    return -total_penalty, violations

# --- Repair Function (Copied and simplified from pfoa_fitness_repair.py) --- #
def repair_solution(solution, all_data):
    repaired_solution = copy.deepcopy(solution)
    # Basic repair: if instructor or room conflict, try a new random timeslot/room for the conflicting assignment.
    # This is a very simplified repair for demonstration. A more robust one would be needed.
    # For now, we rely more on the fitness penalty to guide the search.
    # The previous repair function was complex and might be too slow for many iterations.
    # This version will be a placeholder and can be expanded if PFOA struggles.
    _, violations = calculate_fitness(repaired_solution, all_data) # Check initial violations
    if sum(violations.values()) == 0:
        return repaired_solution, False # No repair needed
    
    # Simple example: try to fix one instructor conflict by random reassignment
    # This is not a comprehensive repair. It's more of a light touch.
    changed = False
    for i in range(len(repaired_solution)):
        # Check instructor conflict for assignment i
        # If conflict, try to change timeslot_id for repaired_solution[i]
        # This requires re-calculating instructor_schedule for the current state of repaired_solution
        # For simplicity, this repair function will be very basic for now.
        pass # Placeholder for a more effective repair strategy if needed.

    return repaired_solution, changed # Return original if no simple repair implemented

# --- PFOA Operators --- # 

def selection(population_with_fitness):
    """Selects two parents using tournament selection."""
    tournament_size = 5
    parents = []
    for _ in range(2):
        tournament = random.sample(population_with_fitness, tournament_size)
        tournament.sort(key=lambda x: x[1], reverse=True) # Sort by fitness (higher is better)
        parents.append(tournament[0][0]) # Select the best from the tournament
    return parents[0], parents[1]

def crossover(parent1, parent2):
    """Performs single-point crossover."""
    if random.random() > CROSSOVER_RATE or len(parent1) <= 1:
        return copy.deepcopy(parent1), copy.deepcopy(parent2)
    
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(solution, all_data):
    """Mutates a solution by changing a few assignments randomly."""
    if random.random() > MUTATION_RATE:
        return solution
    
    mutated_solution = copy.deepcopy(solution)
    num_mutations = 0
    for i in range(len(mutated_solution)):
        if random.random() < GENE_MUTATION_RATE:
            num_mutations += 1
            # Change timeslot or classroom for this assignment
            if random.random() < 0.5: # Mutate timeslot
                mutated_solution[i]["timeslot_id"] = random.choice(all_data["available_timeslots"])
            else: # Mutate classroom
                mutated_solution[i]["classroom_id"] = random.choice(all_data["available_classrooms"])
    # print(f"Performed {num_mutations} gene mutations in one solution")
    return mutated_solution

# PFOA-specific behaviors (Predation and Schooling/Following)
def predation(solution, all_data):
    """ PFOA Predation behavior: Pufferfish inflates, explores new area (strong mutation)."""
    # This is a more drastic mutation than the standard one.
    # For example, re-assign a larger portion of the schedule randomly.
    predated_solution = copy.deepcopy(solution)
    num_genes_to_predate = int(len(predated_solution) * 0.2) # Predate 20% of genes
    indices_to_predate = random.sample(range(len(predated_solution)), num_genes_to_predate)
    for i in indices_to_predate:
        predated_solution[i]["timeslot_id"] = random.choice(all_data["available_timeslots"])
        predated_solution[i]["classroom_id"] = random.choice(all_data["available_classrooms"])
    return predated_solution

def schooling_and_following(solution, best_solution_in_pop, all_data):
    """ PFOA Schooling/Following behavior: Move towards the best solution."""
    # For each assignment, if not matching the best, move towards it with some probability
    schooled_solution = copy.deepcopy(solution)
    for i in range(len(schooled_solution)):
        if random.random() < SCHOOLING_FACTOR: # Probability to follow
            # If this gene differs from the best solution's gene, adopt the best's gene
            if schooled_solution[i]["timeslot_id"] != best_solution_in_pop[i]["timeslot_id"]:
                schooled_solution[i]["timeslot_id"] = best_solution_in_pop[i]["timeslot_id"]
            if schooled_solution[i]["classroom_id"] != best_solution_in_pop[i]["classroom_id"]:
                schooled_solution[i]["classroom_id"] = best_solution_in_pop[i]["classroom_id"]
    return schooled_solution

# --- Main PFOA Loop --- #
def run_pfoa(all_data):
    print("\nStarting Puffer Fish Optimization Algorithm...")
    # Load initial population
    try:
        with open(INITIAL_POP_PATH, "r") as f:
            population = json.load(f)
        if len(population) != POPULATION_SIZE:
            print(f"Warning: Initial population size ({len(population)}) does not match POPULATION_SIZE ({POPULATION_SIZE}). Adjusting.")
            # Could truncate or error, for now, let's use the loaded size if different.
    except Exception as e:
        print(f"Error loading initial population from {INITIAL_POP_PATH}: {e}")
        return None, []

    best_solution_overall = None
    best_fitness_overall = -float("inf")
    fitness_history = [] # To track best fitness per generation

    start_time = time.time()
    for generation in range(NUM_GENERATIONS):
        gen_start_time = time.time()
        print(f"\nGeneration {generation + 1}/{NUM_GENERATIONS}")

        # Calculate fitness for each solution
        population_with_fitness = []
        for sol in population:
            fitness, violations = calculate_fitness(sol, all_data)
            population_with_fitness.append((sol, fitness, violations))
        
        # Sort population by fitness (descending, higher is better)
        population_with_fitness.sort(key=lambda x: x[1], reverse=True)
        
        current_best_solution_in_gen = population_with_fitness[0][0]
        current_best_fitness_in_gen = population_with_fitness[0][1]
        current_best_violations_in_gen = population_with_fitness[0][2]

        fitness_history.append({"generation": generation + 1, "best_fitness": current_best_fitness_in_gen, "violations": current_best_violations_in_gen})
        print(f"Best fitness in Gen {generation + 1}: {current_best_fitness_in_gen}, Violations: {current_best_violations_in_gen}")

        if current_best_fitness_in_gen > best_fitness_overall:
            best_fitness_overall = current_best_fitness_in_gen
            best_solution_overall = copy.deepcopy(current_best_solution_in_gen)
            print(f"New overall best solution found in Gen {generation + 1}!")

        new_population = []
        # Elitism: Carry over the top 10% of solutions
        elitism_count = int(0.1 * len(population))
        for i in range(elitism_count):
            new_population.append(population_with_fitness[i][0])

        # Generate the rest of the new population
        while len(new_population) < len(population):
            parent1, parent2 = selection(population_with_fitness)
            child1, child2 = crossover(parent1, parent2)
            
            child1 = mutate(child1, all_data)
            child2 = mutate(child2, all_data)

            # Apply PFOA specific operators
            if random.random() < PREDATION_RATE:
                child1 = predation(child1, all_data)
            else:
                child1 = schooling_and_following(child1, current_best_solution_in_gen, all_data)
            
            if random.random() < PREDATION_RATE:
                child2 = predation(child2, all_data)
            else:
                child2 = schooling_and_following(child2, current_best_solution_in_gen, all_data)
            
            # Optional: Apply repair function (can be computationally expensive)
            # child1, _ = repair_solution(child1, all_data)
            # child2, _ = repair_solution(child2, all_data)

            new_population.append(child1)
            if len(new_population) < len(population):
                new_population.append(child2)
        
        population = new_population
        gen_end_time = time.time()
        print(f"Generation {generation + 1} took {gen_end_time - gen_start_time:.2f} seconds.")

    total_time = time.time() - start_time
    print(f"\nPFOA finished after {NUM_GENERATIONS} generations.")
    print(f"Total optimization time: {total_time:.2f} seconds.")
    print(f"Best fitness found: {best_fitness_overall}")
    if best_solution_overall:
        _, best_violations = calculate_fitness(best_solution_overall, all_data)
        print(f"Violations in best solution: {best_violations}")

    return best_solution_overall, fitness_history

if __name__ == "__main__":
    all_data = load_data()
    if not all_data:
        print("Failed to load data. Exiting PFOA.")
        exit(1)
    
    if not all_data.get("available_timeslots") or not all_data.get("available_classrooms"):
        print("Available timeslots or classrooms are empty. PFOA cannot proceed.")
        exit(1)

    best_solution, history = run_pfoa(all_data)

    if best_solution:
        best_solution_path = os.path.join(OUTPUT_DIR, "pfoa_best_solution.json")
        with open(best_solution_path, "w") as f:
            json.dump(best_solution, f, indent=4)
        print(f"Best solution saved to {best_solution_path}")
    
    history_path = os.path.join(OUTPUT_DIR, "pfoa_fitness_history.json")
    with open(history_path, "w") as f:
        json.dump(history, f, indent=4)
    print(f"Fitness history saved to {history_path}")

    # Create PFOA implementation details markdown
    pfoa_details_content = f"""
# PFOA Implementation Details

This document outlines the implementation of the Puffer Fish Optimization Algorithm (PFOA) for the timetable problem.

## 1. Algorithm Parameters
- **Number of Generations**: {NUM_GENERATIONS}
- **Population Size**: {POPULATION_SIZE}
- **Crossover Rate**: {CROSSOVER_RATE}
- **Mutation Rate (per solution)**: {MUTATION_RATE}
- **Gene Mutation Rate (per assignment if solution is mutated)**: {GENE_MUTATION_RATE}
- **Predation Rate (PFOA exploration)**: {PREDATION_RATE}
- **Schooling Factor (PFOA exploitation)**: {SCHOOLING_FACTOR}
- **Elitism**: Top 10% of solutions are carried to the next generation.

## 2. Core Components
- **Fitness Function**: Evaluates solutions based on minimizing penalties for instructor conflicts, room conflicts, capacity violations, and student conflicts. Higher fitness values are better (penalties are negative).
- **Repair Function**: A simplified repair mechanism is in place. (Currently placeholder, can be expanded for more aggressive repair if needed).

## 3. PFOA Operators
- **Selection**: Tournament selection (tournament size: 5).
- **Crossover**: Single-point crossover.
- **Mutation**: Randomly changes timeslot or classroom for a small percentage of assignments in a solution.
- **Predation (Exploration)**: Simulates pufferfish inflating and exploring. Implemented as a more drastic mutation, re-assigning a larger portion (20%) of a solution's assignments randomly.
- **Schooling/Following (Exploitation)**: Simulates pufferfish following the best or schooling. Implemented by moving assignments in a solution towards the corresponding assignments in the current generation's best solution, with a certain probability (schooling_factor).

## 4. Optimization Loop
1.  Initialize population from `initial_population.json`.
2.  For each generation:
    a.  Calculate fitness for all solutions.
    b.  Identify the best solution in the current generation.
    c.  Update the overall best solution if a better one is found.
    d.  Create a new population:
        i.  Apply elitism (carry over top 10%).
        ii. Generate remaining solutions by: selecting parents, applying crossover, mutation, and PFOA-specific predation or schooling/following operators.
    e.  Replace old population with the new population.
3.  Repeat for the specified number of generations.

## 5. Outputs
- **Best Solution**: The best timetable found by PFOA is saved to `pfoa_working_dir/pfoa_best_solution.json`.
- **Fitness History**: The best fitness and violation counts for each generation are saved to `pfoa_working_dir/pfoa_fitness_history.json`.

This implementation aims to balance exploration (finding new areas of the search space) and exploitation (refining good solutions) using PFOA-inspired behaviors.
"""
    md_path = os.path.join(OUTPUT_DIR, "pfoa_implementation_details.md")
    try:
        with open(md_path, "w") as f:
            f.write(pfoa_details_content)
        print(f"PFOA implementation details saved to {md_path}")
    except Exception as e:
        print(f"Error writing PFOA implementation details: {e}")

    print("\nScript pfoa_core.py finished.")

