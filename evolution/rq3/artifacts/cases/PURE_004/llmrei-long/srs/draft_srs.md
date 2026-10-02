# Software Requirements Specification: Qheadache

## 1. Scope and Context

### [SC-001] (stated)
Qheadache shall be a standalone computerized puzzle game.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Qheadache is intended to be a standalone computerized puzzle game for people ranging from young beginners to adult players. Players use a graphical board to move blocks and solve a predefined challenge. The application should support normal play and retain useful information about a player's progress and results, such as time, actions, and scores."
- `[interview_turn:T006]` "Qheadache is a standalone puzzle game where players solve a block-moving challenge on a graphical board. It’s meant to be approachable for younger beginners but still interesting for adults. The game should let players play normally and keep track of useful results like time, actions, and scores."
- `[interview_turn:T008]` "Right now, we don’t really have a formal system in place for this specific game, because Qheadache is intended to be built as a new standalone application. For similar puzzle gameplay, the expectation is just that the game itself handles the board, the moves, and the puzzle state, and then stores player results locally in a simple way. I don’t have a more detailed existing workflow to describe yet."

### [SC-002] (stated)
Qheadache shall be intended for players ranging from young beginners to adult players.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Qheadache is intended to be a standalone computerized puzzle game for people ranging from young beginners to adult players. Players use a graphical board to move blocks and solve a predefined challenge. The application should support normal play and retain useful information about a player's progress and results, such as time, actions, and scores."
- `[interview_turn:T006]` "Qheadache is a standalone puzzle game where players solve a block-moving challenge on a graphical board. It’s meant to be approachable for younger beginners but still interesting for adults. The game should let players play normally and keep track of useful results like time, actions, and scores."
- `[interview_turn:T036]` "The main people besides the player would be whoever is designing the puzzles and whoever is maintaining the game, because they’ll care about how easy it is to create levels, tune difficulty, and support saved progress. If this is for education or younger users, teachers or parents might also matter because they may want simple controls and clear progress tracking. I’d also consider anyone responsible for distribution or updates, since saved results and compatibility can become important for them."
- `[interview_turn:T040]` "Yes, one more thing that would be helpful is some kind of simple player record or history so the game can remember past completion times, actions, and scores for each puzzle. Also, the interface should stay very straightforward, since it needs to work well for beginners as well as adults. Beyond that, I think the main requirements are covered."

## 2. Actors

None specified.

## 3. Functional Requirements

### [FR-001] (stated)
The system shall provide a graphical board for block-moving puzzle play.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Qheadache is intended to be a standalone computerized puzzle game for people ranging from young beginners to adult players. Players use a graphical board to move blocks and solve a predefined challenge. The application should support normal play and retain useful information about a player's progress and results, such as time, actions, and scores."
- `[interview_turn:T006]` "Qheadache is a standalone puzzle game where players solve a block-moving challenge on a graphical board. It’s meant to be approachable for younger beginners but still interesting for adults. The game should let players play normally and keep track of useful results like time, actions, and scores."
- `[interview_turn:T012]` "Yes, that’s right. Those are the core functions we expect from Qheadache. If there’s anything beyond that, it would be nice to discuss later, but that’s the main scope for now."
- `[interview_turn:T020]` "The highest priority should be the graphical block-moving board together with the automatic puzzle and state handling, because that is the actual game. After that, I’d put automatic saving of progress and results, since tracking time, actions, and score is part of the main value. Reset/replay and basic success or failure feedback can come next as helpful supporting features."
- `[interview_turn:T022]` "The board should let the player see the puzzle clearly and move blocks in a straightforward way, using the mouse or touch if possible. The system should enforce the puzzle rules automatically, keep track of the current state after each move, and know when the challenge has been solved. It should feel responsive and make it obvious whether a move is valid."

### [FR-002] (stated)
The system shall allow the player to move blocks to solve a predefined challenge.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Qheadache is intended to be a standalone computerized puzzle game for people ranging from young beginners to adult players. Players use a graphical board to move blocks and solve a predefined challenge. The application should support normal play and retain useful information about a player's progress and results, such as time, actions, and scores."
- `[interview_turn:T006]` "Qheadache is a standalone puzzle game where players solve a block-moving challenge on a graphical board. It’s meant to be approachable for younger beginners but still interesting for adults. The game should let players play normally and keep track of useful results like time, actions, and scores."
- `[interview_turn:T022]` "The board should let the player see the puzzle clearly and move blocks in a straightforward way, using the mouse or touch if possible. The system should enforce the puzzle rules automatically, keep track of the current state after each move, and know when the challenge has been solved. It should feel responsive and make it obvious whether a move is valid."

### [FR-003] (stated)
The system shall support normal play.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Qheadache is intended to be a standalone computerized puzzle game for people ranging from young beginners to adult players. Players use a graphical board to move blocks and solve a predefined challenge. The application should support normal play and retain useful information about a player's progress and results, such as time, actions, and scores."
- `[interview_turn:T006]` "Qheadache is a standalone puzzle game where players solve a block-moving challenge on a graphical board. It’s meant to be approachable for younger beginners but still interesting for adults. The game should let players play normally and keep track of useful results like time, actions, and scores."

### [FR-004] (stated)
The system shall handle the board, the moves, and the puzzle state automatically.

**Source Evidence:**
- `[interview_turn:T008]` "Right now, we don’t really have a formal system in place for this specific game, because Qheadache is intended to be built as a new standalone application. For similar puzzle gameplay, the expectation is just that the game itself handles the board, the moves, and the puzzle state, and then stores player results locally in a simple way. I don’t have a more detailed existing workflow to describe yet."
- `[interview_turn:T010]` "We want to replace any manual or ad hoc tracking with the game handling it automatically, so players don’t have to record anything themselves. The main things we want are a smooth puzzle experience, clear progress tracking, and saved results like completion time, number of actions, and score so players can see how they did."
- `[interview_turn:T012]` "Yes, that’s right. Those are the core functions we expect from Qheadache. If there’s anything beyond that, it would be nice to discuss later, but that’s the main scope for now."
- `[interview_turn:T020]` "The highest priority should be the graphical block-moving board together with the automatic puzzle and state handling, because that is the actual game. After that, I’d put automatic saving of progress and results, since tracking time, actions, and score is part of the main value. Reset/replay and basic success or failure feedback can come next as helpful supporting features."

### [FR-005] (stated)
The system shall enforce puzzle rules automatically.

**Source Evidence:**
- `[interview_turn:T022]` "The board should let the player see the puzzle clearly and move blocks in a straightforward way, using the mouse or touch if possible. The system should enforce the puzzle rules automatically, keep track of the current state after each move, and know when the challenge has been solved. It should feel responsive and make it obvious whether a move is valid."

### [FR-006] (stated)
The system shall keep track of the current puzzle state after each move.

**Source Evidence:**
- `[interview_turn:T022]` "The board should let the player see the puzzle clearly and move blocks in a straightforward way, using the mouse or touch if possible. The system should enforce the puzzle rules automatically, keep track of the current state after each move, and know when the challenge has been solved. It should feel responsive and make it obvious whether a move is valid."

### [FR-007] (stated)
The system shall detect when the challenge has been solved.

**Source Evidence:**
- `[interview_turn:T022]` "The board should let the player see the puzzle clearly and move blocks in a straightforward way, using the mouse or touch if possible. The system should enforce the puzzle rules automatically, keep track of the current state after each move, and know when the challenge has been solved. It should feel responsive and make it obvious whether a move is valid."

### [FR-008] (conditional)
The system shall allow players to use mouse or touch input for block movement if possible.

**Source Evidence:**
- `[interview_turn:T022]` "The board should let the player see the puzzle clearly and move blocks in a straightforward way, using the mouse or touch if possible. The system should enforce the puzzle rules automatically, keep track of the current state after each move, and know when the challenge has been solved. It should feel responsive and make it obvious whether a move is valid."

### [FR-009] (stated)
The system shall prevent invalid moves from occurring.

**Source Evidence:**
- `[interview_turn:T024]` "If a move is invalid, the game should simply prevent it from happening and give a clear indication that the block can’t go there. I’d prefer a gentle visual cue rather than an error message, so it doesn’t interrupt play too much. It should be obvious enough that the player understands the move was rejected."

### [FR-010] (stated)
The system shall give a clear, gentle visual cue when a move is invalid.

**Source Evidence:**
- `[interview_turn:T024]` "If a move is invalid, the game should simply prevent it from happening and give a clear indication that the block can’t go there. I’d prefer a gentle visual cue rather than an error message, so it doesn’t interrupt play too much. It should be obvious enough that the player understands the move was rejected."

### [FR-011] (stated)
The system shall automatically save the player's current progress.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Qheadache is intended to be a standalone computerized puzzle game for people ranging from young beginners to adult players. Players use a graphical board to move blocks and solve a predefined challenge. The application should support normal play and retain useful information about a player's progress and results, such as time, actions, and scores."
- `[interview_turn:T010]` "We want to replace any manual or ad hoc tracking with the game handling it automatically, so players don’t have to record anything themselves. The main things we want are a smooth puzzle experience, clear progress tracking, and saved results like completion time, number of actions, and score so players can see how they did."
- `[interview_turn:T026]` "It should keep a player’s current progress so they can come back later and continue where they left off. It also needs to store results like completion time, number of actions, and score after a puzzle is finished. I’d want that information saved automatically without the player having to do anything extra."

### [FR-012] (stated)
The system shall allow a player to resume an unfinished puzzle from the saved state.

**Source Evidence:**
- `[interview_turn:T028]` "When a player comes back, the game should offer them the option to resume their unfinished puzzle from the saved state. If they choose to continue, it should load the exact board position and keep the earlier time and action count, unless you decide those should reset separately. I’m not sure yet whether we’d preserve the timer continuously or only save the final result, so that might need to be decided."

### [FR-013] (stated)
When a player resumes an unfinished puzzle, the system shall load the exact saved board position.

**Source Evidence:**
- `[interview_turn:T028]` "When a player comes back, the game should offer them the option to resume their unfinished puzzle from the saved state. If they choose to continue, it should load the exact board position and keep the earlier time and action count, unless you decide those should reset separately. I’m not sure yet whether we’d preserve the timer continuously or only save the final result, so that might need to be decided."

### [FR-014] (stated)
When a player resumes an unfinished puzzle, the system shall continue the earlier timer and action count.

**Source Evidence:**
- `[interview_turn:T030]` "I’d want both the timer and action count to continue from where they left off, so the player’s result reflects the whole attempt. It would feel unfair to reset them on resume if they are in the middle of the same puzzle. If there’s a technical reason to treat it differently, we can revisit it, but that would be my preference."

### [FR-015] (stated)
The system shall automatically store completion time, number of actions, and score after a puzzle is finished.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Qheadache is intended to be a standalone computerized puzzle game for people ranging from young beginners to adult players. Players use a graphical board to move blocks and solve a predefined challenge. The application should support normal play and retain useful information about a player's progress and results, such as time, actions, and scores."
- `[interview_turn:T010]` "We want to replace any manual or ad hoc tracking with the game handling it automatically, so players don’t have to record anything themselves. The main things we want are a smooth puzzle experience, clear progress tracking, and saved results like completion time, number of actions, and score so players can see how they did."
- `[interview_turn:T026]` "It should keep a player’s current progress so they can come back later and continue where they left off. It also needs to store results like completion time, number of actions, and score after a puzzle is finished. I’d want that information saved automatically without the player having to do anything extra."

### [FR-016] (stated)
The system shall automatically save results without requiring the player to do anything extra.

**Source Evidence:**
- `[interview_turn:T026]` "It should keep a player’s current progress so they can come back later and continue where they left off. It also needs to store results like completion time, number of actions, and score after a puzzle is finished. I’d want that information saved automatically without the player having to do anything extra."

### [FR-017] (stated)
The system shall provide a reset or replay option for the current puzzle.

**Source Evidence:**
- `[interview_turn:T016]` "Yes, I’d include both of those. A reset or replay option feels important for a puzzle game, and basic success or failure feedback would help players understand what happened without making the game too complicated."
- `[interview_turn:T018]` "Nothing major comes to mind right now. I’d keep the scope focused on those core gameplay and tracking features first, and then we can decide later if anything extra is worth adding."
- `[interview_turn:T020]` "The highest priority should be the graphical block-moving board together with the automatic puzzle and state handling, because that is the actual game. After that, I’d put automatic saving of progress and results, since tracking time, actions, and score is part of the main value. Reset/replay and basic success or failure feedback can come next as helpful supporting features."
- `[interview_turn:T032]` "Reset or replay should let the player start the current puzzle over from the original beginning state. It should clear the current moves and restore the board to the initial layout, so they can try again without leaving the puzzle. I’d also expect it to work quickly and be easy to find during play."

### [FR-018] (stated)
The reset or replay option shall start the current puzzle over from the original beginning state.

**Source Evidence:**
- `[interview_turn:T032]` "Reset or replay should let the player start the current puzzle over from the original beginning state. It should clear the current moves and restore the board to the initial layout, so they can try again without leaving the puzzle. I’d also expect it to work quickly and be easy to find during play."

### [FR-019] (stated)
The reset or replay option shall clear the current moves and restore the board to the initial layout.

**Source Evidence:**
- `[interview_turn:T032]` "Reset or replay should let the player start the current puzzle over from the original beginning state. It should clear the current moves and restore the board to the initial layout, so they can try again without leaving the puzzle. I’d also expect it to work quickly and be easy to find during play."

### [FR-020] (stated)
The reset or replay option shall be easy to find during play.

**Source Evidence:**
- `[interview_turn:T032]` "Reset or replay should let the player start the current puzzle over from the original beginning state. It should clear the current moves and restore the board to the initial layout, so they can try again without leaving the puzzle. I’d also expect it to work quickly and be easy to find during play."

### [FR-021] (stated)
The system shall provide basic success feedback when the player solves the puzzle.

**Source Evidence:**
- `[interview_turn:T016]` "Yes, I’d include both of those. A reset or replay option feels important for a puzzle game, and basic success or failure feedback would help players understand what happened without making the game too complicated."
- `[interview_turn:T034]` "When the player solves the puzzle, the game should clearly show that they’ve completed it, ideally with a simple success message or visual celebration. For failure, I don’t think we need a harsh game-over in the usual sense, since it’s a puzzle; if there is a failure condition at all, it should be something gentle like running out of a limit and then offering restart or retry. If no real failure condition is planned, then success feedback is the main thing."

### [FR-022] (stated)
The success feedback shall clearly show that the puzzle has been completed.

**Source Evidence:**
- `[interview_turn:T034]` "When the player solves the puzzle, the game should clearly show that they’ve completed it, ideally with a simple success message or visual celebration. For failure, I don’t think we need a harsh game-over in the usual sense, since it’s a puzzle; if there is a failure condition at all, it should be something gentle like running out of a limit and then offering restart or retry. If no real failure condition is planned, then success feedback is the main thing."

### [FR-023] (stated)
The success feedback shall use a simple success message or visual celebration.

**Source Evidence:**
- `[interview_turn:T034]` "When the player solves the puzzle, the game should clearly show that they’ve completed it, ideally with a simple success message or visual celebration. For failure, I don’t think we need a harsh game-over in the usual sense, since it’s a puzzle; if there is a failure condition at all, it should be something gentle like running out of a limit and then offering restart or retry. If no real failure condition is planned, then success feedback is the main thing."

### [FR-024] (conditional)
If a failure condition is planned, it shall be gentle and may include offering restart or retry.

**Source Evidence:**
- `[interview_turn:T034]` "When the player solves the puzzle, the game should clearly show that they’ve completed it, ideally with a simple success message or visual celebration. For failure, I don’t think we need a harsh game-over in the usual sense, since it’s a puzzle; if there is a failure condition at all, it should be something gentle like running out of a limit and then offering restart or retry. If no real failure condition is planned, then success feedback is the main thing."

### [FR-025] (stated)
The interface shall stay very straightforward.

**Source Evidence:**
- `[interview_turn:T040]` "Yes, one more thing that would be helpful is some kind of simple player record or history so the game can remember past completion times, actions, and scores for each puzzle. Also, the interface should stay very straightforward, since it needs to work well for beginners as well as adults. Beyond that, I think the main requirements are covered."

## 4. Business Rules and Constraints

### [BR-001] (stated)
The game shall replace manual or ad hoc tracking with automatic in-game tracking.

**Source Evidence:**
- `[interview_turn:T010]` "We want to replace any manual or ad hoc tracking with the game handling it automatically, so players don’t have to record anything themselves. The main things we want are a smooth puzzle experience, clear progress tracking, and saved results like completion time, number of actions, and score so players can see how they did."

### [BR-002] (stated)
The game shall store player results locally in a simple way.

**Source Evidence:**
- `[interview_turn:T008]` "Right now, we don’t really have a formal system in place for this specific game, because Qheadache is intended to be built as a new standalone application. For similar puzzle gameplay, the expectation is just that the game itself handles the board, the moves, and the puzzle state, and then stores player results locally in a simple way. I don’t have a more detailed existing workflow to describe yet."

### [BR-003] (stated)
The game shall not require a harsh game-over as a failure mechanism.

**Source Evidence:**
- `[interview_turn:T034]` "When the player solves the puzzle, the game should clearly show that they’ve completed it, ideally with a simple success message or visual celebration. For failure, I don’t think we need a harsh game-over in the usual sense, since it’s a puzzle; if there is a failure condition at all, it should be something gentle like running out of a limit and then offering restart or retry. If no real failure condition is planned, then success feedback is the main thing."

### [BR-004] (stated)
When a player resumes the same unfinished puzzle, the timer and action count shall continue rather than reset.

**Source Evidence:**
- `[interview_turn:T030]` "I’d want both the timer and action count to continue from where they left off, so the player’s result reflects the whole attempt. It would feel unfair to reset them on resume if they are in the middle of the same puzzle. If there’s a technical reason to treat it differently, we can revisit it, but that would be my preference."

### [BR-005] (stated)
The game shall be designed to work well for beginners as well as adults.

**Source Evidence:**
- `[interview_turn:T040]` "Yes, one more thing that would be helpful is some kind of simple player record or history so the game can remember past completion times, actions, and scores for each puzzle. Also, the interface should stay very straightforward, since it needs to work well for beginners as well as adults. Beyond that, I think the main requirements are covered."

## 5. Data and External Interfaces

### [DI-001] (stated)
The system shall save and restore progress locally.

**Source Evidence:**
- `[interview_turn:T008]` "Right now, we don’t really have a formal system in place for this specific game, because Qheadache is intended to be built as a new standalone application. For similar puzzle gameplay, the expectation is just that the game itself handles the board, the moves, and the puzzle state, and then stores player results locally in a simple way. I don’t have a more detailed existing workflow to describe yet."
- `[interview_turn:T026]` "It should keep a player’s current progress so they can come back later and continue where they left off. It also needs to store results like completion time, number of actions, and score after a puzzle is finished. I’d want that information saved automatically without the player having to do anything extra."
- `[interview_turn:T038]` "A successful deployment would mean the game installs and runs reliably on the intended computer without special setup, and players can open it and start puzzles right away. It should correctly save and restore progress, record results, and let people play through levels without obvious crashes or data loss. If users can understand it quickly and complete puzzles smoothly, I’d consider that a success."

### [DI-002] (stated)
The system shall keep a simple player record or history of past completion times, actions, and scores for each puzzle.

**Source Evidence:**
- `[interview_turn:T040]` "Yes, one more thing that would be helpful is some kind of simple player record or history so the game can remember past completion times, actions, and scores for each puzzle. Also, the interface should stay very straightforward, since it needs to work well for beginners as well as adults. Beyond that, I think the main requirements are covered."

## 6. Quality Requirements

### [QR-001] (stated)
The game shall feel responsive.

**Source Evidence:**
- `[interview_turn:T022]` "The board should let the player see the puzzle clearly and move blocks in a straightforward way, using the mouse or touch if possible. The system should enforce the puzzle rules automatically, keep track of the current state after each move, and know when the challenge has been solved. It should feel responsive and make it obvious whether a move is valid."

### [QR-002] (stated)
The game shall be able to be opened and used right away without special setup on the intended computer.

**Source Evidence:**
- `[interview_turn:T038]` "A successful deployment would mean the game installs and runs reliably on the intended computer without special setup, and players can open it and start puzzles right away. It should correctly save and restore progress, record results, and let people play through levels without obvious crashes or data loss. If users can understand it quickly and complete puzzles smoothly, I’d consider that a success."

### [QR-003] (stated)
The game shall run reliably on the intended computer.

**Source Evidence:**
- `[interview_turn:T038]` "A successful deployment would mean the game installs and runs reliably on the intended computer without special setup, and players can open it and start puzzles right away. It should correctly save and restore progress, record results, and let people play through levels without obvious crashes or data loss. If users can understand it quickly and complete puzzles smoothly, I’d consider that a success."

### [QR-004] (stated)
The game shall let players understand it quickly.

**Source Evidence:**
- `[interview_turn:T038]` "A successful deployment would mean the game installs and runs reliably on the intended computer without special setup, and players can open it and start puzzles right away. It should correctly save and restore progress, record results, and let people play through levels without obvious crashes or data loss. If users can understand it quickly and complete puzzles smoothly, I’d consider that a success."

### [QR-005] (stated)
The game shall support a smooth puzzle experience.

**Source Evidence:**
- `[interview_turn:T010]` "We want to replace any manual or ad hoc tracking with the game handling it automatically, so players don’t have to record anything themselves. The main things we want are a smooth puzzle experience, clear progress tracking, and saved results like completion time, number of actions, and score so players can see how they did."
- `[interview_turn:T038]` "A successful deployment would mean the game installs and runs reliably on the intended computer without special setup, and players can open it and start puzzles right away. It should correctly save and restore progress, record results, and let people play through levels without obvious crashes or data loss. If users can understand it quickly and complete puzzles smoothly, I’d consider that a success."

### [QR-006] (stated)
The game shall avoid obvious crashes and data loss.

**Source Evidence:**
- `[interview_turn:T038]` "A successful deployment would mean the game installs and runs reliably on the intended computer without special setup, and players can open it and start puzzles right away. It should correctly save and restore progress, record results, and let people play through levels without obvious crashes or data loss. If users can understand it quickly and complete puzzles smoothly, I’d consider that a success."

## 7. Exceptions and Boundary Conditions

### [EX-001] (stated)
If a move is invalid, the game shall reject the move and show a gentle visual indication instead of interrupting play with an error message.

**Source Evidence:**
- `[interview_turn:T024]` "If a move is invalid, the game should simply prevent it from happening and give a clear indication that the block can’t go there. I’d prefer a gentle visual cue rather than an error message, so it doesn’t interrupt play too much. It should be obvious enough that the player understands the move was rejected."

### [EX-002] (stated)
If a player returns to an unfinished puzzle, the game shall offer the option to resume from the saved state.

**Source Evidence:**
- `[interview_turn:T028]` "When a player comes back, the game should offer them the option to resume their unfinished puzzle from the saved state. If they choose to continue, it should load the exact board position and keep the earlier time and action count, unless you decide those should reset separately. I’m not sure yet whether we’d preserve the timer continuously or only save the final result, so that might need to be decided."

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
It is unresolved whether the game will include a real failure condition or only success feedback.

**Source Evidence:**
- `[interview_turn:T034]` "When the player solves the puzzle, the game should clearly show that they’ve completed it, ideally with a simple success message or visual celebration. For failure, I don’t think we need a harsh game-over in the usual sense, since it’s a puzzle; if there is a failure condition at all, it should be something gentle like running out of a limit and then offering restart or retry. If no real failure condition is planned, then success feedback is the main thing."

### [UN-002]
It is unresolved whether mouse or touch input support is mandatory or only included if possible.

**Source Evidence:**
- `[interview_turn:T022]` "The board should let the player see the puzzle clearly and move blocks in a straightforward way, using the mouse or touch if possible. The system should enforce the puzzle rules automatically, keep track of the current state after each move, and know when the challenge has been solved. It should feel responsive and make it obvious whether a move is valid."
