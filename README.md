# University Timetable Optimization with the Puffer Fish Optimization Algorithm (PFOA)

A research project that applies a nature-inspired metaheuristic, the Puffer Fish Optimization Algorithm, to the university timetabling problem: assign lectures to timeslots and classrooms without clashes.

## The problem

Each lecture (a course plus an instructor) must get a timeslot and a room such that an instructor is never double-booked, a room never hosts two lectures at once, rooms are big enough, and no student has two lectures at the same time.

## What is here

| Path | Contents |
|---|---|
| `Final Delivering/Code/pfoa_core.py` | The implementation: encoding, penalty-based fitness, a greedy repair step, PFOA operators (predation for exploration, schooling for exploitation), main loop |
| `Final Delivering/Code/Processed Dataset/` | Small CSV samples of the processed inputs |
| `Final Delivering/Paper/`, `Final Delivering/Algo persenration.pptx` | Paper draft and slides |
| `Final ResearchP V/` | Longer research write-up, supplementary notes and the full processed data (folder `Output of Manus` holds the generated write-up drafts) |
| `Dataset/` | Raw input CSVs and the reference papers the work builds on |
| `Flowchart POAF.png`, `create_lecture_distribution_plot.py` | Algorithm flowchart and a plotting script |

The data is synthetic (generated names and `example.com` emails), not real student records.

## Run it

`pfoa_core.py` still has Windows paths from the original machine. Edit the three constants at the top (`PROCESSED_DATA_DIR`, `INITIAL_POP_PATH`, `OUTPUT_DIR`) to point at your copy, then:

```bash
pip install pandas tabulate
python "Final Delivering/Code/pfoa_core.py"
```

It also expects an `initial_population.json`, which the write-up describes generating.

## Results, with caveats

From the write-up (50 generations, 1,100 lectures): fitness improved from about -61.4 million to -59.9 million, but the best timetable is **not feasible**. It still has 168 instructor conflicts, 271 room conflicts, 1,100 capacity violations and 299,175 student conflicts. The write-up itself says the repair step is simple and that stronger repair or a hybrid method is needed. Read this as a first implementation and an honest baseline, not a solved timetable. No comparison with other algorithms was run.

## License

MIT for the code and write-ups, see `LICENSE`. The PDFs in `Dataset/Research papers/` are third-party papers kept as references and are not covered by that license.

## Diagrams and run output

### Algorithm flowcharts

![PFOA flowchart: initialization, leader selection, and the main loop with boundary check, fitness evaluation and leader update](Flowchart%20POAF.png)

![Main-loop flowchart from the research notes: predation and schooling offspring, the repair step and elitism](Delivering/pfoa%20research/WhatsApp%20Image%202025-05-14%20at%2000.13.50_b0e3674c.jpg)

### Full run (1,100 lectures, 50 generations)

![Best fitness per generation for the full run: from about -61.4M to -59.9M (negative penalty)](Final%20ResearchP%20V/Output%20of%20Manus/home/ubuntu/research_paper_pfoa/figures/fitness_over_generations.png)

![Constraint violations per generation: instructor, room, capacity and student conflicts all fall during the run but do not reach zero, which is why the best timetable is not feasible](Delivering/pfoa%20research/4f15b1698d0146a7802c1b8bcd0d04b6.jpg)

### Sample run on the small processed inputs

![Console output of a run on the small sample inputs in Final Delivering/Code/Processed Dataset: 50 generations in about 4 seconds, best fitness 0 with no conflicts, and the final timetable printed as a table. This is the small sample, not the 1,100-lecture run above](Final%20Delivering/Code/Screenshot%202025-05-22%20150905.png)
