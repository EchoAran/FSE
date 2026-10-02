# Software Requirements Specification: GAMMA-J Web Store

## 1. Scope and Context

### [SC-001] (stated)
The web store shall enable people who are new to online commerce to set up and operate an online retail business.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business. Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
- `[interview_turn:T002]` "The main goal is to make it very easy for people who are new to online commerce to get a store up and running without needing a lot of technical help. We want store owners and sales staff to be able to add and maintain products, manage customer accounts, and process orders confidently through a simple interface.
Success for us would mean a new owner can start selling quickly, keep product and customer information current, and handle orders without getting stuck. From a business standpoint, we’d also look for fewer support requests, smoother day-to-day operations, and customers being able to browse, cart, and buy without problems."

## 2. Actors

None specified.

## 3. Functional Requirements

### [FR-001] (stated)
The system shall allow store owners and sales personnel to add and maintain products.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business. Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
- `[interview_turn:T002]` "The main goal is to make it very easy for people who are new to online commerce to get a store up and running without needing a lot of technical help. We want store owners and sales staff to be able to add and maintain products, manage customer accounts, and process orders confidently through a simple interface.
Success for us would mean a new owner can start selling quickly, keep product and customer information current, and handle orders without getting stuck. From a business standpoint, we’d also look for fewer support requests, smoother day-to-day operations, and customers being able to browse, cart, and buy without problems."

### [FR-002] (stated)
The system shall allow store owners and sales personnel to manage customer accounts.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business. Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
- `[interview_turn:T002]` "The main goal is to make it very easy for people who are new to online commerce to get a store up and running without needing a lot of technical help. We want store owners and sales staff to be able to add and maintain products, manage customer accounts, and process orders confidently through a simple interface.
Success for us would mean a new owner can start selling quickly, keep product and customer information current, and handle orders without getting stuck. From a business standpoint, we’d also look for fewer support requests, smoother day-to-day operations, and customers being able to browse, cart, and buy without problems."

### [FR-003] (stated)
The system shall allow customers to browse available products.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business. Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
- `[interview_turn:T002]` "The main goal is to make it very easy for people who are new to online commerce to get a store up and running without needing a lot of technical help. We want store owners and sales staff to be able to add and maintain products, manage customer accounts, and process orders confidently through a simple interface.
Success for us would mean a new owner can start selling quickly, keep product and customer information current, and handle orders without getting stuck. From a business standpoint, we’d also look for fewer support requests, smoother day-to-day operations, and customers being able to browse, cart, and buy without problems."

### [FR-004] (stated)
The system shall allow customers to maintain a shopping cart.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business. Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
- `[interview_turn:T002]` "The main goal is to make it very easy for people who are new to online commerce to get a store up and running without needing a lot of technical help. We want store owners and sales staff to be able to add and maintain products, manage customer accounts, and process orders confidently through a simple interface.
Success for us would mean a new owner can start selling quickly, keep product and customer information current, and handle orders without getting stuck. From a business standpoint, we’d also look for fewer support requests, smoother day-to-day operations, and customers being able to browse, cart, and buy without problems."

### [FR-005] (stated)
The system shall allow customers to place orders through the store.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business. Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
- `[interview_turn:T002]` "The main goal is to make it very easy for people who are new to online commerce to get a store up and running without needing a lot of technical help. We want store owners and sales staff to be able to add and maintain products, manage customer accounts, and process orders confidently through a simple interface.
Success for us would mean a new owner can start selling quickly, keep product and customer information current, and handle orders without getting stuck. From a business standpoint, we’d also look for fewer support requests, smoother day-to-day operations, and customers being able to browse, cart, and buy without problems."

### [FR-006] (stated)
Store owners and sales personnel shall sign in with their own accounts.

**Source Evidence:**
- `[interview_turn:T006]` "Store owners and sales personnel should sign in with their own accounts, and customers should have separate customer logins if they want to place orders or view their account history. Owners should have full access to manage products, customer accounts, and overall store settings, while sales personnel should have more limited access, mainly to products, customers, and order handling, but not to administrative settings. Customers should only be able to view and change their own profile, cart, and orders. For sensitive actions like deleting records, changing order status, or making major account changes, I’d expect tighter restrictions for staff, but I don’t have a finalized approval rule beyond that and would need to check with the business side."

### [FR-007] (conditional)
Customers shall have separate customer logins if they want to place orders or view their account history.

**Source Evidence:**
- `[interview_turn:T006]` "Store owners and sales personnel should sign in with their own accounts, and customers should have separate customer logins if they want to place orders or view their account history. Owners should have full access to manage products, customer accounts, and overall store settings, while sales personnel should have more limited access, mainly to products, customers, and order handling, but not to administrative settings. Customers should only be able to view and change their own profile, cart, and orders. For sensitive actions like deleting records, changing order status, or making major account changes, I’d expect tighter restrictions for staff, but I don’t have a finalized approval rule beyond that and would need to check with the business side."

### [FR-008] (stated)
The system shall support card payments as the standard checkout payment option.

**Source Evidence:**
- `[interview_turn:T010]` "We definitely need card payments as the standard option, and PayPal would be a strong second choice if it’s practical to include. I don’t think we want to rely on cash on delivery as a default because it adds risk and extra handling, though I wouldn’t rule it out for special cases. Bank transfer could be useful for some customers, but I’d want the store to keep the payment options simple at launch rather than support everything at once."

### [FR-009] (conditional)
The system shall support PayPal if it is practical to include.

**Source Evidence:**
- `[interview_turn:T010]` "We definitely need card payments as the standard option, and PayPal would be a strong second choice if it’s practical to include. I don’t think we want to rely on cash on delivery as a default because it adds risk and extra handling, though I wouldn’t rule it out for special cases. Bank transfer could be useful for some customers, but I’d want the store to keep the payment options simple at launch rather than support everything at once."

### [FR-010] (stated)
The system shall support at least the order statuses new, paid, packed, shipped, completed, and cancelled.

**Source Evidence:**
- `[interview_turn:T014]` "We should at least support a basic flow like new, paid, packed, shipped, completed, and cancelled. Sales personnel or owners should be able to move orders forward as work is done, but customers should probably only be able to cancel before shipping, and maybe request a return after delivery if we support that process. Once an order is marked shipped, I’d expect changes to be limited and controlled by staff, and cancellation should usually no longer be allowed unless there’s a special exception."

### [FR-011] (stated)
The system shall provide low-stock warnings.

**Source Evidence:**
- `[interview_turn:T016]` "We should definitely have low-stock warnings, but I don’t have a fixed threshold number yet. My expectation is that the threshold should be configurable, ideally per product and maybe also by category for some items, because fast-moving products will need earlier alerts than slow sellers. The warnings should go to store owners and the staff responsible for purchasing or inventory, so they can restock before we run out."

### [FR-012] (stated)
Low-stock warnings shall be sent to store owners and the staff responsible for purchasing or inventory.

**Source Evidence:**
- `[interview_turn:T016]` "We should definitely have low-stock warnings, but I don’t have a fixed threshold number yet. My expectation is that the threshold should be configurable, ideally per product and maybe also by category for some items, because fast-moving products will need earlier alerts than slow sellers. The warnings should go to store owners and the staff responsible for purchasing or inventory, so they can restock before we run out."

### [FR-013] (stated)
At launch, the system shall support a standard delivery shipping option.

**Source Evidence:**
- `[interview_turn:T018]` "At launch, I’d keep shipping fairly simple with a standard delivery option and an express option if we can support it. Customers should see the available methods at checkout based on their destination, and the shipping cost should be calculated from basic rules like region and possibly weight or order total, rather than something overly complex. If an address can’t be served by a method, the system should just hide that option instead of letting the customer pick it."

### [FR-014] (conditional)
At launch, the system shall support an express shipping option if it can be supported.

**Source Evidence:**
- `[interview_turn:T018]` "At launch, I’d keep shipping fairly simple with a standard delivery option and an express option if we can support it. Customers should see the available methods at checkout based on their destination, and the shipping cost should be calculated from basic rules like region and possibly weight or order total, rather than something overly complex. If an address can’t be served by a method, the system should just hide that option instead of letting the customer pick it."

### [FR-015] (stated)
The system shall support self-service customer registration with immediate access.

**Source Evidence:**
- `[interview_turn:T020]` "I’d prefer self-service registration with immediate access, because the goal is to make this easy for people who are new to online commerce. I don’t think we need a manual approval step for ordinary customers at launch, though we may want to hold an account if something looks suspicious or if verification fails. In that case, a simple pending or blocked status would be enough for now."

### [FR-016] (conditional)
The system shall support pending and blocked customer account statuses.

**Source Evidence:**
- `[interview_turn:T020]` "I’d prefer self-service registration with immediate access, because the goal is to make this easy for people who are new to online commerce. I don’t think we need a manual approval step for ordinary customers at launch, though we may want to hold an account if something looks suspicious or if verification fails. In that case, a simple pending or blocked status would be enough for now."

### [FR-017] (stated)
At launch, the store owner shall be able to set store name, contact details, currency, tax settings, shipping methods, and payment options during initial setup.

**Source Evidence:**
- `[interview_turn:T022]` "At launch, the owner should be able to set the basics during initial setup, like store name, contact details, currency, tax settings, shipping methods, and payment options. Product management and customer account management can happen afterward in normal administration, but the store shouldn’t go live until the core settings are complete. I’d also want a few required fields for the storefront itself, like business address or legal details if those are needed for checkout and invoices."

## 4. Business Rules and Constraints

### [BR-001] (stated)
Staff shall only be able to create or edit products that are active in the catalog.

**Source Evidence:**
- `[interview_turn:T004]` "For products, I’d expect staff to only be able to create or edit items that are active in the catalog, and the store should not allow selling more than what’s in stock unless we later decide to support backorders. Customer accounts should have basic validation so we don’t end up with duplicate or incomplete records, but I don’t have a finalized approval process for new accounts. For carts and orders, the store should prevent checkout if required customer or shipping details are missing, and an order should only be placed when the cart is confirmed and the items are still available. If an order has already been processed, changing it should be restricted and probably require a staff override or cancellation workflow, but the exact rules there still need to be confirmed with the team."

### [BR-002] (conditional)
The store shall not allow selling more than what is in stock unless backorders are later supported.

**Source Evidence:**
- `[interview_turn:T004]` "For products, I’d expect staff to only be able to create or edit items that are active in the catalog, and the store should not allow selling more than what’s in stock unless we later decide to support backorders. Customer accounts should have basic validation so we don’t end up with duplicate or incomplete records, but I don’t have a finalized approval process for new accounts. For carts and orders, the store should prevent checkout if required customer or shipping details are missing, and an order should only be placed when the cart is confirmed and the items are still available. If an order has already been processed, changing it should be restricted and probably require a staff override or cancellation workflow, but the exact rules there still need to be confirmed with the team."

### [BR-003] (stated)
Customer accounts shall be subject to basic validation to avoid duplicate or incomplete records.

**Source Evidence:**
- `[interview_turn:T004]` "For products, I’d expect staff to only be able to create or edit items that are active in the catalog, and the store should not allow selling more than what’s in stock unless we later decide to support backorders. Customer accounts should have basic validation so we don’t end up with duplicate or incomplete records, but I don’t have a finalized approval process for new accounts. For carts and orders, the store should prevent checkout if required customer or shipping details are missing, and an order should only be placed when the cart is confirmed and the items are still available. If an order has already been processed, changing it should be restricted and probably require a staff override or cancellation workflow, but the exact rules there still need to be confirmed with the team."

### [BR-004] (stated)
The system shall prevent checkout if required customer details are missing.

**Source Evidence:**
- `[interview_turn:T004]` "For products, I’d expect staff to only be able to create or edit items that are active in the catalog, and the store should not allow selling more than what’s in stock unless we later decide to support backorders. Customer accounts should have basic validation so we don’t end up with duplicate or incomplete records, but I don’t have a finalized approval process for new accounts. For carts and orders, the store should prevent checkout if required customer or shipping details are missing, and an order should only be placed when the cart is confirmed and the items are still available. If an order has already been processed, changing it should be restricted and probably require a staff override or cancellation workflow, but the exact rules there still need to be confirmed with the team."

### [BR-005] (stated)
The system shall prevent checkout if required shipping details are missing.

**Source Evidence:**
- `[interview_turn:T004]` "For products, I’d expect staff to only be able to create or edit items that are active in the catalog, and the store should not allow selling more than what’s in stock unless we later decide to support backorders. Customer accounts should have basic validation so we don’t end up with duplicate or incomplete records, but I don’t have a finalized approval process for new accounts. For carts and orders, the store should prevent checkout if required customer or shipping details are missing, and an order should only be placed when the cart is confirmed and the items are still available. If an order has already been processed, changing it should be restricted and probably require a staff override or cancellation workflow, but the exact rules there still need to be confirmed with the team."

### [BR-006] (stated)
An order shall only be placed when the cart is confirmed and the items are still available.

**Source Evidence:**
- `[interview_turn:T004]` "For products, I’d expect staff to only be able to create or edit items that are active in the catalog, and the store should not allow selling more than what’s in stock unless we later decide to support backorders. Customer accounts should have basic validation so we don’t end up with duplicate or incomplete records, but I don’t have a finalized approval process for new accounts. For carts and orders, the store should prevent checkout if required customer or shipping details are missing, and an order should only be placed when the cart is confirmed and the items are still available. If an order has already been processed, changing it should be restricted and probably require a staff override or cancellation workflow, but the exact rules there still need to be confirmed with the team."

### [BR-007] (conditional)
If an order has already been processed, changing it shall be restricted.

**Source Evidence:**
- `[interview_turn:T004]` "For products, I’d expect staff to only be able to create or edit items that are active in the catalog, and the store should not allow selling more than what’s in stock unless we later decide to support backorders. Customer accounts should have basic validation so we don’t end up with duplicate or incomplete records, but I don’t have a finalized approval process for new accounts. For carts and orders, the store should prevent checkout if required customer or shipping details are missing, and an order should only be placed when the cart is confirmed and the items are still available. If an order has already been processed, changing it should be restricted and probably require a staff override or cancellation workflow, but the exact rules there still need to be confirmed with the team."

### [BR-008] (stated)
Store owners shall have full access to manage products, customer accounts, and overall store settings.

**Source Evidence:**
- `[interview_turn:T006]` "Store owners and sales personnel should sign in with their own accounts, and customers should have separate customer logins if they want to place orders or view their account history. Owners should have full access to manage products, customer accounts, and overall store settings, while sales personnel should have more limited access, mainly to products, customers, and order handling, but not to administrative settings. Customers should only be able to view and change their own profile, cart, and orders. For sensitive actions like deleting records, changing order status, or making major account changes, I’d expect tighter restrictions for staff, but I don’t have a finalized approval rule beyond that and would need to check with the business side."

### [BR-009] (stated)
Sales personnel shall have limited access mainly to products, customers, and order handling, but not to administrative settings.

**Source Evidence:**
- `[interview_turn:T006]` "Store owners and sales personnel should sign in with their own accounts, and customers should have separate customer logins if they want to place orders or view their account history. Owners should have full access to manage products, customer accounts, and overall store settings, while sales personnel should have more limited access, mainly to products, customers, and order handling, but not to administrative settings. Customers should only be able to view and change their own profile, cart, and orders. For sensitive actions like deleting records, changing order status, or making major account changes, I’d expect tighter restrictions for staff, but I don’t have a finalized approval rule beyond that and would need to check with the business side."

### [BR-010] (stated)
Customers shall only be able to view and change their own profile, cart, and orders.

**Source Evidence:**
- `[interview_turn:T006]` "Store owners and sales personnel should sign in with their own accounts, and customers should have separate customer logins if they want to place orders or view their account history. Owners should have full access to manage products, customer accounts, and overall store settings, while sales personnel should have more limited access, mainly to products, customers, and order handling, but not to administrative settings. Customers should only be able to view and change their own profile, cart, and orders. For sensitive actions like deleting records, changing order status, or making major account changes, I’d expect tighter restrictions for staff, but I don’t have a finalized approval rule beyond that and would need to check with the business side."

### [BR-011] (conditional)
For sensitive actions such as deleting records, changing order status, or making major account changes, tighter restrictions shall apply for staff.

**Source Evidence:**
- `[interview_turn:T006]` "Store owners and sales personnel should sign in with their own accounts, and customers should have separate customer logins if they want to place orders or view their account history. Owners should have full access to manage products, customer accounts, and overall store settings, while sales personnel should have more limited access, mainly to products, customers, and order handling, but not to administrative settings. Customers should only be able to view and change their own profile, cart, and orders. For sensitive actions like deleting records, changing order status, or making major account changes, I’d expect tighter restrictions for staff, but I don’t have a finalized approval rule beyond that and would need to check with the business side."

### [BR-012] (stated)
The system shall support clear pricing at checkout.

**Source Evidence:**
- `[interview_turn:T008]` "At a business level, we need the store to support clear pricing at checkout, but I don’t have the tax model fully decided yet. My assumption would be that prices are shown before tax unless the customer’s region expects tax-inclusive display, and tax should be calculated based on location rather than the product alone, but that needs confirmation. We also expect to support discounts or promotions later, and any rounding should be handled consistently at checkout so the customer sees the final total clearly."

### [BR-013] (conditional)
Prices are expected to be shown before tax unless the customer's region expects tax-inclusive display.

**Source Evidence:**
- `[interview_turn:T008]` "At a business level, we need the store to support clear pricing at checkout, but I don’t have the tax model fully decided yet. My assumption would be that prices are shown before tax unless the customer’s region expects tax-inclusive display, and tax should be calculated based on location rather than the product alone, but that needs confirmation. We also expect to support discounts or promotions later, and any rounding should be handled consistently at checkout so the customer sees the final total clearly."

### [BR-014] (conditional)
Tax should be calculated based on location rather than the product alone, subject to confirmation.

**Source Evidence:**
- `[interview_turn:T008]` "At a business level, we need the store to support clear pricing at checkout, but I don’t have the tax model fully decided yet. My assumption would be that prices are shown before tax unless the customer’s region expects tax-inclusive display, and tax should be calculated based on location rather than the product alone, but that needs confirmation. We also expect to support discounts or promotions later, and any rounding should be handled consistently at checkout so the customer sees the final total clearly."

### [BR-015] (stated)
Rounding shall be handled consistently at checkout so the customer sees the final total clearly.

**Source Evidence:**
- `[interview_turn:T008]` "At a business level, we need the store to support clear pricing at checkout, but I don’t have the tax model fully decided yet. My assumption would be that prices are shown before tax unless the customer’s region expects tax-inclusive display, and tax should be calculated based on location rather than the product alone, but that needs confirmation. We also expect to support discounts or promotions later, and any rounding should be handled consistently at checkout so the customer sees the final total clearly."

### [BR-016] (stated)
The store should keep payment options simple at launch rather than support everything at once.

**Source Evidence:**
- `[interview_turn:T010]` "We definitely need card payments as the standard option, and PayPal would be a strong second choice if it’s practical to include. I don’t think we want to rely on cash on delivery as a default because it adds risk and extra handling, though I wouldn’t rule it out for special cases. Bank transfer could be useful for some customers, but I’d want the store to keep the payment options simple at launch rather than support everything at once."

### [BR-017] (stated)
The system shall require the core shipping address fields: name, street address, city, postal code, country, and a contact phone or email.

**Source Evidence:**
- `[interview_turn:T012]` "We should require the usual core address fields: name, street address, city, postal code, country, and a contact phone or email so shipping problems can be resolved. The system should validate the format as much as possible based on the selected country or region, but I’d still want it to be forgiving enough for international addresses rather than forcing one rigid format. Checkout should be blocked if the address is incomplete or clearly invalid, though I’d expect some manual exception handling for edge cases like rural deliveries or businesses with special delivery instructions."

### [BR-018] (stated)
The system shall validate shipping address format as much as possible based on the selected country or region.

**Source Evidence:**
- `[interview_turn:T012]` "We should require the usual core address fields: name, street address, city, postal code, country, and a contact phone or email so shipping problems can be resolved. The system should validate the format as much as possible based on the selected country or region, but I’d still want it to be forgiving enough for international addresses rather than forcing one rigid format. Checkout should be blocked if the address is incomplete or clearly invalid, though I’d expect some manual exception handling for edge cases like rural deliveries or businesses with special delivery instructions."

### [BR-019] (stated)
The system shall be forgiving enough to accept international addresses rather than forcing one rigid format.

**Source Evidence:**
- `[interview_turn:T012]` "We should require the usual core address fields: name, street address, city, postal code, country, and a contact phone or email so shipping problems can be resolved. The system should validate the format as much as possible based on the selected country or region, but I’d still want it to be forgiving enough for international addresses rather than forcing one rigid format. Checkout should be blocked if the address is incomplete or clearly invalid, though I’d expect some manual exception handling for edge cases like rural deliveries or businesses with special delivery instructions."

### [BR-020] (stated)
Checkout shall be blocked if the shipping address is incomplete or clearly invalid.

**Source Evidence:**
- `[interview_turn:T012]` "We should require the usual core address fields: name, street address, city, postal code, country, and a contact phone or email so shipping problems can be resolved. The system should validate the format as much as possible based on the selected country or region, but I’d still want it to be forgiving enough for international addresses rather than forcing one rigid format. Checkout should be blocked if the address is incomplete or clearly invalid, though I’d expect some manual exception handling for edge cases like rural deliveries or businesses with special delivery instructions."

### [BR-021] (stated)
Sales personnel or owners shall be able to move orders forward as work is done.

**Source Evidence:**
- `[interview_turn:T014]` "We should at least support a basic flow like new, paid, packed, shipped, completed, and cancelled. Sales personnel or owners should be able to move orders forward as work is done, but customers should probably only be able to cancel before shipping, and maybe request a return after delivery if we support that process. Once an order is marked shipped, I’d expect changes to be limited and controlled by staff, and cancellation should usually no longer be allowed unless there’s a special exception."

### [BR-022] (conditional)
Customers shall probably only be able to cancel an order before shipping.

**Source Evidence:**
- `[interview_turn:T014]` "We should at least support a basic flow like new, paid, packed, shipped, completed, and cancelled. Sales personnel or owners should be able to move orders forward as work is done, but customers should probably only be able to cancel before shipping, and maybe request a return after delivery if we support that process. Once an order is marked shipped, I’d expect changes to be limited and controlled by staff, and cancellation should usually no longer be allowed unless there’s a special exception."

### [BR-023] (conditional)
Customers may be able to request a return after delivery if that process is supported.

**Source Evidence:**
- `[interview_turn:T014]` "We should at least support a basic flow like new, paid, packed, shipped, completed, and cancelled. Sales personnel or owners should be able to move orders forward as work is done, but customers should probably only be able to cancel before shipping, and maybe request a return after delivery if we support that process. Once an order is marked shipped, I’d expect changes to be limited and controlled by staff, and cancellation should usually no longer be allowed unless there’s a special exception."

### [BR-024] (stated)
Once an order is marked shipped, changes shall be limited and controlled by staff.

**Source Evidence:**
- `[interview_turn:T014]` "We should at least support a basic flow like new, paid, packed, shipped, completed, and cancelled. Sales personnel or owners should be able to move orders forward as work is done, but customers should probably only be able to cancel before shipping, and maybe request a return after delivery if we support that process. Once an order is marked shipped, I’d expect changes to be limited and controlled by staff, and cancellation should usually no longer be allowed unless there’s a special exception."

### [BR-025] (conditional)
Cancellation should usually no longer be allowed once an order is marked shipped unless there is a special exception.

**Source Evidence:**
- `[interview_turn:T014]` "We should at least support a basic flow like new, paid, packed, shipped, completed, and cancelled. Sales personnel or owners should be able to move orders forward as work is done, but customers should probably only be able to cancel before shipping, and maybe request a return after delivery if we support that process. Once an order is marked shipped, I’d expect changes to be limited and controlled by staff, and cancellation should usually no longer be allowed unless there’s a special exception."

### [BR-026] (conditional)
The low-stock threshold shall be configurable, ideally per product and possibly by category.

**Source Evidence:**
- `[interview_turn:T016]` "We should definitely have low-stock warnings, but I don’t have a fixed threshold number yet. My expectation is that the threshold should be configurable, ideally per product and maybe also by category for some items, because fast-moving products will need earlier alerts than slow sellers. The warnings should go to store owners and the staff responsible for purchasing or inventory, so they can restock before we run out."

### [BR-027] (stated)
Customers shall see available shipping methods at checkout based on their destination.

**Source Evidence:**
- `[interview_turn:T018]` "At launch, I’d keep shipping fairly simple with a standard delivery option and an express option if we can support it. Customers should see the available methods at checkout based on their destination, and the shipping cost should be calculated from basic rules like region and possibly weight or order total, rather than something overly complex. If an address can’t be served by a method, the system should just hide that option instead of letting the customer pick it."

### [BR-028] (conditional)
Shipping cost shall be calculated from basic rules such as region and possibly weight or order total.

**Source Evidence:**
- `[interview_turn:T018]` "At launch, I’d keep shipping fairly simple with a standard delivery option and an express option if we can support it. Customers should see the available methods at checkout based on their destination, and the shipping cost should be calculated from basic rules like region and possibly weight or order total, rather than something overly complex. If an address can’t be served by a method, the system should just hide that option instead of letting the customer pick it."

### [BR-029] (stated)
If an address cannot be served by a shipping method, the system shall hide that option instead of letting the customer pick it.

**Source Evidence:**
- `[interview_turn:T018]` "At launch, I’d keep shipping fairly simple with a standard delivery option and an express option if we can support it. Customers should see the available methods at checkout based on their destination, and the shipping cost should be calculated from basic rules like region and possibly weight or order total, rather than something overly complex. If an address can’t be served by a method, the system should just hide that option instead of letting the customer pick it."

### [BR-030] (stated)
The system shall not require a manual approval step for ordinary customers at launch.

**Source Evidence:**
- `[interview_turn:T020]` "I’d prefer self-service registration with immediate access, because the goal is to make this easy for people who are new to online commerce. I don’t think we need a manual approval step for ordinary customers at launch, though we may want to hold an account if something looks suspicious or if verification fails. In that case, a simple pending or blocked status would be enough for now."

### [BR-031] (conditional)
The system may hold a customer account if something looks suspicious or if verification fails.

**Source Evidence:**
- `[interview_turn:T020]` "I’d prefer self-service registration with immediate access, because the goal is to make this easy for people who are new to online commerce. I don’t think we need a manual approval step for ordinary customers at launch, though we may want to hold an account if something looks suspicious or if verification fails. In that case, a simple pending or blocked status would be enough for now."

### [BR-032] (stated)
Product management and customer account management may occur after initial setup in normal administration.

**Source Evidence:**
- `[interview_turn:T022]` "At launch, the owner should be able to set the basics during initial setup, like store name, contact details, currency, tax settings, shipping methods, and payment options. Product management and customer account management can happen afterward in normal administration, but the store shouldn’t go live until the core settings are complete. I’d also want a few required fields for the storefront itself, like business address or legal details if those are needed for checkout and invoices."

### [BR-033] (stated)
The store shall not go live until the core settings are complete.

**Source Evidence:**
- `[interview_turn:T022]` "At launch, the owner should be able to set the basics during initial setup, like store name, contact details, currency, tax settings, shipping methods, and payment options. Product management and customer account management can happen afterward in normal administration, but the store shouldn’t go live until the core settings are complete. I’d also want a few required fields for the storefront itself, like business address or legal details if those are needed for checkout and invoices."

### [BR-034] (conditional)
The storefront shall require business address or legal details if those are needed for checkout and invoices.

**Source Evidence:**
- `[interview_turn:T022]` "At launch, the owner should be able to set the basics during initial setup, like store name, contact details, currency, tax settings, shipping methods, and payment options. Product management and customer account management can happen afterward in normal administration, but the store shouldn’t go live until the core settings are complete. I’d also want a few required fields for the storefront itself, like business address or legal details if those are needed for checkout and invoices."

## 5. Data and External Interfaces

None specified.

## 6. Quality Requirements

### [QR-001] (stated)
The system shall provide a simple interface that allows store owners and sales staff to manage products, customer accounts, and order processing with minimal technical help.

**Source Evidence:**
- `[interview_turn:T002]` "The main goal is to make it very easy for people who are new to online commerce to get a store up and running without needing a lot of technical help. We want store owners and sales staff to be able to add and maintain products, manage customer accounts, and process orders confidently through a simple interface.
Success for us would mean a new owner can start selling quickly, keep product and customer information current, and handle orders without getting stuck. From a business standpoint, we’d also look for fewer support requests, smoother day-to-day operations, and customers being able to browse, cart, and buy without problems."

## 7. Exceptions and Boundary Conditions

None specified.

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
The tax model and final tax rules are not yet fully decided.

**Source Evidence:**
- `[interview_turn:T008]` "At a business level, we need the store to support clear pricing at checkout, but I don’t have the tax model fully decided yet. My assumption would be that prices are shown before tax unless the customer’s region expects tax-inclusive display, and tax should be calculated based on location rather than the product alone, but that needs confirmation. We also expect to support discounts or promotions later, and any rounding should be handled consistently at checkout so the customer sees the final total clearly."

### [UN-002]
The support for discounts or promotions is planned for later and is not yet part of the confirmed launch scope.

**Source Evidence:**
- `[interview_turn:T008]` "At a business level, we need the store to support clear pricing at checkout, but I don’t have the tax model fully decided yet. My assumption would be that prices are shown before tax unless the customer’s region expects tax-inclusive display, and tax should be calculated based on location rather than the product alone, but that needs confirmation. We also expect to support discounts or promotions later, and any rounding should be handled consistently at checkout so the customer sees the final total clearly."

### [UN-003]
Cash on delivery is not the default payment method, but its availability for special cases is not yet decided.

**Source Evidence:**
- `[interview_turn:T010]` "We definitely need card payments as the standard option, and PayPal would be a strong second choice if it’s practical to include. I don’t think we want to rely on cash on delivery as a default because it adds risk and extra handling, though I wouldn’t rule it out for special cases. Bank transfer could be useful for some customers, but I’d want the store to keep the payment options simple at launch rather than support everything at once."

### [UN-004]
Bank transfer may be useful, but whether it will be supported at launch is not yet decided.

**Source Evidence:**
- `[interview_turn:T010]` "We definitely need card payments as the standard option, and PayPal would be a strong second choice if it’s practical to include. I don’t think we want to rely on cash on delivery as a default because it adds risk and extra handling, though I wouldn’t rule it out for special cases. Bank transfer could be useful for some customers, but I’d want the store to keep the payment options simple at launch rather than support everything at once."

### [UN-005]
Manual exception handling for edge cases such as rural deliveries or businesses with special delivery instructions is expected, but the exact handling is not yet specified.

**Source Evidence:**
- `[interview_turn:T012]` "We should require the usual core address fields: name, street address, city, postal code, country, and a contact phone or email so shipping problems can be resolved. The system should validate the format as much as possible based on the selected country or region, but I’d still want it to be forgiving enough for international addresses rather than forcing one rigid format. Checkout should be blocked if the address is incomplete or clearly invalid, though I’d expect some manual exception handling for edge cases like rural deliveries or businesses with special delivery instructions."

### [UN-006]
The low-stock warning threshold number is not yet fixed.

**Source Evidence:**
- `[interview_turn:T016]` "We should definitely have low-stock warnings, but I don’t have a fixed threshold number yet. My expectation is that the threshold should be configurable, ideally per product and maybe also by category for some items, because fast-moving products will need earlier alerts than slow sellers. The warnings should go to store owners and the staff responsible for purchasing or inventory, so they can restock before we run out."
