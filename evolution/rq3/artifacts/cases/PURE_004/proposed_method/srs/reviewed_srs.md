# Software Requirements Specification: Qheadache

## 1. Scope and Context

### [SC-001]
Qheadache shall be a standalone desktop puzzle game that players run on their own computer.

### [SC-002]
The game shall be intended for younger beginners, casual players, and adults who enjoy puzzle games.

## 2. Actors

None specified.

## 3. Functional Requirements

### [FR-001]
The game shall present a graphical board for gameplay.

### [FR-002]
The game shall allow the player to move blocks on the board.

### [FR-003]
The game shall include predefined challenges or puzzles.

### [FR-004]
The game shall recognize a puzzle as completed when the player reaches the predefined goal state for that challenge.

### [FR-005]
The game shall record completion immediately when the goal state is reached in normal play.

### [FR-006]
The game shall track time, moves, and score for player progress and results.

### [FR-007]
The game shall save player progress or results locally on the same machine.

### [FR-010]
The game shall support keyboard-only control for all essential gameplay and menu actions.

### [FR-011]
The game shall allow the mouse as an optional convenience on the board and in menus, but not require it for any core action.

### [FR-013]
The game shall allow only legal moves that fit the puzzle layout and do not move through other blocks or outside the board boundaries.

### [FR-014]
The game shall count a rejected move attempt as no action.

### [FR-015]
The game shall count one deliberate input that legitimately shifts more than one block as one action.

### [FR-016]
The game shall allow any legal move sequence unless a specific puzzle design requires a strict sequence.

### [FR-017]
If a level requires a strict move sequence, the game shall make that requirement obvious before play and provide clear feedback during play when a move would break the sequence.

### [FR-018]
The game shall keep best time and fewest actions only for completed puzzles.

### [FR-019]
The game shall not count best time and fewest actions for abandoned runs, restarted runs, or obviously invalid cases such as damaged saves or puzzles that were never properly finished.

### [FR-020]
If a puzzle is restarted, the current attempt shall stop counting and a new attempt shall begin while earlier completed results remain in history.

### [FR-021]
When a saved game is restored as a resume of the player's progress, the game shall continue the existing stats for that attempt.

### [FR-022]
If a restore effectively rewinds or changes the puzzle state so the result is no longer comparable, the game shall treat that attempt separately or exclude it from the main results.

### [FR-023]
If undo is included in the first release, the game shall flag undo separately in the record and shall not wipe out the whole attempt.

### [FR-024]
If undo is included in the first release, the game shall keep the time and move count for the attempt and indicate in the final result that undo was used.

### [FR-026]
The game shall support local user profiles or player profiles so that one person's saves do not overwrite another person's progress.

### [FR-027]
If multiple profiles are supported, each player's settings and records shall stay separate.

### [FR-028]
The game shall use simple and consistent terminology for blocks, moves, time, score, level, and puzzle.

### [FR-029]
The game shall keep terms such as current puzzle, completed puzzle, restart, continue, select puzzle, and results consistent across menus, help text, and records as much as possible.

### [FR-030]
The game shall use plain wording and avoid jargon in menus, help text, and records.

### [FR-032]
The game shall let players start, play, view results, and save progress as the focused first-release feature set.

## 4. Business Rules and Constraints

### [FR-025]
The game shall run fully offline and shall not depend on internet access or extra services.

## 5. Data and External Interfaces

None specified.

## 6. Quality Requirements

### [FR-031]
The game shall be quick to open and simple to navigate.

### [QR-001]
The game shall feel easy to understand for younger beginners, with simple controls and clear feedback.

### [QR-002]
The game shall remain engaging and challenging enough for more experienced or adult players.

### [QR-003]
The game shall provide readable text and a clear, high-contrast board.

### [QR-004]
The game should support larger font sizes if that is easy to provide, especially for menus and results screens.

### [QR-005]
The game shall run well on ordinary computers without requiring high-end hardware.

### [QR-006]
The game shall be stable and easy to maintain.

### [QR-007]
The game shall save the player's progress reliably on the local machine.

### [QR-008]
The game shall be usable in a typical home or school setting without requiring special setup.

### [QR-009]
The game shall be responsive and predictable during block movement.

### [QR-010]
The game shall make player actions clearly countable so the player knows what was done.

## 7. Exceptions and Boundary Conditions

### [FR-008]
The game shall let the player continue playing if the local save file cannot be accessed, while clearly indicating that progress or results may not be stored.

### [FR-009]
The game shall avoid corrupting existing data if the machine shuts down during saving and shall restore the last completed save on the next launch.

### [FR-012]
The game shall prevent illegal block moves.

### [EX-001]
A level may require a strict move sequence only if that requirement is part of the puzzle design and is clearly communicated to the player.

### [EX-002]
Completion may be delayed beyond the goal state only if a level has a special rule such as requiring the final arrangement to be held for a moment or confirmed by the player.

### [EX-003]
A different term may be used in a special context only if it is clearer; otherwise terminology shall remain consistent.

### [EX-004]
Starting fresh after an update is acceptable only if a major change makes old saves impossible to use, and that case should be rare and clearly explained.

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
The first release's inclusion of undo is undecided.

### [UN-002]
The first release's inclusion of tutorials is undecided.

### [UN-003]
The first release's inclusion of hints is undecided.

### [UN-004]
The first release's inclusion of account sign-in is undecided.

### [UN-005]
The first release's inclusion of sharing results is undecided.

### [UN-006]
The specific technology, engine, or storage stack for the first release is not mandated.
