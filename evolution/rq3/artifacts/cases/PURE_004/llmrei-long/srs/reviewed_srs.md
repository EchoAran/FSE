# Software Requirements Specification: Qheadache

## 1. Scope and Context

### [SC-001]
Qheadache shall be a standalone computerized puzzle game.

### [SC-002]
Qheadache shall be intended for players ranging from young beginners to adult players.

## 2. Actors

None specified.

## 3. Functional Requirements

### [FR-001]
The system shall provide a graphical board for block-moving puzzle play.

### [FR-002]
The system shall allow the player to move blocks to solve a predefined challenge.

### [FR-003]
The system shall support normal play.

### [FR-004]
The system shall handle the board, the moves, and the puzzle state automatically.

### [FR-005]
The system shall enforce puzzle rules automatically.

### [FR-006]
The system shall keep track of the current puzzle state after each move.

### [FR-007]
The system shall detect when the challenge has been solved.

### [FR-008]
The system shall allow players to use mouse or touch input for block movement if possible.

### [FR-009]
The system shall prevent invalid moves from occurring.

### [FR-010]
The system shall give a clear, gentle visual cue when a move is invalid.

### [FR-011]
The system shall automatically save the player's current progress.

### [FR-012]
The system shall allow a player to resume an unfinished puzzle from the saved state.

### [FR-013]
When a player resumes an unfinished puzzle, the system shall load the exact saved board position.

### [FR-014]
When a player resumes an unfinished puzzle, the system shall continue the earlier timer and action count.

### [FR-015]
The system shall automatically store completion time, number of actions, and score after a puzzle is finished.

### [FR-016]
The system shall automatically save results without requiring the player to do anything extra.

### [FR-017]
The system shall provide a reset or replay option for the current puzzle.

### [FR-018]
The reset or replay option shall start the current puzzle over from the original beginning state.

### [FR-019]
The reset or replay option shall clear the current moves and restore the board to the initial layout.

### [FR-020]
The reset or replay option shall be easy to find during play.

### [FR-021]
The system shall provide basic success feedback when the player solves the puzzle.

### [FR-022]
The success feedback shall clearly show that the puzzle has been completed.

### [FR-023]
The success feedback shall use a simple success message or visual celebration.

### [FR-024]
If a failure condition is planned, it shall be gentle and may include offering restart or retry.

### [FR-025]
The interface shall stay very straightforward.

## 4. Business Rules and Constraints

### [BR-001]
The game shall replace manual or ad hoc tracking with automatic in-game tracking.

### [BR-002]
The game shall store player results locally in a simple way.

### [BR-003]
The game shall not require a harsh game-over as a failure mechanism.

### [BR-004]
When a player resumes the same unfinished puzzle, the timer and action count shall continue rather than reset.

### [BR-005]
The game shall be designed to work well for beginners as well as adults.

## 5. Data and External Interfaces

### [DI-001]
The system shall save and restore progress locally.

### [DI-002]
The system shall keep a simple player record or history of past completion times, actions, and scores for each puzzle.

## 6. Quality Requirements

### [QR-001]
The game shall feel responsive.

### [QR-002]
The game shall be able to be opened and used right away without special setup on the intended computer.

### [QR-003]
The game shall run reliably on the intended computer.

### [QR-004]
The game shall let players understand it quickly.

### [QR-005]
The game shall support a smooth puzzle experience.

### [QR-006]
The game shall avoid obvious crashes and data loss.

## 7. Exceptions and Boundary Conditions

### [EX-001]
If a move is invalid, the game shall reject the move and show a gentle visual indication instead of interrupting play with an error message.

### [EX-002]
If a player returns to an unfinished puzzle, the game shall offer the option to resume from the saved state.

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
It is unresolved whether the game will include a real failure condition or only success feedback.

### [UN-002]
It is unresolved whether mouse or touch input support is mandatory or only included if possible.
