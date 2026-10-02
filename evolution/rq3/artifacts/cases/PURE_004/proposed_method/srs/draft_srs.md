# Software Requirements Specification: Qheadache

## 1. Scope and Context

### [SC-001] (stated)
Qheadache shall be a standalone desktop puzzle game that players run on their own computer.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Qheadache is intended to be a standalone computerized puzzle game for people ranging from young beginners to adult players. Players use a graphical board to move blocks and solve a predefined challenge. The application should support normal play and retain useful information about a player's progress and results, such as time, actions, and scores."
- `[interview_turn:T018]` "It should run as a self-contained desktop game that people open and play on their own computer without needing any other system around it. In normal use, I’d expect it to launch, show the board and menus, and save progress locally on the same machine. The main operating condition that matters is that it should be easy to start and use in a typical home or school setting, without requiring special setup."

### [SC-002] (stated)
The game shall be intended for younger beginners, casual players, and adults who enjoy puzzle games.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Qheadache is intended to be a standalone computerized puzzle game for people ranging from young beginners to adult players. Players use a graphical board to move blocks and solve a predefined challenge. The application should support normal play and retain useful information about a player's progress and results, such as time, actions, and scores."
- `[interview_turn:T002]` "We expect mainly younger beginners, casual players, and adults who enjoy puzzle games. For beginners, the game should feel easy to understand, with simple controls and clear feedback so they can learn quickly without getting frustrated. For more experienced or adult players, it should still be engaging and challenging enough to feel satisfying, with progress tracking and results that make repeated play worthwhile."

## 2. Actors

None specified.

## 3. Functional Requirements

### [FR-001] (stated)
The game shall present a graphical board for gameplay.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Qheadache is intended to be a standalone computerized puzzle game for people ranging from young beginners to adult players. Players use a graphical board to move blocks and solve a predefined challenge. The application should support normal play and retain useful information about a player's progress and results, such as time, actions, and scores."
- `[interview_turn:T004]` "The first release should include the basic playable puzzle game, with a graphical board, block movement, a set of predefined challenges, and the ability to track things like time, moves, and score. It should also save player progress or results so the game feels complete and useful from the start. Later on, I’d expect improvements like more levels, better visuals, maybe difficulty options, and other features that make the game richer, but those wouldn’t be essential for the first version."

### [FR-002] (stated)
The game shall allow the player to move blocks on the board.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Qheadache is intended to be a standalone computerized puzzle game for people ranging from young beginners to adult players. Players use a graphical board to move blocks and solve a predefined challenge. The application should support normal play and retain useful information about a player's progress and results, such as time, actions, and scores."
- `[interview_turn:T004]` "The first release should include the basic playable puzzle game, with a graphical board, block movement, a set of predefined challenges, and the ability to track things like time, moves, and score. It should also save player progress or results so the game feels complete and useful from the start. Later on, I’d expect improvements like more levels, better visuals, maybe difficulty options, and other features that make the game richer, but those wouldn’t be essential for the first version."

### [FR-003] (stated)
The game shall include predefined challenges or puzzles.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Qheadache is intended to be a standalone computerized puzzle game for people ranging from young beginners to adult players. Players use a graphical board to move blocks and solve a predefined challenge. The application should support normal play and retain useful information about a player's progress and results, such as time, actions, and scores."
- `[interview_turn:T004]` "The first release should include the basic playable puzzle game, with a graphical board, block movement, a set of predefined challenges, and the ability to track things like time, moves, and score. It should also save player progress or results so the game feels complete and useful from the start. Later on, I’d expect improvements like more levels, better visuals, maybe difficulty options, and other features that make the game richer, but those wouldn’t be essential for the first version."

### [FR-004] (stated)
The game shall recognize a puzzle as completed when the player reaches the predefined goal state for that challenge.

**Source Evidence:**
- `[interview_turn:T014]` "A puzzle is solved when the player reaches the predefined goal state for that challenge, meaning the blocks are arranged in the required final position. Once that happens, the game should recognize completion right away and record the result. If there’s any special win condition beyond the final block arrangement, I’d need to check, but the main idea is reaching the target layout."
- `[interview_turn:T050]` "In normal play, completion should be recognized as soon as the goal state is reached. The only exception I can think of is if the level has a special rule like requiring the final arrangement to be held for a moment or confirmed by the player, but that would need to be very clearly defined. Otherwise, I’d keep it immediate so the result feels reliable and straightforward."

### [FR-005] (stated)
The game shall record completion immediately when the goal state is reached in normal play.

**Source Evidence:**
- `[interview_turn:T014]` "A puzzle is solved when the player reaches the predefined goal state for that challenge, meaning the blocks are arranged in the required final position. Once that happens, the game should recognize completion right away and record the result. If there’s any special win condition beyond the final block arrangement, I’d need to check, but the main idea is reaching the target layout."
- `[interview_turn:T050]` "In normal play, completion should be recognized as soon as the goal state is reached. The only exception I can think of is if the level has a special rule like requiring the final arrangement to be held for a moment or confirmed by the player, but that would need to be very clearly defined. Otherwise, I’d keep it immediate so the result feels reliable and straightforward."

### [FR-006] (stated)
The game shall track time, moves, and score for player progress and results.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Qheadache is intended to be a standalone computerized puzzle game for people ranging from young beginners to adult players. Players use a graphical board to move blocks and solve a predefined challenge. The application should support normal play and retain useful information about a player's progress and results, such as time, actions, and scores."
- `[interview_turn:T004]` "The first release should include the basic playable puzzle game, with a graphical board, block movement, a set of predefined challenges, and the ability to track things like time, moves, and score. It should also save player progress or results so the game feels complete and useful from the start. Later on, I’d expect improvements like more levels, better visuals, maybe difficulty options, and other features that make the game richer, but those wouldn’t be essential for the first version."
- `[interview_turn:T012]` "Yes, I think records and help text should use terms like time taken, number of moves, score, current puzzle, and completed puzzle. Menus could also refer to things like restart, continue, select puzzle, and results, since those are the kinds of actions players will look for. I’d keep the wording plain and avoid jargon so it stays accessible for younger players too."

### [FR-007] (stated)
The game shall save player progress or results locally on the same machine.

**Source Evidence:**
- `[interview_turn:T004]` "The first release should include the basic playable puzzle game, with a graphical board, block movement, a set of predefined challenges, and the ability to track things like time, moves, and score. It should also save player progress or results so the game feels complete and useful from the start. Later on, I’d expect improvements like more levels, better visuals, maybe difficulty options, and other features that make the game richer, but those wouldn’t be essential for the first version."
- `[interview_turn:T018]` "It should run as a self-contained desktop game that people open and play on their own computer without needing any other system around it. In normal use, I’d expect it to launch, show the board and menus, and save progress locally on the same machine. The main operating condition that matters is that it should be easy to start and use in a typical home or school setting, without requiring special setup."

### [FR-008] (conditional)
The game shall let the player continue playing if the local save file cannot be accessed, while clearly indicating that progress or results may not be stored.

**Source Evidence:**
- `[interview_turn:T024]` "Yes, it should work fully offline, and the player should still be able to play even if there’s no network at all. If the save file can’t be accessed, the game should let them keep playing if possible, but it should clearly tell them that progress or results may not be stored. If the machine shuts down during saving, I’d want the game to avoid corrupting the existing data and recover cleanly on the next start if it can."

### [FR-009] (stated)
The game shall avoid corrupting existing data if the machine shuts down during saving and shall restore the last completed save on the next launch.

**Source Evidence:**
- `[interview_turn:T024]` "Yes, it should work fully offline, and the player should still be able to play even if there’s no network at all. If the save file can’t be accessed, the game should let them keep playing if possible, but it should clearly tell them that progress or results may not be stored. If the machine shuts down during saving, I’d want the game to avoid corrupting the existing data and recover cleanly on the next start if it can."
- `[interview_turn:T052]` "On the next launch, it should restore the last completed save and ignore the interrupted save attempt. I wouldn’t want a partial write to break the player’s progress or leave them in a corrupted state. If possible, it should fail safely and just resume from the most recent valid record."

### [FR-010] (stated)
The game shall support keyboard-only control for all essential gameplay and menu actions.

**Source Evidence:**
- `[interview_turn:T040]` "Yes, I’d want the game to be usable by beginners and also comfortable for adults, so readable text and a clear, high-contrast board would be important from the start. Keyboard-only control would be a strong preference, because some players may not want to rely only on a mouse. If larger font sizing is easy to support, that would be a good inclusion too, especially for menus and results screens."
- `[interview_turn:T042]` "On the board, the keyboard should let players move focus or the selected piece clearly and trigger valid moves without needing the mouse. In menus, the arrow keys, Enter, and Escape would be the basic expected controls, with Tab for moving between controls if needed. I don’t think any core part should require the mouse, though the mouse can still be available as an optional convenience if we want it."
- `[interview_turn:T054]` "Keyboard control should cover everything essential end to end. The mouse can still be allowed as a convenience on the board and in menus, but it shouldn’t be required for any core action. That keeps the game accessible and consistent for keyboard-only players."

### [FR-011] (stated)
The game shall allow the mouse as an optional convenience on the board and in menus, but not require it for any core action.

**Source Evidence:**
- `[interview_turn:T042]` "On the board, the keyboard should let players move focus or the selected piece clearly and trigger valid moves without needing the mouse. In menus, the arrow keys, Enter, and Escape would be the basic expected controls, with Tab for moving between controls if needed. I don’t think any core part should require the mouse, though the mouse can still be available as an optional convenience if we want it."
- `[interview_turn:T054]` "Keyboard control should cover everything essential end to end. The mouse can still be allowed as a convenience on the board and in menus, but it shouldn’t be required for any core action. That keeps the game accessible and consistent for keyboard-only players."

### [FR-012] (stated)
The game shall prevent illegal block moves.

**Source Evidence:**
- `[interview_turn:T030]` "The main rule is that blocks should only move in ways that are valid for the puzzle, so the game should prevent illegal moves rather than letting the player break the board state. Movement needs to feel responsive and predictable, with each action clearly counted so the player knows what was done. If the puzzle has a defined solution path, the game should still allow any legal move, not force a single exact sequence unless that’s part of the puzzle design."
- `[interview_turn:T032]` "That depends on the specific puzzle layout, but in general I’d expect blocks to move only into open space and only in the directions the puzzle allows. If the puzzle is grid-based, then one step at a time is probably the safest default unless a particular level is designed for sliding until blocked. I wouldn’t want movement rules to be loose enough that players can move through other blocks or ignore the board boundaries."

### [FR-013] (stated)
The game shall allow only legal moves that fit the puzzle layout and do not move through other blocks or outside the board boundaries.

**Source Evidence:**
- `[interview_turn:T030]` "The main rule is that blocks should only move in ways that are valid for the puzzle, so the game should prevent illegal moves rather than letting the player break the board state. Movement needs to feel responsive and predictable, with each action clearly counted so the player knows what was done. If the puzzle has a defined solution path, the game should still allow any legal move, not force a single exact sequence unless that’s part of the puzzle design."
- `[interview_turn:T032]` "That depends on the specific puzzle layout, but in general I’d expect blocks to move only into open space and only in the directions the puzzle allows. If the puzzle is grid-based, then one step at a time is probably the safest default unless a particular level is designed for sliding until blocked. I wouldn’t want movement rules to be loose enough that players can move through other blocks or ignore the board boundaries."

### [FR-014] (stated)
The game shall count a rejected move attempt as no action.

**Source Evidence:**
- `[interview_turn:T034]` "Rejected attempts should not count as actions, since nothing actually changed on the board. If one player input legitimately causes more than one block to shift as part of a single move, I’d count that as one action as long as it happens in one deliberate input. The goal is that the action total reflects player decisions, not internal animation or failed tries."

### [FR-015] (stated)
The game shall count one deliberate input that legitimately shifts more than one block as one action.

**Source Evidence:**
- `[interview_turn:T034]` "Rejected attempts should not count as actions, since nothing actually changed on the board. If one player input legitimately causes more than one block to shift as part of a single move, I’d count that as one action as long as it happens in one deliberate input. The goal is that the action total reflects player decisions, not internal animation or failed tries."

### [FR-016] (conditional)
The game shall allow any legal move sequence unless a specific puzzle design requires a strict sequence.

**Source Evidence:**
- `[interview_turn:T030]` "The main rule is that blocks should only move in ways that are valid for the puzzle, so the game should prevent illegal moves rather than letting the player break the board state. Movement needs to feel responsive and predictable, with each action clearly counted so the player knows what was done. If the puzzle has a defined solution path, the game should still allow any legal move, not force a single exact sequence unless that’s part of the puzzle design."
- `[interview_turn:T036]` "I’d prefer that any legal sequence remains valid as long as the player is making correct moves, so the puzzle stays fair and flexible. If a level does require a very specific order, that should be by design and clearly communicated somehow, because otherwise players may think the game is broken. For the first release, I’d lean toward not making move order feel overly restrictive unless a specific puzzle depends on it."

### [FR-017] (conditional)
If a level requires a strict move sequence, the game shall make that requirement obvious before play and provide clear feedback during play when a move would break the sequence.

**Source Evidence:**
- `[interview_turn:T038]` "If a level has a strict sequence, the game should make that obvious before the player starts, maybe with a short level note or a preview hint. During play, it should give clear feedback when a move would break the sequence, rather than silently letting the player get stuck. I’d want the player to understand that the constraint is part of the puzzle, not a bug."

### [FR-018] (stated)
The game shall keep best time and fewest actions only for completed puzzles.

**Source Evidence:**
- `[interview_turn:T028]` "Best time and fewest actions should only count for a completed puzzle, not for an abandoned run or one where the player quits halfway through. If a puzzle is restarted, that current attempt should stop counting and a new attempt should begin, but the earlier completed results should still remain in history. I’d also want us to exclude obviously invalid cases, like if the save was damaged or the game never properly finished the puzzle."

### [FR-019] (stated)
The game shall not count best time and fewest actions for abandoned runs, restarted runs, or obviously invalid cases such as damaged saves or puzzles that were never properly finished.

**Source Evidence:**
- `[interview_turn:T028]` "Best time and fewest actions should only count for a completed puzzle, not for an abandoned run or one where the player quits halfway through. If a puzzle is restarted, that current attempt should stop counting and a new attempt should begin, but the earlier completed results should still remain in history. I’d also want us to exclude obviously invalid cases, like if the save was damaged or the game never properly finished the puzzle."

### [FR-020] (stated)
If a puzzle is restarted, the current attempt shall stop counting and a new attempt shall begin while earlier completed results remain in history.

**Source Evidence:**
- `[interview_turn:T028]` "Best time and fewest actions should only count for a completed puzzle, not for an abandoned run or one where the player quits halfway through. If a puzzle is restarted, that current attempt should stop counting and a new attempt should begin, but the earlier completed results should still remain in history. I’d also want us to exclude obviously invalid cases, like if the save was damaged or the game never properly finished the puzzle."

### [FR-021] (conditional)
When a saved game is restored as a resume of the player's progress, the game shall continue the existing stats for that attempt.

**Source Evidence:**
- `[interview_turn:T044]` "I’d treat a restore as part of the same attempt if it’s just resuming the player’s progress, so the stats continue from the existing record. If the restore effectively rewinds or changes the puzzle in a way that makes the result no longer comparable, then I’d rather mark that attempt separately or not count it in the main results. The important thing is that the saved record stays honest about how the player actually completed that run."

### [FR-022] (conditional)
If a restore effectively rewinds or changes the puzzle state so the result is no longer comparable, the game shall treat that attempt separately or exclude it from the main results.

**Source Evidence:**
- `[interview_turn:T044]` "I’d treat a restore as part of the same attempt if it’s just resuming the player’s progress, so the stats continue from the existing record. If the restore effectively rewinds or changes the puzzle in a way that makes the result no longer comparable, then I’d rather mark that attempt separately or not count it in the main results. The important thing is that the saved record stays honest about how the player actually completed that run."

### [FR-023] (conditional)
If undo is included in the first release, the game shall flag undo separately in the record and shall not wipe out the whole attempt.

**Source Evidence:**
- `[interview_turn:T046]` "Yes, I’d keep the first release focused on the core puzzle experience and basic progress tracking. Hints, tutorials, account sign-in, and sharing results could wait for later unless we find they’re essential for usability. Undo might be the one exception I’d consider, but if we include it, we should be clear whether it affects the recorded stats."
- `[interview_turn:T048]` "If undo is included, I’d flag it separately so the record shows that the player used assistance, but I wouldn’t want it to wipe out the whole attempt. The time and move count should still be kept, because they reflect what happened, but the final result should indicate that undo was used. That way the stats stay useful without pretending the run was completely clean."

### [FR-024] (conditional)
If undo is included in the first release, the game shall keep the time and move count for the attempt and indicate in the final result that undo was used.

**Source Evidence:**
- `[interview_turn:T046]` "Yes, I’d keep the first release focused on the core puzzle experience and basic progress tracking. Hints, tutorials, account sign-in, and sharing results could wait for later unless we find they’re essential for usability. Undo might be the one exception I’d consider, but if we include it, we should be clear whether it affects the recorded stats."
- `[interview_turn:T048]` "If undo is included, I’d flag it separately so the record shows that the player used assistance, but I wouldn’t want it to wipe out the whole attempt. The time and move count should still be kept, because they reflect what happened, but the final result should indicate that undo was used. That way the stats stay useful without pretending the run was completely clean."

### [FR-025] (stated)
The game shall run fully offline and shall not depend on internet access or extra services.

**Source Evidence:**
- `[interview_turn:T020]` "For the first release, I’d keep it lightweight and straightforward, so it runs well on ordinary computers without needing high-end hardware. It should be quick to open, simple to navigate, and not depend on internet access or extra services. I’d also keep the feature set focused on playing, saving progress, and viewing results rather than adding lots of extra functions."
- `[interview_turn:T024]` "Yes, it should work fully offline, and the player should still be able to play even if there’s no network at all. If the save file can’t be accessed, the game should let them keep playing if possible, but it should clearly tell them that progress or results may not be stored. If the machine shuts down during saving, I’d want the game to avoid corrupting the existing data and recover cleanly on the next start if it can."

### [FR-026] (conditional)
The game shall support local user profiles or player profiles so that one person's saves do not overwrite another person's progress.

**Source Evidence:**
- `[interview_turn:T026]` "Yes, that’s likely, especially on a shared home or school computer. I’d expect progress and results to be tied to the local user profile or whatever player profile the game uses, so one person’s saves don’t overwrite another’s. If the game supports multiple profiles, each player’s settings and records should stay separate."

### [FR-027] (conditional)
If multiple profiles are supported, each player's settings and records shall stay separate.

**Source Evidence:**
- `[interview_turn:T026]` "Yes, that’s likely, especially on a shared home or school computer. I’d expect progress and results to be tied to the local user profile or whatever player profile the game uses, so one person’s saves don’t overwrite another’s. If the game supports multiple profiles, each player’s settings and records should stay separate."

### [FR-028] (stated)
The game shall use simple and consistent terminology for blocks, moves, time, score, level, and puzzle.

**Source Evidence:**
- `[interview_turn:T010]` "I’d want the language to stay simple and consistent, like using the same terms for blocks, moves, time, score, level, and puzzle. If we pick one term for the challenge area or the goal, that should be used everywhere in the game instead of switching words. The idea is that players can quickly understand what’s happening without having to learn different names for the same thing."
- `[interview_turn:T012]` "Yes, I think records and help text should use terms like time taken, number of moves, score, current puzzle, and completed puzzle. Menus could also refer to things like restart, continue, select puzzle, and results, since those are the kinds of actions players will look for. I’d keep the wording plain and avoid jargon so it stays accessible for younger players too."
- `[interview_turn:T016]` "Those terms should stay the same everywhere as much as possible, because consistency will make the game easier to use. I wouldn’t want one screen saying “restart” and another saying “try again” unless there’s a very good reason, because that can confuse players. If there’s a special context where a different word is clearer, we could allow it, but that should be the exception."

### [FR-029] (stated)
The game shall keep terms such as current puzzle, completed puzzle, restart, continue, select puzzle, and results consistent across menus, help text, and records as much as possible.

**Source Evidence:**
- `[interview_turn:T012]` "Yes, I think records and help text should use terms like time taken, number of moves, score, current puzzle, and completed puzzle. Menus could also refer to things like restart, continue, select puzzle, and results, since those are the kinds of actions players will look for. I’d keep the wording plain and avoid jargon so it stays accessible for younger players too."
- `[interview_turn:T016]` "Those terms should stay the same everywhere as much as possible, because consistency will make the game easier to use. I wouldn’t want one screen saying “restart” and another saying “try again” unless there’s a very good reason, because that can confuse players. If there’s a special context where a different word is clearer, we could allow it, but that should be the exception."

### [FR-030] (stated)
The game shall use plain wording and avoid jargon in menus, help text, and records.

**Source Evidence:**
- `[interview_turn:T012]` "Yes, I think records and help text should use terms like time taken, number of moves, score, current puzzle, and completed puzzle. Menus could also refer to things like restart, continue, select puzzle, and results, since those are the kinds of actions players will look for. I’d keep the wording plain and avoid jargon so it stays accessible for younger players too."

### [FR-031] (stated)
The game shall be quick to open and simple to navigate.

**Source Evidence:**
- `[interview_turn:T020]` "For the first release, I’d keep it lightweight and straightforward, so it runs well on ordinary computers without needing high-end hardware. It should be quick to open, simple to navigate, and not depend on internet access or extra services. I’d also keep the feature set focused on playing, saving progress, and viewing results rather than adding lots of extra functions."

### [FR-032] (stated)
The game shall let players start, play, view results, and save progress as the focused first-release feature set.

**Source Evidence:**
- `[interview_turn:T020]` "For the first release, I’d keep it lightweight and straightforward, so it runs well on ordinary computers without needing high-end hardware. It should be quick to open, simple to navigate, and not depend on internet access or extra services. I’d also keep the feature set focused on playing, saving progress, and viewing results rather than adding lots of extra functions."
- `[interview_turn:T046]` "Yes, I’d keep the first release focused on the core puzzle experience and basic progress tracking. Hints, tutorials, account sign-in, and sharing results could wait for later unless we find they’re essential for usability. Undo might be the one exception I’d consider, but if we include it, we should be clear whether it affects the recorded stats."

## 4. Business Rules and Constraints

None specified.

## 5. Data and External Interfaces

None specified.

## 6. Quality Requirements

### [QR-001] (stated)
The game shall feel easy to understand for younger beginners, with simple controls and clear feedback.

**Source Evidence:**
- `[interview_turn:T002]` "We expect mainly younger beginners, casual players, and adults who enjoy puzzle games. For beginners, the game should feel easy to understand, with simple controls and clear feedback so they can learn quickly without getting frustrated. For more experienced or adult players, it should still be engaging and challenging enough to feel satisfying, with progress tracking and results that make repeated play worthwhile."

### [QR-002] (stated)
The game shall remain engaging and challenging enough for more experienced or adult players.

**Source Evidence:**
- `[interview_turn:T002]` "We expect mainly younger beginners, casual players, and adults who enjoy puzzle games. For beginners, the game should feel easy to understand, with simple controls and clear feedback so they can learn quickly without getting frustrated. For more experienced or adult players, it should still be engaging and challenging enough to feel satisfying, with progress tracking and results that make repeated play worthwhile."

### [QR-003] (stated)
The game shall provide readable text and a clear, high-contrast board.

**Source Evidence:**
- `[interview_turn:T040]` "Yes, I’d want the game to be usable by beginners and also comfortable for adults, so readable text and a clear, high-contrast board would be important from the start. Keyboard-only control would be a strong preference, because some players may not want to rely only on a mouse. If larger font sizing is easy to support, that would be a good inclusion too, especially for menus and results screens."

### [QR-004] (conditional)
The game should support larger font sizes if that is easy to provide, especially for menus and results screens.

**Source Evidence:**
- `[interview_turn:T040]` "Yes, I’d want the game to be usable by beginners and also comfortable for adults, so readable text and a clear, high-contrast board would be important from the start. Keyboard-only control would be a strong preference, because some players may not want to rely only on a mouse. If larger font sizing is easy to support, that would be a good inclusion too, especially for menus and results screens."

### [QR-005] (stated)
The game shall run well on ordinary computers without requiring high-end hardware.

**Source Evidence:**
- `[interview_turn:T020]` "For the first release, I’d keep it lightweight and straightforward, so it runs well on ordinary computers without needing high-end hardware. It should be quick to open, simple to navigate, and not depend on internet access or extra services. I’d also keep the feature set focused on playing, saving progress, and viewing results rather than adding lots of extra functions."

### [QR-006] (stated)
The game shall be stable and easy to maintain.

**Source Evidence:**
- `[interview_turn:T022]` "No, I don’t think there’s a mandated technology for the first release. What matters more is that it’s stable, easy to maintain, and can save the player’s progress reliably on the local machine. If the team has a preferred stack, we can use that, but I don’t have a required one in mind."

### [QR-007] (stated)
The game shall save the player's progress reliably on the local machine.

**Source Evidence:**
- `[interview_turn:T022]` "No, I don’t think there’s a mandated technology for the first release. What matters more is that it’s stable, easy to maintain, and can save the player’s progress reliably on the local machine. If the team has a preferred stack, we can use that, but I don’t have a required one in mind."

### [QR-008] (stated)
The game shall be usable in a typical home or school setting without requiring special setup.

**Source Evidence:**
- `[interview_turn:T018]` "It should run as a self-contained desktop game that people open and play on their own computer without needing any other system around it. In normal use, I’d expect it to launch, show the board and menus, and save progress locally on the same machine. The main operating condition that matters is that it should be easy to start and use in a typical home or school setting, without requiring special setup."

### [QR-009] (stated)
The game shall be responsive and predictable during block movement.

**Source Evidence:**
- `[interview_turn:T030]` "The main rule is that blocks should only move in ways that are valid for the puzzle, so the game should prevent illegal moves rather than letting the player break the board state. Movement needs to feel responsive and predictable, with each action clearly counted so the player knows what was done. If the puzzle has a defined solution path, the game should still allow any legal move, not force a single exact sequence unless that’s part of the puzzle design."

### [QR-010] (stated)
The game shall make player actions clearly countable so the player knows what was done.

**Source Evidence:**
- `[interview_turn:T030]` "The main rule is that blocks should only move in ways that are valid for the puzzle, so the game should prevent illegal moves rather than letting the player break the board state. Movement needs to feel responsive and predictable, with each action clearly counted so the player knows what was done. If the puzzle has a defined solution path, the game should still allow any legal move, not force a single exact sequence unless that’s part of the puzzle design."
- `[interview_turn:T034]` "Rejected attempts should not count as actions, since nothing actually changed on the board. If one player input legitimately causes more than one block to shift as part of a single move, I’d count that as one action as long as it happens in one deliberate input. The goal is that the action total reflects player decisions, not internal animation or failed tries."

## 7. Exceptions and Boundary Conditions

### [EX-001] (conditional)
A level may require a strict move sequence only if that requirement is part of the puzzle design and is clearly communicated to the player.

**Source Evidence:**
- `[interview_turn:T036]` "I’d prefer that any legal sequence remains valid as long as the player is making correct moves, so the puzzle stays fair and flexible. If a level does require a very specific order, that should be by design and clearly communicated somehow, because otherwise players may think the game is broken. For the first release, I’d lean toward not making move order feel overly restrictive unless a specific puzzle depends on it."
- `[interview_turn:T038]` "If a level has a strict sequence, the game should make that obvious before the player starts, maybe with a short level note or a preview hint. During play, it should give clear feedback when a move would break the sequence, rather than silently letting the player get stuck. I’d want the player to understand that the constraint is part of the puzzle, not a bug."

### [EX-002] (conditional)
Completion may be delayed beyond the goal state only if a level has a special rule such as requiring the final arrangement to be held for a moment or confirmed by the player.

**Source Evidence:**
- `[interview_turn:T050]` "In normal play, completion should be recognized as soon as the goal state is reached. The only exception I can think of is if the level has a special rule like requiring the final arrangement to be held for a moment or confirmed by the player, but that would need to be very clearly defined. Otherwise, I’d keep it immediate so the result feels reliable and straightforward."

### [EX-003] (conditional)
A different term may be used in a special context only if it is clearer; otherwise terminology shall remain consistent.

**Source Evidence:**
- `[interview_turn:T016]` "Those terms should stay the same everywhere as much as possible, because consistency will make the game easier to use. I wouldn’t want one screen saying “restart” and another saying “try again” unless there’s a very good reason, because that can confuse players. If there’s a special context where a different word is clearer, we could allow it, but that should be the exception."

### [EX-004] (conditional)
Starting fresh after an update is acceptable only if a major change makes old saves impossible to use, and that case should be rare and clearly explained.

**Source Evidence:**
- `[interview_turn:T008]` "Older saved games should ideally still work after updates, because players will expect their progress to carry over. I’d only accept starting fresh if there were a major change that makes old saves impossible to use, and even then we’d want that to be rare and clearly explained. For normal updates, preserving saved progress would be important."

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
The first release's inclusion of undo is undecided.

**Source Evidence:**
- `[interview_turn:T046]` "Yes, I’d keep the first release focused on the core puzzle experience and basic progress tracking. Hints, tutorials, account sign-in, and sharing results could wait for later unless we find they’re essential for usability. Undo might be the one exception I’d consider, but if we include it, we should be clear whether it affects the recorded stats."

### [UN-002]
The first release's inclusion of tutorials is undecided.

**Source Evidence:**
- `[interview_turn:T046]` "Yes, I’d keep the first release focused on the core puzzle experience and basic progress tracking. Hints, tutorials, account sign-in, and sharing results could wait for later unless we find they’re essential for usability. Undo might be the one exception I’d consider, but if we include it, we should be clear whether it affects the recorded stats."

### [UN-003]
The first release's inclusion of hints is undecided.

**Source Evidence:**
- `[interview_turn:T046]` "Yes, I’d keep the first release focused on the core puzzle experience and basic progress tracking. Hints, tutorials, account sign-in, and sharing results could wait for later unless we find they’re essential for usability. Undo might be the one exception I’d consider, but if we include it, we should be clear whether it affects the recorded stats."

### [UN-004]
The first release's inclusion of account sign-in is undecided.

**Source Evidence:**
- `[interview_turn:T046]` "Yes, I’d keep the first release focused on the core puzzle experience and basic progress tracking. Hints, tutorials, account sign-in, and sharing results could wait for later unless we find they’re essential for usability. Undo might be the one exception I’d consider, but if we include it, we should be clear whether it affects the recorded stats."

### [UN-005]
The first release's inclusion of sharing results is undecided.

**Source Evidence:**
- `[interview_turn:T046]` "Yes, I’d keep the first release focused on the core puzzle experience and basic progress tracking. Hints, tutorials, account sign-in, and sharing results could wait for later unless we find they’re essential for usability. Undo might be the one exception I’d consider, but if we include it, we should be clear whether it affects the recorded stats."

### [UN-006]
The specific technology, engine, or storage stack for the first release is not mandated.

**Source Evidence:**
- `[interview_turn:T022]` "No, I don’t think there’s a mandated technology for the first release. What matters more is that it’s stable, easy to maintain, and can save the player’s progress reliably on the local machine. If the team has a preferred stack, we can use that, but I don’t have a required one in mind."
