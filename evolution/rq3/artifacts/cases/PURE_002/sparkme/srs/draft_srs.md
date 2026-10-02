# Software Requirements Specification: GAMMA-J Web Store

## 1. Scope and Context

### [SC-001] (stated)
The project is a web store for people who are new to online commerce and need a simple way to set up and operate an online retail business.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business. Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
- `[interview_turn:T002]` "The main goal is to give people who are new to online selling a simple way to start and run a web store without needing a lot of technical knowledge. We want store owners and sales staff to be able to handle products and customer records easily, while customers can browse items, keep a cart, and place orders online. The problem we’re trying to solve is that setting up and operating a small online retail business is usually too complicated and fragmented for beginners."

### [SC-002] (stated)
The system is intended to help small businesses and first-time sellers get online quickly without needing a lot of technical knowledge.

**Source Evidence:**
- `[interview_turn:T002]` "The main goal is to give people who are new to online selling a simple way to start and run a web store without needing a lot of technical knowledge. We want store owners and sales staff to be able to handle products and customer records easily, while customers can browse items, keep a cart, and place orders online. The problem we’re trying to solve is that setting up and operating a small online retail business is usually too complicated and fragmented for beginners."
- `[interview_turn:T004]` "We’re mainly seeing demand from small businesses and first-time sellers who want to get online quickly without buying a lot of separate tools or hiring specialists. A lot of them need something that is straightforward, affordable, and easy to learn because they’re coming from physical retail or very small operations. The general trend pushing this is that more customers expect to shop online, so these businesses need a simple way to compete and reach them."

## 2. Actors

### [SA-001] (stated)
Store owners shall be able to manage products and customer accounts.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business. Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
- `[interview_turn:T002]` "The main goal is to give people who are new to online selling a simple way to start and run a web store without needing a lot of technical knowledge. We want store owners and sales staff to be able to handle products and customer records easily, while customers can browse items, keep a cart, and place orders online. The problem we’re trying to solve is that setting up and operating a small online retail business is usually too complicated and fragmented for beginners."
- `[interview_turn:T020]` "A store owner would usually start by adding or updating products, checking customer accounts, and reviewing incoming orders. Sales staff would spend more time helping customers, updating product availability, and making sure orders are entered or corrected properly. Customers would browse products, add items to the cart, and place orders, so the system needs to support those flows smoothly throughout the day."

### [SA-002] (stated)
Sales staff shall be able to handle products and customer records.

**Source Evidence:**
- `[interview_turn:T002]` "The main goal is to give people who are new to online selling a simple way to start and run a web store without needing a lot of technical knowledge. We want store owners and sales staff to be able to handle products and customer records easily, while customers can browse items, keep a cart, and place orders online. The problem we’re trying to solve is that setting up and operating a small online retail business is usually too complicated and fragmented for beginners."

### [SA-003] (stated)
Customers shall be able to browse products, maintain a cart, and place orders.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business. Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
- `[interview_turn:T002]` "The main goal is to give people who are new to online selling a simple way to start and run a web store without needing a lot of technical knowledge. We want store owners and sales staff to be able to handle products and customer records easily, while customers can browse items, keep a cart, and place orders online. The problem we’re trying to solve is that setting up and operating a small online retail business is usually too complicated and fragmented for beginners."
- `[interview_turn:T020]` "A store owner would usually start by adding or updating products, checking customer accounts, and reviewing incoming orders. Sales staff would spend more time helping customers, updating product availability, and making sure orders are entered or corrected properly. Customers would browse products, add items to the cart, and place orders, so the system needs to support those flows smoothly throughout the day."

## 3. Functional Requirements

### [FR-001] (stated)
The system shall support browsing available products.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business. Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
- `[interview_turn:T020]` "A store owner would usually start by adding or updating products, checking customer accounts, and reviewing incoming orders. Sales staff would spend more time helping customers, updating product availability, and making sure orders are entered or corrected properly. Customers would browse products, add items to the cart, and place orders, so the system needs to support those flows smoothly throughout the day."

### [FR-002] (stated)
The system shall support maintaining a shopping cart.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business. Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
- `[interview_turn:T020]` "A store owner would usually start by adding or updating products, checking customer accounts, and reviewing incoming orders. Sales staff would spend more time helping customers, updating product availability, and making sure orders are entered or corrected properly. Customers would browse products, add items to the cart, and place orders, so the system needs to support those flows smoothly throughout the day."

### [FR-003] (stated)
The system shall support placing orders online.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business. Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
- `[interview_turn:T020]` "A store owner would usually start by adding or updating products, checking customer accounts, and reviewing incoming orders. Sales staff would spend more time helping customers, updating product availability, and making sure orders are entered or corrected properly. Customers would browse products, add items to the cart, and place orders, so the system needs to support those flows smoothly throughout the day."

### [FR-004] (stated)
Store owners shall be able to add or update products.

**Source Evidence:**
- `[interview_turn:T020]` "A store owner would usually start by adding or updating products, checking customer accounts, and reviewing incoming orders. Sales staff would spend more time helping customers, updating product availability, and making sure orders are entered or corrected properly. Customers would browse products, add items to the cart, and place orders, so the system needs to support those flows smoothly throughout the day."

### [FR-005] (stated)
Store owners shall be able to check customer accounts.

**Source Evidence:**
- `[interview_turn:T020]` "A store owner would usually start by adding or updating products, checking customer accounts, and reviewing incoming orders. Sales staff would spend more time helping customers, updating product availability, and making sure orders are entered or corrected properly. Customers would browse products, add items to the cart, and place orders, so the system needs to support those flows smoothly throughout the day."

### [FR-006] (stated)
Store owners shall be able to review incoming orders.

**Source Evidence:**
- `[interview_turn:T020]` "A store owner would usually start by adding or updating products, checking customer accounts, and reviewing incoming orders. Sales staff would spend more time helping customers, updating product availability, and making sure orders are entered or corrected properly. Customers would browse products, add items to the cart, and place orders, so the system needs to support those flows smoothly throughout the day."

### [FR-007] (stated)
Sales staff shall be able to update product availability.

**Source Evidence:**
- `[interview_turn:T020]` "A store owner would usually start by adding or updating products, checking customer accounts, and reviewing incoming orders. Sales staff would spend more time helping customers, updating product availability, and making sure orders are entered or corrected properly. Customers would browse products, add items to the cart, and place orders, so the system needs to support those flows smoothly throughout the day."
- `[interview_turn:T034]` "Sales staff usually handle exceptions by checking the order details, confirming with the owner or warehouse person, and then editing the record manually if they’re allowed to. For product availability, they often update stock after a sale or after a restock comes in, but if the change is urgent they may also need to mark an item unavailable right away to avoid more orders. GAMMA-J should make those edits fast and traceable, because the main pain point is making sure everyone sees the updated status without creating more mistakes."

### [FR-008] (stated)
Sales staff shall be able to enter or correct orders.

**Source Evidence:**
- `[interview_turn:T020]` "A store owner would usually start by adding or updating products, checking customer accounts, and reviewing incoming orders. Sales staff would spend more time helping customers, updating product availability, and making sure orders are entered or corrected properly. Customers would browse products, add items to the cart, and place orders, so the system needs to support those flows smoothly throughout the day."

### [FR-009] (stated)
The system shall provide a guided setup flow for new sellers.

**Source Evidence:**
- `[interview_turn:T014]` "The biggest pain point is usually getting the catalog set up correctly, because new sellers often have a lot of products but aren’t sure how to organize them or enter them consistently. Another bottleneck is managing customer information and order handling once sales start coming in, since that can quickly become overwhelming for beginners. They also tend to get stuck when they have to figure things out without much guidance, so a guided flow would help a lot."
- `[interview_turn:T032]` "An ideal setup flow would guide them step by step instead of letting them face a blank system all at once. It would probably start with basic store information, then help them add categories, products, and customer account settings with clear examples and simple prompts for things like pricing, stock, and variants. It would also be helpful if the system flagged incomplete entries right away and explained mistakes in plain language so they can correct them before they start selling."

### [FR-010] (stated)
The setup flow shall start with basic store information.

**Source Evidence:**
- `[interview_turn:T032]` "An ideal setup flow would guide them step by step instead of letting them face a blank system all at once. It would probably start with basic store information, then help them add categories, products, and customer account settings with clear examples and simple prompts for things like pricing, stock, and variants. It would also be helpful if the system flagged incomplete entries right away and explained mistakes in plain language so they can correct them before they start selling."

### [FR-011] (stated)
The setup flow shall help users add categories, products, and customer account settings.

**Source Evidence:**
- `[interview_turn:T032]` "An ideal setup flow would guide them step by step instead of letting them face a blank system all at once. It would probably start with basic store information, then help them add categories, products, and customer account settings with clear examples and simple prompts for things like pricing, stock, and variants. It would also be helpful if the system flagged incomplete entries right away and explained mistakes in plain language so they can correct them before they start selling."

### [FR-012] (stated)
The system shall provide clear examples and simple prompts during setup.

**Source Evidence:**
- `[interview_turn:T032]` "An ideal setup flow would guide them step by step instead of letting them face a blank system all at once. It would probably start with basic store information, then help them add categories, products, and customer account settings with clear examples and simple prompts for things like pricing, stock, and variants. It would also be helpful if the system flagged incomplete entries right away and explained mistakes in plain language so they can correct them before they start selling."

### [FR-013] (stated)
The system shall flag incomplete entries right away during setup.

**Source Evidence:**
- `[interview_turn:T032]` "An ideal setup flow would guide them step by step instead of letting them face a blank system all at once. It would probably start with basic store information, then help them add categories, products, and customer account settings with clear examples and simple prompts for things like pricing, stock, and variants. It would also be helpful if the system flagged incomplete entries right away and explained mistakes in plain language so they can correct them before they start selling."

### [FR-014] (stated)
The system shall explain setup mistakes in plain language so users can correct them before they start selling.

**Source Evidence:**
- `[interview_turn:T032]` "An ideal setup flow would guide them step by step instead of letting them face a blank system all at once. It would probably start with basic store information, then help them add categories, products, and customer account settings with clear examples and simple prompts for things like pricing, stock, and variants. It would also be helpful if the system flagged incomplete entries right away and explained mistakes in plain language so they can correct them before they start selling."

### [FR-015] (stated)
The system shall support a change log for edits to orders and products.

**Source Evidence:**
- `[interview_turn:T036]` "Yes, a change log would be very useful so staff can see who changed an order or product and when it happened. Notifications would also help, especially for important updates like stock changes, cancelled orders, or customer account edits, so other staff know right away. I’d expect the system to keep the history visible in a simple way, since new users may not be comfortable digging through technical audit screens."
- `[interview_turn:T052]` "In practice, staff should see the error on the order or shipment screen, along with a plain-language explanation and a suggested next step like retry, contact the customer, or correct the details. If they choose a manual override, the system should require a reason and the staff member’s identity before saving the change, so there’s a clear history. An audit trail showing the original error, the action taken, the time, and who handled it would be the most helpful for tracking and later review."
- `[interview_turn:T064]` "I’d want customer data collection to be limited to what’s actually needed for the order and account, with clear consent and privacy notices shown during signup and checkout. Users should also get order confirmations and any refund or cancellation notices automatically, because that helps both compliance and customer trust. For staff, the system should keep good logs of edits to customer records, prices, orders, and payments so we can trace changes if there’s ever a complaint or audit."

### [FR-016] (stated)
The system shall provide notifications for important updates such as stock changes, cancelled orders, and customer account edits.

**Source Evidence:**
- `[interview_turn:T036]` "Yes, a change log would be very useful so staff can see who changed an order or product and when it happened. Notifications would also help, especially for important updates like stock changes, cancelled orders, or customer account edits, so other staff know right away. I’d expect the system to keep the history visible in a simple way, since new users may not be comfortable digging through technical audit screens."
- `[interview_turn:T040]` "They’d probably want the tips most during the first few uses, then only occasionally after that so it doesn’t get annoying. Notifications should appear when something important changes, like an order correction, stock adjustment, or customer account update, because that’s when people need to stay in sync. I’d make the help more prominent for new store owners and sales staff, while experienced users should be able to keep it lighter or turn some of it off."

### [FR-017] (stated)
The system shall provide brief tips and plain-language summaries to help users learn logs and notifications.

**Source Evidence:**
- `[interview_turn:T038]` "I think brief tips and plain-language summaries would be the most helpful, especially at first. A short walkthrough during onboarding could show them where to find recent changes and what the notifications mean, without sending them into a full training course. After that, small contextual help inside the screens would probably be enough for most people."
- `[interview_turn:T040]` "They’d probably want the tips most during the first few uses, then only occasionally after that so it doesn’t get annoying. Notifications should appear when something important changes, like an order correction, stock adjustment, or customer account update, because that’s when people need to stay in sync. I’d make the help more prominent for new store owners and sales staff, while experienced users should be able to keep it lighter or turn some of it off."

### [FR-018] (stated)
The system shall provide a short onboarding walkthrough that shows users where to find recent changes and what notifications mean.

**Source Evidence:**
- `[interview_turn:T038]` "I think brief tips and plain-language summaries would be the most helpful, especially at first. A short walkthrough during onboarding could show them where to find recent changes and what the notifications mean, without sending them into a full training course. After that, small contextual help inside the screens would probably be enough for most people."

### [FR-019] (conditional)
The system shall support payment processing through at least one mainstream payment gateway in the initial release.

**Source Evidence:**
- `[interview_turn:T042]` "I know payment processing will be important, because customers need a smooth checkout experience, but I’m not sure yet which gateway we’ll standardize on. Shipping support would also be useful so orders can move from placed to fulfilled without a lot of manual re-entry, and that would save staff time. If we connect to inventory tools later, that would help keep stock numbers accurate, but I’d need to check with the team on which external systems are actually in scope for the first release."
- `[interview_turn:T046]` "For the initial release, I’d expect at least one mainstream payment gateway and basic shipping carrier support, but I can’t name the exact vendors yet without checking with the team. I don’t think we need a full inventory system integration on day one if the store can manage stock inside GAMMA-J, though that could come later. These integrations would mainly save owners and sales staff from retyping order and shipment details, and they’d make checkout and fulfillment feel more professional for customers."
- `[interview_turn:T050]` "For the first release, I’d keep it limited to one payment gateway, one shipping carrier integration, and the store’s own built-in product and stock management. I don’t have the exact vendor names locked down yet, so I’d need to confirm those with the business team before committing. The main value is that owners and sales staff can process orders, confirm payments, and generate shipping info without switching tools all the time, which should make day-to-day work much faster and less error-prone."

### [FR-020] (conditional)
The system shall support basic shipping carrier integration in the initial release.

**Source Evidence:**
- `[interview_turn:T042]` "I know payment processing will be important, because customers need a smooth checkout experience, but I’m not sure yet which gateway we’ll standardize on. Shipping support would also be useful so orders can move from placed to fulfilled without a lot of manual re-entry, and that would save staff time. If we connect to inventory tools later, that would help keep stock numbers accurate, but I’d need to check with the team on which external systems are actually in scope for the first release."
- `[interview_turn:T046]` "For the initial release, I’d expect at least one mainstream payment gateway and basic shipping carrier support, but I can’t name the exact vendors yet without checking with the team. I don’t think we need a full inventory system integration on day one if the store can manage stock inside GAMMA-J, though that could come later. These integrations would mainly save owners and sales staff from retyping order and shipment details, and they’d make checkout and fulfillment feel more professional for customers."
- `[interview_turn:T050]` "For the first release, I’d keep it limited to one payment gateway, one shipping carrier integration, and the store’s own built-in product and stock management. I don’t have the exact vendor names locked down yet, so I’d need to confirm those with the business team before committing. The main value is that owners and sales staff can process orders, confirm payments, and generate shipping info without switching tools all the time, which should make day-to-day work much faster and less error-prone."

### [FR-021] (stated)
The system shall allow staff to see when an order payment is still unpaid after a payment failure.

**Source Evidence:**
- `[interview_turn:T044]` "If a payment fails, the customer should get a clear message right away with a chance to try again or use a different method, and staff should be able to see that the order is still unpaid. For shipping delays or failed updates, I’d want the store staff to get an alert so they can follow up manually, while the customer sees a simple status update rather than silence. It would also help to have a manual override or retry option for staff, but only with a record of who used it and why."

### [FR-022] (stated)
The system shall allow customers to retry payment or use a different payment method after a payment failure.

**Source Evidence:**
- `[interview_turn:T044]` "If a payment fails, the customer should get a clear message right away with a chance to try again or use a different method, and staff should be able to see that the order is still unpaid. For shipping delays or failed updates, I’d want the store staff to get an alert so they can follow up manually, while the customer sees a simple status update rather than silence. It would also help to have a manual override or retry option for staff, but only with a record of who used it and why."

### [FR-023] (stated)
The system shall alert store staff when shipping updates are delayed or fail.

**Source Evidence:**
- `[interview_turn:T044]` "If a payment fails, the customer should get a clear message right away with a chance to try again or use a different method, and staff should be able to see that the order is still unpaid. For shipping delays or failed updates, I’d want the store staff to get an alert so they can follow up manually, while the customer sees a simple status update rather than silence. It would also help to have a manual override or retry option for staff, but only with a record of who used it and why."

### [FR-024] (stated)
The system shall provide a manual override or retry option for staff for payment or shipping issues.

**Source Evidence:**
- `[interview_turn:T044]` "If a payment fails, the customer should get a clear message right away with a chance to try again or use a different method, and staff should be able to see that the order is still unpaid. For shipping delays or failed updates, I’d want the store staff to get an alert so they can follow up manually, while the customer sees a simple status update rather than silence. It would also help to have a manual override or retry option for staff, but only with a record of who used it and why."
- `[interview_turn:T052]` "In practice, staff should see the error on the order or shipment screen, along with a plain-language explanation and a suggested next step like retry, contact the customer, or correct the details. If they choose a manual override, the system should require a reason and the staff member’s identity before saving the change, so there’s a clear history. An audit trail showing the original error, the action taken, the time, and who handled it would be the most helpful for tracking and later review."

### [FR-025] (stated)
The system shall record who used a manual override or retry option and why it was used.

**Source Evidence:**
- `[interview_turn:T044]` "If a payment fails, the customer should get a clear message right away with a chance to try again or use a different method, and staff should be able to see that the order is still unpaid. For shipping delays or failed updates, I’d want the store staff to get an alert so they can follow up manually, while the customer sees a simple status update rather than silence. It would also help to have a manual override or retry option for staff, but only with a record of who used it and why."
- `[interview_turn:T052]` "In practice, staff should see the error on the order or shipment screen, along with a plain-language explanation and a suggested next step like retry, contact the customer, or correct the details. If they choose a manual override, the system should require a reason and the staff member’s identity before saving the change, so there’s a clear history. An audit trail showing the original error, the action taken, the time, and who handled it would be the most helpful for tracking and later review."

### [FR-026] (stated)
The system shall provide in-app alerts for payment and shipping errors.

**Source Evidence:**
- `[interview_turn:T054]` "Yes, I’d want in-app alerts first, because staff will likely be working inside the store system most of the time. Email notifications could be useful for more serious issues or anything that sits unresolved for too long, and a dashboard indicator would help show what still needs attention at a glance. The system should definitely prioritize payment failures and anything blocking fulfillment ahead of minor shipping delays, so the urgent problems are the ones staff see first."
- `[interview_turn:T066]` "I’d want the system to treat payment failures as the highest priority, especially if an order can’t be completed or money might be in an uncertain state. Shipping issues would be next, with things like missed dispatches or bad addresses flagged sooner than minor delays. It should alert the right staff first in-app, then escalate to email or a manager if the issue stays open too long, so the team isn’t flooded but the urgent items still get attention quickly."

### [FR-027] (stated)
The system shall provide email notifications for serious issues or issues that remain unresolved too long.

**Source Evidence:**
- `[interview_turn:T054]` "Yes, I’d want in-app alerts first, because staff will likely be working inside the store system most of the time. Email notifications could be useful for more serious issues or anything that sits unresolved for too long, and a dashboard indicator would help show what still needs attention at a glance. The system should definitely prioritize payment failures and anything blocking fulfillment ahead of minor shipping delays, so the urgent problems are the ones staff see first."
- `[interview_turn:T066]` "I’d want the system to treat payment failures as the highest priority, especially if an order can’t be completed or money might be in an uncertain state. Shipping issues would be next, with things like missed dispatches or bad addresses flagged sooner than minor delays. It should alert the right staff first in-app, then escalate to email or a manager if the issue stays open too long, so the team isn’t flooded but the urgent items still get attention quickly."

### [FR-028] (stated)
The system shall provide a dashboard indicator for unresolved issues.

**Source Evidence:**
- `[interview_turn:T054]` "Yes, I’d want in-app alerts first, because staff will likely be working inside the store system most of the time. Email notifications could be useful for more serious issues or anything that sits unresolved for too long, and a dashboard indicator would help show what still needs attention at a glance. The system should definitely prioritize payment failures and anything blocking fulfillment ahead of minor shipping delays, so the urgent problems are the ones staff see first."

### [FR-029] (stated)
The system shall prioritize payment failures ahead of shipping issues.

**Source Evidence:**
- `[interview_turn:T054]` "Yes, I’d want in-app alerts first, because staff will likely be working inside the store system most of the time. Email notifications could be useful for more serious issues or anything that sits unresolved for too long, and a dashboard indicator would help show what still needs attention at a glance. The system should definitely prioritize payment failures and anything blocking fulfillment ahead of minor shipping delays, so the urgent problems are the ones staff see first."
- `[interview_turn:T066]` "I’d want the system to treat payment failures as the highest priority, especially if an order can’t be completed or money might be in an uncertain state. Shipping issues would be next, with things like missed dispatches or bad addresses flagged sooner than minor delays. It should alert the right staff first in-app, then escalate to email or a manager if the issue stays open too long, so the team isn’t flooded but the urgent items still get attention quickly."

### [FR-030] (stated)
The system shall support basic validation before an order is submitted.

**Source Evidence:**
- `[interview_turn:T068]` "Yes, that would be very useful. I’d want basic validation before an order is submitted, like checking required address fields, obvious payment format issues, and maybe flagging suspicious or incomplete orders right away. For staff, guided messages that explain the likely cause and suggest the next step would be helpful, because a lot of the users are new to online retail and may not know how to troubleshoot quickly."
- `[interview_turn:T088]` "For the first release, I’d want product import to support a simple spreadsheet upload, column mapping, preview, and basic validation for required fields, duplicates, and obvious formatting errors. It should let users fix problems before import and clearly show what was accepted and what was rejected. For orders, I’d expect a basic validation step before submission so customers can see missing shipping or payment information right away and correct it before the order is placed."
- `[interview_turn:T092]` "For the initial launch, product import should definitely include file upload, field mapping, preview, and validation before anything is committed. It needs to catch missing required fields, duplicate entries, and format problems, and it should let users correct issues without restarting the whole import. I’d also want a clear success summary at the end that tells them what came in and what was skipped.
For order validation, the must-have behavior is to check the customer’s required information before the order is submitted, especially shipping details and payment-related fields. If something is wrong, the system should explain it in simple terms and keep the customer on the checkout page so they can fix it right away. That kind of feedback is important because it makes the process feel safe and understandable for new users."
- `[interview_turn:T096]` "For the initial launch, I’d treat spreadsheet import with mapping, preview, and validation as essential, along with a clear result screen that shows what succeeded and what still needs attention. It should handle common errors like missing required fields, invalid data formats, and duplicates, and it should always let the seller fix issues before the import is finalized. For order validation, the checkout should check required customer, shipping, and payment information before submission and give simple, direct guidance on what needs to be corrected."

### [FR-031] (stated)
The order submission validation shall check required address fields and obvious payment format issues.

**Source Evidence:**
- `[interview_turn:T068]` "Yes, that would be very useful. I’d want basic validation before an order is submitted, like checking required address fields, obvious payment format issues, and maybe flagging suspicious or incomplete orders right away. For staff, guided messages that explain the likely cause and suggest the next step would be helpful, because a lot of the users are new to online retail and may not know how to troubleshoot quickly."

### [FR-032] (stated)
The order submission validation shall check required customer, shipping, and payment information before the order is submitted.

**Source Evidence:**
- `[interview_turn:T092]` "For the initial launch, product import should definitely include file upload, field mapping, preview, and validation before anything is committed. It needs to catch missing required fields, duplicate entries, and format problems, and it should let users correct issues without restarting the whole import. I’d also want a clear success summary at the end that tells them what came in and what was skipped.
For order validation, the must-have behavior is to check the customer’s required information before the order is submitted, especially shipping details and payment-related fields. If something is wrong, the system should explain it in simple terms and keep the customer on the checkout page so they can fix it right away. That kind of feedback is important because it makes the process feel safe and understandable for new users."
- `[interview_turn:T096]` "For the initial launch, I’d treat spreadsheet import with mapping, preview, and validation as essential, along with a clear result screen that shows what succeeded and what still needs attention. It should handle common errors like missing required fields, invalid data formats, and duplicates, and it should always let the seller fix issues before the import is finalized. For order validation, the checkout should check required customer, shipping, and payment information before submission and give simple, direct guidance on what needs to be corrected."

### [FR-033] (stated)
The system shall display order validation feedback before submission or immediately after form completion.

**Source Evidence:**
- `[interview_turn:T090]` "In the import wizard, I’d want a clear step indicator, a progress bar, and plain messages that say what stage the user is on and what still needs attention. If something blocks the import, it should be shown right next to the problem row or field, with a simple explanation and a suggested fix, not a generic failure message. When most data is good, the system should say that explicitly, like telling the user how many items are ready to import and how many only need minor review, so they feel encouraged instead of stuck.
For order validation, the feedback should appear before the final submit button is activated, or at least immediately after the user finishes the form, with the missing or incorrect fields highlighted. It would help if the message explains exactly what to do, like adding a postal code or choosing a shipping method, and then keeps the user on the same screen so they can correct it quickly."
- `[interview_turn:T092]` "For the initial launch, product import should definitely include file upload, field mapping, preview, and validation before anything is committed. It needs to catch missing required fields, duplicate entries, and format problems, and it should let users correct issues without restarting the whole import. I’d also want a clear success summary at the end that tells them what came in and what was skipped.
For order validation, the must-have behavior is to check the customer’s required information before the order is submitted, especially shipping details and payment-related fields. If something is wrong, the system should explain it in simple terms and keep the customer on the checkout page so they can fix it right away. That kind of feedback is important because it makes the process feel safe and understandable for new users."

### [FR-034] (stated)
The system shall keep the customer on the checkout page or same screen when correcting order validation issues.

**Source Evidence:**
- `[interview_turn:T090]` "In the import wizard, I’d want a clear step indicator, a progress bar, and plain messages that say what stage the user is on and what still needs attention. If something blocks the import, it should be shown right next to the problem row or field, with a simple explanation and a suggested fix, not a generic failure message. When most data is good, the system should say that explicitly, like telling the user how many items are ready to import and how many only need minor review, so they feel encouraged instead of stuck.
For order validation, the feedback should appear before the final submit button is activated, or at least immediately after the user finishes the form, with the missing or incorrect fields highlighted. It would help if the message explains exactly what to do, like adding a postal code or choosing a shipping method, and then keeps the user on the same screen so they can correct it quickly."
- `[interview_turn:T092]` "For the initial launch, product import should definitely include file upload, field mapping, preview, and validation before anything is committed. It needs to catch missing required fields, duplicate entries, and format problems, and it should let users correct issues without restarting the whole import. I’d also want a clear success summary at the end that tells them what came in and what was skipped.
For order validation, the must-have behavior is to check the customer’s required information before the order is submitted, especially shipping details and payment-related fields. If something is wrong, the system should explain it in simple terms and keep the customer on the checkout page so they can fix it right away. That kind of feedback is important because it makes the process feel safe and understandable for new users."

### [FR-035] (stated)
The system shall support spreadsheet import for product data.

**Source Evidence:**
- `[interview_turn:T070]` "I’d definitely want a spreadsheet import, especially CSV, because that’s probably the easiest starting point for most new sellers. The system should map columns to fields with a preview before anything is saved, and it should flag missing or bad values so users can fix them before the import finishes. If possible, a simple step-by-step import wizard would make it much less intimidating for people who are not technical."
- `[interview_turn:T088]` "For the first release, I’d want product import to support a simple spreadsheet upload, column mapping, preview, and basic validation for required fields, duplicates, and obvious formatting errors. It should let users fix problems before import and clearly show what was accepted and what was rejected. For orders, I’d expect a basic validation step before submission so customers can see missing shipping or payment information right away and correct it before the order is placed."
- `[interview_turn:T092]` "For the initial launch, product import should definitely include file upload, field mapping, preview, and validation before anything is committed. It needs to catch missing required fields, duplicate entries, and format problems, and it should let users correct issues without restarting the whole import. I’d also want a clear success summary at the end that tells them what came in and what was skipped.
For order validation, the must-have behavior is to check the customer’s required information before the order is submitted, especially shipping details and payment-related fields. If something is wrong, the system should explain it in simple terms and keep the customer on the checkout page so they can fix it right away. That kind of feedback is important because it makes the process feel safe and understandable for new users."
- `[interview_turn:T096]` "For the initial launch, I’d treat spreadsheet import with mapping, preview, and validation as essential, along with a clear result screen that shows what succeeded and what still needs attention. It should handle common errors like missing required fields, invalid data formats, and duplicates, and it should always let the seller fix issues before the import is finalized. For order validation, the checkout should check required customer, shipping, and payment information before submission and give simple, direct guidance on what needs to be corrected."

### [FR-036] (stated)
The system shall support CSV import for product data.

**Source Evidence:**
- `[interview_turn:T070]` "I’d definitely want a spreadsheet import, especially CSV, because that’s probably the easiest starting point for most new sellers. The system should map columns to fields with a preview before anything is saved, and it should flag missing or bad values so users can fix them before the import finishes. If possible, a simple step-by-step import wizard would make it much less intimidating for people who are not technical."

### [FR-037] (stated)
The system shall support product file upload, field mapping, preview, and validation before imported data is committed.

**Source Evidence:**
- `[interview_turn:T088]` "For the first release, I’d want product import to support a simple spreadsheet upload, column mapping, preview, and basic validation for required fields, duplicates, and obvious formatting errors. It should let users fix problems before import and clearly show what was accepted and what was rejected. For orders, I’d expect a basic validation step before submission so customers can see missing shipping or payment information right away and correct it before the order is placed."
- `[interview_turn:T092]` "For the initial launch, product import should definitely include file upload, field mapping, preview, and validation before anything is committed. It needs to catch missing required fields, duplicate entries, and format problems, and it should let users correct issues without restarting the whole import. I’d also want a clear success summary at the end that tells them what came in and what was skipped.
For order validation, the must-have behavior is to check the customer’s required information before the order is submitted, especially shipping details and payment-related fields. If something is wrong, the system should explain it in simple terms and keep the customer on the checkout page so they can fix it right away. That kind of feedback is important because it makes the process feel safe and understandable for new users."
- `[interview_turn:T096]` "For the initial launch, I’d treat spreadsheet import with mapping, preview, and validation as essential, along with a clear result screen that shows what succeeded and what still needs attention. It should handle common errors like missing required fields, invalid data formats, and duplicates, and it should always let the seller fix issues before the import is finalized. For order validation, the checkout should check required customer, shipping, and payment information before submission and give simple, direct guidance on what needs to be corrected."

### [FR-038] (stated)
The system shall allow users to correct import issues without restarting the whole import.

**Source Evidence:**
- `[interview_turn:T092]` "For the initial launch, product import should definitely include file upload, field mapping, preview, and validation before anything is committed. It needs to catch missing required fields, duplicate entries, and format problems, and it should let users correct issues without restarting the whole import. I’d also want a clear success summary at the end that tells them what came in and what was skipped.
For order validation, the must-have behavior is to check the customer’s required information before the order is submitted, especially shipping details and payment-related fields. If something is wrong, the system should explain it in simple terms and keep the customer on the checkout page so they can fix it right away. That kind of feedback is important because it makes the process feel safe and understandable for new users."
- `[interview_turn:T096]` "For the initial launch, I’d treat spreadsheet import with mapping, preview, and validation as essential, along with a clear result screen that shows what succeeded and what still needs attention. It should handle common errors like missing required fields, invalid data formats, and duplicates, and it should always let the seller fix issues before the import is finalized. For order validation, the checkout should check required customer, shipping, and payment information before submission and give simple, direct guidance on what needs to be corrected."

### [FR-039] (stated)
The system shall show a clear result or success summary after import that identifies what succeeded, what was skipped, and what needs attention.

**Source Evidence:**
- `[interview_turn:T088]` "For the first release, I’d want product import to support a simple spreadsheet upload, column mapping, preview, and basic validation for required fields, duplicates, and obvious formatting errors. It should let users fix problems before import and clearly show what was accepted and what was rejected. For orders, I’d expect a basic validation step before submission so customers can see missing shipping or payment information right away and correct it before the order is placed."
- `[interview_turn:T092]` "For the initial launch, product import should definitely include file upload, field mapping, preview, and validation before anything is committed. It needs to catch missing required fields, duplicate entries, and format problems, and it should let users correct issues without restarting the whole import. I’d also want a clear success summary at the end that tells them what came in and what was skipped.
For order validation, the must-have behavior is to check the customer’s required information before the order is submitted, especially shipping details and payment-related fields. If something is wrong, the system should explain it in simple terms and keep the customer on the checkout page so they can fix it right away. That kind of feedback is important because it makes the process feel safe and understandable for new users."
- `[interview_turn:T096]` "For the initial launch, I’d treat spreadsheet import with mapping, preview, and validation as essential, along with a clear result screen that shows what succeeded and what still needs attention. It should handle common errors like missing required fields, invalid data formats, and duplicates, and it should always let the seller fix issues before the import is finalized. For order validation, the checkout should check required customer, shipping, and payment information before submission and give simple, direct guidance on what needs to be corrected."

### [FR-040] (stated)
The import process shall let users fix problem fields inline within the review screen.

**Source Evidence:**
- `[interview_turn:T074]` "I’d want the user to be able to edit the problem fields right in the review screen, not have to leave the import flow. For duplicates, the system should show the matching records side by side and let the user choose keep, merge, or skip, with a clear explanation of why it flagged them. Some automation is fine for obvious fixes, but for anything ambiguous I’d prefer the system to suggest a resolution and let the user confirm it."
- `[interview_turn:T076]` "A new seller would start by uploading the file, then the system would check the format and ask them to match the spreadsheet columns to the product fields. After that, it would run a validation pass and group the problems together, so they can see missing values, duplicates, and bad categories in one place instead of one at a time. They would fix what they can inline, review any suggested merges or corrections, and then get a final summary before confirming the import."

### [FR-041] (stated)
The import process shall compare potential duplicates and allow the user to keep, merge, or skip matching records.

**Source Evidence:**
- `[interview_turn:T072]` "I’d expect the import to catch duplicates by comparing things like product name, SKU, or maybe barcode if it’s available, and then either warn the user or let them merge records. Inconsistent details, like missing prices or mismatched categories, should be highlighted in a review screen before the import is finalized. The goal would be to let users clean up the data as they go, instead of forcing them to fix a bunch of problems after everything is already loaded."
- `[interview_turn:T074]` "I’d want the user to be able to edit the problem fields right in the review screen, not have to leave the import flow. For duplicates, the system should show the matching records side by side and let the user choose keep, merge, or skip, with a clear explanation of why it flagged them. Some automation is fine for obvious fixes, but for anything ambiguous I’d prefer the system to suggest a resolution and let the user confirm it."

### [FR-042] (stated)
The import process shall provide a review screen before finalizing import so users can resolve missing or inconsistent data.

**Source Evidence:**
- `[interview_turn:T072]` "I’d expect the import to catch duplicates by comparing things like product name, SKU, or maybe barcode if it’s available, and then either warn the user or let them merge records. Inconsistent details, like missing prices or mismatched categories, should be highlighted in a review screen before the import is finalized. The goal would be to let users clean up the data as they go, instead of forcing them to fix a bunch of problems after everything is already loaded."
- `[interview_turn:T076]` "A new seller would start by uploading the file, then the system would check the format and ask them to match the spreadsheet columns to the product fields. After that, it would run a validation pass and group the problems together, so they can see missing values, duplicates, and bad categories in one place instead of one at a time. They would fix what they can inline, review any suggested merges or corrections, and then get a final summary before confirming the import."

### [FR-043] (stated)
The import wizard shall guide users through small steps with a clear progress indicator.

**Source Evidence:**
- `[interview_turn:T080]` "I’d keep it in small steps with one decision at a time, so the user never feels like they’re staring at a huge form. The wizard should show a live preview after column mapping, then highlight only the rows with issues and explain them in plain language, with buttons to fix, ignore, or apply a suggested correction. It would also help to show progress and a simple count of how many items are ready versus how many still need attention, so users can see they’re getting through it."
- `[interview_turn:T084]` "I’d want it to feel like a guided checklist rather than a technical setup screen. Each step should be short, with plain-language explanations, a preview of what the system understood, and an easy way to go back if something looks wrong. It would also help a lot if the wizard reassures users with messages like “most items are ready” and only stops them on issues that truly need attention."
- `[interview_turn:T090]` "In the import wizard, I’d want a clear step indicator, a progress bar, and plain messages that say what stage the user is on and what still needs attention. If something blocks the import, it should be shown right next to the problem row or field, with a simple explanation and a suggested fix, not a generic failure message. When most data is good, the system should say that explicitly, like telling the user how many items are ready to import and how many only need minor review, so they feel encouraged instead of stuck.
For order validation, the feedback should appear before the final submit button is activated, or at least immediately after the user finishes the form, with the missing or incorrect fields highlighted. It would help if the message explains exactly what to do, like adding a postal code or choosing a shipping method, and then keeps the user on the same screen so they can correct it quickly."
- `[interview_turn:T098]` "I’d want the wizard to show one step at a time with a short progress indicator so users can see they are moving forward. The messages should be plain and reassuring, like telling them how many products are ready, how many need review, and exactly what the next action is. For errors, I’d prefer red highlights only where needed, plus a calm explanation and a clear fix option, so the user feels guided rather than punished."
- `[interview_turn:T102]` "I’d want the wizard to break the import into small, visible steps so the user always knows where they are. A simple progress bar, a current step label, and brief confirmation messages after each stage would help a lot. If there’s an error, it should be shown right at the item or field, with a plain explanation and a quick way to fix it, so the user can keep moving instead of feeling stopped."

### [FR-044] (stated)
The import wizard shall show a live preview after column mapping.

**Source Evidence:**
- `[interview_turn:T076]` "A new seller would start by uploading the file, then the system would check the format and ask them to match the spreadsheet columns to the product fields. After that, it would run a validation pass and group the problems together, so they can see missing values, duplicates, and bad categories in one place instead of one at a time. They would fix what they can inline, review any suggested merges or corrections, and then get a final summary before confirming the import."
- `[interview_turn:T080]` "I’d keep it in small steps with one decision at a time, so the user never feels like they’re staring at a huge form. The wizard should show a live preview after column mapping, then highlight only the rows with issues and explain them in plain language, with buttons to fix, ignore, or apply a suggested correction. It would also help to show progress and a simple count of how many items are ready versus how many still need attention, so users can see they’re getting through it."

### [FR-045] (stated)
The import wizard shall highlight rows or fields with issues and explain them in plain language.

**Source Evidence:**
- `[interview_turn:T080]` "I’d keep it in small steps with one decision at a time, so the user never feels like they’re staring at a huge form. The wizard should show a live preview after column mapping, then highlight only the rows with issues and explain them in plain language, with buttons to fix, ignore, or apply a suggested correction. It would also help to show progress and a simple count of how many items are ready versus how many still need attention, so users can see they’re getting through it."
- `[interview_turn:T084]` "I’d want it to feel like a guided checklist rather than a technical setup screen. Each step should be short, with plain-language explanations, a preview of what the system understood, and an easy way to go back if something looks wrong. It would also help a lot if the wizard reassures users with messages like “most items are ready” and only stops them on issues that truly need attention."
- `[interview_turn:T090]` "In the import wizard, I’d want a clear step indicator, a progress bar, and plain messages that say what stage the user is on and what still needs attention. If something blocks the import, it should be shown right next to the problem row or field, with a simple explanation and a suggested fix, not a generic failure message. When most data is good, the system should say that explicitly, like telling the user how many items are ready to import and how many only need minor review, so they feel encouraged instead of stuck.
For order validation, the feedback should appear before the final submit button is activated, or at least immediately after the user finishes the form, with the missing or incorrect fields highlighted. It would help if the message explains exactly what to do, like adding a postal code or choosing a shipping method, and then keeps the user on the same screen so they can correct it quickly."
- `[interview_turn:T098]` "I’d want the wizard to show one step at a time with a short progress indicator so users can see they are moving forward. The messages should be plain and reassuring, like telling them how many products are ready, how many need review, and exactly what the next action is. For errors, I’d prefer red highlights only where needed, plus a calm explanation and a clear fix option, so the user feels guided rather than punished."
- `[interview_turn:T102]` "I’d want the wizard to break the import into small, visible steps so the user always knows where they are. A simple progress bar, a current step label, and brief confirmation messages after each stage would help a lot. If there’s an error, it should be shown right at the item or field, with a plain explanation and a quick way to fix it, so the user can keep moving instead of feeling stopped."

### [FR-046] (stated)
The import wizard shall provide buttons or actions to fix, ignore, or apply a suggested correction for issues.

**Source Evidence:**
- `[interview_turn:T080]` "I’d keep it in small steps with one decision at a time, so the user never feels like they’re staring at a huge form. The wizard should show a live preview after column mapping, then highlight only the rows with issues and explain them in plain language, with buttons to fix, ignore, or apply a suggested correction. It would also help to show progress and a simple count of how many items are ready versus how many still need attention, so users can see they’re getting through it."

### [FR-047] (stated)
The import wizard shall show how many items are ready versus how many need attention.

**Source Evidence:**
- `[interview_turn:T080]` "I’d keep it in small steps with one decision at a time, so the user never feels like they’re staring at a huge form. The wizard should show a live preview after column mapping, then highlight only the rows with issues and explain them in plain language, with buttons to fix, ignore, or apply a suggested correction. It would also help to show progress and a simple count of how many items are ready versus how many still need attention, so users can see they’re getting through it."
- `[interview_turn:T084]` "I’d want it to feel like a guided checklist rather than a technical setup screen. Each step should be short, with plain-language explanations, a preview of what the system understood, and an easy way to go back if something looks wrong. It would also help a lot if the wizard reassures users with messages like “most items are ready” and only stops them on issues that truly need attention."
- `[interview_turn:T090]` "In the import wizard, I’d want a clear step indicator, a progress bar, and plain messages that say what stage the user is on and what still needs attention. If something blocks the import, it should be shown right next to the problem row or field, with a simple explanation and a suggested fix, not a generic failure message. When most data is good, the system should say that explicitly, like telling the user how many items are ready to import and how many only need minor review, so they feel encouraged instead of stuck.
For order validation, the feedback should appear before the final submit button is activated, or at least immediately after the user finishes the form, with the missing or incorrect fields highlighted. It would help if the message explains exactly what to do, like adding a postal code or choosing a shipping method, and then keeps the user on the same screen so they can correct it quickly."
- `[interview_turn:T098]` "I’d want the wizard to show one step at a time with a short progress indicator so users can see they are moving forward. The messages should be plain and reassuring, like telling them how many products are ready, how many need review, and exactly what the next action is. For errors, I’d prefer red highlights only where needed, plus a calm explanation and a clear fix option, so the user feels guided rather than punished."

### [FR-048] (stated)
The import wizard shall allow users to go back to a previous step if something looks wrong.

**Source Evidence:**
- `[interview_turn:T084]` "I’d want it to feel like a guided checklist rather than a technical setup screen. Each step should be short, with plain-language explanations, a preview of what the system understood, and an easy way to go back if something looks wrong. It would also help a lot if the wizard reassures users with messages like “most items are ready” and only stops them on issues that truly need attention."

### [FR-049] (stated)
The system shall support optional suggestions during product import for categories, units of measure, brand, and cleaner product titles.

**Source Evidence:**
- `[interview_turn:T078]` "Yes, that would be a strong addition as long as it stays simple. I’d like the system to suggest likely categories from the product name or description, and maybe recommend standard values for things like unit of measure or brand if it can infer them confidently. If it can also prompt for missing details that improve the storefront, like a short description or image, that would help new sellers build a better catalog without having to know all the best practices up front."
- `[interview_turn:T082]` "Yes, I think a few subtle helpers would be useful if they stay optional. For example, the system could auto-detect units, normalize spelling for common terms, and suggest cleaner product titles based on the imported description, while still letting the user override anything. It could also use small inline hints, like pointing out that adding a photo or a clearer category will improve search results, so beginners learn as they go without feeling lectured."
- `[interview_turn:T094]` "I think those helpers are important, but they should stay secondary to the basic import flow in the first release. They should appear as optional suggestions or fixes the user can review, not as automatic changes that might surprise them. The best presentation would be a simple suggestion panel or inline prompt with a clear accept, edit, or ignore choice for each item."

### [FR-050] (stated)
The system shall allow users to accept, edit, or reject import suggestions.

**Source Evidence:**
- `[interview_turn:T086]` "I think that would be very important, especially for people who are not comfortable with spreadsheets or retail terminology. The automation should be clearly presented as suggestions or default fixes, not silent changes, and the user should always be able to accept, edit, or reject each one. That way the system helps reduce mistakes and speed things up, but the seller still feels in control of their catalog."
- `[interview_turn:T094]` "I think those helpers are important, but they should stay secondary to the basic import flow in the first release. They should appear as optional suggestions or fixes the user can review, not as automatic changes that might surprise them. The best presentation would be a simple suggestion panel or inline prompt with a clear accept, edit, or ignore choice for each item."

### [FR-051] (stated)
The system shall suggest likely categories from a product name or description when it can infer them confidently.

**Source Evidence:**
- `[interview_turn:T078]` "Yes, that would be a strong addition as long as it stays simple. I’d like the system to suggest likely categories from the product name or description, and maybe recommend standard values for things like unit of measure or brand if it can infer them confidently. If it can also prompt for missing details that improve the storefront, like a short description or image, that would help new sellers build a better catalog without having to know all the best practices up front."

### [FR-052] (stated)
The system shall prompt for missing product details such as a short description or image when those details would improve the storefront.

**Source Evidence:**
- `[interview_turn:T078]` "Yes, that would be a strong addition as long as it stays simple. I’d like the system to suggest likely categories from the product name or description, and maybe recommend standard values for things like unit of measure or brand if it can infer them confidently. If it can also prompt for missing details that improve the storefront, like a short description or image, that would help new sellers build a better catalog without having to know all the best practices up front."

### [FR-053] (stated)
The system shall auto-detect units and normalize spelling for common terms as optional import helpers.

**Source Evidence:**
- `[interview_turn:T082]` "Yes, I think a few subtle helpers would be useful if they stay optional. For example, the system could auto-detect units, normalize spelling for common terms, and suggest cleaner product titles based on the imported description, while still letting the user override anything. It could also use small inline hints, like pointing out that adding a photo or a clearer category will improve search results, so beginners learn as they go without feeling lectured."
- `[interview_turn:T086]` "I think that would be very important, especially for people who are not comfortable with spreadsheets or retail terminology. The automation should be clearly presented as suggestions or default fixes, not silent changes, and the user should always be able to accept, edit, or reject each one. That way the system helps reduce mistakes and speed things up, but the seller still feels in control of their catalog."
- `[interview_turn:T094]` "I think those helpers are important, but they should stay secondary to the basic import flow in the first release. They should appear as optional suggestions or fixes the user can review, not as automatic changes that might surprise them. The best presentation would be a simple suggestion panel or inline prompt with a clear accept, edit, or ignore choice for each item."

### [FR-054] (stated)
The system shall not make silent automatic changes during import suggestions; suggestions shall be presented for user review.

**Source Evidence:**
- `[interview_turn:T086]` "I think that would be very important, especially for people who are not comfortable with spreadsheets or retail terminology. The automation should be clearly presented as suggestions or default fixes, not silent changes, and the user should always be able to accept, edit, or reject each one. That way the system helps reduce mistakes and speed things up, but the seller still feels in control of their catalog."
- `[interview_turn:T094]` "I think those helpers are important, but they should stay secondary to the basic import flow in the first release. They should appear as optional suggestions or fixes the user can review, not as automatic changes that might surprise them. The best presentation would be a simple suggestion panel or inline prompt with a clear accept, edit, or ignore choice for each item."

### [FR-055] (stated)
The system shall provide clear step indicators, plain messages, and a simple count of items ready versus items needing review during import.

**Source Evidence:**
- `[interview_turn:T080]` "I’d keep it in small steps with one decision at a time, so the user never feels like they’re staring at a huge form. The wizard should show a live preview after column mapping, then highlight only the rows with issues and explain them in plain language, with buttons to fix, ignore, or apply a suggested correction. It would also help to show progress and a simple count of how many items are ready versus how many still need attention, so users can see they’re getting through it."
- `[interview_turn:T084]` "I’d want it to feel like a guided checklist rather than a technical setup screen. Each step should be short, with plain-language explanations, a preview of what the system understood, and an easy way to go back if something looks wrong. It would also help a lot if the wizard reassures users with messages like “most items are ready” and only stops them on issues that truly need attention."
- `[interview_turn:T090]` "In the import wizard, I’d want a clear step indicator, a progress bar, and plain messages that say what stage the user is on and what still needs attention. If something blocks the import, it should be shown right next to the problem row or field, with a simple explanation and a suggested fix, not a generic failure message. When most data is good, the system should say that explicitly, like telling the user how many items are ready to import and how many only need minor review, so they feel encouraged instead of stuck.
For order validation, the feedback should appear before the final submit button is activated, or at least immediately after the user finishes the form, with the missing or incorrect fields highlighted. It would help if the message explains exactly what to do, like adding a postal code or choosing a shipping method, and then keeps the user on the same screen so they can correct it quickly."
- `[interview_turn:T098]` "I’d want the wizard to show one step at a time with a short progress indicator so users can see they are moving forward. The messages should be plain and reassuring, like telling them how many products are ready, how many need review, and exactly what the next action is. For errors, I’d prefer red highlights only where needed, plus a calm explanation and a clear fix option, so the user feels guided rather than punished."
- `[interview_turn:T102]` "I’d want the wizard to break the import into small, visible steps so the user always knows where they are. A simple progress bar, a current step label, and brief confirmation messages after each stage would help a lot. If there’s an error, it should be shown right at the item or field, with a plain explanation and a quick way to fix it, so the user can keep moving instead of feeling stopped."

### [FR-056] (stated)
The system shall support product category assignment during import and normal product management.

**Source Evidence:**
- `[interview_turn:T024]` "Products are the main sellable items, and each product usually belongs to one category so customers can browse more easily. Customer accounts hold the buyer’s contact and order history information, while categories are just the way we group products for navigation and management. A common confusion is that new users may think a category is the same as a product variation, so we’d want to explain that categories organize the store, while variations are differences within one product."
- `[interview_turn:T072]` "I’d expect the import to catch duplicates by comparing things like product name, SKU, or maybe barcode if it’s available, and then either warn the user or let them merge records. Inconsistent details, like missing prices or mismatched categories, should be highlighted in a review screen before the import is finalized. The goal would be to let users clean up the data as they go, instead of forcing them to fix a bunch of problems after everything is already loaded."
- `[interview_turn:T078]` "Yes, that would be a strong addition as long as it stays simple. I’d like the system to suggest likely categories from the product name or description, and maybe recommend standard values for things like unit of measure or brand if it can infer them confidently. If it can also prompt for missing details that improve the storefront, like a short description or image, that would help new sellers build a better catalog without having to know all the best practices up front."

### [FR-057] (stated)
The system shall support products that have variations distinct from categories.

**Source Evidence:**
- `[interview_turn:T024]` "Products are the main sellable items, and each product usually belongs to one category so customers can browse more easily. Customer accounts hold the buyer’s contact and order history information, while categories are just the way we group products for navigation and management. A common confusion is that new users may think a category is the same as a product variation, so we’d want to explain that categories organize the store, while variations are differences within one product."
- `[interview_turn:T026]` "The most common issues are missing prices, inconsistent product names, wrong categories, and unclear stock quantities. Sometimes they also upload duplicate items because they’re not sure whether a product variation should be a separate product or just an option under one product. Usually they try to fix it by editing the entries directly after they notice the mistake, or by comparing against their spreadsheet and re-entering the information by hand."

### [FR-058] (stated)
The system shall provide a simple browser-based web interface.

**Source Evidence:**
- `[interview_turn:T008]` "We expect it to be a web-based system that runs in a standard browser, since the users we’re targeting shouldn’t need special software installed. It should work well for people with limited technical experience, so we’d want the interface to stay simple and the setup process to be guided. I don’t have firm decisions yet on integrations or specific technical constraints, so those would need to be checked with the team."

### [FR-059] (stated)
The system shall be usable in a standard browser without requiring special software to be installed.

**Source Evidence:**
- `[interview_turn:T008]` "We expect it to be a web-based system that runs in a standard browser, since the users we’re targeting shouldn’t need special software installed. It should work well for people with limited technical experience, so we’d want the interface to stay simple and the setup process to be guided. I don’t have firm decisions yet on integrations or specific technical constraints, so those would need to be checked with the team."

### [FR-060] (stated)
The interface shall stay simple and the setup process shall be guided for users with limited technical experience.

**Source Evidence:**
- `[interview_turn:T008]` "We expect it to be a web-based system that runs in a standard browser, since the users we’re targeting shouldn’t need special software installed. It should work well for people with limited technical experience, so we’d want the interface to stay simple and the setup process to be guided. I don’t have firm decisions yet on integrations or specific technical constraints, so those would need to be checked with the team."
- `[interview_turn:T032]` "An ideal setup flow would guide them step by step instead of letting them face a blank system all at once. It would probably start with basic store information, then help them add categories, products, and customer account settings with clear examples and simple prompts for things like pricing, stock, and variants. It would also be helpful if the system flagged incomplete entries right away and explained mistakes in plain language so they can correct them before they start selling."

### [FR-061] (stated)
The system shall support customer order confirmation and refund or cancellation notices automatically.

**Source Evidence:**
- `[interview_turn:T064]` "I’d want customer data collection to be limited to what’s actually needed for the order and account, with clear consent and privacy notices shown during signup and checkout. Users should also get order confirmations and any refund or cancellation notices automatically, because that helps both compliance and customer trust. For staff, the system should keep good logs of edits to customer records, prices, orders, and payments so we can trace changes if there’s ever a complaint or audit."

### [FR-062] (stated)
The system shall provide clear pricing information to support consumer-facing compliance.

**Source Evidence:**
- `[interview_turn:T062]` "We’ll definitely need to comply with standard data protection and privacy requirements, since the system will store customer account information and order history. Consumer-facing rules around refunds, order confirmation, and clear pricing will matter too, but I’d need to verify the exact legal jurisdictions before being specific. I’d also expect basic security and recordkeeping practices so we can show who changed what and when if there’s ever a dispute."

### [FR-063] (stated)
The system shall collect only customer data needed for the order and customer account.

**Source Evidence:**
- `[interview_turn:T064]` "I’d want customer data collection to be limited to what’s actually needed for the order and account, with clear consent and privacy notices shown during signup and checkout. Users should also get order confirmations and any refund or cancellation notices automatically, because that helps both compliance and customer trust. For staff, the system should keep good logs of edits to customer records, prices, orders, and payments so we can trace changes if there’s ever a complaint or audit."

### [FR-064] (stated)
The system shall provide clear consent and privacy notices during signup and checkout.

**Source Evidence:**
- `[interview_turn:T064]` "I’d want customer data collection to be limited to what’s actually needed for the order and account, with clear consent and privacy notices shown during signup and checkout. Users should also get order confirmations and any refund or cancellation notices automatically, because that helps both compliance and customer trust. For staff, the system should keep good logs of edits to customer records, prices, orders, and payments so we can trace changes if there’s ever a complaint or audit."

### [FR-065] (stated)
The system shall support keeping logs of edits to customer records, prices, orders, and payments.

**Source Evidence:**
- `[interview_turn:T062]` "We’ll definitely need to comply with standard data protection and privacy requirements, since the system will store customer account information and order history. Consumer-facing rules around refunds, order confirmation, and clear pricing will matter too, but I’d need to verify the exact legal jurisdictions before being specific. I’d also expect basic security and recordkeeping practices so we can show who changed what and when if there’s ever a dispute."
- `[interview_turn:T064]` "I’d want customer data collection to be limited to what’s actually needed for the order and account, with clear consent and privacy notices shown during signup and checkout. Users should also get order confirmations and any refund or cancellation notices automatically, because that helps both compliance and customer trust. For staff, the system should keep good logs of edits to customer records, prices, orders, and payments so we can trace changes if there’s ever a complaint or audit."

### [FR-066] (stated)
The system shall support product availability updates after a sale or restock, and allow urgent marking of an item as unavailable.

**Source Evidence:**
- `[interview_turn:T034]` "Sales staff usually handle exceptions by checking the order details, confirming with the owner or warehouse person, and then editing the record manually if they’re allowed to. For product availability, they often update stock after a sale or after a restock comes in, but if the change is urgent they may also need to mark an item unavailable right away to avoid more orders. GAMMA-J should make those edits fast and traceable, because the main pain point is making sure everyone sees the updated status without creating more mistakes."

### [FR-067] (stated)
The system shall support browsing, cart updates, and order entry that remain responsive during normal growth and seasonal spikes.

**Source Evidence:**
- `[interview_turn:T056]` "I’d expect it to handle normal growth without staff noticing much difference, so browsing, cart updates, and order entry should stay responsive even as traffic increases. If the store gets busy, it should still let owners and staff process orders and update products without lag or timeouts. I don’t know the exact volume yet, but I’d want it to feel reliable enough that a small business could grow into a busy season without needing a bigger system right away."
- `[interview_turn:T058]` "I don’t have exact numbers yet, but I’d want it to handle a small business’s normal day plus a noticeable seasonal spike, like a promotion or holiday rush, without staff seeing slowdowns. The most important things to stay fast would be customer browsing, cart checkout, and staff order processing, since those directly affect sales. Product updates can be a little less urgent, but they still shouldn’t feel sluggish if someone is trying to correct stock or pricing during a busy period."
- `[interview_turn:T060]` "I’d want it to scale in a way that new stores can be added without each one affecting the others. From a user perspective, that means the system should keep page loads quick, save changes reliably, and not drop orders or updates even when activity picks up. I don’t know the technical approach we’d use, but I’d definitely expect the platform to handle growth behind the scenes without forcing store owners or staff to change how they work."

### [FR-068] (stated)
The system shall allow page loads, browsing, cart checkout, staff order processing, and product updates to remain responsive during higher activity.

**Source Evidence:**
- `[interview_turn:T056]` "I’d expect it to handle normal growth without staff noticing much difference, so browsing, cart updates, and order entry should stay responsive even as traffic increases. If the store gets busy, it should still let owners and staff process orders and update products without lag or timeouts. I don’t know the exact volume yet, but I’d want it to feel reliable enough that a small business could grow into a busy season without needing a bigger system right away."
- `[interview_turn:T058]` "I don’t have exact numbers yet, but I’d want it to handle a small business’s normal day plus a noticeable seasonal spike, like a promotion or holiday rush, without staff seeing slowdowns. The most important things to stay fast would be customer browsing, cart checkout, and staff order processing, since those directly affect sales. Product updates can be a little less urgent, but they still shouldn’t feel sluggish if someone is trying to correct stock or pricing during a busy period."
- `[interview_turn:T060]` "I’d want it to scale in a way that new stores can be added without each one affecting the others. From a user perspective, that means the system should keep page loads quick, save changes reliably, and not drop orders or updates even when activity picks up. I don’t know the technical approach we’d use, but I’d definitely expect the platform to handle growth behind the scenes without forcing store owners or staff to change how they work."

### [FR-069] (stated)
The platform shall allow new stores to be added without each store affecting the others.

**Source Evidence:**
- `[interview_turn:T060]` "I’d want it to scale in a way that new stores can be added without each one affecting the others. From a user perspective, that means the system should keep page loads quick, save changes reliably, and not drop orders or updates even when activity picks up. I don’t know the technical approach we’d use, but I’d definitely expect the platform to handle growth behind the scenes without forcing store owners or staff to change how they work."

### [FR-070] (stated)
The system shall save changes reliably and not drop orders or updates when activity increases.

**Source Evidence:**
- `[interview_turn:T060]` "I’d want it to scale in a way that new stores can be added without each one affecting the others. From a user perspective, that means the system should keep page loads quick, save changes reliably, and not drop orders or updates even when activity picks up. I don’t know the technical approach we’d use, but I’d definitely expect the platform to handle growth behind the scenes without forcing store owners or staff to change how they work."

### [FR-071] (stated)
The system shall allow the store to manage stock inside GAMMA-J if a full inventory system integration is not in place.

**Source Evidence:**
- `[interview_turn:T046]` "For the initial release, I’d expect at least one mainstream payment gateway and basic shipping carrier support, but I can’t name the exact vendors yet without checking with the team. I don’t think we need a full inventory system integration on day one if the store can manage stock inside GAMMA-J, though that could come later. These integrations would mainly save owners and sales staff from retyping order and shipment details, and they’d make checkout and fulfillment feel more professional for customers."
- `[interview_turn:T050]` "For the first release, I’d keep it limited to one payment gateway, one shipping carrier integration, and the store’s own built-in product and stock management. I don’t have the exact vendor names locked down yet, so I’d need to confirm those with the business team before committing. The main value is that owners and sales staff can process orders, confirm payments, and generate shipping info without switching tools all the time, which should make day-to-day work much faster and less error-prone."

## 4. Business Rules and Constraints

### [BR-001] (stated)
Account means a customer profile with contact and order details, not a paid subscription.

**Source Evidence:**
- `[interview_turn:T010]` "We usually keep the language pretty plain, so terms like store owner, sales staff, customer, product, cart, and order are the main ones people use. One thing to watch is that when we say account, we usually mean a customer profile with contact and order details, not necessarily a paid subscription or anything like that. If there are any other special terms, I’d need to check with the business side."

### [BR-002] (stated)
Categories are used to organize products for navigation and management, and are not the same as product variations.

**Source Evidence:**
- `[interview_turn:T024]` "Products are the main sellable items, and each product usually belongs to one category so customers can browse more easily. Customer accounts hold the buyer’s contact and order history information, while categories are just the way we group products for navigation and management. A common confusion is that new users may think a category is the same as a product variation, so we’d want to explain that categories organize the store, while variations are differences within one product."

### [BR-003] (conditional)
The initial release shall be limited to one payment gateway and one shipping carrier integration.

**Source Evidence:**
- `[interview_turn:T050]` "For the first release, I’d keep it limited to one payment gateway, one shipping carrier integration, and the store’s own built-in product and stock management. I don’t have the exact vendor names locked down yet, so I’d need to confirm those with the business team before committing. The main value is that owners and sales staff can process orders, confirm payments, and generate shipping info without switching tools all the time, which should make day-to-day work much faster and less error-prone."

### [BR-004] (conditional)
The initial release shall not require a full inventory system integration if the store can manage stock inside GAMMA-J.

**Source Evidence:**
- `[interview_turn:T046]` "For the initial release, I’d expect at least one mainstream payment gateway and basic shipping carrier support, but I can’t name the exact vendors yet without checking with the team. I don’t think we need a full inventory system integration on day one if the store can manage stock inside GAMMA-J, though that could come later. These integrations would mainly save owners and sales staff from retyping order and shipment details, and they’d make checkout and fulfillment feel more professional for customers."
- `[interview_turn:T050]` "For the first release, I’d keep it limited to one payment gateway, one shipping carrier integration, and the store’s own built-in product and stock management. I don’t have the exact vendor names locked down yet, so I’d need to confirm those with the business team before committing. The main value is that owners and sales staff can process orders, confirm payments, and generate shipping info without switching tools all the time, which should make day-to-day work much faster and less error-prone."

### [BR-005] (stated)
Payment failures shall be treated as the highest-priority issues.

**Source Evidence:**
- `[interview_turn:T054]` "Yes, I’d want in-app alerts first, because staff will likely be working inside the store system most of the time. Email notifications could be useful for more serious issues or anything that sits unresolved for too long, and a dashboard indicator would help show what still needs attention at a glance. The system should definitely prioritize payment failures and anything blocking fulfillment ahead of minor shipping delays, so the urgent problems are the ones staff see first."
- `[interview_turn:T066]` "I’d want the system to treat payment failures as the highest priority, especially if an order can’t be completed or money might be in an uncertain state. Shipping issues would be next, with things like missed dispatches or bad addresses flagged sooner than minor delays. It should alert the right staff first in-app, then escalate to email or a manager if the issue stays open too long, so the team isn’t flooded but the urgent items still get attention quickly."

### [BR-006] (stated)
Shipping issues such as missed dispatches or bad addresses shall be prioritized ahead of minor shipping delays.

**Source Evidence:**
- `[interview_turn:T066]` "I’d want the system to treat payment failures as the highest priority, especially if an order can’t be completed or money might be in an uncertain state. Shipping issues would be next, with things like missed dispatches or bad addresses flagged sooner than minor delays. It should alert the right staff first in-app, then escalate to email or a manager if the issue stays open too long, so the team isn’t flooded but the urgent items still get attention quickly."

### [BR-007] (stated)
Manual override actions shall require the staff member’s identity and a reason before the change is saved.

**Source Evidence:**
- `[interview_turn:T052]` "In practice, staff should see the error on the order or shipment screen, along with a plain-language explanation and a suggested next step like retry, contact the customer, or correct the details. If they choose a manual override, the system should require a reason and the staff member’s identity before saving the change, so there’s a clear history. An audit trail showing the original error, the action taken, the time, and who handled it would be the most helpful for tracking and later review."

### [BR-008] (stated)
The system shall show who changed an order or product and when the change happened.

**Source Evidence:**
- `[interview_turn:T036]` "Yes, a change log would be very useful so staff can see who changed an order or product and when it happened. Notifications would also help, especially for important updates like stock changes, cancelled orders, or customer account edits, so other staff know right away. I’d expect the system to keep the history visible in a simple way, since new users may not be comfortable digging through technical audit screens."
- `[interview_turn:T052]` "In practice, staff should see the error on the order or shipment screen, along with a plain-language explanation and a suggested next step like retry, contact the customer, or correct the details. If they choose a manual override, the system should require a reason and the staff member’s identity before saving the change, so there’s a clear history. An audit trail showing the original error, the action taken, the time, and who handled it would be the most helpful for tracking and later review."

### [BR-009] (stated)
The system shall allow product import to detect duplicates by comparing product name, SKU, or barcode when available.

**Source Evidence:**
- `[interview_turn:T072]` "I’d expect the import to catch duplicates by comparing things like product name, SKU, or maybe barcode if it’s available, and then either warn the user or let them merge records. Inconsistent details, like missing prices or mismatched categories, should be highlighted in a review screen before the import is finalized. The goal would be to let users clean up the data as they go, instead of forcing them to fix a bunch of problems after everything is already loaded."

### [BR-010] (stated)
The system shall highlight missing prices, inconsistent product names, wrong categories, and unclear stock quantities during product data cleanup.

**Source Evidence:**
- `[interview_turn:T026]` "The most common issues are missing prices, inconsistent product names, wrong categories, and unclear stock quantities. Sometimes they also upload duplicate items because they’re not sure whether a product variation should be a separate product or just an option under one product. Usually they try to fix it by editing the entries directly after they notice the mistake, or by comparing against their spreadsheet and re-entering the information by hand."
- `[interview_turn:T072]` "I’d expect the import to catch duplicates by comparing things like product name, SKU, or maybe barcode if it’s available, and then either warn the user or let them merge records. Inconsistent details, like missing prices or mismatched categories, should be highlighted in a review screen before the import is finalized. The goal would be to let users clean up the data as they go, instead of forcing them to fix a bunch of problems after everything is already loaded."

### [BR-011] (stated)
The system shall require customer, shipping, and payment information checks before an order is submitted.

**Source Evidence:**
- `[interview_turn:T092]` "For the initial launch, product import should definitely include file upload, field mapping, preview, and validation before anything is committed. It needs to catch missing required fields, duplicate entries, and format problems, and it should let users correct issues without restarting the whole import. I’d also want a clear success summary at the end that tells them what came in and what was skipped.
For order validation, the must-have behavior is to check the customer’s required information before the order is submitted, especially shipping details and payment-related fields. If something is wrong, the system should explain it in simple terms and keep the customer on the checkout page so they can fix it right away. That kind of feedback is important because it makes the process feel safe and understandable for new users."
- `[interview_turn:T096]` "For the initial launch, I’d treat spreadsheet import with mapping, preview, and validation as essential, along with a clear result screen that shows what succeeded and what still needs attention. It should handle common errors like missing required fields, invalid data formats, and duplicates, and it should always let the seller fix issues before the import is finalized. For order validation, the checkout should check required customer, shipping, and payment information before submission and give simple, direct guidance on what needs to be corrected."

### [BR-012] (stated)
The system shall allow customer data collection to be limited to what is needed for the order and account.

**Source Evidence:**
- `[interview_turn:T064]` "I’d want customer data collection to be limited to what’s actually needed for the order and account, with clear consent and privacy notices shown during signup and checkout. Users should also get order confirmations and any refund or cancellation notices automatically, because that helps both compliance and customer trust. For staff, the system should keep good logs of edits to customer records, prices, orders, and payments so we can trace changes if there’s ever a complaint or audit."

## 5. Data and External Interfaces

### [DI-001] (stated)
The initial release shall support a spreadsheet import interface for product data.

**Source Evidence:**
- `[interview_turn:T070]` "I’d definitely want a spreadsheet import, especially CSV, because that’s probably the easiest starting point for most new sellers. The system should map columns to fields with a preview before anything is saved, and it should flag missing or bad values so users can fix them before the import finishes. If possible, a simple step-by-step import wizard would make it much less intimidating for people who are not technical."
- `[interview_turn:T088]` "For the first release, I’d want product import to support a simple spreadsheet upload, column mapping, preview, and basic validation for required fields, duplicates, and obvious formatting errors. It should let users fix problems before import and clearly show what was accepted and what was rejected. For orders, I’d expect a basic validation step before submission so customers can see missing shipping or payment information right away and correct it before the order is placed."
- `[interview_turn:T092]` "For the initial launch, product import should definitely include file upload, field mapping, preview, and validation before anything is committed. It needs to catch missing required fields, duplicate entries, and format problems, and it should let users correct issues without restarting the whole import. I’d also want a clear success summary at the end that tells them what came in and what was skipped.
For order validation, the must-have behavior is to check the customer’s required information before the order is submitted, especially shipping details and payment-related fields. If something is wrong, the system should explain it in simple terms and keep the customer on the checkout page so they can fix it right away. That kind of feedback is important because it makes the process feel safe and understandable for new users."
- `[interview_turn:T096]` "For the initial launch, I’d treat spreadsheet import with mapping, preview, and validation as essential, along with a clear result screen that shows what succeeded and what still needs attention. It should handle common errors like missing required fields, invalid data formats, and duplicates, and it should always let the seller fix issues before the import is finalized. For order validation, the checkout should check required customer, shipping, and payment information before submission and give simple, direct guidance on what needs to be corrected."

### [DI-002] (conditional)
The initial release shall support at least one mainstream payment gateway.

**Source Evidence:**
- `[interview_turn:T042]` "I know payment processing will be important, because customers need a smooth checkout experience, but I’m not sure yet which gateway we’ll standardize on. Shipping support would also be useful so orders can move from placed to fulfilled without a lot of manual re-entry, and that would save staff time. If we connect to inventory tools later, that would help keep stock numbers accurate, but I’d need to check with the team on which external systems are actually in scope for the first release."
- `[interview_turn:T046]` "For the initial release, I’d expect at least one mainstream payment gateway and basic shipping carrier support, but I can’t name the exact vendors yet without checking with the team. I don’t think we need a full inventory system integration on day one if the store can manage stock inside GAMMA-J, though that could come later. These integrations would mainly save owners and sales staff from retyping order and shipment details, and they’d make checkout and fulfillment feel more professional for customers."
- `[interview_turn:T050]` "For the first release, I’d keep it limited to one payment gateway, one shipping carrier integration, and the store’s own built-in product and stock management. I don’t have the exact vendor names locked down yet, so I’d need to confirm those with the business team before committing. The main value is that owners and sales staff can process orders, confirm payments, and generate shipping info without switching tools all the time, which should make day-to-day work much faster and less error-prone."

### [DI-003] (conditional)
The initial release shall support basic shipping carrier integration.

**Source Evidence:**
- `[interview_turn:T042]` "I know payment processing will be important, because customers need a smooth checkout experience, but I’m not sure yet which gateway we’ll standardize on. Shipping support would also be useful so orders can move from placed to fulfilled without a lot of manual re-entry, and that would save staff time. If we connect to inventory tools later, that would help keep stock numbers accurate, but I’d need to check with the team on which external systems are actually in scope for the first release."
- `[interview_turn:T046]` "For the initial release, I’d expect at least one mainstream payment gateway and basic shipping carrier support, but I can’t name the exact vendors yet without checking with the team. I don’t think we need a full inventory system integration on day one if the store can manage stock inside GAMMA-J, though that could come later. These integrations would mainly save owners and sales staff from retyping order and shipment details, and they’d make checkout and fulfillment feel more professional for customers."
- `[interview_turn:T050]` "For the first release, I’d keep it limited to one payment gateway, one shipping carrier integration, and the store’s own built-in product and stock management. I don’t have the exact vendor names locked down yet, so I’d need to confirm those with the business team before committing. The main value is that owners and sales staff can process orders, confirm payments, and generate shipping info without switching tools all the time, which should make day-to-day work much faster and less error-prone."

### [DI-004] (stated)
The system shall use a standard browser as its runtime interface.

**Source Evidence:**
- `[interview_turn:T008]` "We expect it to be a web-based system that runs in a standard browser, since the users we’re targeting shouldn’t need special software installed. It should work well for people with limited technical experience, so we’d want the interface to stay simple and the setup process to be guided. I don’t have firm decisions yet on integrations or specific technical constraints, so those would need to be checked with the team."

## 6. Quality Requirements

### [QR-001] (stated)
The system shall present a simple interface for users with limited technical experience.

**Source Evidence:**
- `[interview_turn:T008]` "We expect it to be a web-based system that runs in a standard browser, since the users we’re targeting shouldn’t need special software installed. It should work well for people with limited technical experience, so we’d want the interface to stay simple and the setup process to be guided. I don’t have firm decisions yet on integrations or specific technical constraints, so those would need to be checked with the team."

### [QR-002] (stated)
The system shall use plain-language explanations, brief tips, and short help text for operations and technical concepts.

**Source Evidence:**
- `[interview_turn:T012]` "Yes, a few common e-commerce terms can be confusing for beginners, especially things like inventory, fulfillment, shipping method, and order status. New users also sometimes mix up product categories versus product variants, so those should probably be explained carefully. In general, anything that sounds operational or technical should be presented in very simple language with short help text."
- `[interview_turn:T038]` "I think brief tips and plain-language summaries would be the most helpful, especially at first. A short walkthrough during onboarding could show them where to find recent changes and what the notifications mean, without sending them into a full training course. After that, small contextual help inside the screens would probably be enough for most people."
- `[interview_turn:T084]` "I’d want it to feel like a guided checklist rather than a technical setup screen. Each step should be short, with plain-language explanations, a preview of what the system understood, and an easy way to go back if something looks wrong. It would also help a lot if the wizard reassures users with messages like “most items are ready” and only stops them on issues that truly need attention."
- `[interview_turn:T100]` "I’d keep the design very plain and predictable, with the same button positions and terminology throughout both flows. For visual cues, I’d use color sparingly, mainly to point out errors and confirmations, and rely more on labels, icons, and inline messages than on big alarms or popups. The messaging should sound calm and practical, explaining what happened, why it matters, and what the user can do next in one short sentence."

### [QR-003] (stated)
The setup process shall be guided and step by step.

**Source Evidence:**
- `[interview_turn:T008]` "We expect it to be a web-based system that runs in a standard browser, since the users we’re targeting shouldn’t need special software installed. It should work well for people with limited technical experience, so we’d want the interface to stay simple and the setup process to be guided. I don’t have firm decisions yet on integrations or specific technical constraints, so those would need to be checked with the team."
- `[interview_turn:T032]` "An ideal setup flow would guide them step by step instead of letting them face a blank system all at once. It would probably start with basic store information, then help them add categories, products, and customer account settings with clear examples and simple prompts for things like pricing, stock, and variants. It would also be helpful if the system flagged incomplete entries right away and explained mistakes in plain language so they can correct them before they start selling."
- `[interview_turn:T084]` "I’d want it to feel like a guided checklist rather than a technical setup screen. Each step should be short, with plain-language explanations, a preview of what the system understood, and an easy way to go back if something looks wrong. It would also help a lot if the wizard reassures users with messages like “most items are ready” and only stops them on issues that truly need attention."

### [QR-004] (stated)
The import wizard shall present one decision at a time and avoid overwhelming the user.

**Source Evidence:**
- `[interview_turn:T080]` "I’d keep it in small steps with one decision at a time, so the user never feels like they’re staring at a huge form. The wizard should show a live preview after column mapping, then highlight only the rows with issues and explain them in plain language, with buttons to fix, ignore, or apply a suggested correction. It would also help to show progress and a simple count of how many items are ready versus how many still need attention, so users can see they’re getting through it."
- `[interview_turn:T084]` "I’d want it to feel like a guided checklist rather than a technical setup screen. Each step should be short, with plain-language explanations, a preview of what the system understood, and an easy way to go back if something looks wrong. It would also help a lot if the wizard reassures users with messages like “most items are ready” and only stops them on issues that truly need attention."

### [QR-005] (stated)
The import wizard shall use calm, practical, and reassuring messages.

**Source Evidence:**
- `[interview_turn:T084]` "I’d want it to feel like a guided checklist rather than a technical setup screen. Each step should be short, with plain-language explanations, a preview of what the system understood, and an easy way to go back if something looks wrong. It would also help a lot if the wizard reassures users with messages like “most items are ready” and only stops them on issues that truly need attention."
- `[interview_turn:T098]` "I’d want the wizard to show one step at a time with a short progress indicator so users can see they are moving forward. The messages should be plain and reassuring, like telling them how many products are ready, how many need review, and exactly what the next action is. For errors, I’d prefer red highlights only where needed, plus a calm explanation and a clear fix option, so the user feels guided rather than punished."
- `[interview_turn:T100]` "I’d keep the design very plain and predictable, with the same button positions and terminology throughout both flows. For visual cues, I’d use color sparingly, mainly to point out errors and confirmations, and rely more on labels, icons, and inline messages than on big alarms or popups. The messaging should sound calm and practical, explaining what happened, why it matters, and what the user can do next in one short sentence."

### [QR-006] (stated)
The interface shall use color sparingly and rely more on labels, icons, and inline messages than on alarms or popups.

**Source Evidence:**
- `[interview_turn:T100]` "I’d keep the design very plain and predictable, with the same button positions and terminology throughout both flows. For visual cues, I’d use color sparingly, mainly to point out errors and confirmations, and rely more on labels, icons, and inline messages than on big alarms or popups. The messaging should sound calm and practical, explaining what happened, why it matters, and what the user can do next in one short sentence."

### [QR-007] (stated)
The system shall keep browsing, cart checkout, order processing, and product updates responsive during normal growth and seasonal spikes.

**Source Evidence:**
- `[interview_turn:T056]` "I’d expect it to handle normal growth without staff noticing much difference, so browsing, cart updates, and order entry should stay responsive even as traffic increases. If the store gets busy, it should still let owners and staff process orders and update products without lag or timeouts. I don’t know the exact volume yet, but I’d want it to feel reliable enough that a small business could grow into a busy season without needing a bigger system right away."
- `[interview_turn:T058]` "I don’t have exact numbers yet, but I’d want it to handle a small business’s normal day plus a noticeable seasonal spike, like a promotion or holiday rush, without staff seeing slowdowns. The most important things to stay fast would be customer browsing, cart checkout, and staff order processing, since those directly affect sales. Product updates can be a little less urgent, but they still shouldn’t feel sluggish if someone is trying to correct stock or pricing during a busy period."
- `[interview_turn:T060]` "I’d want it to scale in a way that new stores can be added without each one affecting the others. From a user perspective, that means the system should keep page loads quick, save changes reliably, and not drop orders or updates even when activity picks up. I don’t know the technical approach we’d use, but I’d definitely expect the platform to handle growth behind the scenes without forcing store owners or staff to change how they work."

### [QR-008] (stated)
The system shall save changes reliably.

**Source Evidence:**
- `[interview_turn:T060]` "I’d want it to scale in a way that new stores can be added without each one affecting the others. From a user perspective, that means the system should keep page loads quick, save changes reliably, and not drop orders or updates even when activity picks up. I don’t know the technical approach we’d use, but I’d definitely expect the platform to handle growth behind the scenes without forcing store owners or staff to change how they work."

### [QR-009] (stated)
The system shall not drop orders or updates when activity increases.

**Source Evidence:**
- `[interview_turn:T060]` "I’d want it to scale in a way that new stores can be added without each one affecting the others. From a user perspective, that means the system should keep page loads quick, save changes reliably, and not drop orders or updates even when activity picks up. I don’t know the technical approach we’d use, but I’d definitely expect the platform to handle growth behind the scenes without forcing store owners or staff to change how they work."

### [QR-010] (stated)
The import wizard shall show a progress bar or progress indicator and a current step label.

**Source Evidence:**
- `[interview_turn:T090]` "In the import wizard, I’d want a clear step indicator, a progress bar, and plain messages that say what stage the user is on and what still needs attention. If something blocks the import, it should be shown right next to the problem row or field, with a simple explanation and a suggested fix, not a generic failure message. When most data is good, the system should say that explicitly, like telling the user how many items are ready to import and how many only need minor review, so they feel encouraged instead of stuck.
For order validation, the feedback should appear before the final submit button is activated, or at least immediately after the user finishes the form, with the missing or incorrect fields highlighted. It would help if the message explains exactly what to do, like adding a postal code or choosing a shipping method, and then keeps the user on the same screen so they can correct it quickly."
- `[interview_turn:T102]` "I’d want the wizard to break the import into small, visible steps so the user always knows where they are. A simple progress bar, a current step label, and brief confirmation messages after each stage would help a lot. If there’s an error, it should be shown right at the item or field, with a plain explanation and a quick way to fix it, so the user can keep moving instead of feeling stopped."

### [QR-011] (stated)
The import wizard shall provide a clear, predictable layout with consistent button positions and terminology.

**Source Evidence:**
- `[interview_turn:T100]` "I’d keep the design very plain and predictable, with the same button positions and terminology throughout both flows. For visual cues, I’d use color sparingly, mainly to point out errors and confirmations, and rely more on labels, icons, and inline messages than on big alarms or popups. The messaging should sound calm and practical, explaining what happened, why it matters, and what the user can do next in one short sentence."

### [QR-012] (stated)
The system shall make automation optional during import suggestions and let users override suggestions.

**Source Evidence:**
- `[interview_turn:T086]` "I think that would be very important, especially for people who are not comfortable with spreadsheets or retail terminology. The automation should be clearly presented as suggestions or default fixes, not silent changes, and the user should always be able to accept, edit, or reject each one. That way the system helps reduce mistakes and speed things up, but the seller still feels in control of their catalog."
- `[interview_turn:T094]` "I think those helpers are important, but they should stay secondary to the basic import flow in the first release. They should appear as optional suggestions or fixes the user can review, not as automatic changes that might surprise them. The best presentation would be a simple suggestion panel or inline prompt with a clear accept, edit, or ignore choice for each item."

### [QR-013] (stated)
The system shall keep the import process manageable by showing small steps, progress feedback, and clear counts of items needing attention.

**Source Evidence:**
- `[interview_turn:T080]` "I’d keep it in small steps with one decision at a time, so the user never feels like they’re staring at a huge form. The wizard should show a live preview after column mapping, then highlight only the rows with issues and explain them in plain language, with buttons to fix, ignore, or apply a suggested correction. It would also help to show progress and a simple count of how many items are ready versus how many still need attention, so users can see they’re getting through it."
- `[interview_turn:T084]` "I’d want it to feel like a guided checklist rather than a technical setup screen. Each step should be short, with plain-language explanations, a preview of what the system understood, and an easy way to go back if something looks wrong. It would also help a lot if the wizard reassures users with messages like “most items are ready” and only stops them on issues that truly need attention."
- `[interview_turn:T090]` "In the import wizard, I’d want a clear step indicator, a progress bar, and plain messages that say what stage the user is on and what still needs attention. If something blocks the import, it should be shown right next to the problem row or field, with a simple explanation and a suggested fix, not a generic failure message. When most data is good, the system should say that explicitly, like telling the user how many items are ready to import and how many only need minor review, so they feel encouraged instead of stuck.
For order validation, the feedback should appear before the final submit button is activated, or at least immediately after the user finishes the form, with the missing or incorrect fields highlighted. It would help if the message explains exactly what to do, like adding a postal code or choosing a shipping method, and then keeps the user on the same screen so they can correct it quickly."
- `[interview_turn:T098]` "I’d want the wizard to show one step at a time with a short progress indicator so users can see they are moving forward. The messages should be plain and reassuring, like telling them how many products are ready, how many need review, and exactly what the next action is. For errors, I’d prefer red highlights only where needed, plus a calm explanation and a clear fix option, so the user feels guided rather than punished."
- `[interview_turn:T102]` "I’d want the wizard to break the import into small, visible steps so the user always knows where they are. A simple progress bar, a current step label, and brief confirmation messages after each stage would help a lot. If there’s an error, it should be shown right at the item or field, with a plain explanation and a quick way to fix it, so the user can keep moving instead of feeling stopped."

## 7. Exceptions and Boundary Conditions

### [EX-001] (stated)
If a payment fails, the customer shall see a clear message and the order shall remain unpaid for staff visibility.

**Source Evidence:**
- `[interview_turn:T044]` "If a payment fails, the customer should get a clear message right away with a chance to try again or use a different method, and staff should be able to see that the order is still unpaid. For shipping delays or failed updates, I’d want the store staff to get an alert so they can follow up manually, while the customer sees a simple status update rather than silence. It would also help to have a manual override or retry option for staff, but only with a record of who used it and why."

### [EX-002] (stated)
If shipping updates are delayed or fail, staff shall receive an alert and the customer shall see a simple status update.

**Source Evidence:**
- `[interview_turn:T044]` "If a payment fails, the customer should get a clear message right away with a chance to try again or use a different method, and staff should be able to see that the order is still unpaid. For shipping delays or failed updates, I’d want the store staff to get an alert so they can follow up manually, while the customer sees a simple status update rather than silence. It would also help to have a manual override or retry option for staff, but only with a record of who used it and why."

### [EX-003] (stated)
If a manual override is used, the system shall record the staff member, the reason, the original error, the action taken, and the time.

**Source Evidence:**
- `[interview_turn:T052]` "In practice, staff should see the error on the order or shipment screen, along with a plain-language explanation and a suggested next step like retry, contact the customer, or correct the details. If they choose a manual override, the system should require a reason and the staff member’s identity before saving the change, so there’s a clear history. An audit trail showing the original error, the action taken, the time, and who handled it would be the most helpful for tracking and later review."

### [EX-004] (stated)
If an import problem blocks completion, the issue shall be shown next to the affected row or field with a simple explanation and suggested fix.

**Source Evidence:**
- `[interview_turn:T090]` "In the import wizard, I’d want a clear step indicator, a progress bar, and plain messages that say what stage the user is on and what still needs attention. If something blocks the import, it should be shown right next to the problem row or field, with a simple explanation and a suggested fix, not a generic failure message. When most data is good, the system should say that explicitly, like telling the user how many items are ready to import and how many only need minor review, so they feel encouraged instead of stuck.
For order validation, the feedback should appear before the final submit button is activated, or at least immediately after the user finishes the form, with the missing or incorrect fields highlighted. It would help if the message explains exactly what to do, like adding a postal code or choosing a shipping method, and then keeps the user on the same screen so they can correct it quickly."
- `[interview_turn:T102]` "I’d want the wizard to break the import into small, visible steps so the user always knows where they are. A simple progress bar, a current step label, and brief confirmation messages after each stage would help a lot. If there’s an error, it should be shown right at the item or field, with a plain explanation and a quick way to fix it, so the user can keep moving instead of feeling stopped."

### [EX-005] (stated)
If order validation fails, the customer shall remain on the checkout page and be told exactly what to correct.

**Source Evidence:**
- `[interview_turn:T090]` "In the import wizard, I’d want a clear step indicator, a progress bar, and plain messages that say what stage the user is on and what still needs attention. If something blocks the import, it should be shown right next to the problem row or field, with a simple explanation and a suggested fix, not a generic failure message. When most data is good, the system should say that explicitly, like telling the user how many items are ready to import and how many only need minor review, so they feel encouraged instead of stuck.
For order validation, the feedback should appear before the final submit button is activated, or at least immediately after the user finishes the form, with the missing or incorrect fields highlighted. It would help if the message explains exactly what to do, like adding a postal code or choosing a shipping method, and then keeps the user on the same screen so they can correct it quickly."
- `[interview_turn:T092]` "For the initial launch, product import should definitely include file upload, field mapping, preview, and validation before anything is committed. It needs to catch missing required fields, duplicate entries, and format problems, and it should let users correct issues without restarting the whole import. I’d also want a clear success summary at the end that tells them what came in and what was skipped.
For order validation, the must-have behavior is to check the customer’s required information before the order is submitted, especially shipping details and payment-related fields. If something is wrong, the system should explain it in simple terms and keep the customer on the checkout page so they can fix it right away. That kind of feedback is important because it makes the process feel safe and understandable for new users."

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
The exact payment gateway vendor for the initial release has not yet been decided.

**Source Evidence:**
- `[interview_turn:T042]` "I know payment processing will be important, because customers need a smooth checkout experience, but I’m not sure yet which gateway we’ll standardize on. Shipping support would also be useful so orders can move from placed to fulfilled without a lot of manual re-entry, and that would save staff time. If we connect to inventory tools later, that would help keep stock numbers accurate, but I’d need to check with the team on which external systems are actually in scope for the first release."
- `[interview_turn:T046]` "For the initial release, I’d expect at least one mainstream payment gateway and basic shipping carrier support, but I can’t name the exact vendors yet without checking with the team. I don’t think we need a full inventory system integration on day one if the store can manage stock inside GAMMA-J, though that could come later. These integrations would mainly save owners and sales staff from retyping order and shipment details, and they’d make checkout and fulfillment feel more professional for customers."
- `[interview_turn:T050]` "For the first release, I’d keep it limited to one payment gateway, one shipping carrier integration, and the store’s own built-in product and stock management. I don’t have the exact vendor names locked down yet, so I’d need to confirm those with the business team before committing. The main value is that owners and sales staff can process orders, confirm payments, and generate shipping info without switching tools all the time, which should make day-to-day work much faster and less error-prone."

### [UN-002]
The exact shipping carrier vendor for the initial release has not yet been decided.

**Source Evidence:**
- `[interview_turn:T046]` "For the initial release, I’d expect at least one mainstream payment gateway and basic shipping carrier support, but I can’t name the exact vendors yet without checking with the team. I don’t think we need a full inventory system integration on day one if the store can manage stock inside GAMMA-J, though that could come later. These integrations would mainly save owners and sales staff from retyping order and shipment details, and they’d make checkout and fulfillment feel more professional for customers."
- `[interview_turn:T050]` "For the first release, I’d keep it limited to one payment gateway, one shipping carrier integration, and the store’s own built-in product and stock management. I don’t have the exact vendor names locked down yet, so I’d need to confirm those with the business team before committing. The main value is that owners and sales staff can process orders, confirm payments, and generate shipping info without switching tools all the time, which should make day-to-day work much faster and less error-prone."

### [UN-003]
The exact integrations and technical constraints beyond the initial payment and shipping support have not yet been confirmed with the team.

**Source Evidence:**
- `[interview_turn:T008]` "We expect it to be a web-based system that runs in a standard browser, since the users we’re targeting shouldn’t need special software installed. It should work well for people with limited technical experience, so we’d want the interface to stay simple and the setup process to be guided. I don’t have firm decisions yet on integrations or specific technical constraints, so those would need to be checked with the team."
- `[interview_turn:T042]` "I know payment processing will be important, because customers need a smooth checkout experience, but I’m not sure yet which gateway we’ll standardize on. Shipping support would also be useful so orders can move from placed to fulfilled without a lot of manual re-entry, and that would save staff time. If we connect to inventory tools later, that would help keep stock numbers accurate, but I’d need to check with the team on which external systems are actually in scope for the first release."
- `[interview_turn:T046]` "For the initial release, I’d expect at least one mainstream payment gateway and basic shipping carrier support, but I can’t name the exact vendors yet without checking with the team. I don’t think we need a full inventory system integration on day one if the store can manage stock inside GAMMA-J, though that could come later. These integrations would mainly save owners and sales staff from retyping order and shipment details, and they’d make checkout and fulfillment feel more professional for customers."

### [UN-004]
The exact legal jurisdictions and resulting compliance specifics for consumer-facing rules have not yet been verified.

**Source Evidence:**
- `[interview_turn:T062]` "We’ll definitely need to comply with standard data protection and privacy requirements, since the system will store customer account information and order history. Consumer-facing rules around refunds, order confirmation, and clear pricing will matter too, but I’d need to verify the exact legal jurisdictions before being specific. I’d also expect basic security and recordkeeping practices so we can show who changed what and when if there’s ever a dispute."
- `[interview_turn:T064]` "I’d want customer data collection to be limited to what’s actually needed for the order and account, with clear consent and privacy notices shown during signup and checkout. Users should also get order confirmations and any refund or cancellation notices automatically, because that helps both compliance and customer trust. For staff, the system should keep good logs of edits to customer records, prices, orders, and payments so we can trace changes if there’s ever a complaint or audit."
