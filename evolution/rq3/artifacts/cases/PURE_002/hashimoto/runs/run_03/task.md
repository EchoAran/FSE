# Implementation task: GAMMA-J Web Store

The requirements below were elicited in an interview and reviewed before delivery.

## Reviewed requirements

# Software Requirements Specification: GAMMA-J Web Store

## 1. Scope and Context

### [SC-001]
The web store shall enable people who are new to online commerce to set up and operate an online retail business.

## 2. Actors

None specified.

## 3. Functional Requirements

### [FR-001]
The system shall allow store owners and sales personnel to add and maintain products.

### [FR-002]
The system shall allow store owners and sales personnel to manage customer accounts.

### [FR-003]
The system shall allow customers to browse available products.

### [FR-004]
The system shall allow customers to maintain a shopping cart.

### [FR-005]
The system shall allow customers to place orders through the store.

### [FR-006]
Store owners and sales personnel shall sign in with their own accounts.

### [FR-007]
Customers shall have separate customer logins if they want to place orders or view their account history.

### [FR-008]
The system shall support card payments as the standard checkout payment option.

### [FR-009]
The system shall support PayPal if it is practical to include.

### [FR-010]
The system shall support at least the order statuses new, paid, packed, shipped, completed, and cancelled.

### [FR-011]
The system shall provide low-stock warnings.

### [FR-012]
Low-stock warnings shall be sent to store owners and the staff responsible for purchasing or inventory.

### [FR-013]
At launch, the system shall support a standard delivery shipping option.

### [FR-014]
At launch, the system shall support an express shipping option if it can be supported.

### [FR-015]
The system shall support self-service customer registration with immediate access.

### [FR-016]
The system shall support pending and blocked customer account statuses.

### [FR-017]
At launch, the store owner shall be able to set store name, contact details, currency, tax settings, shipping methods, and payment options during initial setup.

## 4. Business Rules and Constraints

### [BR-001]
Staff shall only be able to create or edit products that are active in the catalog.

### [BR-002]
The store shall not allow selling more than what is in stock unless backorders are later supported.

### [BR-003]
Customer accounts shall be subject to basic validation to avoid duplicate or incomplete records.

### [BR-004]
The system shall prevent checkout if required customer details are missing.

### [BR-005]
The system shall prevent checkout if required shipping details are missing.

### [BR-006]
An order shall only be placed when the cart is confirmed and the items are still available.

### [BR-007]
If an order has already been processed, changing it shall be restricted.

### [BR-008]
Store owners shall have full access to manage products, customer accounts, and overall store settings.

### [BR-009]
Sales personnel shall have limited access mainly to products, customers, and order handling, but not to administrative settings.

### [BR-010]
Customers shall only be able to view and change their own profile, cart, and orders.

### [BR-011]
For sensitive actions such as deleting records, changing order status, or making major account changes, tighter restrictions shall apply for staff.

### [BR-012]
The system shall support clear pricing at checkout.

### [BR-013]
Prices are expected to be shown before tax unless the customer's region expects tax-inclusive display.

### [BR-014]
Tax should be calculated based on location rather than the product alone, subject to confirmation.

### [BR-015]
Rounding shall be handled consistently at checkout so the customer sees the final total clearly.

### [BR-016]
The store should keep payment options simple at launch rather than support everything at once.

### [BR-017]
The system shall require the core shipping address fields: name, street address, city, postal code, country, and a contact phone or email.

### [BR-018]
The system shall validate shipping address format as much as possible based on the selected country or region.

### [BR-019]
The system shall be forgiving enough to accept international addresses rather than forcing one rigid format.

### [BR-020]
Checkout shall be blocked if the shipping address is incomplete or clearly invalid.

### [BR-021]
Sales personnel or owners shall be able to move orders forward as work is done.

### [BR-022]
Customers shall probably only be able to cancel an order before shipping.

### [BR-023]
Customers may be able to request a return after delivery if that process is supported.

### [BR-024]
Once an order is marked shipped, changes shall be limited and controlled by staff.

### [BR-025]
Cancellation should usually no longer be allowed once an order is marked shipped unless there is a special exception.

### [BR-026]
The low-stock threshold shall be configurable, ideally per product and possibly by category.

### [BR-027]
Customers shall see available shipping methods at checkout based on their destination.

### [BR-028]
Shipping cost shall be calculated from basic rules such as region and possibly weight or order total.

### [BR-029]
If an address cannot be served by a shipping method, the system shall hide that option instead of letting the customer pick it.

### [BR-030]
The system shall not require a manual approval step for ordinary customers at launch.

### [BR-031]
The system may hold a customer account if something looks suspicious or if verification fails.

### [BR-032]
Product management and customer account management may occur after initial setup in normal administration.

### [BR-033]
The store shall not go live until the core settings are complete.

### [BR-034]
The storefront shall require business address or legal details if those are needed for checkout and invoices.

## 5. Data and External Interfaces

None specified.

## 6. Quality Requirements

### [QR-001]
The system shall provide a simple interface that allows store owners and sales staff to manage products, customer accounts, and order processing with minimal technical help.

## 7. Exceptions and Boundary Conditions

None specified.

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
The tax model and final tax rules are not yet fully decided.

### [UN-002]
The support for discounts or promotions is planned for later and is not yet part of the confirmed launch scope.

### [UN-003]
Cash on delivery is not the default payment method, but its availability for special cases is not yet decided.

### [UN-004]
Bank transfer may be useful, but whether it will be supported at launch is not yet decided.

### [UN-005]
Manual exception handling for edge cases such as rural deliveries or businesses with special delivery instructions is expected, but the exact handling is not yet specified.

### [UN-006]
The low-stock warning threshold number is not yet fixed.

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
