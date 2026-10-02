# Software Requirements Specification: PDF Split and Merge

## 1. Scope and Context

### [SC-001] (stated)
The project is a free graphical tool for manipulating PDF documents.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."
- `[interview_turn:T002]` "Yes, that scope sounds right to me. We want a free PDF tool that lets people manipulate documents without changing the originals, and it should support both visual, manual work and command-line use for repeatable tasks."

### [SC-002] (stated)
The tool must allow users to manipulate PDF documents without altering the original input files.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."
- `[interview_turn:T002]` "Yes, that scope sounds right to me. We want a free PDF tool that lets people manipulate documents without changing the originals, and it should support both visual, manual work and command-line use for repeatable tasks."

### [SC-003] (stated)
The tool must support both visual, manual work and command-line use for repeatable tasks.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."
- `[interview_turn:T002]` "Yes, that scope sounds right to me. We want a free PDF tool that lets people manipulate documents without changing the originals, and it should support both visual, manual work and command-line use for repeatable tasks."

## 2. Actors

### [ST-001] (stated)
The tool is intended for users who need everyday PDF handling, including casual users working through a graphical interface and users performing automated or recurring jobs through the command line.

**Source Evidence:**
- `[interview_turn:T004]` "I’m representing the team that needs this tool for everyday PDF handling, especially for splitting, merging, and rearranging files without risking the source documents. I’m familiar with the practical workflow we want, including both the graphical interface for casual users and the command-line option for automated or recurring jobs."
- `[interview_turn:T002]` "Yes, that scope sounds right to me. We want a free PDF tool that lets people manipulate documents without changing the originals, and it should support both visual, manual work and command-line use for repeatable tasks."
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."

## 3. Functional Requirements

### [FR-001] (stated)
The system shall support splitting PDF documents.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."
- `[interview_turn:T004]` "I’m representing the team that needs this tool for everyday PDF handling, especially for splitting, merging, and rearranging files without risking the source documents. I’m familiar with the practical workflow we want, including both the graphical interface for casual users and the command-line option for automated or recurring jobs."
- `[interview_turn:T008]` "We want to replace the ad hoc mix of tools with one free, reliable application that can do the common PDF manipulation tasks in one place. The main improvements are preserving the original files, making visual composition and page rearrangement easy, and supporting automated or repeatable operations through the command line."

### [FR-002] (stated)
The system shall support merging selected files or sections.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."

### [FR-003] (stated)
The system shall support extracting selected pages from PDF documents.

**Source Evidence:**
- `[interview_turn:T010]` "Yes, we’d also want the ability to save reusable work setups so someone can come back later and continue the same kind of PDF assembly or splitting job. It would also be useful to have alternation of pages from different documents and extraction of selected pages, since those are common document-prep tasks for us."

### [FR-004] (stated)
The system shall support rotating pages.

**Source Evidence:**
- `[interview_turn:T012]` "Yes, rotation should definitely be included. In practice people often need to fix scanned pages or mix documents that aren’t oriented the same way, so being able to rotate pages as part of the workflow is important."

### [FR-005] (stated)
The system shall support reordering pages.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."
- `[interview_turn:T008]` "We want to replace the ad hoc mix of tools with one free, reliable application that can do the common PDF manipulation tasks in one place. The main improvements are preserving the original files, making visual composition and page rearrangement easy, and supporting automated or repeatable operations through the command line."

### [FR-006] (stated)
The system shall support alternating pages from different documents.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."
- `[interview_turn:T010]` "Yes, we’d also want the ability to save reusable work setups so someone can come back later and continue the same kind of PDF assembly or splitting job. It would also be useful to have alternation of pages from different documents and extraction of selected pages, since those are common document-prep tasks for us."

### [FR-007] (stated)
The system shall support visually composing new documents.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."
- `[interview_turn:T008]` "We want to replace the ad hoc mix of tools with one free, reliable application that can do the common PDF manipulation tasks in one place. The main improvements are preserving the original files, making visual composition and page rearrangement easy, and supporting automated or repeatable operations through the command line."

### [FR-008] (stated)
The system shall allow users to save reusable work environments or setups.

**Source Evidence:**
- `[interview_turn:T010]` "Yes, we’d also want the ability to save reusable work setups so someone can come back later and continue the same kind of PDF assembly or splitting job. It would also be useful to have alternation of pages from different documents and extraction of selected pages, since those are common document-prep tasks for us."

### [FR-009] (stated)
The system shall provide a command-line path for recurring or automated operations.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."
- `[interview_turn:T002]` "Yes, that scope sounds right to me. We want a free PDF tool that lets people manipulate documents without changing the originals, and it should support both visual, manual work and command-line use for repeatable tasks."
- `[interview_turn:T004]` "I’m representing the team that needs this tool for everyday PDF handling, especially for splitting, merging, and rearranging files without risking the source documents. I’m familiar with the practical workflow we want, including both the graphical interface for casual users and the command-line option for automated or recurring jobs."
- `[interview_turn:T008]` "We want to replace the ad hoc mix of tools with one free, reliable application that can do the common PDF manipulation tasks in one place. The main improvements are preserving the original files, making visual composition and page rearrangement easy, and supporting automated or repeatable operations through the command line."

## 4. Business Rules and Constraints

None specified.

## 5. Data and External Interfaces

None specified.

## 6. Quality Requirements

None specified.

## 7. Exceptions and Boundary Conditions

None specified.

## 8. Unresolved Information

No unresolved items identified.
