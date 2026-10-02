# Software Requirements Specification: PDF Split and Merge

## 1. Scope and Context

### [SC-001] (stated)
The product is a free graphical tool for manipulating PDF documents without altering the original input files.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."

## 2. Actors

### [SA-001] (stated)
The tool shall support regular office users who need quick one-off PDF fixes.

**Source Evidence:**
- `[interview_turn:T004]` "The main user groups are probably regular office users who just need quick one-off PDF fixes, like splitting a file or combining a few documents, and they’ll want a simple visual interface with minimal setup. Then there are power users or support staff who repeat the same kinds of operations often, so they’ll care more about reusable workspaces and the command-line option for automation.
We should also support people who need careful page-level control, like reordering, rotating, or extracting specific pages, because they’ll expect precision and a clear preview of what will happen. I don’t know yet if there are separate stakeholder groups on the business side beyond that, but from a product perspective those are the main usage patterns we need to cover."

### [SA-002] (stated)
The tool shall support power users or support staff who repeat the same operations often.

**Source Evidence:**
- `[interview_turn:T004]` "The main user groups are probably regular office users who just need quick one-off PDF fixes, like splitting a file or combining a few documents, and they’ll want a simple visual interface with minimal setup. Then there are power users or support staff who repeat the same kinds of operations often, so they’ll care more about reusable workspaces and the command-line option for automation.
We should also support people who need careful page-level control, like reordering, rotating, or extracting specific pages, because they’ll expect precision and a clear preview of what will happen. I don’t know yet if there are separate stakeholder groups on the business side beyond that, but from a product perspective those are the main usage patterns we need to cover."

## 3. Functional Requirements

### [FR-001] (stated)
The tool shall support splitting PDF documents.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."
- `[interview_turn:T002]` "The main goal is to let people manipulate PDFs quickly without risking the originals, and to do it in a way that feels simpler than a full document editor. The most important user outcomes are being able to split, merge, extract, rotate, reorder, and compose documents visually with little effort, and also having a command-line option for repeatable tasks.
I’d judge success by whether users can complete those common PDF tasks accurately and without confusion, whether they can do it without modifying the source files, and whether they can save and reuse their setup for similar work later. If both casual users and power users can finish their jobs faster than with their current tools, I’d consider that a good sign the tool is meeting its goals."

### [FR-002] (stated)
The tool shall support merging selected files or sections.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."
- `[interview_turn:T002]` "The main goal is to let people manipulate PDFs quickly without risking the originals, and to do it in a way that feels simpler than a full document editor. The most important user outcomes are being able to split, merge, extract, rotate, reorder, and compose documents visually with little effort, and also having a command-line option for repeatable tasks.
I’d judge success by whether users can complete those common PDF tasks accurately and without confusion, whether they can do it without modifying the source files, and whether they can save and reuse their setup for similar work later. If both casual users and power users can finish their jobs faster than with their current tools, I’d consider that a good sign the tool is meeting its goals."

### [FR-003] (stated)
The tool shall support extracting pages from PDF documents.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."
- `[interview_turn:T002]` "The main goal is to let people manipulate PDFs quickly without risking the originals, and to do it in a way that feels simpler than a full document editor. The most important user outcomes are being able to split, merge, extract, rotate, reorder, and compose documents visually with little effort, and also having a command-line option for repeatable tasks.
I’d judge success by whether users can complete those common PDF tasks accurately and without confusion, whether they can do it without modifying the source files, and whether they can save and reuse their setup for similar work later. If both casual users and power users can finish their jobs faster than with their current tools, I’d consider that a good sign the tool is meeting its goals."

### [FR-004] (stated)
The tool shall support rotating pages.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."
- `[interview_turn:T002]` "The main goal is to let people manipulate PDFs quickly without risking the originals, and to do it in a way that feels simpler than a full document editor. The most important user outcomes are being able to split, merge, extract, rotate, reorder, and compose documents visually with little effort, and also having a command-line option for repeatable tasks.
I’d judge success by whether users can complete those common PDF tasks accurately and without confusion, whether they can do it without modifying the source files, and whether they can save and reuse their setup for similar work later. If both casual users and power users can finish their jobs faster than with their current tools, I’d consider that a good sign the tool is meeting its goals."

### [FR-005] (stated)
The tool shall support reordering pages.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."
- `[interview_turn:T002]` "The main goal is to let people manipulate PDFs quickly without risking the originals, and to do it in a way that feels simpler than a full document editor. The most important user outcomes are being able to split, merge, extract, rotate, reorder, and compose documents visually with little effort, and also having a command-line option for repeatable tasks.
I’d judge success by whether users can complete those common PDF tasks accurately and without confusion, whether they can do it without modifying the source files, and whether they can save and reuse their setup for similar work later. If both casual users and power users can finish their jobs faster than with their current tools, I’d consider that a good sign the tool is meeting its goals."

### [FR-006] (stated)
The tool shall support alternating pages from different documents.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."

### [FR-007] (stated)
The tool shall support visually composing new documents.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."
- `[interview_turn:T002]` "The main goal is to let people manipulate PDFs quickly without risking the originals, and to do it in a way that feels simpler than a full document editor. The most important user outcomes are being able to split, merge, extract, rotate, reorder, and compose documents visually with little effort, and also having a command-line option for repeatable tasks.
I’d judge success by whether users can complete those common PDF tasks accurately and without confusion, whether they can do it without modifying the source files, and whether they can save and reuse their setup for similar work later. If both casual users and power users can finish their jobs faster than with their current tools, I’d consider that a good sign the tool is meeting its goals."

### [FR-008] (stated)
The tool shall provide a command-line option for repeatable or automated tasks.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."
- `[interview_turn:T002]` "The main goal is to let people manipulate PDFs quickly without risking the originals, and to do it in a way that feels simpler than a full document editor. The most important user outcomes are being able to split, merge, extract, rotate, reorder, and compose documents visually with little effort, and also having a command-line option for repeatable tasks.
I’d judge success by whether users can complete those common PDF tasks accurately and without confusion, whether they can do it without modifying the source files, and whether they can save and reuse their setup for similar work later. If both casual users and power users can finish their jobs faster than with their current tools, I’d consider that a good sign the tool is meeting its goals."

### [FR-009] (stated)
The tool shall allow users to save and reuse their setup or work environment.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."
- `[interview_turn:T002]` "The main goal is to let people manipulate PDFs quickly without risking the originals, and to do it in a way that feels simpler than a full document editor. The most important user outcomes are being able to split, merge, extract, rotate, reorder, and compose documents visually with little effort, and also having a command-line option for repeatable tasks.
I’d judge success by whether users can complete those common PDF tasks accurately and without confusion, whether they can do it without modifying the source files, and whether they can save and reuse their setup for similar work later. If both casual users and power users can finish their jobs faster than with their current tools, I’d consider that a good sign the tool is meeting its goals."

### [FR-010] (stated)
The tool shall perform PDF manipulation quickly.

**Source Evidence:**
- `[interview_turn:T002]` "The main goal is to let people manipulate PDFs quickly without risking the originals, and to do it in a way that feels simpler than a full document editor. The most important user outcomes are being able to split, merge, extract, rotate, reorder, and compose documents visually with little effort, and also having a command-line option for repeatable tasks.
I’d judge success by whether users can complete those common PDF tasks accurately and without confusion, whether they can do it without modifying the source files, and whether they can save and reuse their setup for similar work later. If both casual users and power users can finish their jobs faster than with their current tools, I’d consider that a good sign the tool is meeting its goals."

### [FR-011] (stated)
The graphical tool shall support a simple visual interface with minimal setup for one-off PDF tasks.

**Source Evidence:**
- `[interview_turn:T004]` "The main user groups are probably regular office users who just need quick one-off PDF fixes, like splitting a file or combining a few documents, and they’ll want a simple visual interface with minimal setup. Then there are power users or support staff who repeat the same kinds of operations often, so they’ll care more about reusable workspaces and the command-line option for automation.
We should also support people who need careful page-level control, like reordering, rotating, or extracting specific pages, because they’ll expect precision and a clear preview of what will happen. I don’t know yet if there are separate stakeholder groups on the business side beyond that, but from a product perspective those are the main usage patterns we need to cover."

### [FR-012] (stated)
The tool shall support careful page-level control with a clear preview of the result.

**Source Evidence:**
- `[interview_turn:T004]` "The main user groups are probably regular office users who just need quick one-off PDF fixes, like splitting a file or combining a few documents, and they’ll want a simple visual interface with minimal setup. Then there are power users or support staff who repeat the same kinds of operations often, so they’ll care more about reusable workspaces and the command-line option for automation.
We should also support people who need careful page-level control, like reordering, rotating, or extracting specific pages, because they’ll expect precision and a clear preview of what will happen. I don’t know yet if there are separate stakeholder groups on the business side beyond that, but from a product perspective those are the main usage patterns we need to cover."

### [FR-013] (stated)
The tool shall write output as a new file unless the user explicitly chooses otherwise.

**Source Evidence:**
- `[interview_turn:T006]` "It should definitely avoid overwriting the original files by default, and the output should be written as a new file unless the user explicitly chooses otherwise. For a simple workflow, I’d expect it to remember a default output folder or let users save alongside the source when that makes sense, and for repeated jobs it would be useful to have naming rules or a saved destination in the reusable workspace.
I’d also want a clear confirmation before writing if there’s any chance of replacing an existing file, or if the chosen operation would produce multiple outputs. For the command-line side, the destination should be explicit in the command or configurable through the saved setup so automated runs don’t need manual prompts."

### [FR-014] (conditional)
The tool shall support a default output folder for simple workflows.

**Source Evidence:**
- `[interview_turn:T006]` "It should definitely avoid overwriting the original files by default, and the output should be written as a new file unless the user explicitly chooses otherwise. For a simple workflow, I’d expect it to remember a default output folder or let users save alongside the source when that makes sense, and for repeated jobs it would be useful to have naming rules or a saved destination in the reusable workspace.
I’d also want a clear confirmation before writing if there’s any chance of replacing an existing file, or if the chosen operation would produce multiple outputs. For the command-line side, the destination should be explicit in the command or configurable through the saved setup so automated runs don’t need manual prompts."

### [FR-015] (conditional)
The tool shall allow users to save output alongside the source when that makes sense for the workflow.

**Source Evidence:**
- `[interview_turn:T006]` "It should definitely avoid overwriting the original files by default, and the output should be written as a new file unless the user explicitly chooses otherwise. For a simple workflow, I’d expect it to remember a default output folder or let users save alongside the source when that makes sense, and for repeated jobs it would be useful to have naming rules or a saved destination in the reusable workspace.
I’d also want a clear confirmation before writing if there’s any chance of replacing an existing file, or if the chosen operation would produce multiple outputs. For the command-line side, the destination should be explicit in the command or configurable through the saved setup so automated runs don’t need manual prompts."

### [FR-016] (conditional)
The tool shall support naming rules or a saved destination in the reusable workspace for repeated jobs.

**Source Evidence:**
- `[interview_turn:T006]` "It should definitely avoid overwriting the original files by default, and the output should be written as a new file unless the user explicitly chooses otherwise. For a simple workflow, I’d expect it to remember a default output folder or let users save alongside the source when that makes sense, and for repeated jobs it would be useful to have naming rules or a saved destination in the reusable workspace.
I’d also want a clear confirmation before writing if there’s any chance of replacing an existing file, or if the chosen operation would produce multiple outputs. For the command-line side, the destination should be explicit in the command or configurable through the saved setup so automated runs don’t need manual prompts."

### [FR-017] (conditional)
The graphical tool shall provide a clear confirmation before writing if there is any chance of replacing an existing file.

**Source Evidence:**
- `[interview_turn:T006]` "It should definitely avoid overwriting the original files by default, and the output should be written as a new file unless the user explicitly chooses otherwise. For a simple workflow, I’d expect it to remember a default output folder or let users save alongside the source when that makes sense, and for repeated jobs it would be useful to have naming rules or a saved destination in the reusable workspace.
I’d also want a clear confirmation before writing if there’s any chance of replacing an existing file, or if the chosen operation would produce multiple outputs. For the command-line side, the destination should be explicit in the command or configurable through the saved setup so automated runs don’t need manual prompts."

### [FR-018] (conditional)
The graphical tool shall provide a clear confirmation before writing if the chosen operation would produce multiple outputs.

**Source Evidence:**
- `[interview_turn:T006]` "It should definitely avoid overwriting the original files by default, and the output should be written as a new file unless the user explicitly chooses otherwise. For a simple workflow, I’d expect it to remember a default output folder or let users save alongside the source when that makes sense, and for repeated jobs it would be useful to have naming rules or a saved destination in the reusable workspace.
I’d also want a clear confirmation before writing if there’s any chance of replacing an existing file, or if the chosen operation would produce multiple outputs. For the command-line side, the destination should be explicit in the command or configurable through the saved setup so automated runs don’t need manual prompts."

### [FR-019] (conditional)
The command-line interface shall require the destination to be explicit in the command or configurable through the saved setup.

**Source Evidence:**
- `[interview_turn:T006]` "It should definitely avoid overwriting the original files by default, and the output should be written as a new file unless the user explicitly chooses otherwise. For a simple workflow, I’d expect it to remember a default output folder or let users save alongside the source when that makes sense, and for repeated jobs it would be useful to have naming rules or a saved destination in the reusable workspace.
I’d also want a clear confirmation before writing if there’s any chance of replacing an existing file, or if the chosen operation would produce multiple outputs. For the command-line side, the destination should be explicit in the command or configurable through the saved setup so automated runs don’t need manual prompts."

### [FR-020] (stated)
The graphical tool shall let users review the full set of outputs before anything is saved.

**Source Evidence:**
- `[interview_turn:T008]` "In the graphical tool, I’d expect users to see the full set of outputs before anything is saved, so they can review what will be produced and catch mistakes early. If one operation creates multiple files, it should support a consistent naming pattern or a way to assign destinations in bulk, rather than forcing people to handle each output one by one unless they really want that level of control.
In command-line mode, I’d expect the output behavior to be fully defined up front, with naming patterns or destination rules passed in as part of the command or saved configuration. A confirmation step would be useful in the GUI before writing files, but in automated command-line runs I’d expect it to fail safely or require explicit overwrite options instead of stopping for interactive confirmation."

### [FR-021] (stated)
When one operation creates multiple files, the tool shall support a consistent naming pattern or bulk destination assignment.

**Source Evidence:**
- `[interview_turn:T008]` "In the graphical tool, I’d expect users to see the full set of outputs before anything is saved, so they can review what will be produced and catch mistakes early. If one operation creates multiple files, it should support a consistent naming pattern or a way to assign destinations in bulk, rather than forcing people to handle each output one by one unless they really want that level of control.
In command-line mode, I’d expect the output behavior to be fully defined up front, with naming patterns or destination rules passed in as part of the command or saved configuration. A confirmation step would be useful in the GUI before writing files, but in automated command-line runs I’d expect it to fail safely or require explicit overwrite options instead of stopping for interactive confirmation."

### [FR-022] (stated)
In command-line mode, the output behavior shall be fully defined up front.

**Source Evidence:**
- `[interview_turn:T008]` "In the graphical tool, I’d expect users to see the full set of outputs before anything is saved, so they can review what will be produced and catch mistakes early. If one operation creates multiple files, it should support a consistent naming pattern or a way to assign destinations in bulk, rather than forcing people to handle each output one by one unless they really want that level of control.
In command-line mode, I’d expect the output behavior to be fully defined up front, with naming patterns or destination rules passed in as part of the command or saved configuration. A confirmation step would be useful in the GUI before writing files, but in automated command-line runs I’d expect it to fail safely or require explicit overwrite options instead of stopping for interactive confirmation."

### [FR-023] (stated)
In command-line mode, naming patterns or destination rules shall be passed in as part of the command or saved configuration.

**Source Evidence:**
- `[interview_turn:T008]` "In the graphical tool, I’d expect users to see the full set of outputs before anything is saved, so they can review what will be produced and catch mistakes early. If one operation creates multiple files, it should support a consistent naming pattern or a way to assign destinations in bulk, rather than forcing people to handle each output one by one unless they really want that level of control.
In command-line mode, I’d expect the output behavior to be fully defined up front, with naming patterns or destination rules passed in as part of the command or saved configuration. A confirmation step would be useful in the GUI before writing files, but in automated command-line runs I’d expect it to fail safely or require explicit overwrite options instead of stopping for interactive confirmation."

### [FR-024] (stated)
In automated command-line runs, the tool shall fail safely or require explicit overwrite options instead of stopping for interactive confirmation.

**Source Evidence:**
- `[interview_turn:T008]` "In the graphical tool, I’d expect users to see the full set of outputs before anything is saved, so they can review what will be produced and catch mistakes early. If one operation creates multiple files, it should support a consistent naming pattern or a way to assign destinations in bulk, rather than forcing people to handle each output one by one unless they really want that level of control.
In command-line mode, I’d expect the output behavior to be fully defined up front, with naming patterns or destination rules passed in as part of the command or saved configuration. A confirmation step would be useful in the GUI before writing files, but in automated command-line runs I’d expect it to fail safely or require explicit overwrite options instead of stopping for interactive confirmation."

## 4. Business Rules and Constraints

### [BR-001] (stated)
The tool shall avoid overwriting the original files by default.

**Source Evidence:**
- `[interview_turn:T006]` "It should definitely avoid overwriting the original files by default, and the output should be written as a new file unless the user explicitly chooses otherwise. For a simple workflow, I’d expect it to remember a default output folder or let users save alongside the source when that makes sense, and for repeated jobs it would be useful to have naming rules or a saved destination in the reusable workspace.
I’d also want a clear confirmation before writing if there’s any chance of replacing an existing file, or if the chosen operation would produce multiple outputs. For the command-line side, the destination should be explicit in the command or configurable through the saved setup so automated runs don’t need manual prompts."

## 5. Data and External Interfaces

None specified.

## 6. Quality Requirements

None specified.

## 7. Exceptions and Boundary Conditions

None specified.

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
Whether there are separate stakeholder groups on the business side beyond the user groups described is not yet known.

**Source Evidence:**
- `[interview_turn:T004]` "The main user groups are probably regular office users who just need quick one-off PDF fixes, like splitting a file or combining a few documents, and they’ll want a simple visual interface with minimal setup. Then there are power users or support staff who repeat the same kinds of operations often, so they’ll care more about reusable workspaces and the command-line option for automation.
We should also support people who need careful page-level control, like reordering, rotating, or extracting specific pages, because they’ll expect precision and a clear preview of what will happen. I don’t know yet if there are separate stakeholder groups on the business side beyond that, but from a product perspective those are the main usage patterns we need to cover."
