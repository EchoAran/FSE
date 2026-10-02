# Implementation task: GAMMA-J Web Store

The requirements below were elicited in an interview and reviewed before delivery.

## Reviewed requirements

# Software Requirements Specification: GAMMA-J Web Store

## 1. Scope and Context

### [SC-001]
The system shall be a web store for people who are new to online commerce and for new online business owners.

## 2. Actors

### [ACT-001]
Store owners shall use the system to manage the online retail business.

### [ACT-002]
Sales personnel shall use the system to manage products and customer accounts.

### [ACT-003]
Customers shall use the system to browse products, maintain a shopping cart, and place orders.

## 3. Functional Requirements

### [FR-001]
The system shall allow staff to create and update products.

### [FR-002]
The system shall allow staff to create and update customer accounts.

### [FR-003]
The system shall allow customers to browse available products.

### [FR-004]
The system shall allow customers to search products by name.

### [FR-005]
The system shall allow customers to filter products by category and price range.

### [FR-006]
The system shall allow customers to add products to a shopping cart.

### [FR-007]
The system shall allow customers to change quantities in the shopping cart.

### [FR-008]
The system shall allow customers to remove items from the shopping cart.

### [FR-009]
The system shall show customers the cart total before checkout.

### [FR-010]
The system shall allow customers to enter order details, confirm the items, and submit the order.

### [FR-011]
The system shall generate an immediate order confirmation for customers after an order is placed.

### [FR-012]
The system shall provide staff visibility that a new order has been placed.

### [FR-013]
The system shall allow customers to view their order history.

### [FR-014]
The system shall provide basic sales reporting for staff so they can see sales activity.

### [FR-015]
The system shall allow customers to view and update their own contact details and address.

### [FR-016]
The system shall support a simple checkout process for first-time customers.

### [FR-017]
The system shall require the customer's name, contact email, and delivery address before an order can be submitted.

### [FR-018]
The system shall treat the contact number as optional at checkout.

### [FR-019]
The system shall display product name, short description, price, and current availability for each product.

### [FR-020]
The system shall display a product image when one is available.

### [FR-021]
The system shall allow customers to get immediate confirmation that their purchase was successful.

## 4. Business Rules and Constraints

### [BR-001]
The first version shall prioritize order placement, shopping cart, product browsing, and product management.

### [BR-002]
The first release shall stay focused on the core buying and management tasks rather than including too many extras.

### [BR-003]
The system should be simple enough that someone with little e-commerce experience can use it without training.

### [BR-004]
The system should let a new store owner get the shop running without much technical help.

### [BR-005]
The system should be stable and easy to learn.

## 5. Data and External Interfaces

None specified.

## 6. Quality Requirements

None specified.

## 7. Exceptions and Boundary Conditions

None specified.

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
It is unresolved whether order confirmation notifications should be advanced or simple.

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
