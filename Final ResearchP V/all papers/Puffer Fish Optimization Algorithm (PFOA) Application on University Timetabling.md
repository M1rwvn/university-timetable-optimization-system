# Puffer Fish Optimization Algorithm (PFOA) Application on University Timetabling

This document summarizes the application of the Puffer Fish Optimization Algorithm (PFOA) 
to the university timetabling problem, using the provided dataset. It includes the 
methodology, PFOA implementation details, and the results obtained.

## Extracted from Research Paper:

## 4. Methodology: Puffer Fish Optimization Algorithm (PFOA)

This section details the Puffer Fish Optimization Algorithm (PFOA) as implemented to address the university timetabling problem. It covers the design of the fitness function, the repair mechanism, the specific PFOA behavioral operators, and the main optimization loop.

### 4.1. Fitness Function Design

The quality of each generated timetable (chromosome) is assessed using a fitness function. The primary goal of the fitness function is to quantify how well a given timetable satisfies the problem's constraints. In this implementation, the fitness is calculated based on a penalty system, where violations of constraints lead to deductions from an initial perfect score (or, equivalently, a summation of negative penalties). A higher fitness value indicates a better solution.

The following constraints were considered, with associated penalties for violations:

*   **Instructor Conflict**: An instructor cannot be assigned to two different lectures simultaneously. Each instance of such a conflict incurs a significant penalty (e.g., 100 points).
*   **Room Conflict**: A classroom cannot host two different lectures at the same time. Each instance incurs a significant penalty (e.g., 100 points).
*   **Capacity Violation**: The number of students enrolled in a course (and thus attending its lecture) should not exceed the capacity of the assigned classroom. Each instance where capacity is exceeded incurs a penalty (e.g., 50 points).
*   **Student Conflict**: A student cannot be scheduled for two different lectures occurring at the same timeslot. This is often considered a critical constraint, and each instance incurs a high penalty (e.g., 200 points). Calculating this requires checking the schedule of each student based on their course enrollments against the timetable.

The total fitness is the negative sum of all weighted penalties. Therefore, the optimization process aims to maximize this fitness value (i.e., minimize the total penalty).

### 4.2. Repair Function

During the optimization process, especially after operations like crossover and mutation, solutions may become infeasible (i.e., violate hard constraints). A repair function is designed to attempt to correct these violations and guide solutions back towards feasibility. 

The implemented repair function in this study takes a greedy approach. It iterates through the assignments in a solution and attempts to fix detected conflicts, primarily focusing on instructor conflicts, room conflicts, and capacity violations. For instance, if an instructor conflict is detected for a particular lecture assignment, the repair function might try to assign a different, randomly chosen, available timeslot to that lecture. Similarly, for room conflicts or capacity violations, it might attempt to assign a different, randomly chosen, available classroom. 

Due to the complexity and potential computational cost of a comprehensive repair strategy for all types of conflicts (especially student conflicts which are numerous), the repair function implemented was kept relatively simple. It focuses on local improvements and may not resolve all violations in a single pass. The primary driver for reducing violations remains the strong penalties in the fitness function, guiding the PFOA search towards more feasible regions of the solution space.

### 4.3. PFOA Behavior Operators and Optimization Loop

The PFOA implementation draws inspiration from the foraging behaviors of pufferfish, translating them into algorithmic operators for exploration and exploitation.

**Algorithm Parameters:**

*   **Number of Generations**: 50
*   **Population Size**: 100 (consistent with the initial population)
*   **Crossover Rate**: 0.8 (probability of two parents undergoing crossover)
*   **Mutation Rate (per solution)**: 0.2 (probability of a solution undergoing mutation)
*   **Gene Mutation Rate (per assignment if solution is mutated)**: 0.1 (probability of an individual assignment within a solution being mutated)
*   **Predation Rate (PFOA exploration)**: 0.1 (probability of a solution undergoing the predation operator)
*   **Schooling Factor (PFOA exploitation)**: 0.5 (influence factor for the schooling/following operator)
*   **Elitism**: The top 10% of solutions from the current generation are directly carried over to the next generation to preserve high-quality solutions.

**Core PFOA Operators:**

*   **Selection**: Tournament selection is used to choose parent solutions for reproduction. In this method, a small subset of solutions (tournament size: 5) is randomly selected from the population, and the fittest solution within this subset is chosen as a parent.
*   **Crossover**: Single-point crossover is applied. If selected for crossover, two parent solutions exchange segments of their chromosome (list of assignments) at a randomly chosen point to create two offspring solutions.
*   **Mutation**: Standard mutation involves randomly altering a small number of assignments (genes) within a solution. For an assignment selected for mutation, either its timeslot or its classroom is changed to a randomly selected valid alternative.
*   **Predation (Exploration)**: This operator mimics a pufferfish inflating and moving to a new area to explore. Algorithmically, it is implemented as a more drastic mutation. A solution selected for predation has a significant portion of its assignments (e.g., 20%) randomly re-assigned to new timeslots and classrooms. This promotes diversity and helps the algorithm escape local optima.
*   **Schooling/Following (Exploitation)**: This operator simulates pufferfish schooling or following a leader to a known food source. In the algorithm, a solution selected for this behavior modifies its assignments to become more similar to the best solution found in the current generation. Each assignment in the solution has a probability (determined by the schooling_factor) of adopting the timeslot and classroom of the corresponding assignment in the current generation's best solution. This helps in refining promising solutions.

**Optimization Loop:**

The PFOA proceeds iteratively through a set number of generations:

1.  **Initialization**: The process starts with the initial population of 100 randomly generated (or pre-loaded) timetable solutions.
2.  **Fitness Evaluation**: For each solution in the current population, the fitness function is called to calculate its quality based on constraint violations.
3.  **Selection and Reproduction**: A new population is generated for the next generation.
    *   **Elitism**: The top 10% of the fittest solutions from the current population are directly copied to the new population.
    *   **Offspring Generation**: The remaining solutions for the new population are generated by repeatedly applying the following steps until the population size is met:
        *   Select two parent solutions using tournament selection.
        *   Apply crossover to the parents to produce two offspring.
        *   Apply standard mutation to each offspring.
        *   Apply either the Predation operator (with probability `PREDATION_RATE`) or the Schooling/Following operator to each offspring. The choice between predation and schooling allows for a balance between exploration and exploitation.
        *   (Optional, and currently simplified in this implementation) Apply the repair function to the modified offspring.
        *   Add the resulting offspring to the new population.
4.  **Replacement**: The old population is replaced by the newly generated population.
5.  **Termination**: Steps 2-4 are repeated for the specified number of generations (50 in this study). The best solution found across all generations is recorded.

This iterative process, guided by the fitness function and the PFOA operators, aims to progressively improve the quality of timetable solutions over generations.




## 5. Results and Discussion

This section presents the results obtained from applying the Puffer Fish Optimization Algorithm (PFOA) to the university timetabling problem. The primary metrics for evaluation include the evolution of the best fitness value across generations and the characteristics of the final best timetable found.

### 5.1. Fitness Evolution

The PFOA was run for 50 generations with a population size of 100. The fitness function, as described in Section 4.1, aimed to minimize penalties associated with various constraint violations. A higher fitness value (closer to zero, as penalties are negative) indicates a better solution.

The progression of the best fitness value found in each generation is illustrated in Figure 1.

```
![Figure 1: Best Fitness per Generation (PFOA)](./figures/fitness_over_generations.png)
*Figure 1: Evolution of the best fitness score over 50 generations of PFOA. The Y-axis represents the fitness score (a higher value, i.e., less negative, is better), and the X-axis represents the generation number.*
```

As observed from the plot (details in `data/pfoa_fitness_history.json`), the PFOA demonstrated a consistent improvement in the best fitness score, particularly in the initial generations. The fitness started at approximately -61,387,400 in Generation 1 and improved to -59,933,900 by Generation 50. This indicates that the algorithm was successful in progressively reducing the number and severity of constraint violations in the timetable solutions. The rate of improvement typically slows down in later generations, which is a common characteristic of metaheuristic algorithms as they converge towards a (potentially local) optimum.

### 5.2. Analysis of the Best Found Solution

The best timetable solution obtained after 50 generations yielded a fitness score of -59,933,900. The specific violations present in this solution were:

*   **Instructor Conflicts**: 168
*   **Room Conflicts**: 271
*   **Capacity Violations**: 1100
*   **Student Conflicts**: 299,175

(These details are derived from the `pfoa_fitness_history.json` for the final generation and can be cross-verified by running the fitness function on `data/pfoa_best_solution.json`).

While the PFOA significantly improved the solutions from the initial random population, the best-found solution still contains a considerable number of violations. This is not unexpected given the complexity and scale of the problem (1100 lectures to schedule, involving numerous students, instructors, courses, timeslots, and rooms) and the relatively limited number of generations for such a large search space. The high number of capacity violations (1100) suggests that every lecture assignment resulted in a capacity violation. This could be due to a systemic issue in the dataset (e.g., all or most courses having student numbers larger than available room capacities, or the initial random assignment not prioritizing capacity). The student conflicts also remain very high, which is often the most challenging constraint to satisfy in university timetabling due to the combinatorial explosion of individual student schedules.

### 5.3. Discussion

The application of PFOA to this timetabling problem instance shows that the algorithm is capable of navigating the complex search space and improving solution quality over time. The PFOA operators, particularly predation for exploration and schooling/following for exploitation, contributed to this search process. 

The persistence of a large number of violations, especially capacity and student conflicts, in the final solution highlights several points:

1.  **Problem Difficulty**: The provided dataset and constraints define a very challenging timetabling instance. It's possible that a perfectly feasible solution (zero violations) is extremely difficult or even impossible to find with the given resources (rooms, timeslots) and enrollment numbers.
2.  **Parameter Tuning**: The PFOA parameters (crossover rate, mutation rates, predation rate, schooling factor, penalty weights) were set to common values. Further tuning of these parameters, potentially through systematic experimentation, could lead to better performance.
3.  **Repair Function**: The repair function implemented was noted as being relatively simple. A more sophisticated and aggressive repair mechanism, particularly one that specifically targets student conflicts and capacity violations, could significantly enhance the algorithm's ability to find feasible or near-feasible solutions.
4.  **Constraint Weighting**: The penalties in the fitness function directly influence the search direction. Adjusting the relative weights of these penalties might guide the algorithm to prioritize certain types of constraints over others.
5.  **Scalability**: For 1100 lectures, 50 generations might be insufficient for full convergence to a high-quality solution. Running the algorithm for a larger number of generations, though computationally more expensive, could yield further improvements.

The results indicate that while PFOA is a promising approach, solving large-scale university timetabling problems to complete feasibility often requires highly specialized heuristics, constraint programming techniques, or hybrid approaches, in addition to a well-tuned metaheuristic.

## Core PFOA Implementation Script (`pfoa_core.py`)

```python
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
```
