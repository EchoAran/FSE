# Implementation task: Qheadache

The requirements below were elicited in an interview and reviewed before delivery.

## Reviewed requirements

# Software Requirements Specification: Qheadache

## 1. Scope and Context

### [SC-001]
Qheadache is a standalone computerized puzzle game.

### [SC-002]
Qheadache is intended for players ranging from young beginners to adult players.

### [SC-003]
The game shall use a graphical board for gameplay.

### [SC-004]
Qheadache is intended to be a solid standalone game that people enjoy using and returning to.

## 2. Actors

### [ST-001]
Players are key stakeholders of Qheadache.

### [ST-002]
Game designers or content owners are key stakeholders of Qheadache.

### [ST-003]
An administrator or support person may be a stakeholder for Qheadache.

## 3. Functional Requirements

### [FR-001]
The player shall move blocks on the graphical board to solve a predefined challenge.

### [FR-002]
The application shall support normal play.

### [FR-003]
The application shall retain player progress and results information, including time, actions, and scores.

### [FR-005]
The game shall be easy to pick up for players.

### [FR-007]
The game shall remain interesting for adults.

### [FR-009]
Players shall be able to complete puzzles without confusion.

### [FR-010]
Players shall be able to understand their progress clearly.

### [FR-011]
Players shall be able to replay the game or improve their times and scores.

### [FR-012]
The administrator shall be able to set up or change the puzzles that are available.

### [FR-013]
The administrator shall be able to configure the board layout.

### [FR-014]
The administrator shall be able to configure the predefined challenge the player has to solve.

### [FR-015]
The administrator shall be able to adjust difficulty-related settings.

### [FR-016]
The administrator shall be able to control which challenges are shown to beginners versus more advanced players.

### [FR-017]
The administrator shall have access to player results and progress records.

### [FR-018]
The administrator shall be able to clear player results and progress records if needed.

### [FR-019]
The administrator shall be able to archive player results and progress records if needed.

### [FR-020]
Changes made by the administrator shall be applied centrally.

## 4. Business Rules and Constraints

### [FR-021]
Unless a change is a very small setting change that can safely be applied immediately, administrator changes shall take effect the next time the game starts.

## 5. Data and External Interfaces

None specified.

## 6. Quality Requirements

None specified.

## 7. Exceptions and Boundary Conditions

None specified.

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
It is not yet confirmed whether Qheadache needs a separate technical support role beyond the administrator or support person.

## Delivery requirements

Implement the software described by the requirements above in `/workspace`.
`/workspace` is the only directory available to this task and starts empty.

1. Create a runnable program that implements the requirements.
2. Decide a build command, a test command and a run command for the program.
3. Run the build and test commands that apply and fix the problems you find.
4. Write `/workspace/delivery.json` describing how to build, test and run the program.

`delivery.json` is a JSON object with exactly these fields:

- `build_command`: shell command that prepares the program, or an empty string when no build step is needed
- `test_command`: shell command that runs the delivered tests, or an empty string when no tests are delivered
- `run_command`: shell command that starts the program
- `interface_type`: one of `http`, `cli`, `gui`, `file`
- `local_url`: URL that reaches the program when `interface_type` is `http`, otherwise an empty string
- `known_limitations`: list of strings describing what the delivered software does not do

An empty `test_command` records that no test entry point was delivered. It does
not mean that the software passes tests. Implement only what the requirements
state and do not assume behaviour that the requirements leave open.
