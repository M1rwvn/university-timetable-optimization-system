
# PFOA Implementation Details

This document outlines the implementation of the Puffer Fish Optimization Algorithm (PFOA) for the timetable problem.

## 1. Algorithm Parameters
- **Number of Generations**: 50
- **Population Size**: 100
- **Crossover Rate**: 0.8
- **Mutation Rate (per solution)**: 0.2
- **Gene Mutation Rate (per assignment if solution is mutated)**: 0.1
- **Predation Rate (PFOA exploration)**: 0.1
- **Schooling Factor (PFOA exploitation)**: 0.5
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
