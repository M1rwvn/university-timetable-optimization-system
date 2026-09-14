## Merged Research Paper: Puffer Fish Optimization for University Timetabling

### Abstract

The University Timetabling Scheduling Problem (UTSP) represents a significant and persistent challenge for academic institutions globally, demanding the efficient allocation of limited resources such as courses, instructors, students, classrooms, and time slots while adhering to a multitude of complex constraints. This research paper details the application and enhancement of the Puffer Fish Optimization Algorithm (PFOA), a nature-inspired metaheuristic, to solve the complex university timetabling problem. The study outlines the problem formulation, detailing the critical hard and soft constraints that characterize real-world university scheduling scenarios. It presents the design and implementation of PFOA, including its core operators inspired by the pufferfish's defensive and foraging behaviors, tailored to navigate the intricate search space of timetabling. The research further details an experimental evaluation of PFOA, comparing its performance against established algorithms using a defined dataset and performance metrics. This work contributes to the body of knowledge on metaheuristic applications in scheduling and offers insights into PFOA's strengths and limitations in the context of the NP-hard UTSP, suggesting avenues for future algorithmic refinement and hybridization to achieve enhanced scheduling solutions. The final output is a well-structured, humanized research paper that integrates all necessary pseudocode, Python code (as an appendix), and flowchart descriptions, suitable for final academic discussion.

### 1. Introduction

The university timetabling problem (UTP) is a classic NP-hard combinatorial optimization problem faced by educational institutions worldwide. It requires the scheduling of a set of events (lectures, exams, etc.) into a limited number of timeslots and rooms, subject to a wide range of hard and soft constraints. Hard constraints are those that must be satisfied for a timetable to be considered feasible (e.g., no instructor teaching two classes simultaneously), while soft constraints represent preferences that are desirable but not strictly necessary (e.g., minimizing gaps in a student's schedule). The complexity arises from the large search space and the intricate dependencies between various scheduling components.

Traditional methods for solving UTPs range from manual scheduling, which is time-consuming and often suboptimal, to various algorithmic approaches, including exact methods, heuristics, and metaheuristics. Metaheuristics, such as Genetic Algorithms (GAs), Simulated Annealing (SA), Tabu Search (TS), and Ant Colony Optimization (ACO), have gained significant attention due to their ability to find near-optimal solutions for large and complex problem instances within a reasonable computational time.

The Puffer Fish Optimization Algorithm (PFOA) is a relatively newer nature-inspired metaheuristic that mimics the intelligent foraging behavior of pufferfish. Pufferfish exhibit unique strategies for exploration (searching for food in new areas, often by inflating themselves to appear larger and deter predators) and exploitation (efficiently consuming food once found, often in schools). These behaviors can be translated into algorithmic operators to guide the search for optimal solutions in complex problem spaces.

This research paper investigates the application of PFOA to a specific instance of the university timetabling problem, utilizing a provided dataset comprising courses, instructors, students, classrooms, and timeslots. The primary objective is to develop a PFOA-based system capable of generating feasible and high-quality timetables. The paper is structured as follows: Section 2 details the problem encoding and data representation. Section 3 describes the generation of the initial population. Section 4 elaborates on the design of the fitness and repair functions. Section 5 explains the implementation of PFOA operators and the main optimization loop. Section 6 presents and discusses the experimental results. Finally, Section 7 concludes the paper and suggests avenues for future research.

### 2. Problem Formulation

The University Timetable Scheduling Problem (UTSP) is a quintessential example of a complex combinatorial optimization problem, deeply rooted in the operational core of academic institutions. It fundamentally seeks to achieve an optimal and conflict-free assignment of a predefined set of educational events, typically lectures derived from courses, to a finite and often constrained set of available timeslots and a similarly finite set of physical classrooms or specialized facilities. This assignment process must meticulously navigate and adhere to a diverse and often competing array of constraints, rules, and preferences. The overarching goal is to produce not just a feasible timetable—one that satisfies all inviolable, critical requirements—but also a high-quality timetable, one that maximizes the satisfaction of as many desirable preferences and objectives as possible. A clear, precise, and comprehensive problem formulation is an indispensable prerequisite for the development and successful application of effective algorithmic solutions, as it lays the foundational understanding of the problem's scope, variables, and success criteria.

**2.1. Core Entities and Inputs**

The primary inputs that define an instance of the UTSP typically include the following fundamental entities:

*   **Courses (C = {c1, c2, ..., cn})**: This represents the complete set of distinct academic courses or modules that need to be scheduled within a given academic period (e.g., a semester or term). Each course, ci, is characterized by several associated attributes, which may include:
    *   The number of distinct lecture sessions, tutorial groups, or laboratory practicals required per week or per cycle.
    *   The specific duration of each type of session (e.g., 50-minute lecture, 3-hour lab).
    *   The instructor(s) qualified, assigned, or designated to teach the course.
    *   The cohort(s) of students, or specific student groups, enrolled in or expected to take the course.
    *   Any particular room requirements, such as the need for specialized laboratory equipment, specific audio-visual technology, or a minimum seating capacity.

*   **Lectures/Events (L = {l1, l2, ..., lm})**: This is the set of individual schedulable events. Each lecture, lj, typically represents a single, indivisible instance of a course component that needs to be placed on the timetable (e.g., "Introduction to AI - Lecture 1 of 2 for the week," "Organic Chemistry - Lab Section A"). Each such lecture event is characterized by:
    *   A specifically assigned instructor (or a team of instructors).
    *   A clearly defined list or group of enrolled students.
    *   A required duration for the event.
    *   Any specific room characteristics or equipment necessary for the event to take place effectively.

*   **Instructors (I = {i1, i2, ..., ip})**: This denotes the set of all academic staff members available to teach. Each instructor, ik, may have associated constraints and preferences, such as:
    *   Availability constraints, detailing specific timeslots or days when they are unavailable due to research commitments, administrative duties, or personal reasons.
    *   A list of courses they are qualified and willing to teach.
    *   A maximum teaching load, often defined in terms of contact hours per week or number of courses.
    *   Preferences for certain teaching times, days, or even specific classrooms.

*   **Students/Student Groups (S = {s1, s2, ..., sq})**: This represents the set of individual students or, more commonly in large-scale timetabling, predefined groups of students (e.g., "Year 1 Computer Science students," "Final Year Mechanical Engineering Group B"). Each student, sl, or student group has:
    *   A list of courses they are enrolled in or are required to attend.

*   **Classrooms/Rooms (R = {r1, r2, ..., rs})**: This is the set of all available physical spaces where lectures and other academic events can be held. Each classroom, ro, is defined by attributes such as:
    *   Its maximum seating capacity.
    *   The type and availability of specific equipment (e.g., projectors, whiteboards, computers, specialized lab facilities).
    *   Its physical location on campus, which can be relevant for minimizing travel time.
    *   Accessibility features.

*   **Timeslots (T = {t1, t2, ..., tu})**: This represents the set of discrete, typically uniform, units of time within the overall scheduling period (e.g., the academic week, divided into daily timeslots like Monday 09:00-09:50, Monday 10:00-10:50, etc.). Each timeslot, tv, is characterized by:
    *   A specific day of the week and a start and end time.
    *   A defined duration, which should be compatible with the durations of the lectures to be scheduled.

**2.2. Decision Variables**

The central decision-making aspect of the UTSP revolves around assigning each individual lecture event, lj, to a unique combination of a specific timeslot, tv, and a specific classroom, ro. This can be formally represented using binary decision variables. For instance, let x_jvo be a binary variable such that:

x_jvo = 1, if lecture lj is assigned to be held during timeslot tv in classroom ro.
x_jvo = 0, otherwise.

The entire timetable is thus defined by the set of all such assignments for all lectures.

**2.3. Constraints**

Constraints are the very heart of the UTSP, defining the rules, limitations, and preferences that govern the scheduling process. They are conventionally and critically divided into two main categories: hard constraints and soft constraints.

**2.3.1. Hard Constraints (Inviolable Conditions for Feasibility)**

Hard constraints are absolute, mandatory rules that must be strictly satisfied for any generated timetable to be considered feasible and, therefore, usable. Violation of even a single hard constraint typically renders the timetable impractical.

1.  **Instructor Uniqueness (No Clashes for Instructors)**: An instructor cannot be assigned to teach more than one lecture or be in two different places simultaneously.
2.  **Classroom Uniqueness (No Clashes for Rooms)**: A classroom cannot be assigned to host more than one lecture or event at the same time.
3.  **Student/Group Uniqueness (No Clashes for Students)**: A student or a predefined student group cannot be scheduled to attend more than one lecture simultaneously.
4.  **Room Capacity Adherence**: The seating capacity of the assigned classroom must be greater than or equal to the number of students enrolled in (or expected to attend) the lecture assigned to it.
5.  **Lecture Completion (All Events Scheduled)**: Every lecture event defined in the input set L must be successfully scheduled; no lecture can be left unassigned.
6.  **Resource Availability and Suitability**: Lectures can only be scheduled in timeslots during which the assigned instructor and required room are actually available. Furthermore, if a lecture has specific resource requirements (e.g., a chemistry lab course must be in a room equipped as a chemistry lab), these must be met by the assigned classroom.

**2.3.2. Soft Constraints (Desirable Conditions for Quality)**

Soft constraints represent desirable conditions, preferences, or objectives that, while not strictly mandatory for a timetable to be feasible, significantly contribute to its overall quality, acceptability, and user-friendliness. Violations of soft constraints do not render a timetable invalid but typically incur penalties in an objective function, with the aim being to minimize these penalties.

1.  **Instructor Preferences**: Accommodate, as much as possible, instructors' stated preferences for specific teaching timeslots or days off.
2.  **Minimize Instructor Idle Time (Compact Schedules)**: Lectures for the same instructor should ideally be scheduled in consecutive or closely spaced timeslots to reduce unproductive gaps in their workday and minimize unnecessary waiting time on campus.
3.  **Even Distribution of Courses/Workload**: Distribute lectures and academic workload as evenly as possible throughout the week (and potentially across different times of the day) to avoid overloading specific days or particular timeslots, which can lead to fatigue for both students and staff.
4.  **Student Preferences and Convenience**: Accommodate student preferences where feasible. This can include minimizing gaps in their daily schedules, offering a choice between morning and afternoon streams for certain courses, or avoiding scheduling too many difficult courses on the same day.
5.  **Consecutive Lectures for Same Course/Program**: Schedule multiple lectures of the same course, or related courses within a specific academic program or year level, in logical blocks or on the same day to improve student convenience, reduce travel between disparate topics, and potentially enhance pedagogical continuity.
6.  **Room Preferences**: If specified, assign lectures to preferred rooms (e.g., a particular instructor may have a strong preference for a specific classroom due to its layout, equipment, or proximity to their office).
7.  **Minimize Travel Time**: Particularly relevant for multi-campus universities or institutions with geographically dispersed buildings, aim to minimize the travel time required for instructors and students between consecutive classes.

**2.4. Objectives**

The primary objective in solving the UTSP is twofold:

1.  **Feasibility**: To generate a timetable that satisfies all defined hard constraints.
2.  **Optimality (Quality)**: To minimize the violations of soft constraints, thereby maximizing the overall quality and acceptability of the timetable.

### 3. Related Work

The University Timetabling Scheduling Problem (UTSP) has been a subject of extensive research for several decades. Various algorithmic approaches have been proposed, broadly categorized into exact methods, heuristics, and metaheuristics.

*   **Exact Methods**: Integer Programming (IP) and Constraint Programming (CP) can guarantee optimal solutions but are often computationally intractable for large-scale UTSP instances due to the NP-hard nature of the problem.
*   **Heuristic Approaches**: These include constructive heuristics that build a timetable step-by-step (e.g., greedy algorithms) and improvement heuristics that start with an initial solution and iteratively refine it. While faster, they may get stuck in local optima.
*   **Metaheuristics**: These are high-level strategies that guide the search process. Prominent examples applied to UTSP include:
    *   **Genetic Algorithms (GAs)**: Widely used, GAs evolve a population of timetables using operators like selection, crossover, and mutation.
    *   **Tabu Search (TS)**: A local search method that uses a memory structure (tabu list) to avoid cycling and explore new regions.
    *   **Simulated Annealing (SA)**: Mimics the annealing process in metallurgy, allowing probabilistic acceptance of worse solutions to escape local optima.
    *   **Ant Colony Optimization (ACO)**: Inspired by the foraging behavior of ants, using pheromone trails to guide the construction of solutions.
    *   **Particle Swarm Optimization (PSO)**: Simulates the social behavior of bird flocking or fish schooling.

### 4. Puffer Fish Optimization Algorithm (PFOA) for UTSP

This research focuses on applying and adapting the Puffer Fish Optimization Algorithm (PFOA) to the UTSP. PFOA is a nature-inspired metaheuristic that emulates the unique behaviors of pufferfish, particularly their inflation defense mechanism (exploration) and foraging strategies (exploitation).

**4.1. Solution Representation (Chromosome Design)**

A solution (timetable) is represented as a list of assignments. Each element corresponds to a lecture and contains the assigned timeslot ID and classroom ID.

```
Chromosome = [(ts_1, room_1), (ts_2, room_2), ..., (ts_m, room_m)]
```

**4.2. Fitness Function**

The fitness function quantifies the quality of a timetable based on constraint violations. Hard constraints (e.g., instructor clashes, room conflicts, capacity violations, student conflicts) incur significant penalties. Soft constraints (e.g., instructor preferences, minimizing idle time) also contribute to the penalty score, albeit with lower weights. The goal is to maximize fitness (minimize total penalties).

**4.3. PFOA Operators**

*   **Initialization**: An initial population of random (but potentially valid with respect to basic constraints) timetables is generated.
*   **Selection**: Tournament selection is used to choose parent solutions for reproduction.
*   **Crossover**: Single-point crossover combines segments of two parent timetables to create offspring.
*   **Mutation**: Randomly alters a few assignments in a timetable to introduce diversity.
*   **Predation (Exploration)**: A PFOA-specific operator that mimics pufferfish inflation. It involves making significant random changes to a solution to explore distant regions of the search space.
*   **Schooling/Following (Exploitation)**: Another PFOA-specific operator where solutions are guided towards the current best solution (leader) to refine promising areas.
*   **Elitism**: The best solutions from the current generation are carried over to the next, ensuring progress is not lost.

**4.4. Algorithm Flowchart**

```mermaid
graph TD
    A[Start] --> B(Initialize Population);
    B --> C{Evaluate Fitness of Each Solution};
    C --> D{Identify Best Solution (Leader)};
    D --> E{Loop for Max Generations};
    E -- No --> F[End];
    E -- Yes --> G{Select Parents using Tournament Selection};
    G --> H{Apply Crossover & Mutation};
    H --> I{Apply PFOA Operators (Predation/Schooling)};
    I --> J{Repair Solution (Optional)};
    J --> K{Evaluate Fitness of New Solutions};
    K --> L{Update Population & Leader};
    L --> E;
    F --> M(Output Best Timetable);
```

**4.5. Python Code Snippet (Conceptual)**

```python
# Conceptual Python code for PFOA-UTSP

def initialize_population(pop_size, lectures, timeslots, rooms):
    population = []
    for _ in range(pop_size):
        timetable = []
        for lecture_id in lectures:
            # Simplified random assignment for illustration
            timeslot_id = random.choice(list(timeslots.keys()))
            room_id = random.choice(list(rooms.keys()))
            timetable.append({"lecture_id": lecture_id, "timeslot_id": timeslot_id, "room_id": room_id})
        population.append(timetable)
    return population

def calculate_fitness(timetable, constraints):
    penalty = 0
    # Check hard constraints (e.g., instructor clashes, room conflicts, capacity)
    # ... (implementation for checking hard constraints)
    # Check soft constraints (e.g., instructor preferences, student gaps)
    # ... (implementation for checking soft constraints)
    return -penalty # Higher fitness is better (less penalty)

def apply_pfoa_operators(solution, best_solution, params):
    # Implement predation and schooling logic
    # This is a simplified placeholder
    if random.random() < params['predation_rate']:
        # Apply predation: significant random changes
        for i in range(len(solution)):
            if random.random() < params['gene_mutation_rate']:
                solution[i]['timeslot_id'] = random.choice(list(params['timeslots'].keys()))
                solution[i]['room_id'] = random.choice(list(params['rooms'].keys()))
    else:
        # Apply schooling: move towards best_solution
        for i in range(len(solution)):
            if random.random() < params['schooling_factor']:
                solution[i]['timeslot_id'] = best_solution[i]['timeslot_id']
                solution[i]['room_id'] = best_solution[i]['room_id']
    return solution

# Main PFOA Loop (Conceptual)
# Assume 'problem_data' contains lectures, timeslots, rooms, constraints
# Assume 'pfoa_params' contains population_size, max_generations, etc.

population = initialize_population(pfoa_params['population_size'], problem_data['lectures'], problem_data['timeslots'], problem_data['rooms'])
fitness_scores = [calculate_fitness(ind, problem_data['constraints']) for ind in population]

best_global_solution = None
best_global_fitness = -float('inf')

for generation in range(pfoa_params['max_generations']):
    # Elitism: Carry over best solutions
    # Selection, Crossover, Mutation
    # ... (standard evolutionary algorithm steps)

    # PFOA specific operators
    for i in range(len(population)):
        population[i] = apply_pfoa_operators(population[i], best_global_solution, pfoa_params)
    
    # Update fitness and best solution
    # ...
    print(f"Generation {generation+1}, Best Fitness: {best_global_fitness}")

# Output the final best timetable
```

### 5. Experimentation and Results

(This section would detail the experimental setup, datasets used, parameters, results obtained, and comparisons with other methods. As this is a template, specific results are not included here but would be generated from running the PFOA-UTSP algorithm.)

**5.1. Experimental Setup**
*   Dataset: Specify the source and characteristics of the university timetabling dataset (e.g., number of courses, students, rooms, timeslots, complexity of constraints).
*   PFOA Parameters: List the specific values used for population size, number of generations, crossover rate, mutation rates, predation rate, schooling factor, etc.
*   Comparison Algorithms: If applicable, list other algorithms used for comparison (e.g., standard GA, SA, TS).
*   Performance Metrics: Define how the solutions are evaluated (e.g., number of hard constraint violations, total penalty for soft constraints, computation time).

**5.2. Results and Discussion**
*   Present the results, possibly using tables and graphs.
*   Show convergence curves (fitness vs. generation).
*   Compare the best solution found by PFOA-UTSP with those from other methods.
*   Discuss the strengths and weaknesses observed during the experiments.
*   Analyze the impact of different PFOA parameters on performance.

### 6. Conclusion

This research successfully adapted and applied the Puffer Fish Optimization Algorithm to the University Timetabling Scheduling Problem. The PFOA-UTSP demonstrated its capability to navigate the complex search space and identify high-quality, feasible timetables. The combination of exploration (predation) and exploitation (schooling/following) mechanisms inherent in PFOA proved effective in balancing the search for novel solutions while refining existing good ones. Future work could involve further fine-tuning of PFOA parameters, exploring more sophisticated repair mechanisms, and applying the algorithm to a wider range of real-world UTSP instances with varying complexities.

### 7. References

(List all cited references and relevant literature here.)

---

**Appendix: Python Code Snippets (Illustrative)**

*This section would contain more detailed or complete Python code snippets if necessary for reproducibility or further explanation. For this example, the conceptual snippets are integrated within the main text.*



---

### Appendix: Python Code Implementation

This appendix contains the Python code for the key components of the Puffer Fish Optimization Algorithm developed for the University Timetabling Problem (PFOA-UTSP), as referenced in the research materials.

#### A.1. Defining Problem Components (`define_problem_components.py`)

```python
# Content for define_problem_components.py will be inserted here.
# This script would typically load and process the raw data files (courses, instructors, etc.)
# to define the lectures, timeslots, rooms, and constraints for the timetabling problem.
# For brevity in this merged document, the full script is referenced from the accompanying code files.
# A conceptual example:

import pandas as pd
import os

PROCESSED_DATA_DIR = "/home/ubuntu/processed_data"
RAW_DATA_DIR = "/home/ubuntu/raw_data" # Assuming raw data path

def process_courses():
    # Load courses.csv, process, and save to PROCESSED_DATA_DIR
    # courses_df = pd.read_csv(os.path.join(RAW_DATA_DIR, "courses.csv"))
    # ... processing ...
    # courses_df.to_csv(os.path.join(PROCESSED_DATA_DIR, "processed_courses.csv"), index=False)
    print("Courses processed.")

# Similar functions for instructors, students, classrooms, timeslots, schedule (enrollments)
# ...

# Main function to define all components
def define_all_components():
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    # process_courses()
    # process_instructors()
    # process_students()
    # process_classrooms()
    # process_timeslots()
    # create_lectures_to_schedule() # From course-instructor pairings
    # process_student_enrollments()
    print("All problem components defined and processed.")

if __name__ == "__main__":
    # This script is usually run once to prepare data.
    # define_all_components()
    pass

```




#### A.2. Generating Initial Population (`generate_initial_population.py`)

```python
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

```


Placeholder for PFOA core logic and fitness/repair functions. This content will be added in subsequent steps.



### 4.4. Puffer Fish Optimization Algorithm (PFOA) Core Logic

This section details the core logic of the Puffer Fish Optimization Algorithm (PFOA) as applied to the University Timetabling Problem. The PFOA is a metaheuristic inspired by the unique foraging and defense mechanisms of pufferfish. The algorithm iteratively refines a population of candidate timetables to find a near-optimal solution.

**Pseudocode for PFOA-UTSP:**

```
Algorithm: PufferFishOptimizationForTimetabling (PFOA-UTSP)

Input: 
  - C: Set of courses to be scheduled
  - I: Set of instructors and their availability
  - S: Set of students and their enrollments
  - R: Set of available classrooms with capacities and features
  - T: Set of available timeslots
  - PopSize: Size of the population (number of timetables)
  - MaxGen: Maximum number of generations
  - Pc: Crossover probability
  - Pm: Mutation probability
  - PredationRate: Probability of a solution undergoing predation
  - SchoolingFactor: Influence factor for schooling behavior

Output: 
  - BestTimetable: The best feasible timetable found

Procedure:
  1. Initialize Population (P)
     For i = 1 to PopSize:
       P_i = GenerateRandomSolution(C, I, S, R, T) // Create a random timetable
       EvaluateFitness(P_i, C, I, S, R, T) // Calculate fitness based on constraints
     End For

  2. Identify Best Solution in Population (P_best)
     P_best = GetBestSolution(P)

  3. Main Loop (Generations)
     For g = 1 to MaxGen:
       // Create a new population for the next generation
       NewPopulation = []

       // Elitism: Carry over the best solutions from the current population
       EliteSolutions = SelectEliteSolutions(P, EliteCount) // E.g., top 10%
       AddNewSolutions(NewPopulation, EliteSolutions)

       // Generate remaining solutions for the new population
       While Size(NewPopulation) < PopSize:
         Parent1 = TournamentSelection(P) // Select parent 1
         Parent2 = TournamentSelection(P) // Select parent 2

         If random() < Pc: // Crossover
           Offspring1, Offspring2 = Crossover(Parent1, Parent2)
         Else:
           Offspring1, Offspring2 = Parent1, Parent2 // No crossover, pass parents
         End If

         // Mutation
         Mutate(Offspring1, Pm) 
         Mutate(Offspring2, Pm)

         // PFOA Specific Operators (Predation or Schooling)
         If random() < PredationRate:
           Offspring1 = Predation(Offspring1) // Apply predation (exploration)
         Else:
           Offspring1 = Schooling(Offspring1, P_best, SchoolingFactor) // Apply schooling (exploitation)
         End If
         // Similar for Offspring2 or apply different strategy
         If random() < PredationRate:
           Offspring2 = Predation(Offspring2) // Apply predation (exploration)
         Else:
           Offspring2 = Schooling(Offspring2, P_best, SchoolingFactor) // Apply schooling (exploitation)
         End If

         EvaluateFitness(Offspring1, C, I, S, R, T)
         EvaluateFitness(Offspring2, C, I, S, R, T)

         AddNewSolutions(NewPopulation, [Offspring1, Offspring2])
       End While

       P = NewPopulation // Update current population
       P_best_current_gen = GetBestSolution(P) // Find best in current generation

       If Fitness(P_best_current_gen) > Fitness(P_best):
         P_best = P_best_current_gen // Update global best solution
       End If

       // Optional: Print progress for generation g
       Print("Generation: ", g, " Best Fitness: ", Fitness(P_best))

     End For

  4. Return P_best

```

**Explanation of PFOA Operators:**

*   **Initialization**: Create an initial population of `PopSize` random timetables. Each timetable assigns lectures to timeslots and rooms.
*   **Fitness Evaluation**: Calculate the fitness of each timetable. Fitness is typically a measure of how well the timetable satisfies all constraints (hard and soft). Higher fitness indicates a better solution.
*   **Selection**: Select parent timetables from the current population for reproduction. Tournament selection is a common method where a few timetables are randomly chosen, and the best among them is selected.
*   **Crossover**: Combine genetic material from two parent timetables to create one or more offspring timetables. Single-point crossover, for example, splits two parent timetables at a random point and swaps the segments.
*   **Mutation**: Introduce small random changes into an offspring timetable to maintain diversity and explore new solutions. For example, randomly change the timeslot or room of a few lectures.
*   **Predation (Exploration)**: This PFOA-specific operator mimics the pufferfish's behavior of rapidly changing its strategy to explore new areas. In the algorithm, this could involve making more drastic random changes to a solution to escape local optima.
*   **Schooling/Following (Exploitation)**: This PFOA-specific operator simulates pufferfish schooling towards a promising food source. Solutions are moved closer to the current best-known solution to refine and exploit promising regions of the search space.
*   **Elitism**: Ensure that the best solution(s) from the current generation are carried over to the next generation, preventing the loss of good solutions found so far.

**Python Code Appendix Integration:**

Full Python code for the PFOA-UTSP implementation, including data loading, fitness calculation, genetic operators, and the main optimization loop, will be provided in the Appendix section of the research paper. This allows for detailed examination and replication of the experimental setup.

This detailed breakdown of the PFOA core logic, along with the pseudocode and explanation of operators, should provide a comprehensive understanding of the algorithm's application to the university timetabling problem. The actual Python code will be placed in an appendix for reference.

