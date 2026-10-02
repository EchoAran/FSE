# Software Requirements Specification: Qheadache

## 1. Scope and Context

### [SC-001] (stated)
Qheadache is a standalone computerized puzzle game.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Qheadache is intended to be a standalone computerized puzzle game for people ranging from young beginners to adult players. Players use a graphical board to move blocks and solve a predefined challenge. The application should support normal play and retain useful information about a player's progress and results, such as time, actions, and scores."

### [SC-002] (stated)
Qheadache is intended for players ranging from young beginners to adult players.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Qheadache is intended to be a standalone computerized puzzle game for people ranging from young beginners to adult players. Players use a graphical board to move blocks and solve a predefined challenge. The application should support normal play and retain useful information about a player's progress and results, such as time, actions, and scores."

### [SC-003] (stated)
The game shall use a graphical board for gameplay.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Qheadache is intended to be a standalone computerized puzzle game for people ranging from young beginners to adult players. Players use a graphical board to move blocks and solve a predefined challenge. The application should support normal play and retain useful information about a player's progress and results, such as time, actions, and scores."

### [SC-004] (stated)
Qheadache is intended to be a solid standalone game that people enjoy using and returning to.

**Source Evidence:**
- `[interview_turn:T002]` "The main goal is to give players a smooth, enjoyable puzzle experience that feels easy to pick up but still satisfying to solve. We want it to work well for beginners and also stay interesting for adults, so the game should be both entertaining and mentally engaging.
From a usage standpoint, success would mean players can complete puzzles without confusion, understand their progress clearly, and want to keep replaying or improving their times and scores. We are not really aiming for a business-heavy product here, more for a solid standalone game that people actually enjoy using and returning to."

## 2. Actors

### [ST-001] (stated)
Players are key stakeholders of Qheadache.

**Source Evidence:**
- `[interview_turn:T004]` "The key stakeholders are mainly the players, since they’re the ones using the game and caring about the puzzle experience, progress, and scores. Then there are the game designers or content owners, who care about the puzzle challenges themselves and whether the gameplay feels balanced and engaging.
We’d also have an administrator or support person if needed, mostly to manage the game setup, review progress data, or handle updates and issues. I’m not sure yet if we need any separate technical support role beyond that, but those are the main groups I’d expect."

### [ST-002] (stated)
Game designers or content owners are key stakeholders of Qheadache.

**Source Evidence:**
- `[interview_turn:T004]` "The key stakeholders are mainly the players, since they’re the ones using the game and caring about the puzzle experience, progress, and scores. Then there are the game designers or content owners, who care about the puzzle challenges themselves and whether the gameplay feels balanced and engaging.
We’d also have an administrator or support person if needed, mostly to manage the game setup, review progress data, or handle updates and issues. I’m not sure yet if we need any separate technical support role beyond that, but those are the main groups I’d expect."

### [ST-003] (conditional)
An administrator or support person may be a stakeholder for Qheadache.

**Source Evidence:**
- `[interview_turn:T004]` "The key stakeholders are mainly the players, since they’re the ones using the game and caring about the puzzle experience, progress, and scores. Then there are the game designers or content owners, who care about the puzzle challenges themselves and whether the gameplay feels balanced and engaging.
We’d also have an administrator or support person if needed, mostly to manage the game setup, review progress data, or handle updates and issues. I’m not sure yet if we need any separate technical support role beyond that, but those are the main groups I’d expect."

## 3. Functional Requirements

### [FR-001] (stated)
The player shall move blocks on the graphical board to solve a predefined challenge.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Qheadache is intended to be a standalone computerized puzzle game for people ranging from young beginners to adult players. Players use a graphical board to move blocks and solve a predefined challenge. The application should support normal play and retain useful information about a player's progress and results, such as time, actions, and scores."

### [FR-002] (stated)
The application shall support normal play.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Qheadache is intended to be a standalone computerized puzzle game for people ranging from young beginners to adult players. Players use a graphical board to move blocks and solve a predefined challenge. The application should support normal play and retain useful information about a player's progress and results, such as time, actions, and scores."

### [FR-003] (stated)
The application shall retain player progress and results information, including time, actions, and scores.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Qheadache is intended to be a standalone computerized puzzle game for people ranging from young beginners to adult players. Players use a graphical board to move blocks and solve a predefined challenge. The application should support normal play and retain useful information about a player's progress and results, such as time, actions, and scores."

### [FR-004] (stated)
The game shall provide a smooth and enjoyable puzzle experience.

**Source Evidence:**
- `[interview_turn:T002]` "The main goal is to give players a smooth, enjoyable puzzle experience that feels easy to pick up but still satisfying to solve. We want it to work well for beginners and also stay interesting for adults, so the game should be both entertaining and mentally engaging.
From a usage standpoint, success would mean players can complete puzzles without confusion, understand their progress clearly, and want to keep replaying or improving their times and scores. We are not really aiming for a business-heavy product here, more for a solid standalone game that people actually enjoy using and returning to."

### [FR-005] (stated)
The game shall be easy to pick up for players.

**Source Evidence:**
- `[interview_turn:T002]` "The main goal is to give players a smooth, enjoyable puzzle experience that feels easy to pick up but still satisfying to solve. We want it to work well for beginners and also stay interesting for adults, so the game should be both entertaining and mentally engaging.
From a usage standpoint, success would mean players can complete puzzles without confusion, understand their progress clearly, and want to keep replaying or improving their times and scores. We are not really aiming for a business-heavy product here, more for a solid standalone game that people actually enjoy using and returning to."

### [FR-006] (stated)
The game shall be satisfying to solve.

**Source Evidence:**
- `[interview_turn:T002]` "The main goal is to give players a smooth, enjoyable puzzle experience that feels easy to pick up but still satisfying to solve. We want it to work well for beginners and also stay interesting for adults, so the game should be both entertaining and mentally engaging.
From a usage standpoint, success would mean players can complete puzzles without confusion, understand their progress clearly, and want to keep replaying or improving their times and scores. We are not really aiming for a business-heavy product here, more for a solid standalone game that people actually enjoy using and returning to."

### [FR-007] (stated)
The game shall remain interesting for adults.

**Source Evidence:**
- `[interview_turn:T002]` "The main goal is to give players a smooth, enjoyable puzzle experience that feels easy to pick up but still satisfying to solve. We want it to work well for beginners and also stay interesting for adults, so the game should be both entertaining and mentally engaging.
From a usage standpoint, success would mean players can complete puzzles without confusion, understand their progress clearly, and want to keep replaying or improving their times and scores. We are not really aiming for a business-heavy product here, more for a solid standalone game that people actually enjoy using and returning to."

### [FR-008] (stated)
The game shall be entertaining and mentally engaging.

**Source Evidence:**
- `[interview_turn:T002]` "The main goal is to give players a smooth, enjoyable puzzle experience that feels easy to pick up but still satisfying to solve. We want it to work well for beginners and also stay interesting for adults, so the game should be both entertaining and mentally engaging.
From a usage standpoint, success would mean players can complete puzzles without confusion, understand their progress clearly, and want to keep replaying or improving their times and scores. We are not really aiming for a business-heavy product here, more for a solid standalone game that people actually enjoy using and returning to."

### [FR-009] (stated)
Players shall be able to complete puzzles without confusion.

**Source Evidence:**
- `[interview_turn:T002]` "The main goal is to give players a smooth, enjoyable puzzle experience that feels easy to pick up but still satisfying to solve. We want it to work well for beginners and also stay interesting for adults, so the game should be both entertaining and mentally engaging.
From a usage standpoint, success would mean players can complete puzzles without confusion, understand their progress clearly, and want to keep replaying or improving their times and scores. We are not really aiming for a business-heavy product here, more for a solid standalone game that people actually enjoy using and returning to."

### [FR-010] (stated)
Players shall be able to understand their progress clearly.

**Source Evidence:**
- `[interview_turn:T002]` "The main goal is to give players a smooth, enjoyable puzzle experience that feels easy to pick up but still satisfying to solve. We want it to work well for beginners and also stay interesting for adults, so the game should be both entertaining and mentally engaging.
From a usage standpoint, success would mean players can complete puzzles without confusion, understand their progress clearly, and want to keep replaying or improving their times and scores. We are not really aiming for a business-heavy product here, more for a solid standalone game that people actually enjoy using and returning to."

### [FR-011] (stated)
Players shall be able to replay the game or improve their times and scores.

**Source Evidence:**
- `[interview_turn:T002]` "The main goal is to give players a smooth, enjoyable puzzle experience that feels easy to pick up but still satisfying to solve. We want it to work well for beginners and also stay interesting for adults, so the game should be both entertaining and mentally engaging.
From a usage standpoint, success would mean players can complete puzzles without confusion, understand their progress clearly, and want to keep replaying or improving their times and scores. We are not really aiming for a business-heavy product here, more for a solid standalone game that people actually enjoy using and returning to."

### [FR-012] (stated)
The administrator shall be able to set up or change the puzzles that are available.

**Source Evidence:**
- `[interview_turn:T006]` "At a minimum, the administrator should be able to set up or change the puzzles that are available, including the board layout and the predefined challenge the player has to solve. It would also be useful to adjust difficulty-related things like how hard a puzzle is or which challenges are shown to beginners versus more advanced players.
For data management, I’d expect access to player results and progress records, maybe with the ability to clear or archive them if needed. As for updates, I think changes should be applied centrally and then take effect the next time the game starts, unless it’s a very small setting change that can safely be applied immediately."

### [FR-013] (stated)
The administrator shall be able to configure the board layout.

**Source Evidence:**
- `[interview_turn:T006]` "At a minimum, the administrator should be able to set up or change the puzzles that are available, including the board layout and the predefined challenge the player has to solve. It would also be useful to adjust difficulty-related things like how hard a puzzle is or which challenges are shown to beginners versus more advanced players.
For data management, I’d expect access to player results and progress records, maybe with the ability to clear or archive them if needed. As for updates, I think changes should be applied centrally and then take effect the next time the game starts, unless it’s a very small setting change that can safely be applied immediately."

### [FR-014] (stated)
The administrator shall be able to configure the predefined challenge the player has to solve.

**Source Evidence:**
- `[interview_turn:T006]` "At a minimum, the administrator should be able to set up or change the puzzles that are available, including the board layout and the predefined challenge the player has to solve. It would also be useful to adjust difficulty-related things like how hard a puzzle is or which challenges are shown to beginners versus more advanced players.
For data management, I’d expect access to player results and progress records, maybe with the ability to clear or archive them if needed. As for updates, I think changes should be applied centrally and then take effect the next time the game starts, unless it’s a very small setting change that can safely be applied immediately."

### [FR-015] (stated)
The administrator shall be able to adjust difficulty-related settings.

**Source Evidence:**
- `[interview_turn:T006]` "At a minimum, the administrator should be able to set up or change the puzzles that are available, including the board layout and the predefined challenge the player has to solve. It would also be useful to adjust difficulty-related things like how hard a puzzle is or which challenges are shown to beginners versus more advanced players.
For data management, I’d expect access to player results and progress records, maybe with the ability to clear or archive them if needed. As for updates, I think changes should be applied centrally and then take effect the next time the game starts, unless it’s a very small setting change that can safely be applied immediately."

### [FR-016] (stated)
The administrator shall be able to control which challenges are shown to beginners versus more advanced players.

**Source Evidence:**
- `[interview_turn:T006]` "At a minimum, the administrator should be able to set up or change the puzzles that are available, including the board layout and the predefined challenge the player has to solve. It would also be useful to adjust difficulty-related things like how hard a puzzle is or which challenges are shown to beginners versus more advanced players.
For data management, I’d expect access to player results and progress records, maybe with the ability to clear or archive them if needed. As for updates, I think changes should be applied centrally and then take effect the next time the game starts, unless it’s a very small setting change that can safely be applied immediately."

### [FR-017] (stated)
The administrator shall have access to player results and progress records.

**Source Evidence:**
- `[interview_turn:T006]` "At a minimum, the administrator should be able to set up or change the puzzles that are available, including the board layout and the predefined challenge the player has to solve. It would also be useful to adjust difficulty-related things like how hard a puzzle is or which challenges are shown to beginners versus more advanced players.
For data management, I’d expect access to player results and progress records, maybe with the ability to clear or archive them if needed. As for updates, I think changes should be applied centrally and then take effect the next time the game starts, unless it’s a very small setting change that can safely be applied immediately."

### [FR-018] (stated)
The administrator shall be able to clear player results and progress records if needed.

**Source Evidence:**
- `[interview_turn:T006]` "At a minimum, the administrator should be able to set up or change the puzzles that are available, including the board layout and the predefined challenge the player has to solve. It would also be useful to adjust difficulty-related things like how hard a puzzle is or which challenges are shown to beginners versus more advanced players.
For data management, I’d expect access to player results and progress records, maybe with the ability to clear or archive them if needed. As for updates, I think changes should be applied centrally and then take effect the next time the game starts, unless it’s a very small setting change that can safely be applied immediately."

### [FR-019] (stated)
The administrator shall be able to archive player results and progress records if needed.

**Source Evidence:**
- `[interview_turn:T006]` "At a minimum, the administrator should be able to set up or change the puzzles that are available, including the board layout and the predefined challenge the player has to solve. It would also be useful to adjust difficulty-related things like how hard a puzzle is or which challenges are shown to beginners versus more advanced players.
For data management, I’d expect access to player results and progress records, maybe with the ability to clear or archive them if needed. As for updates, I think changes should be applied centrally and then take effect the next time the game starts, unless it’s a very small setting change that can safely be applied immediately."

### [FR-020] (stated)
Changes made by the administrator shall be applied centrally.

**Source Evidence:**
- `[interview_turn:T006]` "At a minimum, the administrator should be able to set up or change the puzzles that are available, including the board layout and the predefined challenge the player has to solve. It would also be useful to adjust difficulty-related things like how hard a puzzle is or which challenges are shown to beginners versus more advanced players.
For data management, I’d expect access to player results and progress records, maybe with the ability to clear or archive them if needed. As for updates, I think changes should be applied centrally and then take effect the next time the game starts, unless it’s a very small setting change that can safely be applied immediately."

### [FR-021] (conditional)
Unless a change is a very small setting change that can safely be applied immediately, administrator changes shall take effect the next time the game starts.

**Source Evidence:**
- `[interview_turn:T006]` "At a minimum, the administrator should be able to set up or change the puzzles that are available, including the board layout and the predefined challenge the player has to solve. It would also be useful to adjust difficulty-related things like how hard a puzzle is or which challenges are shown to beginners versus more advanced players.
For data management, I’d expect access to player results and progress records, maybe with the ability to clear or archive them if needed. As for updates, I think changes should be applied centrally and then take effect the next time the game starts, unless it’s a very small setting change that can safely be applied immediately."

## 4. Business Rules and Constraints

None specified.

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

**Source Evidence:**
- `[interview_turn:T004]` "The key stakeholders are mainly the players, since they’re the ones using the game and caring about the puzzle experience, progress, and scores. Then there are the game designers or content owners, who care about the puzzle challenges themselves and whether the gameplay feels balanced and engaging.
We’d also have an administrator or support person if needed, mostly to manage the game setup, review progress data, or handle updates and issues. I’m not sure yet if we need any separate technical support role beyond that, but those are the main groups I’d expect."
