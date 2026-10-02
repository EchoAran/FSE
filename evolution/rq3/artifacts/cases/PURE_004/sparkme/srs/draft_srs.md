# Software Requirements Specification: Qheadache

## 1. Scope and Context

### [SC-001] (stated)
Qheadache shall be a standalone computerized puzzle game.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Qheadache is intended to be a standalone computerized puzzle game for people ranging from young beginners to adult players. Players use a graphical board to move blocks and solve a predefined challenge. The application should support normal play and retain useful information about a player's progress and results, such as time, actions, and scores."
- `[interview_turn:T002]` "Qheadache is meant to be a simple standalone puzzle game where players can pick it up and start solving challenges right away without needing anything else. The main goal is to give people a fun block-moving puzzle that works for beginners as well as adults, with clear feedback on how they’re doing. We also want it to keep track of progress and results like time, moves or actions, and score so players can see improvement and replay challenges."

### [SC-002] (stated)
Qheadache shall be usable by young beginners and adult players.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Qheadache is intended to be a standalone computerized puzzle game for people ranging from young beginners to adult players. Players use a graphical board to move blocks and solve a predefined challenge. The application should support normal play and retain useful information about a player's progress and results, such as time, actions, and scores."
- `[interview_turn:T002]` "Qheadache is meant to be a simple standalone puzzle game where players can pick it up and start solving challenges right away without needing anything else. The main goal is to give people a fun block-moving puzzle that works for beginners as well as adults, with clear feedback on how they’re doing. We also want it to keep track of progress and results like time, moves or actions, and score so players can see improvement and replay challenges."
- `[interview_turn:T008]` "We mainly think of two broad groups: younger beginners who need a very straightforward experience, and more experienced players or adults who want a bit more of a challenge. The younger group would likely benefit from simpler presentation and easier onboarding, while the more experienced group will care more about challenge, speed, and score. I don’t have a more formal segmentation than that yet, but those are the main differences we’re planning around."

### [SC-003] (stated)
Qheadache shall present a block-moving puzzle challenge on a graphical board.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Qheadache is intended to be a standalone computerized puzzle game for people ranging from young beginners to adult players. Players use a graphical board to move blocks and solve a predefined challenge. The application should support normal play and retain useful information about a player's progress and results, such as time, actions, and scores."
- `[interview_turn:T002]` "Qheadache is meant to be a simple standalone puzzle game where players can pick it up and start solving challenges right away without needing anything else. The main goal is to give people a fun block-moving puzzle that works for beginners as well as adults, with clear feedback on how they’re doing. We also want it to keep track of progress and results like time, moves or actions, and score so players can see improvement and replay challenges."

### [SC-004] (stated)
Qheadache shall support normal play without requiring external services or a network connection.

**Source Evidence:**
- `[interview_turn:T006]` "We’re assuming it will run as a standalone application on a typical desktop or laptop, and it should be simple to install and launch without needing extra services. Offline use is important, since players should still be able to play and have their progress saved locally even without internet access. I’m not sure yet whether we need to support mobile devices or automatic updates, so I’d want to check that with the team."
- `[interview_turn:T040]` "At the moment, I’d treat external integrations as out of scope for the first version. The game should stand on its own without needing a network connection, accounts, or third-party services. If we do anything later, the most likely candidates would be simple update checks or maybe optional stats export, but that hasn’t been decided."

## 2. Actors

### [ST-001] (stated)
The product owner or sponsor shall define the overall direction, approve scope, and make final decisions on priority changes.

**Source Evidence:**
- `[interview_turn:T012]` "At the moment, the main stakeholders are the product owner or sponsor, the small development team, and whoever is responsible for testing the gameplay and usability. The sponsor decides the overall direction and what counts as success, while the developers handle the implementation and any technical constraints. Testing is important to make sure the puzzles are understandable and that the progress tracking, timing, and scoring behave correctly for players."
- `[interview_turn:T014]` "The product owner would usually define the puzzle vision, approve the scope, and make the final call on priority changes during design and development. Developers would turn that into the actual game, build the board logic and tracking features, and fix issues as they come up. Testers would play through the game, check that the challenges are solvable and fair, and report anything confusing or broken, especially around gameplay flow and saved results."

### [ST-002] (stated)
The development team shall implement the game, including board logic and tracking features, and fix issues as they arise.

**Source Evidence:**
- `[interview_turn:T012]` "At the moment, the main stakeholders are the product owner or sponsor, the small development team, and whoever is responsible for testing the gameplay and usability. The sponsor decides the overall direction and what counts as success, while the developers handle the implementation and any technical constraints. Testing is important to make sure the puzzles are understandable and that the progress tracking, timing, and scoring behave correctly for players."
- `[interview_turn:T014]` "The product owner would usually define the puzzle vision, approve the scope, and make the final call on priority changes during design and development. Developers would turn that into the actual game, build the board logic and tracking features, and fix issues as they come up. Testers would play through the game, check that the challenges are solvable and fair, and report anything confusing or broken, especially around gameplay flow and saved results."

### [ST-003] (stated)
Testers shall play through the game to verify solvability, fairness, usability, and correct behavior of tracking and saved results.

**Source Evidence:**
- `[interview_turn:T012]` "At the moment, the main stakeholders are the product owner or sponsor, the small development team, and whoever is responsible for testing the gameplay and usability. The sponsor decides the overall direction and what counts as success, while the developers handle the implementation and any technical constraints. Testing is important to make sure the puzzles are understandable and that the progress tracking, timing, and scoring behave correctly for players."
- `[interview_turn:T014]` "The product owner would usually define the puzzle vision, approve the scope, and make the final call on priority changes during design and development. Developers would turn that into the actual game, build the board logic and tracking features, and fix issues as they come up. Testers would play through the game, check that the challenges are solvable and fair, and report anything confusing or broken, especially around gameplay flow and saved results."
- `[interview_turn:T016]` "The product owner will mostly care that the game is fun, easy to understand, and keeps players coming back, so they’ll pay attention to challenge balance, replay value, and whether the progress data is useful. Testers are likely to focus on whether the interface is clear, whether moves and scoring are consistent, and whether the game behaves reliably when saving results. Developers will be concerned with keeping the logic maintainable and making sure the board interactions, timing, and stored player information all work correctly without introducing bugs."

## 3. Functional Requirements

### [FR-001] (stated)
The system shall allow a player to start a puzzle session by launching a puzzle.

**Source Evidence:**
- `[interview_turn:T018]` "A session would start when the player launches a puzzle and ends when they either solve it, give up, or exit the game. Progress should be saved whenever a level is completed, and probably also during play if we can do that safely, so results aren’t lost unexpectedly. I’m not aware of any special business triggers beyond those core gameplay events, but the team would obviously want to review results and issues after testing or release."

### [FR-002] (stated)
The system shall end a puzzle session when the player solves the puzzle, gives up, or exits the game.

**Source Evidence:**
- `[interview_turn:T018]` "A session would start when the player launches a puzzle and ends when they either solve it, give up, or exit the game. Progress should be saved whenever a level is completed, and probably also during play if we can do that safely, so results aren’t lost unexpectedly. I’m not aware of any special business triggers beyond those core gameplay events, but the team would obviously want to review results and issues after testing or release."

### [FR-003] (stated)
The system shall save progress when a level is completed.

**Source Evidence:**
- `[interview_turn:T018]` "A session would start when the player launches a puzzle and ends when they either solve it, give up, or exit the game. Progress should be saved whenever a level is completed, and probably also during play if we can do that safely, so results aren’t lost unexpectedly. I’m not aware of any special business triggers beyond those core gameplay events, but the team would obviously want to review results and issues after testing or release."

### [FR-004] (conditional)
The system shall save progress during play when it can do so safely.

**Source Evidence:**
- `[interview_turn:T018]` "A session would start when the player launches a puzzle and ends when they either solve it, give up, or exit the game. Progress should be saved whenever a level is completed, and probably also during play if we can do that safely, so results aren’t lost unexpectedly. I’m not aware of any special business triggers beyond those core gameplay events, but the team would obviously want to review results and issues after testing or release."
- `[interview_turn:T032]` "We haven’t settled anything specific yet, but adaptive autosave based on activity would make sense, like saving more often after a few moves or after a longer session. For alerts, I’d prefer small non-blocking cues only when there’s a real problem, such as a save failure or recovery event, and otherwise let the game keep moving. The big priority is that the player should feel protected, not constantly interrupted."

### [FR-005] (stated)
The system shall preserve the current puzzle state as much as possible if the player closes the game in the middle of a puzzle so play can continue later.

**Source Evidence:**
- `[interview_turn:T022]` "One tricky case is if the player closes the game in the middle of a puzzle, and we’d want the current state to be preserved as much as possible so they can continue later. Another is if a saved result can’t be read properly, where the game should recover without blocking the rest of the app. Beyond that, I’d expect basic invalid actions to be handled quietly and consistently so the player never feels punished for exploring the interface."
- `[interview_turn:T026]` "Yes, I’d want the game to handle a few things very carefully. If the player makes an invalid move, it should just be rejected with clear feedback and no loss of progress. If the game is interrupted or closed suddenly, it should restore the last safe state on restart, and if a save file is corrupted, it should isolate that problem and let the player start a new session without crashing the whole game."

### [FR-006] (stated)
The system shall restore the last safe state when the game is interrupted or closed suddenly.

**Source Evidence:**
- `[interview_turn:T026]` "Yes, I’d want the game to handle a few things very carefully. If the player makes an invalid move, it should just be rejected with clear feedback and no loss of progress. If the game is interrupted or closed suddenly, it should restore the last safe state on restart, and if a save file is corrupted, it should isolate that problem and let the player start a new session without crashing the whole game."
- `[interview_turn:T030]` "The main ones are invalid moves, sudden exits, and bad save data. Invalid moves should never change the board state, sudden exits should preserve whatever was safely captured most recently, and corrupted saves should be skipped or quarantined so the player can keep using the game. I’d also want repeated rapid clicks or inputs handled calmly so the interface doesn’t get into a weird state."

### [FR-007] (stated)
The system shall block invalid moves cleanly and provide immediate, clear feedback explaining why the move cannot happen.

**Source Evidence:**
- `[interview_turn:T020]` "Invalid moves should just be blocked cleanly, with some immediate feedback so the player understands why the move can’t happen. For corrupted save data, we’d want the game to fail gracefully, ideally by ignoring the bad file and starting fresh rather than crashing. Unexpected actions should be handled conservatively, meaning we’d rather prevent confusion and keep the game stable than try to be clever in those edge cases."
- `[interview_turn:T026]` "Yes, I’d want the game to handle a few things very carefully. If the player makes an invalid move, it should just be rejected with clear feedback and no loss of progress. If the game is interrupted or closed suddenly, it should restore the last safe state on restart, and if a save file is corrupted, it should isolate that problem and let the player start a new session without crashing the whole game."

### [FR-008] (stated)
The system shall reject invalid moves without changing the board state or losing progress.

**Source Evidence:**
- `[interview_turn:T026]` "Yes, I’d want the game to handle a few things very carefully. If the player makes an invalid move, it should just be rejected with clear feedback and no loss of progress. If the game is interrupted or closed suddenly, it should restore the last safe state on restart, and if a save file is corrupted, it should isolate that problem and let the player start a new session without crashing the whole game."
- `[interview_turn:T030]` "The main ones are invalid moves, sudden exits, and bad save data. Invalid moves should never change the board state, sudden exits should preserve whatever was safely captured most recently, and corrupted saves should be skipped or quarantined so the player can keep using the game. I’d also want repeated rapid clicks or inputs handled calmly so the interface doesn’t get into a weird state."

### [FR-009] (stated)
The system shall allow the player to undo moves easily without penalty.

**Source Evidence:**
- `[interview_turn:T044]` "I’d want the game to be forgiving, so players can undo moves and restart a puzzle easily without penalty. If someone is stuck, a subtle hint system would be better than a big explanation, maybe something optional they can ask for rather than having it pushed at them. The idea is to keep the challenge intact while making sure mistakes don’t turn into frustration."

### [FR-010] (stated)
The system shall allow the player to restart a puzzle easily without penalty.

**Source Evidence:**
- `[interview_turn:T044]` "I’d want the game to be forgiving, so players can undo moves and restart a puzzle easily without penalty. If someone is stuck, a subtle hint system would be better than a big explanation, maybe something optional they can ask for rather than having it pushed at them. The idea is to keep the challenge intact while making sure mistakes don’t turn into frustration."

### [FR-011] (stated)
The system shall provide a subtle hint capability that players can request rather than having hints pushed at them.

**Source Evidence:**
- `[interview_turn:T044]` "I’d want the game to be forgiving, so players can undo moves and restart a puzzle easily without penalty. If someone is stuck, a subtle hint system would be better than a big explanation, maybe something optional they can ask for rather than having it pushed at them. The idea is to keep the challenge intact while making sure mistakes don’t turn into frustration."

### [FR-012] (stated)
The system shall ignore extra inputs once an action is already being processed, rather than queueing them.

**Source Evidence:**
- `[interview_turn:T034]` "I’d lean toward ignoring extra inputs once an action is already being processed, rather than queueing them, because queueing could create confusing or unintended moves. If the player is clicking too fast, a small visual cue like a brief highlight or button lockout would be enough to show the input was received but not duplicated. The important thing is to keep the board state predictable and prevent accidental double actions."

### [FR-013] (stated)
The system shall preserve the board state predictably when rapid repeated clicks or inputs occur.

**Source Evidence:**
- `[interview_turn:T030]` "The main ones are invalid moves, sudden exits, and bad save data. Invalid moves should never change the board state, sudden exits should preserve whatever was safely captured most recently, and corrupted saves should be skipped or quarantined so the player can keep using the game. I’d also want repeated rapid clicks or inputs handled calmly so the interface doesn’t get into a weird state."
- `[interview_turn:T034]` "I’d lean toward ignoring extra inputs once an action is already being processed, rather than queueing them, because queueing could create confusing or unintended moves. If the player is clicking too fast, a small visual cue like a brief highlight or button lockout would be enough to show the input was received but not duplicated. The important thing is to keep the board state predictable and prevent accidental double actions."

### [FR-014] (stated)
The system shall keep track of the player's session, puzzle state, completion time, move count, and score.

**Source Evidence:**
- `[interview_turn:T038]` "The main data we care about is the player’s session, the puzzle state, completion time, move count, and score. We’d also want to keep some history of completed puzzles or attempts so we can see whether players are improving and where they tend to struggle. That helps us tune difficulty, keep the game replayable, and give players a sense of progress without making it feel competitive in a heavy way."

### [FR-015] (stated)
The system shall retain a history of completed puzzles or attempts.

**Source Evidence:**
- `[interview_turn:T038]` "The main data we care about is the player’s session, the puzzle state, completion time, move count, and score. We’d also want to keep some history of completed puzzles or attempts so we can see whether players are improving and where they tend to struggle. That helps us tune difficulty, keep the game replayable, and give players a sense of progress without making it feel competitive in a heavy way."

### [FR-016] (stated)
The system shall provide a simple progress view showing puzzles completed, current time on the active puzzle, moves made, and best results if available.

**Source Evidence:**
- `[interview_turn:T052]` "I’d want a very simple progress view that shows the basics at a glance, like puzzles completed, current time on the active puzzle, moves made, and perhaps best results if available. It should be easy to understand quickly, especially for younger players, so no dense charts or too much text. If someone wants more detail, that could be available behind an extra click, but the default view should stay clean and lightweight."

### [FR-017] (stated)
The system shall allow a player to access progress and stats from a dedicated menu area such as Progress or Stats.

**Source Evidence:**
- `[interview_turn:T048]` "A dedicated menu option would be the cleanest approach, probably from a progress or settings area rather than tied to finishing a puzzle. I’d want the player to see their overall progress there, with the export option available from the same place so it feels intentional instead of forced. As for control, they should be able to export only the basic stats by default, and if we include more detail later, it should be optional and clearly labeled."
- `[interview_turn:T054]` "I’d expect the player to go into a menu like Progress or Stats, choose what they want to look at, and then select an export option from there. The export should default to the core summary data, with an optional choice to include more detailed session records if we decide to support that. After it finishes, the game should show a clear confirmation message with the file location or name so the player knows it really worked."

### [FR-018] (stated)
The system shall allow players to export stats from the same Progress or Stats area.

**Source Evidence:**
- `[interview_turn:T048]` "A dedicated menu option would be the cleanest approach, probably from a progress or settings area rather than tied to finishing a puzzle. I’d want the player to see their overall progress there, with the export option available from the same place so it feels intentional instead of forced. As for control, they should be able to export only the basic stats by default, and if we include more detail later, it should be optional and clearly labeled."
- `[interview_turn:T054]` "I’d expect the player to go into a menu like Progress or Stats, choose what they want to look at, and then select an export option from there. The export should default to the core summary data, with an optional choice to include more detailed session records if we decide to support that. After it finishes, the game should show a clear confirmation message with the file location or name so the player knows it really worked."

### [FR-019] (stated)
The system shall export basic stats by default.

**Source Evidence:**
- `[interview_turn:T048]` "A dedicated menu option would be the cleanest approach, probably from a progress or settings area rather than tied to finishing a puzzle. I’d want the player to see their overall progress there, with the export option available from the same place so it feels intentional instead of forced. As for control, they should be able to export only the basic stats by default, and if we include more detail later, it should be optional and clearly labeled."
- `[interview_turn:T054]` "I’d expect the player to go into a menu like Progress or Stats, choose what they want to look at, and then select an export option from there. The export should default to the core summary data, with an optional choice to include more detailed session records if we decide to support that. After it finishes, the game should show a clear confirmation message with the file location or name so the player knows it really worked."

### [FR-020] (conditional)
The system shall allow optional inclusion of more detailed session records in stats export if supported.

**Source Evidence:**
- `[interview_turn:T048]` "A dedicated menu option would be the cleanest approach, probably from a progress or settings area rather than tied to finishing a puzzle. I’d want the player to see their overall progress there, with the export option available from the same place so it feels intentional instead of forced. As for control, they should be able to export only the basic stats by default, and if we include more detail later, it should be optional and clearly labeled."
- `[interview_turn:T054]` "I’d expect the player to go into a menu like Progress or Stats, choose what they want to look at, and then select an export option from there. The export should default to the core summary data, with an optional choice to include more detailed session records if we decide to support that. After it finishes, the game should show a clear confirmation message with the file location or name so the player knows it really worked."

### [FR-021] (stated)
The system shall show a clear confirmation message after a successful stats export, including the file location or file name.

**Source Evidence:**
- `[interview_turn:T046]` "Update prompts should feel rare and low-pressure, ideally only after the player finishes a game or returns to a menu, not in the middle of solving a puzzle. If there’s a choice, they should be able to dismiss it easily and keep playing. For stats, I’d want a simple view with clear numbers and maybe an export confirmation so the player knows the file was created successfully, but nothing overly detailed or technical."
- `[interview_turn:T054]` "I’d expect the player to go into a menu like Progress or Stats, choose what they want to look at, and then select an export option from there. The export should default to the core summary data, with an optional choice to include more detailed session records if we decide to support that. After it finishes, the game should show a clear confirmation message with the file location or name so the player knows it really worked."

### [FR-022] (stated)
The system shall provide a selectable view of the player's overall progress in the Progress or Stats area.

**Source Evidence:**
- `[interview_turn:T048]` "A dedicated menu option would be the cleanest approach, probably from a progress or settings area rather than tied to finishing a puzzle. I’d want the player to see their overall progress there, with the export option available from the same place so it feels intentional instead of forced. As for control, they should be able to export only the basic stats by default, and if we include more detail later, it should be optional and clearly labeled."
- `[interview_turn:T052]` "I’d want a very simple progress view that shows the basics at a glance, like puzzles completed, current time on the active puzzle, moves made, and perhaps best results if available. It should be easy to understand quickly, especially for younger players, so no dense charts or too much text. If someone wants more detail, that could be available behind an extra click, but the default view should stay clean and lightweight."

### [FR-023] (conditional)
The system shall support a progress view with more detail available behind an extra click.

**Source Evidence:**
- `[interview_turn:T052]` "I’d want a very simple progress view that shows the basics at a glance, like puzzles completed, current time on the active puzzle, moves made, and perhaps best results if available. It should be easy to understand quickly, especially for younger players, so no dense charts or too much text. If someone wants more detail, that could be available behind an extra click, but the default view should stay clean and lightweight."

### [FR-024] (stated)
The system shall support player scores, times, and other progress data in a way that helps players see improvement and replay challenges.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Qheadache is intended to be a standalone computerized puzzle game for people ranging from young beginners to adult players. Players use a graphical board to move blocks and solve a predefined challenge. The application should support normal play and retain useful information about a player's progress and results, such as time, actions, and scores."
- `[interview_turn:T002]` "Qheadache is meant to be a simple standalone puzzle game where players can pick it up and start solving challenges right away without needing anything else. The main goal is to give people a fun block-moving puzzle that works for beginners as well as adults, with clear feedback on how they’re doing. We also want it to keep track of progress and results like time, moves or actions, and score so players can see improvement and replay challenges."
- `[interview_turn:T038]` "The main data we care about is the player’s session, the puzzle state, completion time, move count, and score. We’d also want to keep some history of completed puzzles or attempts so we can see whether players are improving and where they tend to struggle. That helps us tune difficulty, keep the game replayable, and give players a sense of progress without making it feel competitive in a heavy way."

### [FR-025] (stated)
The system shall allow the player to play offline and save progress locally without internet access.

**Source Evidence:**
- `[interview_turn:T006]` "We’re assuming it will run as a standalone application on a typical desktop or laptop, and it should be simple to install and launch without needing extra services. Offline use is important, since players should still be able to play and have their progress saved locally even without internet access. I’m not sure yet whether we need to support mobile devices or automatic updates, so I’d want to check that with the team."

### [FR-026] (stated)
The system shall be simple to install and launch without requiring extra services.

**Source Evidence:**
- `[interview_turn:T006]` "We’re assuming it will run as a standalone application on a typical desktop or laptop, and it should be simple to install and launch without needing extra services. Offline use is important, since players should still be able to play and have their progress saved locally even without internet access. I’m not sure yet whether we need to support mobile devices or automatic updates, so I’d want to check that with the team."

### [FR-027] (stated)
The system shall support a very clear and forgiving beginner experience with simple instructions, visual guidance, and an easier first level or challenge.

**Source Evidence:**
- `[interview_turn:T010]` "For beginners, we’d want the game to be very clear and forgiving, with simple instructions, visual guidance, and an easier first level or challenge. For more experienced players, the same core interface can stay, but the puzzles should become harder and the feedback around time, moves, and score should matter more. I don’t think we want entirely separate modes at this stage, just a progression that feels accessible at the start and more demanding as players continue."

### [FR-028] (stated)
The system shall make the puzzles harder for more experienced players as they continue.

**Source Evidence:**
- `[interview_turn:T010]` "For beginners, we’d want the game to be very clear and forgiving, with simple instructions, visual guidance, and an easier first level or challenge. For more experienced players, the same core interface can stay, but the puzzles should become harder and the feedback around time, moves, and score should matter more. I don’t think we want entirely separate modes at this stage, just a progression that feels accessible at the start and more demanding as players continue."

### [FR-029] (stated)
The system shall make time, moves, and score more prominent for more experienced players.

**Source Evidence:**
- `[interview_turn:T010]` "For beginners, we’d want the game to be very clear and forgiving, with simple instructions, visual guidance, and an easier first level or challenge. For more experienced players, the same core interface can stay, but the puzzles should become harder and the feedback around time, moves, and score should matter more. I don’t think we want entirely separate modes at this stage, just a progression that feels accessible at the start and more demanding as players continue."
- `[interview_turn:T008]` "We mainly think of two broad groups: younger beginners who need a very straightforward experience, and more experienced players or adults who want a bit more of a challenge. The younger group would likely benefit from simpler presentation and easier onboarding, while the more experienced group will care more about challenge, speed, and score. I don’t have a more formal segmentation than that yet, but those are the main differences we’re planning around."

### [FR-030] (stated)
The system shall provide an easy way to resume play after a sudden exit or interruption.

**Source Evidence:**
- `[interview_turn:T026]` "Yes, I’d want the game to handle a few things very carefully. If the player makes an invalid move, it should just be rejected with clear feedback and no loss of progress. If the game is interrupted or closed suddenly, it should restore the last safe state on restart, and if a save file is corrupted, it should isolate that problem and let the player start a new session without crashing the whole game."
- `[interview_turn:T030]` "The main ones are invalid moves, sudden exits, and bad save data. Invalid moves should never change the board state, sudden exits should preserve whatever was safely captured most recently, and corrupted saves should be skipped or quarantined so the player can keep using the game. I’d also want repeated rapid clicks or inputs handled calmly so the interface doesn’t get into a weird state."

### [FR-031] (stated)
The system shall preserve the most recently captured safe state after a sudden exit.

**Source Evidence:**
- `[interview_turn:T030]` "The main ones are invalid moves, sudden exits, and bad save data. Invalid moves should never change the board state, sudden exits should preserve whatever was safely captured most recently, and corrupted saves should be skipped or quarantined so the player can keep using the game. I’d also want repeated rapid clicks or inputs handled calmly so the interface doesn’t get into a weird state."

### [FR-032] (stated)
The system shall recover from a save file or saved result that cannot be read properly without blocking the rest of the application.

**Source Evidence:**
- `[interview_turn:T022]` "One tricky case is if the player closes the game in the middle of a puzzle, and we’d want the current state to be preserved as much as possible so they can continue later. Another is if a saved result can’t be read properly, where the game should recover without blocking the rest of the app. Beyond that, I’d expect basic invalid actions to be handled quietly and consistently so the player never feels punished for exploring the interface."
- `[interview_turn:T026]` "Yes, I’d want the game to handle a few things very carefully. If the player makes an invalid move, it should just be rejected with clear feedback and no loss of progress. If the game is interrupted or closed suddenly, it should restore the last safe state on restart, and if a save file is corrupted, it should isolate that problem and let the player start a new session without crashing the whole game."

### [FR-033] (stated)
The system shall let the player start a new session when corrupted save data is encountered.

**Source Evidence:**
- `[interview_turn:T020]` "Invalid moves should just be blocked cleanly, with some immediate feedback so the player understands why the move can’t happen. For corrupted save data, we’d want the game to fail gracefully, ideally by ignoring the bad file and starting fresh rather than crashing. Unexpected actions should be handled conservatively, meaning we’d rather prevent confusion and keep the game stable than try to be clever in those edge cases."
- `[interview_turn:T026]` "Yes, I’d want the game to handle a few things very carefully. If the player makes an invalid move, it should just be rejected with clear feedback and no loss of progress. If the game is interrupted or closed suddenly, it should restore the last safe state on restart, and if a save file is corrupted, it should isolate that problem and let the player start a new session without crashing the whole game."

### [FR-034] (stated)
The system shall support subtle non-blocking cues only when a real problem occurs, such as a save failure or recovery event.

**Source Evidence:**
- `[interview_turn:T032]` "We haven’t settled anything specific yet, but adaptive autosave based on activity would make sense, like saving more often after a few moves or after a longer session. For alerts, I’d prefer small non-blocking cues only when there’s a real problem, such as a save failure or recovery event, and otherwise let the game keep moving. The big priority is that the player should feel protected, not constantly interrupted."

### [FR-035] (conditional)
The system shall support update checks that are optional and unobtrusive.

**Source Evidence:**
- `[interview_turn:T024]` "Right now I’d treat both as out of scope unless the sponsor decides otherwise. If mobile support is added, the interface would need to be simpler and touch-friendly, and that could affect board size, controls, and how much information we show at once. Automatic updates would mostly be a distribution concern, but they’d need to be careful not to disrupt saved progress or break compatibility with existing puzzle data."
- `[interview_turn:T042]` "If we add update checks, I’d want them to be unobtrusive and optional, with a clear prompt only when something important is available. For stats export, it should be simple and local, like saving a readable file the player can keep or share if they want. I wouldn’t want either feature to interrupt gameplay or require the player to create an account."

### [FR-036] (conditional)
The system shall display update prompts only when important updates are available and preferably after a game ends or when the player returns to a menu.

**Source Evidence:**
- `[interview_turn:T042]` "If we add update checks, I’d want them to be unobtrusive and optional, with a clear prompt only when something important is available. For stats export, it should be simple and local, like saving a readable file the player can keep or share if they want. I wouldn’t want either feature to interrupt gameplay or require the player to create an account."
- `[interview_turn:T046]` "Update prompts should feel rare and low-pressure, ideally only after the player finishes a game or returns to a menu, not in the middle of solving a puzzle. If there’s a choice, they should be able to dismiss it easily and keep playing. For stats, I’d want a simple view with clear numbers and maybe an export confirmation so the player knows the file was created successfully, but nothing overly detailed or technical."

### [FR-037] (conditional)
The system shall allow the player to dismiss an update prompt easily and continue playing.

**Source Evidence:**
- `[interview_turn:T046]` "Update prompts should feel rare and low-pressure, ideally only after the player finishes a game or returns to a menu, not in the middle of solving a puzzle. If there’s a choice, they should be able to dismiss it easily and keep playing. For stats, I’d want a simple view with clear numbers and maybe an export confirmation so the player knows the file was created successfully, but nothing overly detailed or technical."

### [FR-038] (conditional)
The system shall support a simple local stats export that saves a readable file the player can keep or share.

**Source Evidence:**
- `[interview_turn:T042]` "If we add update checks, I’d want them to be unobtrusive and optional, with a clear prompt only when something important is available. For stats export, it should be simple and local, like saving a readable file the player can keep or share if they want. I wouldn’t want either feature to interrupt gameplay or require the player to create an account."

### [FR-039] (stated)
The system shall not require the player to create an account for update checks or stats export.

**Source Evidence:**
- `[interview_turn:T042]` "If we add update checks, I’d want them to be unobtrusive and optional, with a clear prompt only when something important is available. For stats export, it should be simple and local, like saving a readable file the player can keep or share if they want. I wouldn’t want either feature to interrupt gameplay or require the player to create an account."

### [FR-040] (stated)
The system shall provide a simple plain-language explanation if stats export fails and indicate whether the data was saved elsewhere.

**Source Evidence:**
- `[interview_turn:T050]` "If an update check fails, I’d want it to fail quietly with a simple message that it couldn’t connect, plus an option to try again later, not a disruptive error. For stats export, if something goes wrong, the player should get a clear explanation in plain language and be told whether their data was saved anywhere else or not. In both cases, the game should keep running normally so the player isn’t blocked from playing."

### [FR-041] (stated)
The system shall fail quietly if an update check cannot connect and offer the player an option to try again later.

**Source Evidence:**
- `[interview_turn:T050]` "If an update check fails, I’d want it to fail quietly with a simple message that it couldn’t connect, plus an option to try again later, not a disruptive error. For stats export, if something goes wrong, the player should get a clear explanation in plain language and be told whether their data was saved anywhere else or not. In both cases, the game should keep running normally so the player isn’t blocked from playing."

### [FR-042] (stated)
The system shall keep running normally if an update check fails or stats export fails.

**Source Evidence:**
- `[interview_turn:T050]` "If an update check fails, I’d want it to fail quietly with a simple message that it couldn’t connect, plus an option to try again later, not a disruptive error. For stats export, if something goes wrong, the player should get a clear explanation in plain language and be told whether their data was saved anywhere else or not. In both cases, the game should keep running normally so the player isn’t blocked from playing."

### [FR-043] (stated)
The system shall support a lightweight playable experience that does not make the player feel constantly interrupted.

**Source Evidence:**
- `[interview_turn:T028]` "We’ve talked about keeping interruption to a minimum, so a dynamic autosave approach could fit well if it stays invisible to the player. I’d be cautious about notifications during gameplay, though; if we use them, they should be very subtle and only show up when something really needs the player’s attention. The main goal is to protect progress without breaking concentration."
- `[interview_turn:T032]` "We haven’t settled anything specific yet, but adaptive autosave based on activity would make sense, like saving more often after a few moves or after a longer session. For alerts, I’d prefer small non-blocking cues only when there’s a real problem, such as a save failure or recovery event, and otherwise let the game keep moving. The big priority is that the player should feel protected, not constantly interrupted."

### [FR-044] (stated)
The system shall allow the player to view overall progress in a simple, lightweight presentation without dense charts or excessive text.

**Source Evidence:**
- `[interview_turn:T052]` "I’d want a very simple progress view that shows the basics at a glance, like puzzles completed, current time on the active puzzle, moves made, and perhaps best results if available. It should be easy to understand quickly, especially for younger players, so no dense charts or too much text. If someone wants more detail, that could be available behind an extra click, but the default view should stay clean and lightweight."

### [FR-045] (stated)
The system shall support a clear and meaningful replayable challenge experience.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Qheadache is intended to be a standalone computerized puzzle game for people ranging from young beginners to adult players. Players use a graphical board to move blocks and solve a predefined challenge. The application should support normal play and retain useful information about a player's progress and results, such as time, actions, and scores."
- `[interview_turn:T004]` "The main motivation is to have a lightweight puzzle product that is easy to distribute and easy for people to understand immediately. We see an opportunity for a game that appeals across ages without requiring a lot of setup, training, or ongoing online services. It also gives us a simple way to offer replayable challenges with progress tracking, which is useful both for player engagement and for measuring how well someone is doing over time."
- `[interview_turn:T038]` "The main data we care about is the player’s session, the puzzle state, completion time, move count, and score. We’d also want to keep some history of completed puzzles or attempts so we can see whether players are improving and where they tend to struggle. That helps us tune difficulty, keep the game replayable, and give players a sense of progress without making it feel competitive in a heavy way."

## 4. Business Rules and Constraints

### [BR-001] (stated)
Mobile support is out of scope unless the sponsor decides otherwise.

**Source Evidence:**
- `[interview_turn:T024]` "Right now I’d treat both as out of scope unless the sponsor decides otherwise. If mobile support is added, the interface would need to be simpler and touch-friendly, and that could affect board size, controls, and how much information we show at once. Automatic updates would mostly be a distribution concern, but they’d need to be careful not to disrupt saved progress or break compatibility with existing puzzle data."

### [BR-002] (stated)
Automatic updates are out of scope unless the sponsor decides otherwise.

**Source Evidence:**
- `[interview_turn:T024]` "Right now I’d treat both as out of scope unless the sponsor decides otherwise. If mobile support is added, the interface would need to be simpler and touch-friendly, and that could affect board size, controls, and how much information we show at once. Automatic updates would mostly be a distribution concern, but they’d need to be careful not to disrupt saved progress or break compatibility with existing puzzle data."

### [BR-003] (stated)
The game shall be treated as standalone and shall not need a network connection, accounts, or third-party services in the first version.

**Source Evidence:**
- `[interview_turn:T040]` "At the moment, I’d treat external integrations as out of scope for the first version. The game should stand on its own without needing a network connection, accounts, or third-party services. If we do anything later, the most likely candidates would be simple update checks or maybe optional stats export, but that hasn’t been decided."

### [BR-004] (stated)
The system shall keep saved data minimal and avoid collecting personal information unless there is a very clear reason.

**Source Evidence:**
- `[interview_turn:T056]` "Since it’s a local standalone game, I wouldn’t want anything heavy-handed like account security or online protection. Basic integrity checks would be enough so corrupted save data can be detected and the game can recover cleanly rather than crashing or showing nonsense. For privacy, we should keep the saved data minimal, just gameplay progress and stats, and avoid collecting anything personal unless there’s a very clear reason."

### [BR-005] (stated)
The system shall treat the player's current game and recent progress as higher priority than minimizing save file size.

**Source Evidence:**
- `[interview_turn:T068]` "The top priority should be never losing recent progress, because that would feel like a real bug to the player. After that, I’d rank clear warnings and honest messaging very high, so the player understands what happened if anything gets summarized or trimmed. Keeping the save file small matters too, but I’d treat that as a technical goal beneath protecting the player’s current game and making sure the behavior is predictable."
- `[interview_turn:T070]` "I still wouldn’t want to lock in a hard number yet, because that really depends on the final storage format and how much data a typical session produces. Practically, I’d want warnings to begin well before the save becomes a problem, and summarizing to kick in first for the oldest detailed history, not anything current or recent. If the limit is actually exceeded, the game should finish the save as safely as possible, preserve the important progress, and clearly tell the player that older detail was condensed."

### [BR-006] (stated)
The system shall not use heavy-handed account security or online protection.

**Source Evidence:**
- `[interview_turn:T056]` "Since it’s a local standalone game, I wouldn’t want anything heavy-handed like account security or online protection. Basic integrity checks would be enough so corrupted save data can be detected and the game can recover cleanly rather than crashing or showing nonsense. For privacy, we should keep the saved data minimal, just gameplay progress and stats, and avoid collecting anything personal unless there’s a very clear reason."

### [BR-007] (stated)
The system shall handle corrupted save data by detecting it with basic integrity checks and recovering cleanly rather than crashing or showing nonsense.

**Source Evidence:**
- `[interview_turn:T056]` "Since it’s a local standalone game, I wouldn’t want anything heavy-handed like account security or online protection. Basic integrity checks would be enough so corrupted save data can be detected and the game can recover cleanly rather than crashing or showing nonsense. For privacy, we should keep the saved data minimal, just gameplay progress and stats, and avoid collecting anything personal unless there’s a very clear reason."

### [BR-008] (conditional)
The system shall mark obvious tampering as unreliable only if doing so does not cause problems for honest players.

**Source Evidence:**
- `[interview_turn:T058]` "I’d prefer the game to detect obvious tampering only if it can do so without causing problems for honest players. If something looks invalid, it should probably mark that save as unreliable, reset just the affected stats or progress if needed, and tell the player in plain language rather than failing silently. I wouldn’t want it to be punitive, just protective of the save data."

### [BR-009] (conditional)
If a save looks invalid, the system shall reset only the affected stats or progress as needed and inform the player in plain language.

**Source Evidence:**
- `[interview_turn:T058]` "I’d prefer the game to detect obvious tampering only if it can do so without causing problems for honest players. If something looks invalid, it should probably mark that save as unreliable, reset just the affected stats or progress if needed, and tell the player in plain language rather than failing silently. I wouldn’t want it to be punitive, just protective of the save data."

### [BR-010] (stated)
The system shall preserve meaningful recent progress and avoid losing it during storage management.

**Source Evidence:**
- `[interview_turn:T060]` "I’d expect it to stay lightweight, but it should still be able to handle a fairly large number of puzzle records without slowing down the game. Old session data could be summarized after a while so the save file doesn’t grow forever, while still keeping the important totals and best results. If storage does become an issue, the game should warn the player and cleanly keep the essential progress rather than lose everything."
- `[interview_turn:T064]` "I’d want the game to automatically summarize older puzzle records once they’re no longer needed in full detail, while keeping the key totals and best results intact. If the save file gets close to a practical limit, it should warn the player and explain what’s happening before anything is lost. The main goal would be to preserve meaningful progress and keep the game responsive without making the player manage storage manually."
- `[interview_turn:T068]` "The top priority should be never losing recent progress, because that would feel like a real bug to the player. After that, I’d rank clear warnings and honest messaging very high, so the player understands what happened if anything gets summarized or trimmed. Keeping the save file small matters too, but I’d treat that as a technical goal beneath protecting the player’s current game and making sure the behavior is predictable."
- `[interview_turn:T070]` "I still wouldn’t want to lock in a hard number yet, because that really depends on the final storage format and how much data a typical session produces. Practically, I’d want warnings to begin well before the save becomes a problem, and summarizing to kick in first for the oldest detailed history, not anything current or recent. If the limit is actually exceeded, the game should finish the save as safely as possible, preserve the important progress, and clearly tell the player that older detail was condensed."

### [BR-011] (stated)
The system shall automatically summarize older puzzle records once they are no longer needed in full detail while keeping key totals and best results intact.

**Source Evidence:**
- `[interview_turn:T064]` "I’d want the game to automatically summarize older puzzle records once they’re no longer needed in full detail, while keeping the key totals and best results intact. If the save file gets close to a practical limit, it should warn the player and explain what’s happening before anything is lost. The main goal would be to preserve meaningful progress and keep the game responsive without making the player manage storage manually."
- `[interview_turn:T070]` "I still wouldn’t want to lock in a hard number yet, because that really depends on the final storage format and how much data a typical session produces. Practically, I’d want warnings to begin well before the save becomes a problem, and summarizing to kick in first for the oldest detailed history, not anything current or recent. If the limit is actually exceeded, the game should finish the save as safely as possible, preserve the important progress, and clearly tell the player that older detail was condensed."

### [BR-012] (stated)
The system shall begin warnings well before the save becomes a problem.

**Source Evidence:**
- `[interview_turn:T066]` "I don’t have an exact size in mind, but I’d keep it well below anything the average local machine would notice, so the player never has to think about disk space in normal use. If the limit is approaching, the game should give a gentle warning and start trimming or summarizing old detailed session data first, not the recent progress the player is most likely to care about. If it is exceeded, it should still save the essential record, explain that some older detail was condensed, and continue normally."
- `[interview_turn:T070]` "I still wouldn’t want to lock in a hard number yet, because that really depends on the final storage format and how much data a typical session produces. Practically, I’d want warnings to begin well before the save becomes a problem, and summarizing to kick in first for the oldest detailed history, not anything current or recent. If the limit is actually exceeded, the game should finish the save as safely as possible, preserve the important progress, and clearly tell the player that older detail was condensed."

### [BR-013] (stated)
The system shall trim or summarize the oldest detailed history first, not current or recent progress, when storage needs to be reduced.

**Source Evidence:**
- `[interview_turn:T066]` "I don’t have an exact size in mind, but I’d keep it well below anything the average local machine would notice, so the player never has to think about disk space in normal use. If the limit is approaching, the game should give a gentle warning and start trimming or summarizing old detailed session data first, not the recent progress the player is most likely to care about. If it is exceeded, it should still save the essential record, explain that some older detail was condensed, and continue normally."
- `[interview_turn:T070]` "I still wouldn’t want to lock in a hard number yet, because that really depends on the final storage format and how much data a typical session produces. Practically, I’d want warnings to begin well before the save becomes a problem, and summarizing to kick in first for the oldest detailed history, not anything current or recent. If the limit is actually exceeded, the game should finish the save as safely as possible, preserve the important progress, and clearly tell the player that older detail was condensed."

### [BR-014] (stated)
If the save file limit is exceeded, the system shall finish saving as safely as possible, preserve essential progress, and explain that older detail was condensed.

**Source Evidence:**
- `[interview_turn:T066]` "I don’t have an exact size in mind, but I’d keep it well below anything the average local machine would notice, so the player never has to think about disk space in normal use. If the limit is approaching, the game should give a gentle warning and start trimming or summarizing old detailed session data first, not the recent progress the player is most likely to care about. If it is exceeded, it should still save the essential record, explain that some older detail was condensed, and continue normally."
- `[interview_turn:T070]` "I still wouldn’t want to lock in a hard number yet, because that really depends on the final storage format and how much data a typical session produces. Practically, I’d want warnings to begin well before the save becomes a problem, and summarizing to kick in first for the oldest detailed history, not anything current or recent. If the limit is actually exceeded, the game should finish the save as safely as possible, preserve the important progress, and clearly tell the player that older detail was condensed."

### [BR-015] (conditional)
The system shall detect obvious tampering only when it can do so without causing problems for honest players.

**Source Evidence:**
- `[interview_turn:T058]` "I’d prefer the game to detect obvious tampering only if it can do so without causing problems for honest players. If something looks invalid, it should probably mark that save as unreliable, reset just the affected stats or progress if needed, and tell the player in plain language rather than failing silently. I wouldn’t want it to be punitive, just protective of the save data."

### [BR-016] (stated)
The system shall handle repeated rapid inputs calmly by ignoring extra inputs while an action is already being processed.

**Source Evidence:**
- `[interview_turn:T034]` "I’d lean toward ignoring extra inputs once an action is already being processed, rather than queueing them, because queueing could create confusing or unintended moves. If the player is clicking too fast, a small visual cue like a brief highlight or button lockout would be enough to show the input was received but not duplicated. The important thing is to keep the board state predictable and prevent accidental double actions."

### [BR-017] (stated)
The system shall provide only small non-blocking cues when there is a real problem such as a save failure or recovery event.

**Source Evidence:**
- `[interview_turn:T032]` "We haven’t settled anything specific yet, but adaptive autosave based on activity would make sense, like saving more often after a few moves or after a longer session. For alerts, I’d prefer small non-blocking cues only when there’s a real problem, such as a save failure or recovery event, and otherwise let the game keep moving. The big priority is that the player should feel protected, not constantly interrupted."

### [BR-018] (stated)
The system shall show warnings as subtle notifications during normal play, such as after a save or between puzzles, and use a modal dialog only when the player must make a decision or acknowledge condensed data.

**Source Evidence:**
- `[interview_turn:T072]` "I’d want the warnings to be subtle during normal play, like a small notification after a save or between puzzles, so the game flow isn’t interrupted. If the situation becomes more serious, then a modal dialog is appropriate, but only when the player actually needs to make a decision or acknowledge that older data was condensed. I wouldn’t show repeated reminders unless the problem is still unresolved, because that would get annoying fast."

### [BR-019] (stated)
The system shall not repeatedly remind the player about a save status problem unless the problem is still unresolved.

**Source Evidence:**
- `[interview_turn:T072]` "I’d want the warnings to be subtle during normal play, like a small notification after a save or between puzzles, so the game flow isn’t interrupted. If the situation becomes more serious, then a modal dialog is appropriate, but only when the player actually needs to make a decision or acknowledge that older data was condensed. I wouldn’t show repeated reminders unless the problem is still unresolved, because that would get annoying fast."

## 5. Data and External Interfaces

### [DI-001] (stated)
The system shall store progress locally on the player's device.

**Source Evidence:**
- `[interview_turn:T006]` "We’re assuming it will run as a standalone application on a typical desktop or laptop, and it should be simple to install and launch without needing extra services. Offline use is important, since players should still be able to play and have their progress saved locally even without internet access. I’m not sure yet whether we need to support mobile devices or automatic updates, so I’d want to check that with the team."
- `[interview_turn:T056]` "Since it’s a local standalone game, I wouldn’t want anything heavy-handed like account security or online protection. Basic integrity checks would be enough so corrupted save data can be detected and the game can recover cleanly rather than crashing or showing nonsense. For privacy, we should keep the saved data minimal, just gameplay progress and stats, and avoid collecting anything personal unless there’s a very clear reason."

### [DI-002] (conditional)
The system shall support a readable local file format for exported stats.

**Source Evidence:**
- `[interview_turn:T042]` "If we add update checks, I’d want them to be unobtrusive and optional, with a clear prompt only when something important is available. For stats export, it should be simple and local, like saving a readable file the player can keep or share if they want. I wouldn’t want either feature to interrupt gameplay or require the player to create an account."

### [DI-003] (conditional)
The system shall support optional update-check communication when update checks are enabled.

**Source Evidence:**
- `[interview_turn:T042]` "If we add update checks, I’d want them to be unobtrusive and optional, with a clear prompt only when something important is available. For stats export, it should be simple and local, like saving a readable file the player can keep or share if they want. I wouldn’t want either feature to interrupt gameplay or require the player to create an account."
- `[interview_turn:T050]` "If an update check fails, I’d want it to fail quietly with a simple message that it couldn’t connect, plus an option to try again later, not a disruptive error. For stats export, if something goes wrong, the player should get a clear explanation in plain language and be told whether their data was saved anywhere else or not. In both cases, the game should keep running normally so the player isn’t blocked from playing."

## 6. Quality Requirements

### [QR-001] (stated)
The system shall be easy to understand immediately and require little or no setup or training.

**Source Evidence:**
- `[interview_turn:T004]` "The main motivation is to have a lightweight puzzle product that is easy to distribute and easy for people to understand immediately. We see an opportunity for a game that appeals across ages without requiring a lot of setup, training, or ongoing online services. It also gives us a simple way to offer replayable challenges with progress tracking, which is useful both for player engagement and for measuring how well someone is doing over time."
- `[interview_turn:T006]` "We’re assuming it will run as a standalone application on a typical desktop or laptop, and it should be simple to install and launch without needing extra services. Offline use is important, since players should still be able to play and have their progress saved locally even without internet access. I’m not sure yet whether we need to support mobile devices or automatic updates, so I’d want to check that with the team."

### [QR-002] (stated)
The system shall provide clear feedback on player performance.

**Source Evidence:**
- `[interview_turn:T002]` "Qheadache is meant to be a simple standalone puzzle game where players can pick it up and start solving challenges right away without needing anything else. The main goal is to give people a fun block-moving puzzle that works for beginners as well as adults, with clear feedback on how they’re doing. We also want it to keep track of progress and results like time, moves or actions, and score so players can see improvement and replay challenges."

### [QR-003] (stated)
The system shall remain lightweight and easy to distribute.

**Source Evidence:**
- `[interview_turn:T004]` "The main motivation is to have a lightweight puzzle product that is easy to distribute and easy for people to understand immediately. We see an opportunity for a game that appeals across ages without requiring a lot of setup, training, or ongoing online services. It also gives us a simple way to offer replayable challenges with progress tracking, which is useful both for player engagement and for measuring how well someone is doing over time."

### [QR-004] (stated)
The system shall be fun for players and encourage them to come back and replay challenges.

**Source Evidence:**
- `[interview_turn:T002]` "Qheadache is meant to be a simple standalone puzzle game where players can pick it up and start solving challenges right away without needing anything else. The main goal is to give people a fun block-moving puzzle that works for beginners as well as adults, with clear feedback on how they’re doing. We also want it to keep track of progress and results like time, moves or actions, and score so players can see improvement and replay challenges."
- `[interview_turn:T016]` "The product owner will mostly care that the game is fun, easy to understand, and keeps players coming back, so they’ll pay attention to challenge balance, replay value, and whether the progress data is useful. Testers are likely to focus on whether the interface is clear, whether moves and scoring are consistent, and whether the game behaves reliably when saving results. Developers will be concerned with keeping the logic maintainable and making sure the board interactions, timing, and stored player information all work correctly without introducing bugs."

### [QR-005] (stated)
The system shall behave reliably when saving results and during gameplay flow.

**Source Evidence:**
- `[interview_turn:T016]` "The product owner will mostly care that the game is fun, easy to understand, and keeps players coming back, so they’ll pay attention to challenge balance, replay value, and whether the progress data is useful. Testers are likely to focus on whether the interface is clear, whether moves and scoring are consistent, and whether the game behaves reliably when saving results. Developers will be concerned with keeping the logic maintainable and making sure the board interactions, timing, and stored player information all work correctly without introducing bugs."
- `[interview_turn:T020]` "Invalid moves should just be blocked cleanly, with some immediate feedback so the player understands why the move can’t happen. For corrupted save data, we’d want the game to fail gracefully, ideally by ignoring the bad file and starting fresh rather than crashing. Unexpected actions should be handled conservatively, meaning we’d rather prevent confusion and keep the game stable than try to be clever in those edge cases."

### [QR-006] (stated)
The system shall keep the interface clear for younger beginners.

**Source Evidence:**
- `[interview_turn:T008]` "We mainly think of two broad groups: younger beginners who need a very straightforward experience, and more experienced players or adults who want a bit more of a challenge. The younger group would likely benefit from simpler presentation and easier onboarding, while the more experienced group will care more about challenge, speed, and score. I don’t have a more formal segmentation than that yet, but those are the main differences we’re planning around."
- `[interview_turn:T052]` "I’d want a very simple progress view that shows the basics at a glance, like puzzles completed, current time on the active puzzle, moves made, and perhaps best results if available. It should be easy to understand quickly, especially for younger players, so no dense charts or too much text. If someone wants more detail, that could be available behind an extra click, but the default view should stay clean and lightweight."

### [QR-007] (stated)
The system shall keep the game logic maintainable and board interactions, timing, and stored player information working correctly without introducing bugs.

**Source Evidence:**
- `[interview_turn:T016]` "The product owner will mostly care that the game is fun, easy to understand, and keeps players coming back, so they’ll pay attention to challenge balance, replay value, and whether the progress data is useful. Testers are likely to focus on whether the interface is clear, whether moves and scoring are consistent, and whether the game behaves reliably when saving results. Developers will be concerned with keeping the logic maintainable and making sure the board interactions, timing, and stored player information all work correctly without introducing bugs."

### [QR-008] (stated)
The system shall remain responsive and lightweight even with a fairly large number of puzzle records.

**Source Evidence:**
- `[interview_turn:T060]` "I’d expect it to stay lightweight, but it should still be able to handle a fairly large number of puzzle records without slowing down the game. Old session data could be summarized after a while so the save file doesn’t grow forever, while still keeping the important totals and best results. If storage does become an issue, the game should warn the player and cleanly keep the essential progress rather than lose everything."

### [QR-009] (stated)
The system shall keep the board state predictable and prevent accidental double actions.

**Source Evidence:**
- `[interview_turn:T034]` "I’d lean toward ignoring extra inputs once an action is already being processed, rather than queueing them, because queueing could create confusing or unintended moves. If the player is clicking too fast, a small visual cue like a brief highlight or button lockout would be enough to show the input was received but not duplicated. The important thing is to keep the board state predictable and prevent accidental double actions."

### [QR-010] (stated)
The system shall keep the gameplay challenge intact while preventing mistakes from turning into frustration.

**Source Evidence:**
- `[interview_turn:T044]` "I’d want the game to be forgiving, so players can undo moves and restart a puzzle easily without penalty. If someone is stuck, a subtle hint system would be better than a big explanation, maybe something optional they can ask for rather than having it pushed at them. The idea is to keep the challenge intact while making sure mistakes don’t turn into frustration."

### [QR-011] (stated)
The system shall remain simple and reliable rather than using overly complex techniques that risk reliability.

**Source Evidence:**
- `[interview_turn:T062]` "Yes, I’d want some practical measures there, especially compression for saved data if it helps keep files small, and a simple indexed structure so the game doesn’t have to scan everything every time it opens stats or progress. Modular loading would also make sense for the puzzle library so only what’s needed is loaded rather than the whole set at once. I wouldn’t want anything too complex if it risks reliability, but those kinds of techniques sound appropriate."

### [QR-012] (conditional)
The system shall keep saved data small through practical measures such as compression and indexing when they help without harming reliability.

**Source Evidence:**
- `[interview_turn:T062]` "Yes, I’d want some practical measures there, especially compression for saved data if it helps keep files small, and a simple indexed structure so the game doesn’t have to scan everything every time it opens stats or progress. Modular loading would also make sense for the puzzle library so only what’s needed is loaded rather than the whole set at once. I wouldn’t want anything too complex if it risks reliability, but those kinds of techniques sound appropriate."

### [QR-013] (stated)
The system shall load puzzle data modularly so only needed parts are loaded rather than the entire library at once.

**Source Evidence:**
- `[interview_turn:T062]` "Yes, I’d want some practical measures there, especially compression for saved data if it helps keep files small, and a simple indexed structure so the game doesn’t have to scan everything every time it opens stats or progress. Modular loading would also make sense for the puzzle library so only what’s needed is loaded rather than the whole set at once. I wouldn’t want anything too complex if it risks reliability, but those kinds of techniques sound appropriate."

### [QR-014] (stated)
The system shall use subtle, low-pressure prompts for important non-gameplay features and avoid interrupting gameplay.

**Source Evidence:**
- `[interview_turn:T046]` "Update prompts should feel rare and low-pressure, ideally only after the player finishes a game or returns to a menu, not in the middle of solving a puzzle. If there’s a choice, they should be able to dismiss it easily and keep playing. For stats, I’d want a simple view with clear numbers and maybe an export confirmation so the player knows the file was created successfully, but nothing overly detailed or technical."
- `[interview_turn:T072]` "I’d want the warnings to be subtle during normal play, like a small notification after a save or between puzzles, so the game flow isn’t interrupted. If the situation becomes more serious, then a modal dialog is appropriate, but only when the player actually needs to make a decision or acknowledge that older data was condensed. I wouldn’t show repeated reminders unless the problem is still unresolved, because that would get annoying fast."

## 7. Exceptions and Boundary Conditions

### [EX-001] (stated)
If a save file is corrupted, the system shall skip or quarantine the corrupted save so the player can continue using the game.

**Source Evidence:**
- `[interview_turn:T020]` "Invalid moves should just be blocked cleanly, with some immediate feedback so the player understands why the move can’t happen. For corrupted save data, we’d want the game to fail gracefully, ideally by ignoring the bad file and starting fresh rather than crashing. Unexpected actions should be handled conservatively, meaning we’d rather prevent confusion and keep the game stable than try to be clever in those edge cases."
- `[interview_turn:T030]` "The main ones are invalid moves, sudden exits, and bad save data. Invalid moves should never change the board state, sudden exits should preserve whatever was safely captured most recently, and corrupted saves should be skipped or quarantined so the player can keep using the game. I’d also want repeated rapid clicks or inputs handled calmly so the interface doesn’t get into a weird state."

### [EX-002] (stated)
If a saved result cannot be read properly, the system shall recover without blocking the rest of the application.

**Source Evidence:**
- `[interview_turn:T022]` "One tricky case is if the player closes the game in the middle of a puzzle, and we’d want the current state to be preserved as much as possible so they can continue later. Another is if a saved result can’t be read properly, where the game should recover without blocking the rest of the app. Beyond that, I’d expect basic invalid actions to be handled quietly and consistently so the player never feels punished for exploring the interface."

### [EX-003] (stated)
If the game is interrupted or closed suddenly, the system shall preserve the last safe state on restart.

**Source Evidence:**
- `[interview_turn:T026]` "Yes, I’d want the game to handle a few things very carefully. If the player makes an invalid move, it should just be rejected with clear feedback and no loss of progress. If the game is interrupted or closed suddenly, it should restore the last safe state on restart, and if a save file is corrupted, it should isolate that problem and let the player start a new session without crashing the whole game."
- `[interview_turn:T030]` "The main ones are invalid moves, sudden exits, and bad save data. Invalid moves should never change the board state, sudden exits should preserve whatever was safely captured most recently, and corrupted saves should be skipped or quarantined so the player can keep using the game. I’d also want repeated rapid clicks or inputs handled calmly so the interface doesn’t get into a weird state."

### [EX-004] (stated)
If an update check cannot connect, the system shall fail quietly and keep the game available for play.

**Source Evidence:**
- `[interview_turn:T050]` "If an update check fails, I’d want it to fail quietly with a simple message that it couldn’t connect, plus an option to try again later, not a disruptive error. For stats export, if something goes wrong, the player should get a clear explanation in plain language and be told whether their data was saved anywhere else or not. In both cases, the game should keep running normally so the player isn’t blocked from playing."

### [EX-005] (stated)
If stats export fails, the system shall provide a clear explanation and keep the game running normally.

**Source Evidence:**
- `[interview_turn:T050]` "If an update check fails, I’d want it to fail quietly with a simple message that it couldn’t connect, plus an option to try again later, not a disruptive error. For stats export, if something goes wrong, the player should get a clear explanation in plain language and be told whether their data was saved anywhere else or not. In both cases, the game should keep running normally so the player isn’t blocked from playing."

### [EX-006] (stated)
If storage becomes an issue, the system shall warn the player and preserve essential progress rather than losing everything.

**Source Evidence:**
- `[interview_turn:T060]` "I’d expect it to stay lightweight, but it should still be able to handle a fairly large number of puzzle records without slowing down the game. Old session data could be summarized after a while so the save file doesn’t grow forever, while still keeping the important totals and best results. If storage does become an issue, the game should warn the player and cleanly keep the essential progress rather than lose everything."
- `[interview_turn:T064]` "I’d want the game to automatically summarize older puzzle records once they’re no longer needed in full detail, while keeping the key totals and best results intact. If the save file gets close to a practical limit, it should warn the player and explain what’s happening before anything is lost. The main goal would be to preserve meaningful progress and keep the game responsive without making the player manage storage manually."
- `[interview_turn:T066]` "I don’t have an exact size in mind, but I’d keep it well below anything the average local machine would notice, so the player never has to think about disk space in normal use. If the limit is approaching, the game should give a gentle warning and start trimming or summarizing old detailed session data first, not the recent progress the player is most likely to care about. If it is exceeded, it should still save the essential record, explain that some older detail was condensed, and continue normally."

### [EX-007] (stated)
If the player switches between sessions or reopens a game after a long time, the system shall load cleanly and not lose track of the player's location.

**Source Evidence:**
- `[interview_turn:T036]` "One other area is if the player switches between sessions or reopens a game after a long time, the game should still load cleanly and not lose track of where they were. I’d also want it to handle partial progress records safely, so scores and times aren’t shown as nonsense if something was interrupted mid-save. Beyond that, I think the main concern is just making sure nothing in the game can trap the player in an unrecoverable state."

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
Support for mobile devices remains undecided.

**Source Evidence:**
- `[interview_turn:T006]` "We’re assuming it will run as a standalone application on a typical desktop or laptop, and it should be simple to install and launch without needing extra services. Offline use is important, since players should still be able to play and have their progress saved locally even without internet access. I’m not sure yet whether we need to support mobile devices or automatic updates, so I’d want to check that with the team."
- `[interview_turn:T024]` "Right now I’d treat both as out of scope unless the sponsor decides otherwise. If mobile support is added, the interface would need to be simpler and touch-friendly, and that could affect board size, controls, and how much information we show at once. Automatic updates would mostly be a distribution concern, but they’d need to be careful not to disrupt saved progress or break compatibility with existing puzzle data."

### [UN-002]
Automatic updates remain undecided beyond being out of scope for the first version unless the sponsor decides otherwise.

**Source Evidence:**
- `[interview_turn:T024]` "Right now I’d treat both as out of scope unless the sponsor decides otherwise. If mobile support is added, the interface would need to be simpler and touch-friendly, and that could affect board size, controls, and how much information we show at once. Automatic updates would mostly be a distribution concern, but they’d need to be careful not to disrupt saved progress or break compatibility with existing puzzle data."

### [UN-003]
The final decision on whether to include adaptive autosave timing has not yet been settled.

**Source Evidence:**
- `[interview_turn:T028]` "We’ve talked about keeping interruption to a minimum, so a dynamic autosave approach could fit well if it stays invisible to the player. I’d be cautious about notifications during gameplay, though; if we use them, they should be very subtle and only show up when something really needs the player’s attention. The main goal is to protect progress without breaking concentration."
- `[interview_turn:T032]` "We haven’t settled anything specific yet, but adaptive autosave based on activity would make sense, like saving more often after a few moves or after a longer session. For alerts, I’d prefer small non-blocking cues only when there’s a real problem, such as a save failure or recovery event, and otherwise let the game keep moving. The big priority is that the player should feel protected, not constantly interrupted."

### [UN-004]
The exact capacity limit or storage threshold for saved progress data has not been defined.

**Source Evidence:**
- `[interview_turn:T060]` "I’d expect it to stay lightweight, but it should still be able to handle a fairly large number of puzzle records without slowing down the game. Old session data could be summarized after a while so the save file doesn’t grow forever, while still keeping the important totals and best results. If storage does become an issue, the game should warn the player and cleanly keep the essential progress rather than lose everything."
- `[interview_turn:T066]` "I don’t have an exact size in mind, but I’d keep it well below anything the average local machine would notice, so the player never has to think about disk space in normal use. If the limit is approaching, the game should give a gentle warning and start trimming or summarizing old detailed session data first, not the recent progress the player is most likely to care about. If it is exceeded, it should still save the essential record, explain that some older detail was condensed, and continue normally."
- `[interview_turn:T070]` "I still wouldn’t want to lock in a hard number yet, because that really depends on the final storage format and how much data a typical session produces. Practically, I’d want warnings to begin well before the save becomes a problem, and summarizing to kick in first for the oldest detailed history, not anything current or recent. If the limit is actually exceeded, the game should finish the save as safely as possible, preserve the important progress, and clearly tell the player that older detail was condensed."

### [UN-005]
The inclusion of more detailed session records in stats export is not yet decided.

**Source Evidence:**
- `[interview_turn:T048]` "A dedicated menu option would be the cleanest approach, probably from a progress or settings area rather than tied to finishing a puzzle. I’d want the player to see their overall progress there, with the export option available from the same place so it feels intentional instead of forced. As for control, they should be able to export only the basic stats by default, and if we include more detail later, it should be optional and clearly labeled."
- `[interview_turn:T054]` "I’d expect the player to go into a menu like Progress or Stats, choose what they want to look at, and then select an export option from there. The export should default to the core summary data, with an optional choice to include more detailed session records if we decide to support that. After it finishes, the game should show a clear confirmation message with the file location or name so the player knows it really worked."
