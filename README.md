# Evolutionary Dynamics Repository

## Overview

This repository contains Python scripts for simulating and analyzing evolutionary dynamics on various graph structures. The repository is designed to study fixation probabilities and visualize evolutionary processes, offering both computational and graphical insights. Below is a description of the key files included and their functionality:

### Key Files

1. **`probComputing.py`**  
   - Computes fixation probabilities for various graph structures.
   - Supports plotting fixation probabilities based on:
     - Relative fitness values.
     - Population size.
   - Includes computations for:
     - The fixation probability of a counterexample by Galanis.
     - The fixation probability of a suppressor of selection.

2. **`lineGraph.py`**  
   - Simulates the evolutionary process on a line graph.
   - Produces an animated visualization of the simulation.

3. **`burstGraph.py`**  
   - Simulates the evolutionary process on a burst graph.
   - Produces an animated visualization of the simulation.

### Future Plans
- Additional simulations and analyses may be added to expand the repository's capabilities.

---

## Usage Instructions

### 1. Setting up a Python Virtual Environment
To ensure a clean and isolated environment for running the scripts, it is recommended to use a Python virtual environment. Follow these steps:

1. **Create a Virtual Environment**  
   Run the following command in the terminal:
   ```bash
   python3 -m venv venv
   ```

2. **Activate the Virtual Environment**
    - On Linux/macOS:
    ```bash
    source venv/bin/activate
    ```
    - On Windows:
    ```bash
    .\venv\Scripts\activate
    ```
3. **Install Dependencies**
Once the virtual environment is activated, install the required dependencies using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

### 2. Running the Scripts
- **probComputing.py**
Compute fixation probabilities and generate plots:
```bash
python probComputing.py <args>
```
Replace `<args>`with the appropriate command-line arguments (see the script for details).

- **lineGraph.py**
Simulate and visualize the evolutionary process on a line graph:
```bash
python lineGraph.py <number_of_nodes> <mutation_rate> <mutant_on_first>
```

- **burstGraph.py**
Simulate and visualize the evolutionary process on a burst graph:
```bash
python burstGraph.py <number_of_nodes> <mutation_rate> <mutant_on_first>
```