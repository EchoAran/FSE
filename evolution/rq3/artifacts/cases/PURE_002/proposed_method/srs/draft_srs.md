# Software Requirements Specification: GAMMA-J Web Store

## 1. Scope and Context

### [SC-001] (stated)
The system shall provide a web store for people who are new to online commerce so they can set up and operate an online retail business.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business. Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
- `[interview_turn:T002]` "The main goal is to help new store owners get selling online quickly without needing much technical knowledge, so they can set up a storefront, manage what they sell, and start taking orders. For the first version, we want support for fairly standard retail products, like items with names, descriptions, prices, and available quantities, and the day-to-day work of adding or updating products, managing customer accounts, handling carts, and processing orders. We’re not trying to cover every possible retail scenario at the beginning, just the core operations needed to run a small online shop reliably."

### [SC-002] (conditional)
The first release shall focus on a basic small-shop workflow with core retail operations only, excluding specialized product types, complicated order flows, subscriptions, marketplace selling, complex promotions, multi-warehouse inventory, and deep accounting or ERP integrations.

**Source Evidence:**
- `[interview_turn:T004]` "I’d prefer a limited pilot scope for the first launch. It should cover a basic small-shop workflow with a straightforward product catalog, regular customer accounts, shopping cart, and standard order placement, but not specialized product types or complicated order flows yet. That would let us validate the core experience and keep it manageable for users who are new to online commerce."
- `[interview_turn:T068]` "For the first release, I’d keep it focused on the core shop workflow: product catalog, customer accounts, cart, checkout, order processing, and basic admin management. I would leave out more advanced things like subscriptions, marketplace selling, complex promotions, multi-warehouse inventory, and deep accounting or ERP integrations. If an item or order is unusual, I’d expect staff to handle it manually outside the system rather than building a special automated path right away."
- `[interview_turn:T082]` "Yes, anything beyond the basic store setup, product management, cart, ordering, and customer account handling should be treated as a nice-to-have for later. Things like advanced reporting, promotions, automatic syncing, and richer onboarding tools can come after the core launch if they don’t slow down delivery. My priority is getting a simple, reliable store that new operators can actually run without too much complexity."

## 2. Actors

### [ACT-001] (stated)
Store owners shall be able to handle overall setup, product management, customer oversight, and business settings.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business. Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
- `[interview_turn:T012]` "Store owners need to handle the overall setup, product management, customer oversight, and business settings, while sales personnel should focus on routine updates like maintaining products, helping with customer accounts, and reviewing orders. Customers need to browse products, manage their cart, and place orders without getting into back-office functions. The main limits matter around who can change what, because we’d want customers completely separated from administrative work, and we’d probably want some actions reserved for owners rather than general staff."

### [ACT-002] (stated)
Sales personnel shall be able to maintain products, help with customer accounts, review orders, and perform routine store updates.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business. Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
- `[interview_turn:T012]` "Store owners need to handle the overall setup, product management, customer oversight, and business settings, while sales personnel should focus on routine updates like maintaining products, helping with customer accounts, and reviewing orders. Customers need to browse products, manage their cart, and place orders without getting into back-office functions. The main limits matter around who can change what, because we’d want customers completely separated from administrative work, and we’d probably want some actions reserved for owners rather than general staff."
- `[interview_turn:T066]` "The basics should be very easy, especially adding and editing products, updating prices and stock, managing customer accounts, and checking orders. A new store operator should be able to do those from the web interface without any technical setup. I’d also want simple tools for changing order status and handling common customer issues without needing a developer."

### [ACT-003] (stated)
Customers shall be able to browse products, manage their shopping cart, and place orders.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business. Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
- `[interview_turn:T012]` "Store owners need to handle the overall setup, product management, customer oversight, and business settings, while sales personnel should focus on routine updates like maintaining products, helping with customer accounts, and reviewing orders. Customers need to browse products, manage their cart, and place orders without getting into back-office functions. The main limits matter around who can change what, because we’d want customers completely separated from administrative work, and we’d probably want some actions reserved for owners rather than general staff."

### [ACT-004] (stated)
Customers shall be separated from administrative work and shall not access back-office functions.

**Source Evidence:**
- `[interview_turn:T012]` "Store owners need to handle the overall setup, product management, customer oversight, and business settings, while sales personnel should focus on routine updates like maintaining products, helping with customer accounts, and reviewing orders. Customers need to browse products, manage their cart, and place orders without getting into back-office functions. The main limits matter around who can change what, because we’d want customers completely separated from administrative work, and we’d probably want some actions reserved for owners rather than general staff."

## 3. Functional Requirements

### [FR-001] (stated)
The system shall allow store operators to set up a storefront.

**Source Evidence:**
- `[interview_turn:T002]` "The main goal is to help new store owners get selling online quickly without needing much technical knowledge, so they can set up a storefront, manage what they sell, and start taking orders. For the first version, we want support for fairly standard retail products, like items with names, descriptions, prices, and available quantities, and the day-to-day work of adding or updating products, managing customer accounts, handling carts, and processing orders. We’re not trying to cover every possible retail scenario at the beginning, just the core operations needed to run a small online shop reliably."

### [FR-002] (stated)
The system shall allow users to manage products.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business. Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
- `[interview_turn:T002]` "The main goal is to help new store owners get selling online quickly without needing much technical knowledge, so they can set up a storefront, manage what they sell, and start taking orders. For the first version, we want support for fairly standard retail products, like items with names, descriptions, prices, and available quantities, and the day-to-day work of adding or updating products, managing customer accounts, handling carts, and processing orders. We’re not trying to cover every possible retail scenario at the beginning, just the core operations needed to run a small online shop reliably."

### [FR-003] (stated)
The system shall support standard retail products with names, descriptions, prices, and available quantities.

**Source Evidence:**
- `[interview_turn:T002]` "The main goal is to help new store owners get selling online quickly without needing much technical knowledge, so they can set up a storefront, manage what they sell, and start taking orders. For the first version, we want support for fairly standard retail products, like items with names, descriptions, prices, and available quantities, and the day-to-day work of adding or updating products, managing customer accounts, handling carts, and processing orders. We’re not trying to cover every possible retail scenario at the beginning, just the core operations needed to run a small online shop reliably."

### [FR-004] (stated)
The system shall allow staff to add products and update products.

**Source Evidence:**
- `[interview_turn:T002]` "The main goal is to help new store owners get selling online quickly without needing much technical knowledge, so they can set up a storefront, manage what they sell, and start taking orders. For the first version, we want support for fairly standard retail products, like items with names, descriptions, prices, and available quantities, and the day-to-day work of adding or updating products, managing customer accounts, handling carts, and processing orders. We’re not trying to cover every possible retail scenario at the beginning, just the core operations needed to run a small online shop reliably."
- `[interview_turn:T066]` "The basics should be very easy, especially adding and editing products, updating prices and stock, managing customer accounts, and checking orders. A new store operator should be able to do those from the web interface without any technical setup. I’d also want simple tools for changing order status and handling common customer issues without needing a developer."

### [FR-005] (stated)
The system shall allow staff to manage customer accounts.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business. Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
- `[interview_turn:T002]` "The main goal is to help new store owners get selling online quickly without needing much technical knowledge, so they can set up a storefront, manage what they sell, and start taking orders. For the first version, we want support for fairly standard retail products, like items with names, descriptions, prices, and available quantities, and the day-to-day work of adding or updating products, managing customer accounts, handling carts, and processing orders. We’re not trying to cover every possible retail scenario at the beginning, just the core operations needed to run a small online shop reliably."
- `[interview_turn:T066]` "The basics should be very easy, especially adding and editing products, updating prices and stock, managing customer accounts, and checking orders. A new store operator should be able to do those from the web interface without any technical setup. I’d also want simple tools for changing order status and handling common customer issues without needing a developer."

### [FR-006] (stated)
The system shall allow customers to browse products through clear categories and simple filtering.

**Source Evidence:**
- `[interview_turn:T030]` "Usually they’ll start from categories or a search box, then narrow down by what they need, price, or other filters. Since many of our customers may be new to online shopping, the store should make browsing very straightforward with clear categories, simple product descriptions, and helpful filtering so they can compare options without needing to know exact product names. If they start broad, the system should guide them toward the right items rather than force them to search precisely."

### [FR-007] (stated)
The system shall allow customers to maintain a shopping cart.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business. Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
- `[interview_turn:T002]` "The main goal is to help new store owners get selling online quickly without needing much technical knowledge, so they can set up a storefront, manage what they sell, and start taking orders. For the first version, we want support for fairly standard retail products, like items with names, descriptions, prices, and available quantities, and the day-to-day work of adding or updating products, managing customer accounts, handling carts, and processing orders. We’re not trying to cover every possible retail scenario at the beginning, just the core operations needed to run a small online shop reliably."

### [FR-008] (stated)
The system shall allow customers to place orders through the store.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business. Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
- `[interview_turn:T002]` "The main goal is to help new store owners get selling online quickly without needing much technical knowledge, so they can set up a storefront, manage what they sell, and start taking orders. For the first version, we want support for fairly standard retail products, like items with names, descriptions, prices, and available quantities, and the day-to-day work of adding or updating products, managing customer accounts, handling carts, and processing orders. We’re not trying to cover every possible retail scenario at the beginning, just the core operations needed to run a small online shop reliably."

### [FR-009] (conditional)
The system shall support product catalog onboarding by manual entry or file import when file import is supported.

**Source Evidence:**
- `[interview_turn:T020]` "We’d expect the store owner or staff to load the initial product catalog before the site goes live, either by entering products manually or importing them from an existing file if we support that. After the data is loaded, someone should review the listings for correctness, images, pricing, and availability, then mark the catalog ready for customers. If anything is incomplete, it should stay hidden or unavailable until it’s fixed."
- `[interview_turn:T022]` "Yes, that’s likely to be needed if the business already has product data somewhere else, especially for the first launch. Clean records should be brought over into the new catalog, and anything that doesn’t map cleanly should be reported for manual review instead of guessed at automatically. If a record is incomplete, I’d rather have it skipped or marked as needing attention until someone corrects it."
- `[interview_turn:T072]` "For the first pass, I’d keep imports pretty simple and stick to common files like CSV or maybe Excel, with staff uploading them through the web interface. Every imported row should be validated before it goes live, and if something conflicts with existing product data, the system should either stop that row or flag it for review rather than silently overwriting it. For future automatic syncing, I’d want the same rule: no unexpected changes going live without validation, and clear reporting when there’s a mismatch so a non-technical operator can see what needs attention."

### [FR-010] (stated)
The system shall allow an initial product catalog to be loaded before the site goes live.

**Source Evidence:**
- `[interview_turn:T020]` "We’d expect the store owner or staff to load the initial product catalog before the site goes live, either by entering products manually or importing them from an existing file if we support that. After the data is loaded, someone should review the listings for correctness, images, pricing, and availability, then mark the catalog ready for customers. If anything is incomplete, it should stay hidden or unavailable until it’s fixed."

### [FR-011] (stated)
The system shall allow staff to review loaded product listings for correctness, images, pricing, and availability before marking the catalog ready for customers.

**Source Evidence:**
- `[interview_turn:T020]` "We’d expect the store owner or staff to load the initial product catalog before the site goes live, either by entering products manually or importing them from an existing file if we support that. After the data is loaded, someone should review the listings for correctness, images, pricing, and availability, then mark the catalog ready for customers. If anything is incomplete, it should stay hidden or unavailable until it’s fixed."

### [FR-012] (stated)
The system shall allow staff to mark the catalog ready for customers after review.

**Source Evidence:**
- `[interview_turn:T020]` "We’d expect the store owner or staff to load the initial product catalog before the site goes live, either by entering products manually or importing them from an existing file if we support that. After the data is loaded, someone should review the listings for correctness, images, pricing, and availability, then mark the catalog ready for customers. If anything is incomplete, it should stay hidden or unavailable until it’s fixed."

### [FR-013] (stated)
The system shall allow customers to browse products by categories or search and narrow results using price or other filters.

**Source Evidence:**
- `[interview_turn:T030]` "Usually they’ll start from categories or a search box, then narrow down by what they need, price, or other filters. Since many of our customers may be new to online shopping, the store should make browsing very straightforward with clear categories, simple product descriptions, and helpful filtering so they can compare options without needing to know exact product names. If they start broad, the system should guide them toward the right items rather than force them to search precisely."

### [FR-014] (stated)
The system shall support secure logins and password reset for account protection.

**Source Evidence:**
- `[interview_turn:T006]` "For the first release, I’d want the store to use standard account protection like secure logins and password reset, and to flag anything obviously suspicious rather than trying to handle every edge case automatically. For payments, we should rely on a trusted payment provider so we’re not storing sensitive card details ourselves. Personal data should be kept to the minimum needed to fulfill orders, and if something looks risky we should block or review the transaction instead of letting it go through unchecked."

### [FR-015] (stated)
The system shall flag obviously suspicious activity rather than attempting to handle every edge case automatically.

**Source Evidence:**
- `[interview_turn:T006]` "For the first release, I’d want the store to use standard account protection like secure logins and password reset, and to flag anything obviously suspicious rather than trying to handle every edge case automatically. For payments, we should rely on a trusted payment provider so we’re not storing sensitive card details ourselves. Personal data should be kept to the minimum needed to fulfill orders, and if something looks risky we should block or review the transaction instead of letting it go through unchecked."

### [FR-016] (stated)
The system shall rely on a trusted payment provider and shall not store sensitive card details itself.

**Source Evidence:**
- `[interview_turn:T006]` "For the first release, I’d want the store to use standard account protection like secure logins and password reset, and to flag anything obviously suspicious rather than trying to handle every edge case automatically. For payments, we should rely on a trusted payment provider so we’re not storing sensitive card details ourselves. Personal data should be kept to the minimum needed to fulfill orders, and if something looks risky we should block or review the transaction instead of letting it go through unchecked."

### [FR-017] (stated)
The system shall minimize the personal data collected to what is needed to fulfill orders.

**Source Evidence:**
- `[interview_turn:T006]` "For the first release, I’d want the store to use standard account protection like secure logins and password reset, and to flag anything obviously suspicious rather than trying to handle every edge case automatically. For payments, we should rely on a trusted payment provider so we’re not storing sensitive card details ourselves. Personal data should be kept to the minimum needed to fulfill orders, and if something looks risky we should block or review the transaction instead of letting it go through unchecked."
- `[interview_turn:T080]` "Yes, a few cases should be stricter than the default. If an order looks unusual, especially with a high value, mismatched customer details, or repeated failed payment attempts, I’d want it held for review before it goes any further. For personal data, I’d only want to collect what’s necessary to complete the order, and anything sensitive should be handled carefully with tighter access than normal store data."
- `[interview_turn:T084]` "We should avoid storing anything that isn’t needed to process and fulfill the order, so I’d exclude extra personal details like unnecessary profile fields or full payment information if the payment provider can handle that. Only the minimum contact and shipping information needed for the order should be kept. Sensitive data should be limited to a small set of authorized store staff, probably sales or admin roles, and not broadly visible to everyone who can use the system."

### [FR-018] (stated)
The system shall block or review transactions that look risky.

**Source Evidence:**
- `[interview_turn:T006]` "For the first release, I’d want the store to use standard account protection like secure logins and password reset, and to flag anything obviously suspicious rather than trying to handle every edge case automatically. For payments, we should rely on a trusted payment provider so we’re not storing sensitive card details ourselves. Personal data should be kept to the minimum needed to fulfill orders, and if something looks risky we should block or review the transaction instead of letting it go through unchecked."

### [FR-019] (stated)
The system shall record administrative changes in an audit log.

**Source Evidence:**
- `[interview_turn:T008]` "Yes, definitely. We should record who made the change, what they changed, when it happened, and the before-and-after values for important fields like product price, stock, order status, or customer account status. That log is mainly for troubleshooting and accountability, so it doesn’t need to be extremely verbose, but it should be enough to reconstruct what happened if there’s a dispute or mistake."

### [FR-020] (stated)
The audit log shall record who made the change, what changed, when it happened, and the before-and-after values for important fields.

**Source Evidence:**
- `[interview_turn:T008]` "Yes, definitely. We should record who made the change, what they changed, when it happened, and the before-and-after values for important fields like product price, stock, order status, or customer account status. That log is mainly for troubleshooting and accountability, so it doesn’t need to be extremely verbose, but it should be enough to reconstruct what happened if there’s a dispute or mistake."

### [FR-021] (stated)
The system shall record before-and-after values for important fields such as product price, stock, order status, and customer account status.

**Source Evidence:**
- `[interview_turn:T008]` "Yes, definitely. We should record who made the change, what they changed, when it happened, and the before-and-after values for important fields like product price, stock, order status, or customer account status. That log is mainly for troubleshooting and accountability, so it doesn’t need to be extremely verbose, but it should be enough to reconstruct what happened if there’s a dispute or mistake."

### [FR-022] (stated)
The system shall remain responsive under increased browsing demand and shall slow down gracefully or queue non-urgent actions rather than fail outright when demand suddenly rises.

**Source Evidence:**
- `[interview_turn:T010]` "The biggest pressure will probably be keeping the site responsive when more people are browsing at once, especially during promotions or busy periods, and making sure orders don’t get lost if traffic spikes. If demand suddenly rises, I’d rather the store slow down gracefully or queue non-urgent actions than fail outright, and if part of the service is unavailable, it should clearly tell users what’s affected and let them come back later without losing their cart or order progress. We’d also want the system to keep the important sales functions available as much as possible, even if some admin features are temporarily reduced."

### [FR-023] (stated)
The system shall preserve cart and order progress when part of the service is unavailable.

**Source Evidence:**
- `[interview_turn:T010]` "The biggest pressure will probably be keeping the site responsive when more people are browsing at once, especially during promotions or busy periods, and making sure orders don’t get lost if traffic spikes. If demand suddenly rises, I’d rather the store slow down gracefully or queue non-urgent actions than fail outright, and if part of the service is unavailable, it should clearly tell users what’s affected and let them come back later without losing their cart or order progress. We’d also want the system to keep the important sales functions available as much as possible, even if some admin features are temporarily reduced."

### [FR-024] (stated)
The system shall clearly tell users what is affected when part of the service is unavailable.

**Source Evidence:**
- `[interview_turn:T010]` "The biggest pressure will probably be keeping the site responsive when more people are browsing at once, especially during promotions or busy periods, and making sure orders don’t get lost if traffic spikes. If demand suddenly rises, I’d rather the store slow down gracefully or queue non-urgent actions than fail outright, and if part of the service is unavailable, it should clearly tell users what’s affected and let them come back later without losing their cart or order progress. We’d also want the system to keep the important sales functions available as much as possible, even if some admin features are temporarily reduced."

### [FR-025] (stated)
The system shall keep important sales functions available as much as possible even if some admin features are temporarily reduced.

**Source Evidence:**
- `[interview_turn:T010]` "The biggest pressure will probably be keeping the site responsive when more people are browsing at once, especially during promotions or busy periods, and making sure orders don’t get lost if traffic spikes. If demand suddenly rises, I’d rather the store slow down gracefully or queue non-urgent actions than fail outright, and if part of the service is unavailable, it should clearly tell users what’s affected and let them come back later without losing their cart or order progress. We’d also want the system to keep the important sales functions available as much as possible, even if some admin features are temporarily reduced."

### [FR-026] (stated)
The system shall allow product images to be uploaded with one main image and a small number of additional images.

**Source Evidence:**
- `[interview_turn:T014]` "For the first release, I’d keep the media rules pretty simple. A product should be able to have one main image and maybe a small number of additional images, with common formats like JPG and PNG allowed, and if an upload fails or the file is invalid, the system should reject it clearly and let the user try again without saving a broken product record. If an image is missing, the product can still exist, but it should show a default placeholder so the listing doesn’t break."

### [FR-027] (stated)
The system shall allow common image formats such as JPG and PNG.

**Source Evidence:**
- `[interview_turn:T014]` "For the first release, I’d keep the media rules pretty simple. A product should be able to have one main image and maybe a small number of additional images, with common formats like JPG and PNG allowed, and if an upload fails or the file is invalid, the system should reject it clearly and let the user try again without saving a broken product record. If an image is missing, the product can still exist, but it should show a default placeholder so the listing doesn’t break."

### [FR-028] (stated)
If an image upload fails or the file is invalid, the system shall reject the upload clearly and allow the user to try again without saving a broken product record.

**Source Evidence:**
- `[interview_turn:T014]` "For the first release, I’d keep the media rules pretty simple. A product should be able to have one main image and maybe a small number of additional images, with common formats like JPG and PNG allowed, and if an upload fails or the file is invalid, the system should reject it clearly and let the user try again without saving a broken product record. If an image is missing, the product can still exist, but it should show a default placeholder so the listing doesn’t break."

### [FR-029] (stated)
If a product image is missing, the product shall still exist and shall show a default placeholder.

**Source Evidence:**
- `[interview_turn:T014]` "For the first release, I’d keep the media rules pretty simple. A product should be able to have one main image and maybe a small number of additional images, with common formats like JPG and PNG allowed, and if an upload fails or the file is invalid, the system should reject it clearly and let the user try again without saving a broken product record. If an image is missing, the product can still exist, but it should show a default placeholder so the listing doesn’t break."

### [FR-030] (stated)
A product shall be purchasable only when it is marked active and available for sale.

**Source Evidence:**
- `[interview_turn:T016]` "A product should only be purchasable when it’s marked active and available for sale, with a valid price and stock if stock control is being used. If the price changes, I’d want the updated price to apply to new carts and new orders, but not unexpectedly change an order that’s already been placed. If something is out of stock or not yet available, it should be clearly shown as unavailable and the customer shouldn’t be able to complete checkout for it."

### [FR-031] (conditional)
When stock control is being used, a product shall be purchasable only when it has valid stock.

**Source Evidence:**
- `[interview_turn:T016]` "A product should only be purchasable when it’s marked active and available for sale, with a valid price and stock if stock control is being used. If the price changes, I’d want the updated price to apply to new carts and new orders, but not unexpectedly change an order that’s already been placed. If something is out of stock or not yet available, it should be clearly shown as unavailable and the customer shouldn’t be able to complete checkout for it."

### [FR-032] (stated)
When a product price changes, the updated price shall apply to new carts and new orders but shall not unexpectedly change an order that has already been placed.

**Source Evidence:**
- `[interview_turn:T016]` "A product should only be purchasable when it’s marked active and available for sale, with a valid price and stock if stock control is being used. If the price changes, I’d want the updated price to apply to new carts and new orders, but not unexpectedly change an order that’s already been placed. If something is out of stock or not yet available, it should be clearly shown as unavailable and the customer shouldn’t be able to complete checkout for it."

### [FR-033] (stated)
If a product is out of stock or not yet available, the system shall show it as unavailable and shall prevent checkout for it.

**Source Evidence:**
- `[interview_turn:T016]` "A product should only be purchasable when it’s marked active and available for sale, with a valid price and stock if stock control is being used. If the price changes, I’d want the updated price to apply to new carts and new orders, but not unexpectedly change an order that’s already been placed. If something is out of stock or not yet available, it should be clearly shown as unavailable and the customer shouldn’t be able to complete checkout for it."

### [FR-034] (conditional)
The system shall support minimum and maximum quantities per product.

**Source Evidence:**
- `[interview_turn:T018]` "Yes, we should probably support basic limits like minimum and maximum quantities per product, and possibly a maximum total quantity or value per order if the business needs it. If a cart goes outside those limits, the system should flag it before checkout and tell the customer exactly what needs to be adjusted, rather than failing only at the final step. I’m not sure yet whether we need customer-specific limits, so I’d want to check that with the business team."

### [FR-035] (conditional)
The system shall support a maximum total quantity or value per order if the business needs it.

**Source Evidence:**
- `[interview_turn:T018]` "Yes, we should probably support basic limits like minimum and maximum quantities per product, and possibly a maximum total quantity or value per order if the business needs it. If a cart goes outside those limits, the system should flag it before checkout and tell the customer exactly what needs to be adjusted, rather than failing only at the final step. I’m not sure yet whether we need customer-specific limits, so I’d want to check that with the business team."

### [FR-036] (stated)
If a cart exceeds quantity or value limits, the system shall flag the issue before checkout and tell the customer exactly what must be adjusted.

**Source Evidence:**
- `[interview_turn:T018]` "Yes, we should probably support basic limits like minimum and maximum quantities per product, and possibly a maximum total quantity or value per order if the business needs it. If a cart goes outside those limits, the system should flag it before checkout and tell the customer exactly what needs to be adjusted, rather than failing only at the final step. I’m not sure yet whether we need customer-specific limits, so I’d want to check that with the business team."
- `[interview_turn:T040]` "Yes, I’d expect some limits on certain products, especially if stock is low or the item has a business rule like a maximum per customer. If a shopper goes over the limit, the cart should clearly flag the issue and stop checkout until they reduce the quantity or remove the item. It shouldn’t fail silently, because that would be confusing for new customers."

### [FR-037] (conditional)
The system shall support import of the initial product catalog from an existing file if file import is supported.

**Source Evidence:**
- `[interview_turn:T020]` "We’d expect the store owner or staff to load the initial product catalog before the site goes live, either by entering products manually or importing them from an existing file if we support that. After the data is loaded, someone should review the listings for correctness, images, pricing, and availability, then mark the catalog ready for customers. If anything is incomplete, it should stay hidden or unavailable until it’s fixed."
- `[interview_turn:T022]` "Yes, that’s likely to be needed if the business already has product data somewhere else, especially for the first launch. Clean records should be brought over into the new catalog, and anything that doesn’t map cleanly should be reported for manual review instead of guessed at automatically. If a record is incomplete, I’d rather have it skipped or marked as needing attention until someone corrects it."

### [FR-038] (stated)
The system shall report records that do not map cleanly during migration for manual review instead of guessing automatically.

**Source Evidence:**
- `[interview_turn:T022]` "Yes, that’s likely to be needed if the business already has product data somewhere else, especially for the first launch. Clean records should be brought over into the new catalog, and anything that doesn’t map cleanly should be reported for manual review instead of guessed at automatically. If a record is incomplete, I’d rather have it skipped or marked as needing attention until someone corrects it."

### [FR-039] (stated)
If a legacy product record is incomplete, the system shall skip it or mark it as needing attention until it is corrected.

**Source Evidence:**
- `[interview_turn:T022]` "Yes, that’s likely to be needed if the business already has product data somewhere else, especially for the first launch. Clean records should be brought over into the new catalog, and anything that doesn’t map cleanly should be reported for manual review instead of guessed at automatically. If a record is incomplete, I’d rather have it skipped or marked as needing attention until someone corrects it."

### [FR-040] (stated)
The system shall allow manual review of legacy product records by a store admin or designated catalog owner.

**Source Evidence:**
- `[interview_turn:T028]` "A manual review should probably go to a store admin or a designated catalog owner, since they’re the ones who know whether the product data is acceptable for launch. The system should track those records as pending or in review, with notes about what’s missing or inconsistent, so they can be worked through one by one. It should stay hidden from customers and not be publishable until the required fields are fixed and someone approves it."

### [FR-041] (stated)
The system shall track manual review records as pending or in review and include notes about what is missing or inconsistent.

**Source Evidence:**
- `[interview_turn:T028]` "A manual review should probably go to a store admin or a designated catalog owner, since they’re the ones who know whether the product data is acceptable for launch. The system should track those records as pending or in review, with notes about what’s missing or inconsistent, so they can be worked through one by one. It should stay hidden from customers and not be publishable until the required fields are fixed and someone approves it."

### [FR-042] (stated)
A record under manual review shall remain hidden from customers and shall not be publishable until the required fields are fixed and someone approves it.

**Source Evidence:**
- `[interview_turn:T028]` "A manual review should probably go to a store admin or a designated catalog owner, since they’re the ones who know whether the product data is acceptable for launch. The system should track those records as pending or in review, with notes about what’s missing or inconsistent, so they can be worked through one by one. It should stay hidden from customers and not be publishable until the required fields are fixed and someone approves it."
- `[interview_turn:T038]` "It should stay in review until the required fields are complete and the inconsistent data is corrected. If the record is incomplete enough that it could cause problems with orders, shipping, or account access, I’d keep it hidden from the customer until it’s fixed. Once the data matches what we need and an admin or authorized staff member approves it, then it can go live."

### [FR-043] (stated)
The system shall support browsing through categories or search and shall guide broad searches toward the right items with clear descriptions and helpful filtering.

**Source Evidence:**
- `[interview_turn:T030]` "Usually they’ll start from categories or a search box, then narrow down by what they need, price, or other filters. Since many of our customers may be new to online shopping, the store should make browsing very straightforward with clear categories, simple product descriptions, and helpful filtering so they can compare options without needing to know exact product names. If they start broad, the system should guide them toward the right items rather than force them to search precisely."

### [FR-044] (stated)
The system shall process customer requests to suspend or delete accounts.

**Source Evidence:**
- `[interview_turn:T032]` "If a customer wants their account suspended or deleted, we should be able to process that request, but I’d expect some cases where deletion can’t happen immediately because of active orders, payment issues, or legal recordkeeping. Suspension could be immediate in most cases, while deletion should probably be checked against any open business obligations first. If there are exceptions, they would need to be handled by an admin rather than automatically."

### [FR-045] (conditional)
Customer account suspension shall be immediate in most cases.

**Source Evidence:**
- `[interview_turn:T032]` "If a customer wants their account suspended or deleted, we should be able to process that request, but I’d expect some cases where deletion can’t happen immediately because of active orders, payment issues, or legal recordkeeping. Suspension could be immediate in most cases, while deletion should probably be checked against any open business obligations first. If there are exceptions, they would need to be handled by an admin rather than automatically."

### [FR-046] (stated)
Customer account deletion shall be delayed when there are active orders, payment issues, legal recordkeeping needs, return cases, refund cases, unresolved support cases, or necessary order history for customer service or accounting.

**Source Evidence:**
- `[interview_turn:T032]` "If a customer wants their account suspended or deleted, we should be able to process that request, but I’d expect some cases where deletion can’t happen immediately because of active orders, payment issues, or legal recordkeeping. Suspension could be immediate in most cases, while deletion should probably be checked against any open business obligations first. If there are exceptions, they would need to be handled by an admin rather than automatically."
- `[interview_turn:T034]` "If the customer is tied to a return, refund, or unresolved support case, I’d treat that as a reason to delay deletion as well. Also, if their account has order history that we still need for customer service or accounting, that may need to stay in place even if the account is otherwise inactive. Beyond that, I’m not sure there are other hard blockers, but I’d want those edge cases checked with the business before we lock the rule down."

### [FR-047] (stated)
If a customer account deletion request cannot be handled automatically because of an exception, an admin shall handle the exception.

**Source Evidence:**
- `[interview_turn:T032]` "If a customer wants their account suspended or deleted, we should be able to process that request, but I’d expect some cases where deletion can’t happen immediately because of active orders, payment issues, or legal recordkeeping. Suspension could be immediate in most cases, while deletion should probably be checked against any open business obligations first. If there are exceptions, they would need to be handled by an admin rather than automatically."

### [FR-048] (conditional)
If a customer account request is not straightforward or cannot be confidently determined as safe, the system shall route it to an admin review queue before suspension or deletion proceeds.

**Source Evidence:**
- `[interview_turn:T036]` "I’d expect admin approval only when the request is not straightforward, like when the account has unresolved disputes, a suspicious activity flag, or there’s some conflict with an open order or refund. For a normal self-service request with no complications, it should probably go through automatically. If the system can’t confidently determine whether it’s safe to proceed, then it should route it to an admin review queue."

### [FR-049] (stated)
The system shall keep a customer record in review until required fields are complete and inconsistent data is corrected.

**Source Evidence:**
- `[interview_turn:T038]` "It should stay in review until the required fields are complete and the inconsistent data is corrected. If the record is incomplete enough that it could cause problems with orders, shipping, or account access, I’d keep it hidden from the customer until it’s fixed. Once the data matches what we need and an admin or authorized staff member approves it, then it can go live."

### [FR-050] (stated)
The system shall keep a customer record hidden from the customer if the incomplete record could cause problems with orders, shipping, or account access.

**Source Evidence:**
- `[interview_turn:T038]` "It should stay in review until the required fields are complete and the inconsistent data is corrected. If the record is incomplete enough that it could cause problems with orders, shipping, or account access, I’d keep it hidden from the customer until it’s fixed. Once the data matches what we need and an admin or authorized staff member approves it, then it can go live."

### [FR-051] (stated)
A customer record shall go live only after the data matches requirements and an admin or authorized staff member approves it.

**Source Evidence:**
- `[interview_turn:T038]` "It should stay in review until the required fields are complete and the inconsistent data is corrected. If the record is incomplete enough that it could cause problems with orders, shipping, or account access, I’d keep it hidden from the customer until it’s fixed. Once the data matches what we need and an admin or authorized staff member approves it, then it can go live."

### [FR-052] (conditional)
If a shopper exceeds a customer-specific limit, the cart shall clearly flag the issue and stop checkout until the quantity is reduced or the item is removed.

**Source Evidence:**
- `[interview_turn:T040]` "Yes, I’d expect some limits on certain products, especially if stock is low or the item has a business rule like a maximum per customer. If a shopper goes over the limit, the cart should clearly flag the issue and stop checkout until they reduce the quantity or remove the item. It shouldn’t fail silently, because that would be confusing for new customers."

### [FR-053] (stated)
After checkout, the system shall show the customer the order number, purchased items, quantities, totals, taxes or fees if applicable, shipping details, and payment status.

**Source Evidence:**
- `[interview_turn:T042]` "After checkout, the customer should see the order number, items purchased, quantities, totals, taxes or fees if applicable, shipping details, and the payment status. Yes, that confirmation should also go out by email, and if we support another channel like SMS later, that could be useful too. The main thing is they need a clear record immediately after placing the order."

### [FR-054] (stated)
The order confirmation shall be sent by email.

**Source Evidence:**
- `[interview_turn:T042]` "After checkout, the customer should see the order number, items purchased, quantities, totals, taxes or fees if applicable, shipping details, and the payment status. Yes, that confirmation should also go out by email, and if we support another channel like SMS later, that could be useful too. The main thing is they need a clear record immediately after placing the order."

### [FR-055] (stated)
The system shall allow products to remain visible but not purchasable when the price is missing, invalid, or inventory is unavailable under stock control.

**Source Evidence:**
- `[interview_turn:T044]` "Yes, that makes sense. If a product is still something we want customers to see, but we can’t actually sell it right now because the price is missing, invalid, or inventory is unavailable under stock control, it should stay visible but be marked as not purchasable. In that case the add-to-cart or checkout action should be blocked, and the customer should get a clear message about why."

### [FR-056] (stated)
When a product is not purchasable, the system shall block add-to-cart and checkout actions and shall show a clear message explaining why.

**Source Evidence:**
- `[interview_turn:T044]` "Yes, that makes sense. If a product is still something we want customers to see, but we can’t actually sell it right now because the price is missing, invalid, or inventory is unavailable under stock control, it should stay visible but be marked as not purchasable. In that case the add-to-cart or checkout action should be blocked, and the customer should get a clear message about why."
- `[interview_turn:T090]` "If a product isn’t purchasable, I’d want the system to block both add-to-cart and checkout, and also make it clear on the product page that it’s unavailable. I don’t think we need to hide the product completely, unless the business wants it out of sight for some reason, but we should definitely prevent any purchase action until price or inventory is back."
- `[interview_turn:T092]` "Yes, that can happen. Sometimes a product may still be shown because we want customers to see it, but it should not be purchasable if the price hasn’t been confirmed yet, inventory is temporarily uncertain, or there’s some approval step still pending. In those cases it should clearly appear unavailable for purchase so nobody can complete an order by mistake."

### [FR-057] (stated)
The system shall validate shipping addresses enough to catch obvious missing or invalid address components.

**Source Evidence:**
- `[interview_turn:T046]` "Yes, the shipping address should be validated enough to catch obvious problems like missing street, city, postal code, or country, and we should flag addresses that look incomplete or invalid. Delivery options should depend on the customer’s location, because not every method will be available everywhere, and some products may have extra restrictions too. If no delivery method is available for that address, checkout should stop and clearly tell the customer that they need to change the address or contact support."

### [FR-058] (stated)
Delivery options shall depend on the customer's location.

**Source Evidence:**
- `[interview_turn:T046]` "Yes, the shipping address should be validated enough to catch obvious problems like missing street, city, postal code, or country, and we should flag addresses that look incomplete or invalid. Delivery options should depend on the customer’s location, because not every method will be available everywhere, and some products may have extra restrictions too. If no delivery method is available for that address, checkout should stop and clearly tell the customer that they need to change the address or contact support."

### [FR-059] (stated)
If no delivery method is available for a shipping address, checkout shall stop and the customer shall be told to change the address or contact support.

**Source Evidence:**
- `[interview_turn:T046]` "Yes, the shipping address should be validated enough to catch obvious problems like missing street, city, postal code, or country, and we should flag addresses that look incomplete or invalid. Delivery options should depend on the customer’s location, because not every method will be available everywhere, and some products may have extra restrictions too. If no delivery method is available for that address, checkout should stop and clearly tell the customer that they need to change the address or contact support."

### [FR-060] (stated)
The payment step shall allow the customer to choose a payment method and confirm the amount before payment is finalized.

**Source Evidence:**
- `[interview_turn:T048]` "From the customer’s point of view, the payment step should be simple and clearly guided, with the customer choosing a payment method and confirming the amount before anything is finalized. After they submit payment, the store should show a clear success or failure message right away, and if it fails, explain what they can do next without making them start over unnecessarily. If the payment is successful, the order should move to confirmation immediately and they should know the purchase is complete."

### [FR-061] (stated)
After payment submission, the system shall show a clear success or failure message right away.

**Source Evidence:**
- `[interview_turn:T048]` "From the customer’s point of view, the payment step should be simple and clearly guided, with the customer choosing a payment method and confirming the amount before anything is finalized. After they submit payment, the store should show a clear success or failure message right away, and if it fails, explain what they can do next without making them start over unnecessarily. If the payment is successful, the order should move to confirmation immediately and they should know the purchase is complete."

### [FR-062] (stated)
If payment fails, the system shall explain what the customer can do next without forcing them to start over unnecessarily.

**Source Evidence:**
- `[interview_turn:T048]` "From the customer’s point of view, the payment step should be simple and clearly guided, with the customer choosing a payment method and confirming the amount before anything is finalized. After they submit payment, the store should show a clear success or failure message right away, and if it fails, explain what they can do next without making them start over unnecessarily. If the payment is successful, the order should move to confirmation immediately and they should know the purchase is complete."
- `[interview_turn:T052]` "They should see a clear message that the payment did not go through, with enough detail to understand whether it was a card issue, a declined transaction, or something on our side. Before the order is confirmed, they should be able to try the payment again, choose a different payment method, or go back and review the order. If only part of the payment completed, I’d want the system to keep the order from confirming until the full amount is resolved."

### [FR-063] (stated)
If payment is successful, the order shall move to confirmation immediately and the customer shall know the purchase is complete.

**Source Evidence:**
- `[interview_turn:T048]` "From the customer’s point of view, the payment step should be simple and clearly guided, with the customer choosing a payment method and confirming the amount before anything is finalized. After they submit payment, the store should show a clear success or failure message right away, and if it fails, explain what they can do next without making them start over unnecessarily. If the payment is successful, the order should move to confirmation immediately and they should know the purchase is complete."

### [FR-064] (stated)
The system shall allow the customer to try payment again, choose a different payment method, or go back and review the order when payment does not go through.

**Source Evidence:**
- `[interview_turn:T052]` "They should see a clear message that the payment did not go through, with enough detail to understand whether it was a card issue, a declined transaction, or something on our side. Before the order is confirmed, they should be able to try the payment again, choose a different payment method, or go back and review the order. If only part of the payment completed, I’d want the system to keep the order from confirming until the full amount is resolved."

### [FR-065] (stated)
If only part of a payment completed, the system shall keep the order from confirming until the full amount is resolved.

**Source Evidence:**
- `[interview_turn:T052]` "They should see a clear message that the payment did not go through, with enough detail to understand whether it was a card issue, a declined transaction, or something on our side. Before the order is confirmed, they should be able to try the payment again, choose a different payment method, or go back and review the order. If only part of the payment completed, I’d want the system to keep the order from confirming until the full amount is resolved."

### [FR-066] (stated)
An order shall start as pending while payment and availability are checked.

**Source Evidence:**
- `[interview_turn:T054]` "Once the order is submitted, it should start as pending while payment and availability are checked. If everything is fine, it can move to confirmed pretty quickly; if there’s a payment problem, stock issue, or anything that needs manual review, it should stay pending or move to a hold or rejected state instead of confirming. For manual review, I’d expect the customer to see that the order is received but not yet finalized, so they know it’s waiting on approval."

### [FR-067] (stated)
If payment is fully accepted, the order is no longer under review, and items are confirmed available to ship, the order may move into fulfillment.

**Source Evidence:**
- `[interview_turn:T060]` "It should only move into fulfillment when payment is fully accepted, the order is no longer under review, and the items are confirmed available to ship. If any item is out of stock, payment is unresolved, or a staff review is still open, it should wait and not go to picking and packing yet. In practice, I’d want the system to be very strict about that so fulfillment only starts when there’s no blocker left."

### [FR-068] (stated)
If any item is out of stock, payment is unresolved, or a staff review is still open, the order shall wait and shall not go to picking and packing.

**Source Evidence:**
- `[interview_turn:T060]` "It should only move into fulfillment when payment is fully accepted, the order is no longer under review, and the items are confirmed available to ship. If any item is out of stock, payment is unresolved, or a staff review is still open, it should wait and not go to picking and packing yet. In practice, I’d want the system to be very strict about that so fulfillment only starts when there’s no blocker left."

### [FR-069] (stated)
The system shall support manual review of orders that have suspicious payment activity, mismatched customer and shipping details, unusual order size, or policy exceptions.

**Source Evidence:**
- `[interview_turn:T056]` "Manual review should look at things like suspicious payment activity, mismatched customer and shipping details, unusual order size, or any policy exceptions we want staff to catch before fulfillment. If it’s approved, the customer should be told the order is confirmed and moving ahead; if it stays on hold, they should know it’s still under review and no action may be needed yet; if it’s rejected, they should be told the order cannot be completed and, if appropriate, whether they need to try again or contact support. I’d keep the customer message fairly high level and avoid exposing internal fraud or security details."

### [FR-070] (stated)
If an order is approved after manual review, the customer shall be told the order is confirmed and moving ahead.

**Source Evidence:**
- `[interview_turn:T056]` "Manual review should look at things like suspicious payment activity, mismatched customer and shipping details, unusual order size, or any policy exceptions we want staff to catch before fulfillment. If it’s approved, the customer should be told the order is confirmed and moving ahead; if it stays on hold, they should know it’s still under review and no action may be needed yet; if it’s rejected, they should be told the order cannot be completed and, if appropriate, whether they need to try again or contact support. I’d keep the customer message fairly high level and avoid exposing internal fraud or security details."

### [FR-071] (stated)
If an order stays on hold after manual review, the customer shall be told it is still under review and no action may be needed yet.

**Source Evidence:**
- `[interview_turn:T056]` "Manual review should look at things like suspicious payment activity, mismatched customer and shipping details, unusual order size, or any policy exceptions we want staff to catch before fulfillment. If it’s approved, the customer should be told the order is confirmed and moving ahead; if it stays on hold, they should know it’s still under review and no action may be needed yet; if it’s rejected, they should be told the order cannot be completed and, if appropriate, whether they need to try again or contact support. I’d keep the customer message fairly high level and avoid exposing internal fraud or security details."

### [FR-072] (stated)
If an order is rejected after manual review, the customer shall be told the order cannot be completed and, if appropriate, whether to try again or contact support.

**Source Evidence:**
- `[interview_turn:T056]` "Manual review should look at things like suspicious payment activity, mismatched customer and shipping details, unusual order size, or any policy exceptions we want staff to catch before fulfillment. If it’s approved, the customer should be told the order is confirmed and moving ahead; if it stays on hold, they should know it’s still under review and no action may be needed yet; if it’s rejected, they should be told the order cannot be completed and, if appropriate, whether they need to try again or contact support. I’d keep the customer message fairly high level and avoid exposing internal fraud or security details."

### [FR-073] (stated)
If staff cannot quickly verify a manual review issue, the order shall remain on hold first.

**Source Evidence:**
- `[interview_turn:T058]` "If staff can’t verify it quickly, I’d keep the order on hold first rather than making a decision too early. If the missing information is something only the customer can provide, then the order should be sent back for customer action with clear instructions on what to update or send in. If it’s an internal issue that still needs investigation, it should stay on hold until staff can approve or reject it."

### [FR-074] (stated)
If missing information in manual review must come from the customer, the system shall send the order back for customer action with clear instructions.

**Source Evidence:**
- `[interview_turn:T058]` "If staff can’t verify it quickly, I’d keep the order on hold first rather than making a decision too early. If the missing information is something only the customer can provide, then the order should be sent back for customer action with clear instructions on what to update or send in. If it’s an internal issue that still needs investigation, it should stay on hold until staff can approve or reject it."

### [FR-075] (stated)
If a manual review issue is internal and still needs investigation, the order shall stay on hold until staff can approve or reject it.

**Source Evidence:**
- `[interview_turn:T058]` "If staff can’t verify it quickly, I’d keep the order on hold first rather than making a decision too early. If the missing information is something only the customer can provide, then the order should be sent back for customer action with clear instructions on what to update or send in. If it’s an internal issue that still needs investigation, it should stay on hold until staff can approve or reject it."

### [FR-076] (stated)
The web interface shall allow only order status changes that match the real order state.

**Source Evidence:**
- `[interview_turn:T070]` "The web interface should only allow status changes that match the real order state, so an operator can’t skip important steps or mark something complete when it isn’t ready. For example, an unpaid order should not be moved into fulfillment, and a canceled order should not be moved back into normal processing unless there’s a deliberate reopen action. If they try an invalid transition, the system should block it and explain why in plain language."

### [FR-077] (stated)
The web interface shall block invalid order status transitions and explain why in plain language.

**Source Evidence:**
- `[interview_turn:T070]` "The web interface should only allow status changes that match the real order state, so an operator can’t skip important steps or mark something complete when it isn’t ready. For example, an unpaid order should not be moved into fulfillment, and a canceled order should not be moved back into normal processing unless there’s a deliberate reopen action. If they try an invalid transition, the system should block it and explain why in plain language."

### [FR-078] (stated)
An unpaid order shall not be moved into fulfillment.

**Source Evidence:**
- `[interview_turn:T070]` "The web interface should only allow status changes that match the real order state, so an operator can’t skip important steps or mark something complete when it isn’t ready. For example, an unpaid order should not be moved into fulfillment, and a canceled order should not be moved back into normal processing unless there’s a deliberate reopen action. If they try an invalid transition, the system should block it and explain why in plain language."

### [FR-079] (stated)
A canceled order shall not be moved back into normal processing unless a deliberate reopen action is used.

**Source Evidence:**
- `[interview_turn:T070]` "The web interface should only allow status changes that match the real order state, so an operator can’t skip important steps or mark something complete when it isn’t ready. For example, an unpaid order should not be moved into fulfillment, and a canceled order should not be moved back into normal processing unless there’s a deliberate reopen action. If they try an invalid transition, the system should block it and explain why in plain language."

### [FR-080] (stated)
The system shall support configuring frequent and low-risk changes through configuration or business settings.

**Source Evidence:**
- `[interview_turn:T078]` "Mostly through configuration or business settings if it’s something an operator would reasonably adjust, like catalog options, order rules, or display choices. I’d reserve code changes and new releases for things that affect the core checkout flow, security, or any major new capability. If a change is frequent and low risk, it should be configurable; if it’s structural or technically sensitive, it should go through a release."

### [FR-081] (stated)
The system shall require code changes and new releases for changes affecting the core checkout flow, security, or major new capabilities.

**Source Evidence:**
- `[interview_turn:T078]` "Mostly through configuration or business settings if it’s something an operator would reasonably adjust, like catalog options, order rules, or display choices. I’d reserve code changes and new releases for things that affect the core checkout flow, security, or any major new capability. If a change is frequent and low risk, it should be configurable; if it’s structural or technically sensitive, it should go through a release."

### [FR-082] (conditional)
The system shall allow imports through the web interface using common files such as CSV or Excel.

**Source Evidence:**
- `[interview_turn:T072]` "For the first pass, I’d keep imports pretty simple and stick to common files like CSV or maybe Excel, with staff uploading them through the web interface. Every imported row should be validated before it goes live, and if something conflicts with existing product data, the system should either stop that row or flag it for review rather than silently overwriting it. For future automatic syncing, I’d want the same rule: no unexpected changes going live without validation, and clear reporting when there’s a mismatch so a non-technical operator can see what needs attention."

### [FR-083] (stated)
Every imported row shall be validated before it goes live.

**Source Evidence:**
- `[interview_turn:T072]` "For the first pass, I’d keep imports pretty simple and stick to common files like CSV or maybe Excel, with staff uploading them through the web interface. Every imported row should be validated before it goes live, and if something conflicts with existing product data, the system should either stop that row or flag it for review rather than silently overwriting it. For future automatic syncing, I’d want the same rule: no unexpected changes going live without validation, and clear reporting when there’s a mismatch so a non-technical operator can see what needs attention."

### [FR-084] (stated)
If an imported row conflicts with existing product data, the system shall stop that row or flag it for review rather than silently overwriting it.

**Source Evidence:**
- `[interview_turn:T072]` "For the first pass, I’d keep imports pretty simple and stick to common files like CSV or maybe Excel, with staff uploading them through the web interface. Every imported row should be validated before it goes live, and if something conflicts with existing product data, the system should either stop that row or flag it for review rather than silently overwriting it. For future automatic syncing, I’d want the same rule: no unexpected changes going live without validation, and clear reporting when there’s a mismatch so a non-technical operator can see what needs attention."

### [FR-085] (conditional)
For future automatic syncing, the system shall prevent unexpected changes from going live without validation and shall provide clear mismatch reporting.

**Source Evidence:**
- `[interview_turn:T072]` "For the first pass, I’d keep imports pretty simple and stick to common files like CSV or maybe Excel, with staff uploading them through the web interface. Every imported row should be validated before it goes live, and if something conflicts with existing product data, the system should either stop that row or flag it for review rather than silently overwriting it. For future automatic syncing, I’d want the same rule: no unexpected changes going live without validation, and clear reporting when there’s a mismatch so a non-technical operator can see what needs attention."

### [FR-086] (conditional)
If an import fails partway through, the system shall either import only the clean rows with a clear report of the failures or stop the whole import and leave everything unchanged for critical data sets.

**Source Evidence:**
- `[interview_turn:T076]` "I’d prefer it not to partially change live data without the operator being aware. Ideally the system should validate first and then either import only the clean rows with a clear report of the failures, or if it’s a critical data set, stop the whole import and leave everything unchanged. For a new operator, I think clear feedback is more important than a complicated rollback process."

### [FR-087] (stated)
The system shall support basic order status changes through the web interface for new store operators.

**Source Evidence:**
- `[interview_turn:T066]` "The basics should be very easy, especially adding and editing products, updating prices and stock, managing customer accounts, and checking orders. A new store operator should be able to do those from the web interface without any technical setup. I’d also want simple tools for changing order status and handling common customer issues without needing a developer."
- `[interview_turn:T070]` "The web interface should only allow status changes that match the real order state, so an operator can’t skip important steps or mark something complete when it isn’t ready. For example, an unpaid order should not be moved into fulfillment, and a canceled order should not be moved back into normal processing unless there’s a deliberate reopen action. If they try an invalid transition, the system should block it and explain why in plain language."

### [FR-088] (stated)
The system shall allow customers to view the current status of an order that is already being prepared for delivery.

**Source Evidence:**
- `[interview_turn:T094]` "If it was already in a cart, customers should be able to see that it’s no longer available and be prompted to remove it or update the cart before checkout. If it was reserved or already in an order that’s being prepared, staff should still be able to manage that order, but customers should only see the current status and not be able to repurchase it from that order. We’d want the messaging to be clear enough that they understand it’s unavailable, without exposing internal handling details."

### [FR-089] (stated)
The system shall prompt customers to remove or update cart items that are no longer available before checkout.

**Source Evidence:**
- `[interview_turn:T094]` "If it was already in a cart, customers should be able to see that it’s no longer available and be prompted to remove it or update the cart before checkout. If it was reserved or already in an order that’s being prepared, staff should still be able to manage that order, but customers should only see the current status and not be able to repurchase it from that order. We’d want the messaging to be clear enough that they understand it’s unavailable, without exposing internal handling details."

## 4. Business Rules and Constraints

### [BR-001] (stated)
A product shall be visible but not purchasable when its price is missing, invalid, or inventory is unavailable under stock control.

**Source Evidence:**
- `[interview_turn:T044]` "Yes, that makes sense. If a product is still something we want customers to see, but we can’t actually sell it right now because the price is missing, invalid, or inventory is unavailable under stock control, it should stay visible but be marked as not purchasable. In that case the add-to-cart or checkout action should be blocked, and the customer should get a clear message about why."
- `[interview_turn:T090]` "If a product isn’t purchasable, I’d want the system to block both add-to-cart and checkout, and also make it clear on the product page that it’s unavailable. I don’t think we need to hide the product completely, unless the business wants it out of sight for some reason, but we should definitely prevent any purchase action until price or inventory is back."
- `[interview_turn:T092]` "Yes, that can happen. Sometimes a product may still be shown because we want customers to see it, but it should not be purchasable if the price hasn’t been confirmed yet, inventory is temporarily uncertain, or there’s some approval step still pending. In those cases it should clearly appear unavailable for purchase so nobody can complete an order by mistake."

### [BR-002] (conditional)
If stock control is being used, valid stock is required for purchase.

**Source Evidence:**
- `[interview_turn:T016]` "A product should only be purchasable when it’s marked active and available for sale, with a valid price and stock if stock control is being used. If the price changes, I’d want the updated price to apply to new carts and new orders, but not unexpectedly change an order that’s already been placed. If something is out of stock or not yet available, it should be clearly shown as unavailable and the customer shouldn’t be able to complete checkout for it."

### [BR-003] (stated)
If a product is out of stock or not yet available, checkout shall be prevented for that product.

**Source Evidence:**
- `[interview_turn:T016]` "A product should only be purchasable when it’s marked active and available for sale, with a valid price and stock if stock control is being used. If the price changes, I’d want the updated price to apply to new carts and new orders, but not unexpectedly change an order that’s already been placed. If something is out of stock or not yet available, it should be clearly shown as unavailable and the customer shouldn’t be able to complete checkout for it."

### [BR-004] (stated)
If a product is shown as unavailable, add-to-cart and checkout actions shall be blocked.

**Source Evidence:**
- `[interview_turn:T044]` "Yes, that makes sense. If a product is still something we want customers to see, but we can’t actually sell it right now because the price is missing, invalid, or inventory is unavailable under stock control, it should stay visible but be marked as not purchasable. In that case the add-to-cart or checkout action should be blocked, and the customer should get a clear message about why."
- `[interview_turn:T090]` "If a product isn’t purchasable, I’d want the system to block both add-to-cart and checkout, and also make it clear on the product page that it’s unavailable. I don’t think we need to hide the product completely, unless the business wants it out of sight for some reason, but we should definitely prevent any purchase action until price or inventory is back."

### [BR-005] (stated)
The system shall not store full payment card details itself.

**Source Evidence:**
- `[interview_turn:T006]` "For the first release, I’d want the store to use standard account protection like secure logins and password reset, and to flag anything obviously suspicious rather than trying to handle every edge case automatically. For payments, we should rely on a trusted payment provider so we’re not storing sensitive card details ourselves. Personal data should be kept to the minimum needed to fulfill orders, and if something looks risky we should block or review the transaction instead of letting it go through unchecked."
- `[interview_turn:T084]` "We should avoid storing anything that isn’t needed to process and fulfill the order, so I’d exclude extra personal details like unnecessary profile fields or full payment information if the payment provider can handle that. Only the minimum contact and shipping information needed for the order should be kept. Sensitive data should be limited to a small set of authorized store staff, probably sales or admin roles, and not broadly visible to everyone who can use the system."

### [BR-006] (stated)
Sensitive customer data shall be accessible only to authorized staff with a need to know.

**Source Evidence:**
- `[interview_turn:T084]` "We should avoid storing anything that isn’t needed to process and fulfill the order, so I’d exclude extra personal details like unnecessary profile fields or full payment information if the payment provider can handle that. Only the minimum contact and shipping information needed for the order should be kept. Sensitive data should be limited to a small set of authorized store staff, probably sales or admin roles, and not broadly visible to everyone who can use the system."
- `[interview_turn:T086]` "Yes, there are a few situations where extra details would be useful, like a customer’s phone number for delivery issues, tax-related information where required, and enough payment or transaction reference data to handle refunds or disputes. I’d also want to keep order history and status notes for customer support and fraud review, but not more than necessary. Access to that should still be restricted to support, sales, or admin staff who actually need it, with the most sensitive parts kept on a need-to-know basis."
- `[interview_turn:T088]` "I’d base it on job role and the reason they’re handling that specific order. For example, sales staff might see normal contact and order details, but only support or admins should see sensitive notes, refund references, or fraud-related flags, and even then only when they’re assigned to the case. If we can, it should also be logged so we can tell who viewed what and why."

### [BR-007] (stated)
Sales staff may see normal contact and order details, but only support or admins may see sensitive notes, refund references, or fraud-related flags, and only when assigned to the case.

**Source Evidence:**
- `[interview_turn:T088]` "I’d base it on job role and the reason they’re handling that specific order. For example, sales staff might see normal contact and order details, but only support or admins should see sensitive notes, refund references, or fraud-related flags, and even then only when they’re assigned to the case. If we can, it should also be logged so we can tell who viewed what and why."

### [BR-008] (stated)
The system shall keep only the minimum contact and shipping information needed for the order.

**Source Evidence:**
- `[interview_turn:T084]` "We should avoid storing anything that isn’t needed to process and fulfill the order, so I’d exclude extra personal details like unnecessary profile fields or full payment information if the payment provider can handle that. Only the minimum contact and shipping information needed for the order should be kept. Sensitive data should be limited to a small set of authorized store staff, probably sales or admin roles, and not broadly visible to everyone who can use the system."

### [BR-009] (stated)
Sensitive data shall be handled with tighter access than normal store data.

**Source Evidence:**
- `[interview_turn:T080]` "Yes, a few cases should be stricter than the default. If an order looks unusual, especially with a high value, mismatched customer details, or repeated failed payment attempts, I’d want it held for review before it goes any further. For personal data, I’d only want to collect what’s necessary to complete the order, and anything sensitive should be handled carefully with tighter access than normal store data."

### [BR-010] (stated)
A customer account deletion request shall not proceed immediately when active orders, payment issues, legal recordkeeping, return cases, refund cases, unresolved support cases, or required order history exist.

**Source Evidence:**
- `[interview_turn:T032]` "If a customer wants their account suspended or deleted, we should be able to process that request, but I’d expect some cases where deletion can’t happen immediately because of active orders, payment issues, or legal recordkeeping. Suspension could be immediate in most cases, while deletion should probably be checked against any open business obligations first. If there are exceptions, they would need to be handled by an admin rather than automatically."
- `[interview_turn:T034]` "If the customer is tied to a return, refund, or unresolved support case, I’d treat that as a reason to delay deletion as well. Also, if their account has order history that we still need for customer service or accounting, that may need to stay in place even if the account is otherwise inactive. Beyond that, I’m not sure there are other hard blockers, but I’d want those edge cases checked with the business before we lock the rule down."

### [BR-011] (stated)
A customer account request may require admin approval when it involves unresolved disputes, a suspicious activity flag, or a conflict with an open order or refund.

**Source Evidence:**
- `[interview_turn:T036]` "I’d expect admin approval only when the request is not straightforward, like when the account has unresolved disputes, a suspicious activity flag, or there’s some conflict with an open order or refund. For a normal self-service request with no complications, it should probably go through automatically. If the system can’t confidently determine whether it’s safe to proceed, then it should route it to an admin review queue."

### [BR-012] (stated)
A customer account request shall be routed to admin review when the system cannot confidently determine whether it is safe to proceed.

**Source Evidence:**
- `[interview_turn:T036]` "I’d expect admin approval only when the request is not straightforward, like when the account has unresolved disputes, a suspicious activity flag, or there’s some conflict with an open order or refund. For a normal self-service request with no complications, it should probably go through automatically. If the system can’t confidently determine whether it’s safe to proceed, then it should route it to an admin review queue."

### [BR-013] (stated)
A product shall only be purchasable when it is marked active and available for sale.

**Source Evidence:**
- `[interview_turn:T016]` "A product should only be purchasable when it’s marked active and available for sale, with a valid price and stock if stock control is being used. If the price changes, I’d want the updated price to apply to new carts and new orders, but not unexpectedly change an order that’s already been placed. If something is out of stock or not yet available, it should be clearly shown as unavailable and the customer shouldn’t be able to complete checkout for it."

### [BR-014] (stated)
A price change shall apply to new carts and new orders only, not to an order already placed.

**Source Evidence:**
- `[interview_turn:T016]` "A product should only be purchasable when it’s marked active and available for sale, with a valid price and stock if stock control is being used. If the price changes, I’d want the updated price to apply to new carts and new orders, but not unexpectedly change an order that’s already been placed. If something is out of stock or not yet available, it should be clearly shown as unavailable and the customer shouldn’t be able to complete checkout for it."

### [BR-015] (stated)
If a cart exceeds quantity or value limits, checkout shall not proceed until the customer adjusts the cart.

**Source Evidence:**
- `[interview_turn:T018]` "Yes, we should probably support basic limits like minimum and maximum quantities per product, and possibly a maximum total quantity or value per order if the business needs it. If a cart goes outside those limits, the system should flag it before checkout and tell the customer exactly what needs to be adjusted, rather than failing only at the final step. I’m not sure yet whether we need customer-specific limits, so I’d want to check that with the business team."
- `[interview_turn:T040]` "Yes, I’d expect some limits on certain products, especially if stock is low or the item has a business rule like a maximum per customer. If a shopper goes over the limit, the cart should clearly flag the issue and stop checkout until they reduce the quantity or remove the item. It shouldn’t fail silently, because that would be confusing for new customers."

### [BR-016] (stated)
If a shipping address is technically valid but conflicts with a shipping method or carrier rule, the system shall warn the customer and allow them to choose a different option or address.

**Source Evidence:**
- `[interview_turn:T064]` "Those addresses should be allowed in the system if they’re valid, but the store should flag them when they conflict with a chosen shipping method or carrier rule. For example, if a PO box can’t use a certain carrier, the customer should be told right away and asked to pick a different shipping option or use another address. If the address is acceptable but just limited, I’d rather warn them at checkout than reject it completely."

### [BR-017] (stated)
The system shall validate shipping addresses enough to catch obvious problems such as missing street, city, postal code, or country.

**Source Evidence:**
- `[interview_turn:T046]` "Yes, the shipping address should be validated enough to catch obvious problems like missing street, city, postal code, or country, and we should flag addresses that look incomplete or invalid. Delivery options should depend on the customer’s location, because not every method will be available everywhere, and some products may have extra restrictions too. If no delivery method is available for that address, checkout should stop and clearly tell the customer that they need to change the address or contact support."

### [BR-018] (stated)
The system shall not expose internal fraud or security details in customer-facing manual review messages.

**Source Evidence:**
- `[interview_turn:T056]` "Manual review should look at things like suspicious payment activity, mismatched customer and shipping details, unusual order size, or any policy exceptions we want staff to catch before fulfillment. If it’s approved, the customer should be told the order is confirmed and moving ahead; if it stays on hold, they should know it’s still under review and no action may be needed yet; if it’s rejected, they should be told the order cannot be completed and, if appropriate, whether they need to try again or contact support. I’d keep the customer message fairly high level and avoid exposing internal fraud or security details."

### [BR-019] (conditional)
Administrative actions, sensitive access, and record views should be logged when practical to show who viewed what and why.

**Source Evidence:**
- `[interview_turn:T088]` "I’d base it on job role and the reason they’re handling that specific order. For example, sales staff might see normal contact and order details, but only support or admins should see sensitive notes, refund references, or fraud-related flags, and even then only when they’re assigned to the case. If we can, it should also be logged so we can tell who viewed what and why."

### [BR-020] (stated)
A product record shall not be saved with a broken image upload.

**Source Evidence:**
- `[interview_turn:T014]` "For the first release, I’d keep the media rules pretty simple. A product should be able to have one main image and maybe a small number of additional images, with common formats like JPG and PNG allowed, and if an upload fails or the file is invalid, the system should reject it clearly and let the user try again without saving a broken product record. If an image is missing, the product can still exist, but it should show a default placeholder so the listing doesn’t break."

## 5. Data and External Interfaces

### [DI-001] (stated)
The system shall use a trusted payment provider for payment processing.

**Source Evidence:**
- `[interview_turn:T006]` "For the first release, I’d want the store to use standard account protection like secure logins and password reset, and to flag anything obviously suspicious rather than trying to handle every edge case automatically. For payments, we should rely on a trusted payment provider so we’re not storing sensitive card details ourselves. Personal data should be kept to the minimum needed to fulfill orders, and if something looks risky we should block or review the transaction instead of letting it go through unchecked."

### [DI-002] (stated)
The system shall support sending order confirmation by email.

**Source Evidence:**
- `[interview_turn:T042]` "After checkout, the customer should see the order number, items purchased, quantities, totals, taxes or fees if applicable, shipping details, and the payment status. Yes, that confirmation should also go out by email, and if we support another channel like SMS later, that could be useful too. The main thing is they need a clear record immediately after placing the order."

### [DI-003] (conditional)
The system shall support importing product data from common files such as CSV or Excel through the web interface.

**Source Evidence:**
- `[interview_turn:T072]` "For the first pass, I’d keep imports pretty simple and stick to common files like CSV or maybe Excel, with staff uploading them through the web interface. Every imported row should be validated before it goes live, and if something conflicts with existing product data, the system should either stop that row or flag it for review rather than silently overwriting it. For future automatic syncing, I’d want the same rule: no unexpected changes going live without validation, and clear reporting when there’s a mismatch so a non-technical operator can see what needs attention."

### [DI-004] (conditional)
The system shall support product data migration from an existing legacy system when such data exists.

**Source Evidence:**
- `[interview_turn:T022]` "Yes, that’s likely to be needed if the business already has product data somewhere else, especially for the first launch. Clean records should be brought over into the new catalog, and anything that doesn’t map cleanly should be reported for manual review instead of guessed at automatically. If a record is incomplete, I’d rather have it skipped or marked as needing attention until someone corrects it."

## 6. Quality Requirements

### [QR-001] (stated)
The system shall be simple enough for new store owners to operate without much technical knowledge.

**Source Evidence:**
- `[interview_turn:T002]` "The main goal is to help new store owners get selling online quickly without needing much technical knowledge, so they can set up a storefront, manage what they sell, and start taking orders. For the first version, we want support for fairly standard retail products, like items with names, descriptions, prices, and available quantities, and the day-to-day work of adding or updating products, managing customer accounts, handling carts, and processing orders. We’re not trying to cover every possible retail scenario at the beginning, just the core operations needed to run a small online shop reliably."
- `[interview_turn:T066]` "The basics should be very easy, especially adding and editing products, updating prices and stock, managing customer accounts, and checking orders. A new store operator should be able to do those from the web interface without any technical setup. I’d also want simple tools for changing order status and handling common customer issues without needing a developer."
- `[interview_turn:T082]` "Yes, anything beyond the basic store setup, product management, cart, ordering, and customer account handling should be treated as a nice-to-have for later. Things like advanced reporting, promotions, automatic syncing, and richer onboarding tools can come after the core launch if they don’t slow down delivery. My priority is getting a simple, reliable store that new operators can actually run without too much complexity."

### [QR-002] (stated)
The system shall run reliably for core store operations.

**Source Evidence:**
- `[interview_turn:T002]` "The main goal is to help new store owners get selling online quickly without needing much technical knowledge, so they can set up a storefront, manage what they sell, and start taking orders. For the first version, we want support for fairly standard retail products, like items with names, descriptions, prices, and available quantities, and the day-to-day work of adding or updating products, managing customer accounts, handling carts, and processing orders. We’re not trying to cover every possible retail scenario at the beginning, just the core operations needed to run a small online shop reliably."
- `[interview_turn:T068]` "For the first release, I’d keep it focused on the core shop workflow: product catalog, customer accounts, cart, checkout, order processing, and basic admin management. I would leave out more advanced things like subscriptions, marketplace selling, complex promotions, multi-warehouse inventory, and deep accounting or ERP integrations. If an item or order is unusual, I’d expect staff to handle it manually outside the system rather than building a special automated path right away."
- `[interview_turn:T082]` "Yes, anything beyond the basic store setup, product management, cart, ordering, and customer account handling should be treated as a nice-to-have for later. Things like advanced reporting, promotions, automatic syncing, and richer onboarding tools can come after the core launch if they don’t slow down delivery. My priority is getting a simple, reliable store that new operators can actually run without too much complexity."

### [QR-003] (stated)
The system shall remain responsive when more people are browsing at once.

**Source Evidence:**
- `[interview_turn:T010]` "The biggest pressure will probably be keeping the site responsive when more people are browsing at once, especially during promotions or busy periods, and making sure orders don’t get lost if traffic spikes. If demand suddenly rises, I’d rather the store slow down gracefully or queue non-urgent actions than fail outright, and if part of the service is unavailable, it should clearly tell users what’s affected and let them come back later without losing their cart or order progress. We’d also want the system to keep the important sales functions available as much as possible, even if some admin features are temporarily reduced."

### [QR-004] (stated)
If demand suddenly rises, the system shall slow down gracefully or queue non-urgent actions rather than failing outright.

**Source Evidence:**
- `[interview_turn:T010]` "The biggest pressure will probably be keeping the site responsive when more people are browsing at once, especially during promotions or busy periods, and making sure orders don’t get lost if traffic spikes. If demand suddenly rises, I’d rather the store slow down gracefully or queue non-urgent actions than fail outright, and if part of the service is unavailable, it should clearly tell users what’s affected and let them come back later without losing their cart or order progress. We’d also want the system to keep the important sales functions available as much as possible, even if some admin features are temporarily reduced."

### [QR-005] (stated)
The system shall provide clear validation and feedback for import and data review activities.

**Source Evidence:**
- `[interview_turn:T072]` "For the first pass, I’d keep imports pretty simple and stick to common files like CSV or maybe Excel, with staff uploading them through the web interface. Every imported row should be validated before it goes live, and if something conflicts with existing product data, the system should either stop that row or flag it for review rather than silently overwriting it. For future automatic syncing, I’d want the same rule: no unexpected changes going live without validation, and clear reporting when there’s a mismatch so a non-technical operator can see what needs attention."
- `[interview_turn:T076]` "I’d prefer it not to partially change live data without the operator being aware. Ideally the system should validate first and then either import only the clean rows with a clear report of the failures, or if it’s a critical data set, stop the whole import and leave everything unchanged. For a new operator, I think clear feedback is more important than a complicated rollback process."

### [QR-006] (stated)
The system shall provide clear error messages in plain language for invalid status transitions and blocked purchases.

**Source Evidence:**
- `[interview_turn:T070]` "The web interface should only allow status changes that match the real order state, so an operator can’t skip important steps or mark something complete when it isn’t ready. For example, an unpaid order should not be moved into fulfillment, and a canceled order should not be moved back into normal processing unless there’s a deliberate reopen action. If they try an invalid transition, the system should block it and explain why in plain language."
- `[interview_turn:T044]` "Yes, that makes sense. If a product is still something we want customers to see, but we can’t actually sell it right now because the price is missing, invalid, or inventory is unavailable under stock control, it should stay visible but be marked as not purchasable. In that case the add-to-cart or checkout action should be blocked, and the customer should get a clear message about why."
- `[interview_turn:T090]` "If a product isn’t purchasable, I’d want the system to block both add-to-cart and checkout, and also make it clear on the product page that it’s unavailable. I don’t think we need to hide the product completely, unless the business wants it out of sight for some reason, but we should definitely prevent any purchase action until price or inventory is back."

### [QR-007] (stated)
The system shall support the major current browsers Chrome, Safari, Edge, and Firefox.

**Source Evidence:**
- `[interview_turn:T062]` "We should support the major current browsers that most customers use, like Chrome, Safari, Edge, and Firefox, on both desktop and mobile devices. It should work well on phones and tablets too, since a lot of customers will shop that way. I don’t have a hard requirement for older browser versions yet, so we’d need to define how far back we want to go."

### [QR-008] (stated)
The system shall work on desktop, mobile devices, phones, and tablets.

**Source Evidence:**
- `[interview_turn:T062]` "We should support the major current browsers that most customers use, like Chrome, Safari, Edge, and Firefox, on both desktop and mobile devices. It should work well on phones and tablets too, since a lot of customers will shop that way. I don’t have a hard requirement for older browser versions yet, so we’d need to define how far back we want to go."

### [QR-009] (stated)
The system shall keep important sales functions available as much as possible during partial service unavailability.

**Source Evidence:**
- `[interview_turn:T010]` "The biggest pressure will probably be keeping the site responsive when more people are browsing at once, especially during promotions or busy periods, and making sure orders don’t get lost if traffic spikes. If demand suddenly rises, I’d rather the store slow down gracefully or queue non-urgent actions than fail outright, and if part of the service is unavailable, it should clearly tell users what’s affected and let them come back later without losing their cart or order progress. We’d also want the system to keep the important sales functions available as much as possible, even if some admin features are temporarily reduced."
- `[interview_turn:T025]` "Who would own ongoing support and maintenance for those post-launch onboarding changes when issues come up?"

### [QR-010] (stated)
The system shall provide a clear success or failure message immediately after payment submission.

**Source Evidence:**
- `[interview_turn:T048]` "From the customer’s point of view, the payment step should be simple and clearly guided, with the customer choosing a payment method and confirming the amount before anything is finalized. After they submit payment, the store should show a clear success or failure message right away, and if it fails, explain what they can do next without making them start over unnecessarily. If the payment is successful, the order should move to confirmation immediately and they should know the purchase is complete."

### [QR-011] (stated)
The system shall provide enough detail in payment failure messages for the customer to understand whether the issue was a card issue, a declined transaction, or a system issue.

**Source Evidence:**
- `[interview_turn:T052]` "They should see a clear message that the payment did not go through, with enough detail to understand whether it was a card issue, a declined transaction, or something on our side. Before the order is confirmed, they should be able to try the payment again, choose a different payment method, or go back and review the order. If only part of the payment completed, I’d want the system to keep the order from confirming until the full amount is resolved."

### [QR-012] (stated)
The system shall provide customer-facing confirmation information immediately after checkout.

**Source Evidence:**
- `[interview_turn:T042]` "After checkout, the customer should see the order number, items purchased, quantities, totals, taxes or fees if applicable, shipping details, and the payment status. Yes, that confirmation should also go out by email, and if we support another channel like SMS later, that could be useful too. The main thing is they need a clear record immediately after placing the order."

### [QR-013] (stated)
The system shall use clear messaging for unavailable products and cart or checkout blocks.

**Source Evidence:**
- `[interview_turn:T044]` "Yes, that makes sense. If a product is still something we want customers to see, but we can’t actually sell it right now because the price is missing, invalid, or inventory is unavailable under stock control, it should stay visible but be marked as not purchasable. In that case the add-to-cart or checkout action should be blocked, and the customer should get a clear message about why."
- `[interview_turn:T090]` "If a product isn’t purchasable, I’d want the system to block both add-to-cart and checkout, and also make it clear on the product page that it’s unavailable. I don’t think we need to hide the product completely, unless the business wants it out of sight for some reason, but we should definitely prevent any purchase action until price or inventory is back."
- `[interview_turn:T092]` "Yes, that can happen. Sometimes a product may still be shown because we want customers to see it, but it should not be purchasable if the price hasn’t been confirmed yet, inventory is temporarily uncertain, or there’s some approval step still pending. In those cases it should clearly appear unavailable for purchase so nobody can complete an order by mistake."
- `[interview_turn:T094]` "If it was already in a cart, customers should be able to see that it’s no longer available and be prompted to remove it or update the cart before checkout. If it was reserved or already in an order that’s being prepared, staff should still be able to manage that order, but customers should only see the current status and not be able to repurchase it from that order. We’d want the messaging to be clear enough that they understand it’s unavailable, without exposing internal handling details."

### [QR-014] (conditional)
The system shall keep the live catalog undisturbed by onboarding changes and shall support safe rollback if an import goes wrong.

**Source Evidence:**
- `[interview_turn:T024]` "I’d expect the business to want improvements like importing from different file formats, doing bulk updates, and maybe syncing some data more automatically later on. The store should handle those changes in a way that doesn’t disturb the live catalog, so we’d want clear validation, an ability to preview or review changes, and a safe rollback if an import goes wrong. If a new onboarding rule is added, it should apply consistently to new loads without breaking the existing products already in the system."

### [QR-015] (conditional)
The system shall apply new onboarding rules consistently to new loads without breaking existing products already in the system.

**Source Evidence:**
- `[interview_turn:T024]` "I’d expect the business to want improvements like importing from different file formats, doing bulk updates, and maybe syncing some data more automatically later on. The store should handle those changes in a way that doesn’t disturb the live catalog, so we’d want clear validation, an ability to preview or review changes, and a safe rollback if an import goes wrong. If a new onboarding rule is added, it should apply consistently to new loads without breaking the existing products already in the system."

### [QR-016] (stated)
The system shall allow a new store operator to perform basic administrative tasks from the web interface without technical setup.

**Source Evidence:**
- `[interview_turn:T066]` "The basics should be very easy, especially adding and editing products, updating prices and stock, managing customer accounts, and checking orders. A new store operator should be able to do those from the web interface without any technical setup. I’d also want simple tools for changing order status and handling common customer issues without needing a developer."

## 7. Exceptions and Boundary Conditions

### [EX-001] (stated)
If payment fails or is only partially completed, the order shall not confirm.

**Source Evidence:**
- `[interview_turn:T052]` "They should see a clear message that the payment did not go through, with enough detail to understand whether it was a card issue, a declined transaction, or something on our side. Before the order is confirmed, they should be able to try the payment again, choose a different payment method, or go back and review the order. If only part of the payment completed, I’d want the system to keep the order from confirming until the full amount is resolved."

### [EX-002] (stated)
If a product image upload fails or is invalid, the product shall not be saved with a broken image record.

**Source Evidence:**
- `[interview_turn:T014]` "For the first release, I’d keep the media rules pretty simple. A product should be able to have one main image and maybe a small number of additional images, with common formats like JPG and PNG allowed, and if an upload fails or the file is invalid, the system should reject it clearly and let the user try again without saving a broken product record. If an image is missing, the product can still exist, but it should show a default placeholder so the listing doesn’t break."

### [EX-003] (stated)
If no delivery method is available for a shipping address, checkout shall stop.

**Source Evidence:**
- `[interview_turn:T046]` "Yes, the shipping address should be validated enough to catch obvious problems like missing street, city, postal code, or country, and we should flag addresses that look incomplete or invalid. Delivery options should depend on the customer’s location, because not every method will be available everywhere, and some products may have extra restrictions too. If no delivery method is available for that address, checkout should stop and clearly tell the customer that they need to change the address or contact support."

### [EX-004] (stated)
If a cart exceeds limits, the customer shall be blocked from checkout until the cart is corrected.

**Source Evidence:**
- `[interview_turn:T018]` "Yes, we should probably support basic limits like minimum and maximum quantities per product, and possibly a maximum total quantity or value per order if the business needs it. If a cart goes outside those limits, the system should flag it before checkout and tell the customer exactly what needs to be adjusted, rather than failing only at the final step. I’m not sure yet whether we need customer-specific limits, so I’d want to check that with the business team."
- `[interview_turn:T040]` "Yes, I’d expect some limits on certain products, especially if stock is low or the item has a business rule like a maximum per customer. If a shopper goes over the limit, the cart should clearly flag the issue and stop checkout until they reduce the quantity or remove the item. It shouldn’t fail silently, because that would be confusing for new customers."

### [EX-005] (stated)
If a manual review cannot be quickly verified, the order shall remain on hold until staff can decide or customer action is completed.

**Source Evidence:**
- `[interview_turn:T058]` "If staff can’t verify it quickly, I’d keep the order on hold first rather than making a decision too early. If the missing information is something only the customer can provide, then the order should be sent back for customer action with clear instructions on what to update or send in. If it’s an internal issue that still needs investigation, it should stay on hold until staff can approve or reject it."

### [EX-006] (stated)
If an order is invalidly transitioned to fulfillment, the system shall block the transition.

**Source Evidence:**
- `[interview_turn:T070]` "The web interface should only allow status changes that match the real order state, so an operator can’t skip important steps or mark something complete when it isn’t ready. For example, an unpaid order should not be moved into fulfillment, and a canceled order should not be moved back into normal processing unless there’s a deliberate reopen action. If they try an invalid transition, the system should block it and explain why in plain language."

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
Whether the first release must support customer-specific limits is unresolved.

**Source Evidence:**
- `[interview_turn:T018]` "Yes, we should probably support basic limits like minimum and maximum quantities per product, and possibly a maximum total quantity or value per order if the business needs it. If a cart goes outside those limits, the system should flag it before checkout and tell the customer exactly what needs to be adjusted, rather than failing only at the final step. I’m not sure yet whether we need customer-specific limits, so I’d want to check that with the business team."

### [UN-002]
Whether the first release must support another payment channel beyond email confirmation is unresolved.

**Source Evidence:**
- `[interview_turn:T042]` "After checkout, the customer should see the order number, items purchased, quantities, totals, taxes or fees if applicable, shipping details, and the payment status. Yes, that confirmation should also go out by email, and if we support another channel like SMS later, that could be useful too. The main thing is they need a clear record immediately after placing the order."

### [UN-003]
Whether the first release should capture payment at order confirmation instead of after fulfillment or shipment is unresolved.

**Source Evidence:**
- `[interview_turn:T050]` "I’d expect authorization to happen first, when the customer confirms the order, so we know the payment method is valid and the funds should be available. Capture should happen after that, when the order is accepted for fulfillment or shipped, depending on how the business wants to operate. If we can only support one approach at first, I’d lean toward capturing at order confirmation for simplicity, but that would need to be confirmed with the finance team."

### [UN-004]
Whether the first release should support older browser versions is unresolved.

**Source Evidence:**
- `[interview_turn:T062]` "We should support the major current browsers that most customers use, like Chrome, Safari, Edge, and Firefox, on both desktop and mobile devices. It should work well on phones and tablets too, since a lot of customers will shop that way. I don’t have a hard requirement for older browser versions yet, so we’d need to define how far back we want to go."

### [UN-005]
Whether the first release should include file import support is unresolved.

**Source Evidence:**
- `[interview_turn:T020]` "We’d expect the store owner or staff to load the initial product catalog before the site goes live, either by entering products manually or importing them from an existing file if we support that. After the data is loaded, someone should review the listings for correctness, images, pricing, and availability, then mark the catalog ready for customers. If anything is incomplete, it should stay hidden or unavailable until it’s fixed."
- `[interview_turn:T074]` "I’d record that area as still tentative for the moment. We know we want basic file import and some future automation eventually, but the exact import methods, bulk update behavior, and sync rules can wait until we’ve learned more from real store operators."

### [UN-006]
The exact import methods, bulk update behavior, and sync rules for future onboarding enhancements are unresolved.

**Source Evidence:**
- `[interview_turn:T074]` "I’d record that area as still tentative for the moment. We know we want basic file import and some future automation eventually, but the exact import methods, bulk update behavior, and sync rules can wait until we’ve learned more from real store operators."

### [UN-007]
Whether the system needs customer-specific limits is unresolved.

**Source Evidence:**
- `[interview_turn:T018]` "Yes, we should probably support basic limits like minimum and maximum quantities per product, and possibly a maximum total quantity or value per order if the business needs it. If a cart goes outside those limits, the system should flag it before checkout and tell the customer exactly what needs to be adjusted, rather than failing only at the final step. I’m not sure yet whether we need customer-specific limits, so I’d want to check that with the business team."
