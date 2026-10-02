# Software Requirements Specification: GAMMA-J Web Store

## 1. Scope and Context

### [SC-001]
The system shall provide a web store for people who are new to online commerce so they can set up and operate an online retail business.

### [SC-002]
The first release shall focus on a basic small-shop workflow with core retail operations only, excluding specialized product types, complicated order flows, subscriptions, marketplace selling, complex promotions, multi-warehouse inventory, and deep accounting or ERP integrations.

## 2. Actors

### [ACT-001]
Store owners shall be able to handle overall setup, product management, customer oversight, and business settings.

### [ACT-002]
Sales personnel shall be able to maintain products, help with customer accounts, review orders, and perform routine store updates.

### [ACT-003]
Customers shall be able to browse products, manage their shopping cart, and place orders.

### [ACT-004]
Customers shall be separated from administrative work and shall not access back-office functions.

## 3. Functional Requirements

### [FR-001]
The system shall allow store operators to set up a storefront.

### [FR-002]
The system shall allow users to manage products.

### [FR-003]
The system shall support standard retail products with names, descriptions, prices, and available quantities.

### [FR-004]
The system shall allow staff to add products and update products.

### [FR-005]
The system shall allow staff to manage customer accounts.

### [FR-006]
The system shall allow customers to browse products through clear categories and simple filtering.

### [FR-007]
The system shall allow customers to maintain a shopping cart.

### [FR-008]
The system shall allow customers to place orders through the store.

### [FR-009]
The system shall support product catalog onboarding by manual entry or file import when file import is supported.

### [FR-010]
The system shall allow an initial product catalog to be loaded before the site goes live.

### [FR-011]
The system shall allow staff to review loaded product listings for correctness, images, pricing, and availability before marking the catalog ready for customers.

### [FR-012]
The system shall allow staff to mark the catalog ready for customers after review.

### [FR-013]
The system shall allow customers to browse products by categories or search and narrow results using price or other filters.

### [FR-014]
The system shall support secure logins and password reset for account protection.

### [FR-015]
The system shall flag obviously suspicious activity rather than attempting to handle every edge case automatically.

### [FR-016]
The system shall rely on a trusted payment provider and shall not store sensitive card details itself.

### [FR-017]
The system shall minimize the personal data collected to what is needed to fulfill orders.

### [FR-018]
The system shall block or review transactions that look risky.

### [FR-019]
The system shall record administrative changes in an audit log.

### [FR-020]
The audit log shall record who made the change, what changed, when it happened, and the before-and-after values for important fields.

### [FR-021]
The system shall record before-and-after values for important fields such as product price, stock, order status, and customer account status.

### [FR-022]
The system shall remain responsive under increased browsing demand and shall slow down gracefully or queue non-urgent actions rather than fail outright when demand suddenly rises.

### [FR-023]
The system shall preserve cart and order progress when part of the service is unavailable.

### [FR-024]
The system shall clearly tell users what is affected when part of the service is unavailable.

### [FR-025]
The system shall keep important sales functions available as much as possible even if some admin features are temporarily reduced.

### [FR-026]
The system shall allow product images to be uploaded with one main image and a small number of additional images.

### [FR-027]
The system shall allow common image formats such as JPG and PNG.

### [FR-028]
If an image upload fails or the file is invalid, the system shall reject the upload clearly and allow the user to try again without saving a broken product record.

### [FR-029]
If a product image is missing, the product shall still exist and shall show a default placeholder.

### [FR-030]
A product shall be purchasable only when it is marked active and available for sale.

### [FR-031]
When stock control is being used, a product shall be purchasable only when it has valid stock.

### [FR-032]
When a product price changes, the updated price shall apply to new carts and new orders but shall not unexpectedly change an order that has already been placed.

### [FR-033]
If a product is out of stock or not yet available, the system shall show it as unavailable and shall prevent checkout for it.

### [FR-034]
The system shall support minimum and maximum quantities per product.

### [FR-035]
The system shall support a maximum total quantity or value per order if the business needs it.

### [FR-036]
If a cart exceeds quantity or value limits, the system shall flag the issue before checkout and tell the customer exactly what must be adjusted.

### [FR-037]
The system shall support import of the initial product catalog from an existing file if file import is supported.

### [FR-038]
The system shall report records that do not map cleanly during migration for manual review instead of guessing automatically.

### [FR-039]
If a legacy product record is incomplete, the system shall skip it or mark it as needing attention until it is corrected.

### [FR-040]
The system shall allow manual review of legacy product records by a store admin or designated catalog owner.

### [FR-041]
The system shall track manual review records as pending or in review and include notes about what is missing or inconsistent.

### [FR-042]
A record under manual review shall remain hidden from customers and shall not be publishable until the required fields are fixed and someone approves it.

### [FR-043]
The system shall support browsing through categories or search and shall guide broad searches toward the right items with clear descriptions and helpful filtering.

### [FR-044]
The system shall process customer requests to suspend or delete accounts.

### [FR-045]
Customer account suspension shall be immediate in most cases.

### [FR-046]
Customer account deletion shall be delayed when there are active orders, payment issues, legal recordkeeping needs, return cases, refund cases, unresolved support cases, or necessary order history for customer service or accounting.

### [FR-047]
If a customer account deletion request cannot be handled automatically because of an exception, an admin shall handle the exception.

### [FR-048]
If a customer account request is not straightforward or cannot be confidently determined as safe, the system shall route it to an admin review queue before suspension or deletion proceeds.

### [FR-049]
The system shall keep a customer record in review until required fields are complete and inconsistent data is corrected.

### [FR-050]
The system shall keep a customer record hidden from the customer if the incomplete record could cause problems with orders, shipping, or account access.

### [FR-051]
A customer record shall go live only after the data matches requirements and an admin or authorized staff member approves it.

### [FR-052]
If a shopper exceeds a customer-specific limit, the cart shall clearly flag the issue and stop checkout until the quantity is reduced or the item is removed.

### [FR-053]
After checkout, the system shall show the customer the order number, purchased items, quantities, totals, taxes or fees if applicable, shipping details, and payment status.

### [FR-054]
The order confirmation shall be sent by email.

### [FR-055]
The system shall allow products to remain visible but not purchasable when the price is missing, invalid, or inventory is unavailable under stock control.

### [FR-056]
When a product is not purchasable, the system shall block add-to-cart and checkout actions and shall show a clear message explaining why.

### [FR-057]
The system shall validate shipping addresses enough to catch obvious missing or invalid address components.

### [FR-058]
Delivery options shall depend on the customer's location.

### [FR-059]
If no delivery method is available for a shipping address, checkout shall stop and the customer shall be told to change the address or contact support.

### [FR-060]
The payment step shall allow the customer to choose a payment method and confirm the amount before payment is finalized.

### [FR-061]
After payment submission, the system shall show a clear success or failure message right away.

### [FR-062]
If payment fails, the system shall explain what the customer can do next without forcing them to start over unnecessarily.

### [FR-063]
If payment is successful, the order shall move to confirmation immediately and the customer shall know the purchase is complete.

### [FR-064]
The system shall allow the customer to try payment again, choose a different payment method, or go back and review the order when payment does not go through.

### [FR-065]
If only part of a payment completed, the system shall keep the order from confirming until the full amount is resolved.

### [FR-066]
An order shall start as pending while payment and availability are checked.

### [FR-067]
If payment is fully accepted, the order is no longer under review, and items are confirmed available to ship, the order may move into fulfillment.

### [FR-068]
If any item is out of stock, payment is unresolved, or a staff review is still open, the order shall wait and shall not go to picking and packing.

### [FR-069]
The system shall support manual review of orders that have suspicious payment activity, mismatched customer and shipping details, unusual order size, or policy exceptions.

### [FR-070]
If an order is approved after manual review, the customer shall be told the order is confirmed and moving ahead.

### [FR-071]
If an order stays on hold after manual review, the customer shall be told it is still under review and no action may be needed yet.

### [FR-072]
If an order is rejected after manual review, the customer shall be told the order cannot be completed and, if appropriate, whether to try again or contact support.

### [FR-073]
If staff cannot quickly verify a manual review issue, the order shall remain on hold first.

### [FR-074]
If missing information in manual review must come from the customer, the system shall send the order back for customer action with clear instructions.

### [FR-075]
If a manual review issue is internal and still needs investigation, the order shall stay on hold until staff can approve or reject it.

### [FR-076]
The web interface shall allow only order status changes that match the real order state.

### [FR-077]
The web interface shall block invalid order status transitions and explain why in plain language.

### [FR-078]
An unpaid order shall not be moved into fulfillment.

### [FR-079]
A canceled order shall not be moved back into normal processing unless a deliberate reopen action is used.

### [FR-080]
The system shall support configuring frequent and low-risk changes through configuration or business settings.

### [FR-081]
The system shall require code changes and new releases for changes affecting the core checkout flow, security, or major new capabilities.

### [FR-082]
The system shall allow imports through the web interface using common files such as CSV or Excel.

### [FR-083]
Every imported row shall be validated before it goes live.

### [FR-084]
If an imported row conflicts with existing product data, the system shall stop that row or flag it for review rather than silently overwriting it.

### [FR-085]
For future automatic syncing, the system shall prevent unexpected changes from going live without validation and shall provide clear mismatch reporting.

### [FR-086]
If an import fails partway through, the system shall either import only the clean rows with a clear report of the failures or stop the whole import and leave everything unchanged for critical data sets.

### [FR-087]
The system shall support basic order status changes through the web interface for new store operators.

### [FR-088]
The system shall allow customers to view the current status of an order that is already being prepared for delivery.

### [FR-089]
The system shall prompt customers to remove or update cart items that are no longer available before checkout.

## 4. Business Rules and Constraints

### [BR-001]
A product shall be visible but not purchasable when its price is missing, invalid, or inventory is unavailable under stock control.

### [BR-002]
If stock control is being used, valid stock is required for purchase.

### [BR-003]
If a product is out of stock or not yet available, checkout shall be prevented for that product.

### [BR-004]
If a product is shown as unavailable, add-to-cart and checkout actions shall be blocked.

### [BR-005]
The system shall not store full payment card details itself.

### [BR-006]
Sensitive customer data shall be accessible only to authorized staff with a need to know.

### [BR-007]
Sales staff may see normal contact and order details, but only support or admins may see sensitive notes, refund references, or fraud-related flags, and only when assigned to the case.

### [BR-008]
The system shall keep only the minimum contact and shipping information needed for the order.

### [BR-009]
Sensitive data shall be handled with tighter access than normal store data.

### [BR-010]
A customer account deletion request shall not proceed immediately when active orders, payment issues, legal recordkeeping, return cases, refund cases, unresolved support cases, or required order history exist.

### [BR-011]
A customer account request may require admin approval when it involves unresolved disputes, a suspicious activity flag, or a conflict with an open order or refund.

### [BR-012]
A customer account request shall be routed to admin review when the system cannot confidently determine whether it is safe to proceed.

### [BR-013]
A product shall only be purchasable when it is marked active and available for sale.

### [BR-014]
A price change shall apply to new carts and new orders only, not to an order already placed.

### [BR-015]
If a cart exceeds quantity or value limits, checkout shall not proceed until the customer adjusts the cart.

### [BR-016]
If a shipping address is technically valid but conflicts with a shipping method or carrier rule, the system shall warn the customer and allow them to choose a different option or address.

### [BR-017]
The system shall validate shipping addresses enough to catch obvious problems such as missing street, city, postal code, or country.

### [BR-018]
The system shall not expose internal fraud or security details in customer-facing manual review messages.

### [BR-019]
Administrative actions, sensitive access, and record views should be logged when practical to show who viewed what and why.

### [BR-020]
A product record shall not be saved with a broken image upload.

## 5. Data and External Interfaces

### [DI-001]
The system shall use a trusted payment provider for payment processing.

### [DI-002]
The system shall support sending order confirmation by email.

### [DI-003]
The system shall support importing product data from common files such as CSV or Excel through the web interface.

### [DI-004]
The system shall support product data migration from an existing legacy system when such data exists.

## 6. Quality Requirements

### [QR-001]
The system shall be simple enough for new store owners to operate without much technical knowledge.

### [QR-002]
The system shall run reliably for core store operations.

### [QR-003]
The system shall remain responsive when more people are browsing at once.

### [QR-004]
If demand suddenly rises, the system shall slow down gracefully or queue non-urgent actions rather than failing outright.

### [QR-005]
The system shall provide clear validation and feedback for import and data review activities.

### [QR-006]
The system shall provide clear error messages in plain language for invalid status transitions and blocked purchases.

### [QR-007]
The system shall support the major current browsers Chrome, Safari, Edge, and Firefox.

### [QR-008]
The system shall work on desktop, mobile devices, phones, and tablets.

### [QR-009]
The system shall keep important sales functions available as much as possible during partial service unavailability.

### [QR-010]
The system shall provide a clear success or failure message immediately after payment submission.

### [QR-011]
The system shall provide enough detail in payment failure messages for the customer to understand whether the issue was a card issue, a declined transaction, or a system issue.

### [QR-012]
The system shall provide customer-facing confirmation information immediately after checkout.

### [QR-013]
The system shall use clear messaging for unavailable products and cart or checkout blocks.

### [QR-014]
The system shall keep the live catalog undisturbed by onboarding changes and shall support safe rollback if an import goes wrong.

### [QR-015]
The system shall apply new onboarding rules consistently to new loads without breaking existing products already in the system.

### [QR-016]
The system shall allow a new store operator to perform basic administrative tasks from the web interface without technical setup.

## 7. Exceptions and Boundary Conditions

### [EX-001]
If payment fails or is only partially completed, the order shall not confirm.

### [EX-002]
If a product image upload fails or is invalid, the product shall not be saved with a broken image record.

### [EX-003]
If no delivery method is available for a shipping address, checkout shall stop.

### [EX-004]
If a cart exceeds limits, the customer shall be blocked from checkout until the cart is corrected.

### [EX-005]
If a manual review cannot be quickly verified, the order shall remain on hold until staff can decide or customer action is completed.

### [EX-006]
If an order is invalidly transitioned to fulfillment, the system shall block the transition.

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
Whether the first release must support customer-specific limits is unresolved.

### [UN-002]
Whether the first release must support another payment channel beyond email confirmation is unresolved.

### [UN-003]
Whether the first release should capture payment at order confirmation instead of after fulfillment or shipment is unresolved.

### [UN-004]
Whether the first release should support older browser versions is unresolved.

### [UN-005]
Whether the first release should include file import support is unresolved.

### [UN-006]
The exact import methods, bulk update behavior, and sync rules for future onboarding enhancements are unresolved.

### [UN-007]
Whether the system needs customer-specific limits is unresolved.
