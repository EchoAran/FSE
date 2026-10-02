# Software Requirements Specification: Qheadache

## 1. Scope and Context

### [SC-001]
Qheadache shall be a standalone computerized puzzle game.

### [SC-002]
Qheadache shall be usable by young beginners and adult players.

### [SC-003]
Qheadache shall present a block-moving puzzle challenge on a graphical board.

### [SC-004]
Qheadache shall support normal play without requiring external services or a network connection.

## 2. Actors

### [ST-001]
The product owner or sponsor shall define the overall direction, approve scope, and make final decisions on priority changes.

### [ST-002]
The development team shall implement the game, including board logic and tracking features, and fix issues as they arise.

### [ST-003]
Testers shall play through the game to verify solvability, fairness, usability, and correct behavior of tracking and saved results.

## 3. Functional Requirements

### [FR-001]
The system shall allow a player to start a puzzle session by launching a puzzle.

### [FR-002]
The system shall end a puzzle session when the player solves the puzzle, gives up, or exits the game.

### [FR-003]
The system shall save progress when a level is completed.

### [FR-004]
The system shall save progress during play when it can do so safely.

### [FR-005]
The system shall preserve the current puzzle state as much as possible if the player closes the game in the middle of a puzzle so play can continue later.

### [FR-006]
The system shall restore the last safe state when the game is interrupted or closed suddenly.

### [FR-007]
The system shall block invalid moves cleanly and provide immediate, clear feedback explaining why the move cannot happen.

### [FR-008]
The system shall reject invalid moves without changing the board state or losing progress.

### [FR-009]
The system shall allow the player to undo moves easily without penalty.

### [FR-010]
The system shall allow the player to restart a puzzle easily without penalty.

### [FR-011]
The system shall provide a subtle hint capability that players can request rather than having hints pushed at them.

### [FR-012]
The system shall ignore extra inputs once an action is already being processed, rather than queueing them.

### [FR-013]
The system shall preserve the board state predictably when rapid repeated clicks or inputs occur.

### [FR-014]
The system shall keep track of the player's session, puzzle state, completion time, move count, and score.

### [FR-015]
The system shall retain a history of completed puzzles or attempts.

### [FR-016]
The system shall provide a simple progress view showing puzzles completed, current time on the active puzzle, moves made, and best results if available.

### [FR-017]
The system shall allow a player to access progress and stats from a dedicated menu area such as Progress or Stats.

### [FR-018]
The system shall allow players to export stats from the same Progress or Stats area.

### [FR-019]
The system shall export basic stats by default.

### [FR-020]
The system shall allow optional inclusion of more detailed session records in stats export if supported.

### [FR-021]
The system shall show a clear confirmation message after a successful stats export, including the file location or file name.

### [FR-022]
The system shall provide a selectable view of the player's overall progress in the Progress or Stats area.

### [FR-023]
The system shall support a progress view with more detail available behind an extra click.

### [FR-024]
The system shall support player scores, times, and other progress data in a way that helps players see improvement and replay challenges.

### [FR-025]
The system shall allow the player to play offline and save progress locally without internet access.

### [FR-026]
The system shall be simple to install and launch without requiring extra services.

### [FR-027]
The system shall support a very clear and forgiving beginner experience with simple instructions, visual guidance, and an easier first level or challenge.

### [FR-028]
The system shall make the puzzles harder for more experienced players as they continue.

### [FR-029]
The system shall make time, moves, and score more prominent for more experienced players.

### [FR-030]
The system shall provide an easy way to resume play after a sudden exit or interruption.

### [FR-031]
The system shall preserve the most recently captured safe state after a sudden exit.

### [FR-032]
The system shall recover from a save file or saved result that cannot be read properly without blocking the rest of the application.

### [FR-033]
The system shall let the player start a new session when corrupted save data is encountered.

### [FR-034]
The system shall support subtle non-blocking cues only when a real problem occurs, such as a save failure or recovery event.

### [FR-035]
The system shall support update checks that are optional and unobtrusive.

### [FR-036]
The system shall display update prompts only when important updates are available and preferably after a game ends or when the player returns to a menu.

### [FR-037]
The system shall allow the player to dismiss an update prompt easily and continue playing.

### [FR-038]
The system shall support a simple local stats export that saves a readable file the player can keep or share.

### [FR-039]
The system shall not require the player to create an account for update checks or stats export.

### [FR-040]
The system shall provide a simple plain-language explanation if stats export fails and indicate whether the data was saved elsewhere.

### [FR-041]
The system shall fail quietly if an update check cannot connect and offer the player an option to try again later.

### [FR-042]
The system shall keep running normally if an update check fails or stats export fails.

### [FR-045]
The system shall support a clear and meaningful replayable challenge experience.

## 4. Business Rules and Constraints

### [BR-001]
Mobile support is out of scope unless the sponsor decides otherwise.

### [BR-002]
Automatic updates are out of scope unless the sponsor decides otherwise.

### [BR-003]
The game shall be treated as standalone and shall not need a network connection, accounts, or third-party services in the first version.

### [BR-004]
The system shall keep saved data minimal and avoid collecting personal information unless there is a very clear reason.

### [BR-005]
The system shall treat the player's current game and recent progress as higher priority than minimizing save file size.

### [BR-006]
The system shall not use heavy-handed account security or online protection.

### [BR-007]
The system shall handle corrupted save data by detecting it with basic integrity checks and recovering cleanly rather than crashing or showing nonsense.

### [BR-008]
The system shall mark obvious tampering as unreliable only if doing so does not cause problems for honest players.

### [BR-009]
If a save looks invalid, the system shall reset only the affected stats or progress as needed and inform the player in plain language.

### [BR-010]
The system shall preserve meaningful recent progress and avoid losing it during storage management.

### [BR-011]
The system shall automatically summarize older puzzle records once they are no longer needed in full detail while keeping key totals and best results intact.

### [BR-012]
The system shall begin warnings well before the save becomes a problem.

### [BR-013]
The system shall trim or summarize the oldest detailed history first, not current or recent progress, when storage needs to be reduced.

### [BR-014]
If the save file limit is exceeded, the system shall finish saving as safely as possible, preserve essential progress, and explain that older detail was condensed.

### [BR-015]
The system shall detect obvious tampering only when it can do so without causing problems for honest players.

### [BR-016]
The system shall handle repeated rapid inputs calmly by ignoring extra inputs while an action is already being processed.

### [BR-017]
The system shall provide only small non-blocking cues when there is a real problem such as a save failure or recovery event.

### [BR-018]
The system shall show warnings as subtle notifications during normal play, such as after a save or between puzzles, and use a modal dialog only when the player must make a decision or acknowledge condensed data.

### [BR-019]
The system shall not repeatedly remind the player about a save status problem unless the problem is still unresolved.

## 5. Data and External Interfaces

### [DI-001]
The system shall store progress locally on the player's device.

### [DI-002]
The system shall support a readable local file format for exported stats.

### [DI-003]
The system shall support optional update-check communication when update checks are enabled.

## 6. Quality Requirements

### [FR-043]
The system shall support a lightweight playable experience that does not make the player feel constantly interrupted.

### [FR-044]
The system shall allow the player to view overall progress in a simple, lightweight presentation without dense charts or excessive text.

### [QR-001]
The system shall be easy to understand immediately and require little or no setup or training.

### [QR-002]
The system shall provide clear feedback on player performance.

### [QR-003]
The system shall remain lightweight and easy to distribute.

### [QR-004]
The system shall be fun for players and encourage them to come back and replay challenges.

### [QR-005]
The system shall behave reliably when saving results and during gameplay flow.

### [QR-006]
The system shall keep the interface clear for younger beginners.

### [QR-007]
The system shall keep the game logic maintainable and board interactions, timing, and stored player information working correctly without introducing bugs.

### [QR-008]
The system shall remain responsive and lightweight even with a fairly large number of puzzle records.

### [QR-009]
The system shall keep the board state predictable and prevent accidental double actions.

### [QR-010]
The system shall keep the gameplay challenge intact while preventing mistakes from turning into frustration.

### [QR-011]
The system shall remain simple and reliable rather than using overly complex techniques that risk reliability.

### [QR-012]
The system shall keep saved data small through practical measures such as compression and indexing when they help without harming reliability.

### [QR-013]
The system shall load puzzle data modularly so only needed parts are loaded rather than the entire library at once.

### [QR-014]
The system shall use subtle, low-pressure prompts for important non-gameplay features and avoid interrupting gameplay.

## 7. Exceptions and Boundary Conditions

### [EX-001]
If a save file is corrupted, the system shall skip or quarantine the corrupted save so the player can continue using the game.

### [EX-002]
If a saved result cannot be read properly, the system shall recover without blocking the rest of the application.

### [EX-003]
If the game is interrupted or closed suddenly, the system shall preserve the last safe state on restart.

### [EX-004]
If an update check cannot connect, the system shall fail quietly and keep the game available for play.

### [EX-005]
If stats export fails, the system shall provide a clear explanation and keep the game running normally.

### [EX-006]
If storage becomes an issue, the system shall warn the player and preserve essential progress rather than losing everything.

### [EX-007]
If the player switches between sessions or reopens a game after a long time, the system shall load cleanly and not lose track of the player's location.

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
Support for mobile devices remains undecided.

### [UN-002]
Automatic updates remain undecided beyond being out of scope for the first version unless the sponsor decides otherwise.

### [UN-003]
The final decision on whether to include adaptive autosave timing has not yet been settled.

### [UN-004]
The exact capacity limit or storage threshold for saved progress data has not been defined.

### [UN-005]
The inclusion of more detailed session records in stats export is not yet decided.
