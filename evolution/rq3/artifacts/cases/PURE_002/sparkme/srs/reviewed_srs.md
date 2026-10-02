# Software Requirements Specification: GAMMA-J Web Store

## 1. Scope and Context

### [SC-001]
The project is a web store for people who are new to online commerce and need a simple way to set up and operate an online retail business.

### [SC-002]
The system is intended to help small businesses and first-time sellers get online quickly without needing a lot of technical knowledge.

## 2. Actors

### [SA-001]
Store owners shall be able to manage products and customer accounts.

### [SA-002]
Sales staff shall be able to handle products and customer records.

### [SA-003]
Customers shall be able to browse products, maintain a cart, and place orders.

## 3. Functional Requirements

### [FR-001]
The system shall support browsing available products.

### [FR-002]
The system shall support maintaining a shopping cart.

### [FR-003]
The system shall support placing orders online.

### [FR-004]
Store owners shall be able to add or update products.

### [FR-005]
Store owners shall be able to check customer accounts.

### [FR-006]
Store owners shall be able to review incoming orders.

### [FR-007]
Sales staff shall be able to update product availability.

### [FR-008]
Sales staff shall be able to enter or correct orders.

### [FR-009]
The system shall provide a guided setup flow for new sellers.

### [FR-010]
The setup flow shall start with basic store information.

### [FR-011]
The setup flow shall help users add categories, products, and customer account settings.

### [FR-012]
The system shall provide clear examples and simple prompts during setup.

### [FR-013]
The system shall flag incomplete entries right away during setup.

### [FR-014]
The system shall explain setup mistakes in plain language so users can correct them before they start selling.

### [FR-015]
The system shall support a change log for edits to orders and products.

### [FR-016]
The system shall provide notifications for important updates such as stock changes, cancelled orders, and customer account edits.

### [FR-017]
The system shall provide brief tips and plain-language summaries to help users learn logs and notifications.

### [FR-018]
The system shall provide a short onboarding walkthrough that shows users where to find recent changes and what notifications mean.

### [FR-019]
The system shall support payment processing through at least one mainstream payment gateway in the initial release.

### [FR-020]
The system shall support basic shipping carrier integration in the initial release.

### [FR-021]
The system shall allow staff to see when an order payment is still unpaid after a payment failure.

### [FR-022]
The system shall allow customers to retry payment or use a different payment method after a payment failure.

### [FR-023]
The system shall alert store staff when shipping updates are delayed or fail.

### [FR-024]
The system shall provide a manual override or retry option for staff for payment or shipping issues.

### [FR-025]
The system shall record who used a manual override or retry option and why it was used.

### [FR-026]
The system shall provide in-app alerts for payment and shipping errors.

### [FR-027]
The system shall provide email notifications for serious issues or issues that remain unresolved too long.

### [FR-028]
The system shall provide a dashboard indicator for unresolved issues.

### [FR-029]
The system shall prioritize payment failures ahead of shipping issues.

### [FR-030]
The system shall support basic validation before an order is submitted.

### [FR-031]
The order submission validation shall check required address fields and obvious payment format issues.

### [FR-032]
The order submission validation shall check required customer, shipping, and payment information before the order is submitted.

### [FR-033]
The system shall display order validation feedback before submission or immediately after form completion.

### [FR-034]
The system shall keep the customer on the checkout page or same screen when correcting order validation issues.

### [FR-035]
The system shall support spreadsheet import for product data.

### [FR-036]
The system shall support CSV import for product data.

### [FR-037]
The system shall support product file upload, field mapping, preview, and validation before imported data is committed.

### [FR-038]
The system shall allow users to correct import issues without restarting the whole import.

### [FR-039]
The system shall show a clear result or success summary after import that identifies what succeeded, what was skipped, and what needs attention.

### [FR-040]
The import process shall let users fix problem fields inline within the review screen.

### [FR-041]
The import process shall compare potential duplicates and allow the user to keep, merge, or skip matching records.

### [FR-042]
The import process shall provide a review screen before finalizing import so users can resolve missing or inconsistent data.

### [FR-043]
The import wizard shall guide users through small steps with a clear progress indicator.

### [FR-044]
The import wizard shall show a live preview after column mapping.

### [FR-045]
The import wizard shall highlight rows or fields with issues and explain them in plain language.

### [FR-046]
The import wizard shall provide buttons or actions to fix, ignore, or apply a suggested correction for issues.

### [FR-047]
The import wizard shall show how many items are ready versus how many need attention.

### [FR-048]
The import wizard shall allow users to go back to a previous step if something looks wrong.

### [FR-049]
The system shall support optional suggestions during product import for categories, units of measure, brand, and cleaner product titles.

### [FR-050]
The system shall allow users to accept, edit, or reject import suggestions.

### [FR-051]
The system shall suggest likely categories from a product name or description when it can infer them confidently.

### [FR-052]
The system shall prompt for missing product details such as a short description or image when those details would improve the storefront.

### [FR-053]
The system shall auto-detect units and normalize spelling for common terms as optional import helpers.

### [FR-054]
The system shall not make silent automatic changes during import suggestions; suggestions shall be presented for user review.

### [FR-055]
The system shall provide clear step indicators, plain messages, and a simple count of items ready versus items needing review during import.

### [FR-056]
The system shall support product category assignment during import and normal product management.

### [FR-057]
The system shall support products that have variations distinct from categories.

### [FR-058]
The system shall provide a simple browser-based web interface.

### [FR-059]
The system shall be usable in a standard browser without requiring special software to be installed.

### [FR-060]
The interface shall stay simple and the setup process shall be guided for users with limited technical experience.

### [FR-061]
The system shall support customer order confirmation and refund or cancellation notices automatically.

### [FR-062]
The system shall provide clear pricing information to support consumer-facing compliance.

### [FR-063]
The system shall collect only customer data needed for the order and customer account.

### [FR-064]
The system shall provide clear consent and privacy notices during signup and checkout.

### [FR-065]
The system shall support keeping logs of edits to customer records, prices, orders, and payments.

### [FR-066]
The system shall support product availability updates after a sale or restock, and allow urgent marking of an item as unavailable.

### [FR-067]
The system shall support browsing, cart updates, and order entry that remain responsive during normal growth and seasonal spikes.

### [FR-068]
The system shall allow page loads, browsing, cart checkout, staff order processing, and product updates to remain responsive during higher activity.

### [FR-069]
The platform shall allow new stores to be added without each store affecting the others.

### [FR-070]
The system shall save changes reliably and not drop orders or updates when activity increases.

### [FR-071]
The system shall allow the store to manage stock inside GAMMA-J if a full inventory system integration is not in place.

## 4. Business Rules and Constraints

### [BR-001]
Account means a customer profile with contact and order details, not a paid subscription.

### [BR-002]
Categories are used to organize products for navigation and management, and are not the same as product variations.

### [BR-003]
The initial release shall be limited to one payment gateway and one shipping carrier integration.

### [BR-004]
The initial release shall not require a full inventory system integration if the store can manage stock inside GAMMA-J.

### [BR-005]
Payment failures shall be treated as the highest-priority issues.

### [BR-006]
Shipping issues such as missed dispatches or bad addresses shall be prioritized ahead of minor shipping delays.

### [BR-007]
Manual override actions shall require the staff member’s identity and a reason before the change is saved.

### [BR-008]
The system shall show who changed an order or product and when the change happened.

### [BR-009]
The system shall allow product import to detect duplicates by comparing product name, SKU, or barcode when available.

### [BR-010]
The system shall highlight missing prices, inconsistent product names, wrong categories, and unclear stock quantities during product data cleanup.

### [BR-011]
The system shall require customer, shipping, and payment information checks before an order is submitted.

### [BR-012]
The system shall allow customer data collection to be limited to what is needed for the order and account.

## 5. Data and External Interfaces

### [DI-001]
The initial release shall support a spreadsheet import interface for product data.

### [DI-002]
The initial release shall support at least one mainstream payment gateway.

### [DI-003]
The initial release shall support basic shipping carrier integration.

### [DI-004]
The system shall use a standard browser as its runtime interface.

## 6. Quality Requirements

### [QR-001]
The system shall present a simple interface for users with limited technical experience.

### [QR-002]
The system shall use plain-language explanations, brief tips, and short help text for operations and technical concepts.

### [QR-003]
The setup process shall be guided and step by step.

### [QR-004]
The import wizard shall present one decision at a time and avoid overwhelming the user.

### [QR-005]
The import wizard shall use calm, practical, and reassuring messages.

### [QR-006]
The interface shall use color sparingly and rely more on labels, icons, and inline messages than on alarms or popups.

### [QR-007]
The system shall keep browsing, cart checkout, order processing, and product updates responsive during normal growth and seasonal spikes.

### [QR-008]
The system shall save changes reliably.

### [QR-009]
The system shall not drop orders or updates when activity increases.

### [QR-010]
The import wizard shall show a progress bar or progress indicator and a current step label.

### [QR-011]
The import wizard shall provide a clear, predictable layout with consistent button positions and terminology.

### [QR-012]
The system shall make automation optional during import suggestions and let users override suggestions.

### [QR-013]
The system shall keep the import process manageable by showing small steps, progress feedback, and clear counts of items needing attention.

## 7. Exceptions and Boundary Conditions

### [EX-001]
If a payment fails, the customer shall see a clear message and the order shall remain unpaid for staff visibility.

### [EX-002]
If shipping updates are delayed or fail, staff shall receive an alert and the customer shall see a simple status update.

### [EX-003]
If a manual override is used, the system shall record the staff member, the reason, the original error, the action taken, and the time.

### [EX-004]
If an import problem blocks completion, the issue shall be shown next to the affected row or field with a simple explanation and suggested fix.

### [EX-005]
If order validation fails, the customer shall remain on the checkout page and be told exactly what to correct.

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
The exact payment gateway vendor for the initial release has not yet been decided.

### [UN-002]
The exact shipping carrier vendor for the initial release has not yet been decided.

### [UN-003]
The exact integrations and technical constraints beyond the initial payment and shipping support have not yet been confirmed with the team.

### [UN-004]
The exact legal jurisdictions and resulting compliance specifics for consumer-facing rules have not yet been verified.
