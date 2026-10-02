# Software Requirements Specification: GAMMA-J Web Store

## 1. Scope and Context

### [SC-001] (stated)
The system shall be a web store for people who are new to online commerce and for new online business owners.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business. Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
- `[interview_turn:T002]` "Yes, that scope sounds right to me. I’m here to focus on what the web store needs to let new online business owners manage products and customer accounts, and let customers browse, cart, and order."
- `[interview_turn:T004]` "I’m speaking as the stakeholder for GAMMA-J, so I’m representing the business side of the web store. My role is to help define what the store needs to do for owners, sales staff, and customers so the team can build something practical for people who are new to online commerce."
- `[interview_turn:T030]` "It would be successful if a new store owner could get the shop running without much technical help, and customers could browse, add items to cart, and place orders without confusion. We’d also want staff to manage products and customer accounts efficiently, with fewer manual steps than they have now. If the system is stable and easy to learn, that would be a big win for us."
- `[interview_turn:T032]` "That summary sounds right to me. The only thing I’d add is that the system should stay simple enough that someone with little e-commerce experience can use it without training, and we should probably keep the first release focused on the core buying and management tasks rather than trying to include too many extras."

## 2. Actors

### [ACT-001] (stated)
Store owners shall use the system to manage the online retail business.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business. Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
- `[interview_turn:T004]` "I’m speaking as the stakeholder for GAMMA-J, so I’m representing the business side of the web store. My role is to help define what the store needs to do for owners, sales staff, and customers so the team can build something practical for people who are new to online commerce."
- `[interview_turn:T028]` "The store owners are definitely important because they’ll care about sales flow, product setup, and overall business rules. Sales personnel are also key since they’ll be using the system day to day to manage products and customer accounts, so the screens need to fit their workflow. If possible, it would also help to hear from a few actual customers who are not very comfortable with online shopping, because this store is meant to be easy for beginners."

### [ACT-002] (stated)
Sales personnel shall use the system to manage products and customer accounts.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business. Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
- `[interview_turn:T004]` "I’m speaking as the stakeholder for GAMMA-J, so I’m representing the business side of the web store. My role is to help define what the store needs to do for owners, sales staff, and customers so the team can build something practical for people who are new to online commerce."
- `[interview_turn:T028]` "The store owners are definitely important because they’ll care about sales flow, product setup, and overall business rules. Sales personnel are also key since they’ll be using the system day to day to manage products and customer accounts, so the screens need to fit their workflow. If possible, it would also help to hear from a few actual customers who are not very comfortable with online shopping, because this store is meant to be easy for beginners."
- `[interview_turn:T030]` "It would be successful if a new store owner could get the shop running without much technical help, and customers could browse, add items to cart, and place orders without confusion. We’d also want staff to manage products and customer accounts efficiently, with fewer manual steps than they have now. If the system is stable and easy to learn, that would be a big win for us."

### [ACT-003] (stated)
Customers shall use the system to browse products, maintain a shopping cart, and place orders.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business. Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
- `[interview_turn:T002]` "Yes, that scope sounds right to me. I’m here to focus on what the web store needs to let new online business owners manage products and customer accounts, and let customers browse, cart, and order."
- `[interview_turn:T006]` "Right now, there isn’t a single proper system in place, which is part of why we need this web store. Product and customer information is handled in a mix of spreadsheets, email, and a few manual records, and ordering is not very streamlined. Customers don’t have a consistent online way to browse, keep a cart, or place orders through us yet."
- `[interview_turn:T008]` "The first things we want to improve are product management and the customer buying flow. We need a straightforward way for staff to add and update products and customer accounts, and for customers to browse, add items to a cart, and complete an order without needing much guidance."
- `[interview_turn:T030]` "It would be successful if a new store owner could get the shop running without much technical help, and customers could browse, add items to cart, and place orders without confusion. We’d also want staff to manage products and customer accounts efficiently, with fewer manual steps than they have now. If the system is stable and easy to learn, that would be a big win for us."

## 3. Functional Requirements

### [FR-001] (stated)
The system shall allow staff to create and update products.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business. Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
- `[interview_turn:T008]` "The first things we want to improve are product management and the customer buying flow. We need a straightforward way for staff to add and update products and customer accounts, and for customers to browse, add items to a cart, and complete an order without needing much guidance."
- `[interview_turn:T016]` "For the first version, I’d put order placement and the shopping cart at the top, along with product browsing and product management. If customers can find items, add them to a cart, and place an order, and staff can keep products current, that gives us the essential business value right away."

### [FR-002] (stated)
The system shall allow staff to create and update customer accounts.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business. Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
- `[interview_turn:T008]` "The first things we want to improve are product management and the customer buying flow. We need a straightforward way for staff to add and update products and customer accounts, and for customers to browse, add items to a cart, and complete an order without needing much guidance."
- `[interview_turn:T026]` "Staff should be able to create and update the core account details like customer name, email, phone number if provided, and delivery address. Customers should be able to view and update their own contact details and address, and ideally see their order history as well. I’d prefer to keep staff control over any sensitive account changes if that becomes relevant later."

### [FR-003] (stated)
The system shall allow customers to browse available products.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business. Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
- `[interview_turn:T002]` "Yes, that scope sounds right to me. I’m here to focus on what the web store needs to let new online business owners manage products and customer accounts, and let customers browse, cart, and order."
- `[interview_turn:T006]` "Right now, there isn’t a single proper system in place, which is part of why we need this web store. Product and customer information is handled in a mix of spreadsheets, email, and a few manual records, and ordering is not very streamlined. Customers don’t have a consistent online way to browse, keep a cart, or place orders through us yet."
- `[interview_turn:T008]` "The first things we want to improve are product management and the customer buying flow. We need a straightforward way for staff to add and update products and customer accounts, and for customers to browse, add items to a cart, and complete an order without needing much guidance."
- `[interview_turn:T030]` "It would be successful if a new store owner could get the shop running without much technical help, and customers could browse, add items to cart, and place orders without confusion. We’d also want staff to manage products and customer accounts efficiently, with fewer manual steps than they have now. If the system is stable and easy to learn, that would be a big win for us."

### [FR-004] (stated)
The system shall allow customers to search products by name.

**Source Evidence:**
- `[interview_turn:T024]` "Customers should at least see the product name, a short description, price, and whether it’s currently available. A product image would be very helpful too, if we have one. Search should let them find products by name, and filtering should probably cover basic things like category and price range so they can narrow results without much effort."

### [FR-005] (stated)
The system shall allow customers to filter products by category and price range.

**Source Evidence:**
- `[interview_turn:T024]` "Customers should at least see the product name, a short description, price, and whether it’s currently available. A product image would be very helpful too, if we have one. Search should let them find products by name, and filtering should probably cover basic things like category and price range so they can narrow results without much effort."

### [FR-006] (stated)
The system shall allow customers to add products to a shopping cart.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business. Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
- `[interview_turn:T008]` "The first things we want to improve are product management and the customer buying flow. We need a straightforward way for staff to add and update products and customer accounts, and for customers to browse, add items to a cart, and complete an order without needing much guidance."
- `[interview_turn:T016]` "For the first version, I’d put order placement and the shopping cart at the top, along with product browsing and product management. If customers can find items, add them to a cart, and place an order, and staff can keep products current, that gives us the essential business value right away."
- `[interview_turn:T018]` "For a first-time customer, the cart should let them add products, change quantities, remove items, and clearly see the total before they check out. Order placement should be simple enough that they can enter their details, confirm the items, and submit the order without creating too many obstacles. It would also help if they get a clear confirmation right away so they know the purchase was successful."
- `[interview_turn:T030]` "It would be successful if a new store owner could get the shop running without much technical help, and customers could browse, add items to cart, and place orders without confusion. We’d also want staff to manage products and customer accounts efficiently, with fewer manual steps than they have now. If the system is stable and easy to learn, that would be a big win for us."

### [FR-007] (stated)
The system shall allow customers to change quantities in the shopping cart.

**Source Evidence:**
- `[interview_turn:T018]` "For a first-time customer, the cart should let them add products, change quantities, remove items, and clearly see the total before they check out. Order placement should be simple enough that they can enter their details, confirm the items, and submit the order without creating too many obstacles. It would also help if they get a clear confirmation right away so they know the purchase was successful."

### [FR-008] (stated)
The system shall allow customers to remove items from the shopping cart.

**Source Evidence:**
- `[interview_turn:T018]` "For a first-time customer, the cart should let them add products, change quantities, remove items, and clearly see the total before they check out. Order placement should be simple enough that they can enter their details, confirm the items, and submit the order without creating too many obstacles. It would also help if they get a clear confirmation right away so they know the purchase was successful."

### [FR-009] (stated)
The system shall show customers the cart total before checkout.

**Source Evidence:**
- `[interview_turn:T018]` "For a first-time customer, the cart should let them add products, change quantities, remove items, and clearly see the total before they check out. Order placement should be simple enough that they can enter their details, confirm the items, and submit the order without creating too many obstacles. It would also help if they get a clear confirmation right away so they know the purchase was successful."

### [FR-010] (stated)
The system shall allow customers to enter order details, confirm the items, and submit the order.

**Source Evidence:**
- `[interview_turn:T018]` "For a first-time customer, the cart should let them add products, change quantities, remove items, and clearly see the total before they check out. Order placement should be simple enough that they can enter their details, confirm the items, and submit the order without creating too many obstacles. It would also help if they get a clear confirmation right away so they know the purchase was successful."
- `[interview_turn:T020]` "We would need the customer’s name, contact email, and a delivery address before the order can be submitted. If we support delivery by phone or need a contact number for follow-up, that would be useful too, but I’d want to confirm whether it’s mandatory or optional. I don’t think we need anything overly complicated at checkout for the first version."

### [FR-011] (stated)
The system shall generate an immediate order confirmation for customers after an order is placed.

**Source Evidence:**
- `[interview_turn:T012]` "Yes, I think order confirmation notifications should be included as a core feature. Customers should get immediate confirmation after placing an order so they know it went through, and staff should also have visibility that a new order has come in."
- `[interview_turn:T018]` "For a first-time customer, the cart should let them add products, change quantities, remove items, and clearly see the total before they check out. Order placement should be simple enough that they can enter their details, confirm the items, and submit the order without creating too many obstacles. It would also help if they get a clear confirmation right away so they know the purchase was successful."
- `[interview_turn:T030]` "It would be successful if a new store owner could get the shop running without much technical help, and customers could browse, add items to cart, and place orders without confusion. We’d also want staff to manage products and customer accounts efficiently, with fewer manual steps than they have now. If the system is stable and easy to learn, that would be a big win for us."

### [FR-012] (stated)
The system shall provide staff visibility that a new order has been placed.

**Source Evidence:**
- `[interview_turn:T012]` "Yes, I think order confirmation notifications should be included as a core feature. Customers should get immediate confirmation after placing an order so they know it went through, and staff should also have visibility that a new order has come in."

### [FR-013] (stated)
The system shall allow customers to view their order history.

**Source Evidence:**
- `[interview_turn:T010]` "Yes, a few additional things would be useful if they fit naturally. It would help to have basic search and filtering on products, order history for customers, and some simple admin reporting so staff can see sales activity. We’d also likely want notifications for order confirmation, but I’d need to check how advanced we want that to be."
- `[interview_turn:T026]` "Staff should be able to create and update the core account details like customer name, email, phone number if provided, and delivery address. Customers should be able to view and update their own contact details and address, and ideally see their order history as well. I’d prefer to keep staff control over any sensitive account changes if that becomes relevant later."

### [FR-014] (stated)
The system shall provide basic sales reporting for staff so they can see sales activity.

**Source Evidence:**
- `[interview_turn:T010]` "Yes, a few additional things would be useful if they fit naturally. It would help to have basic search and filtering on products, order history for customers, and some simple admin reporting so staff can see sales activity. We’d also likely want notifications for order confirmation, but I’d need to check how advanced we want that to be."

### [FR-015] (stated)
The system shall allow customers to view and update their own contact details and address.

**Source Evidence:**
- `[interview_turn:T026]` "Staff should be able to create and update the core account details like customer name, email, phone number if provided, and delivery address. Customers should be able to view and update their own contact details and address, and ideally see their order history as well. I’d prefer to keep staff control over any sensitive account changes if that becomes relevant later."

### [FR-016] (conditional)
The system shall support a simple checkout process for first-time customers.

**Source Evidence:**
- `[interview_turn:T018]` "For a first-time customer, the cart should let them add products, change quantities, remove items, and clearly see the total before they check out. Order placement should be simple enough that they can enter their details, confirm the items, and submit the order without creating too many obstacles. It would also help if they get a clear confirmation right away so they know the purchase was successful."
- `[interview_turn:T020]` "We would need the customer’s name, contact email, and a delivery address before the order can be submitted. If we support delivery by phone or need a contact number for follow-up, that would be useful too, but I’d want to confirm whether it’s mandatory or optional. I don’t think we need anything overly complicated at checkout for the first version."
- `[interview_turn:T032]` "That summary sounds right to me. The only thing I’d add is that the system should stay simple enough that someone with little e-commerce experience can use it without training, and we should probably keep the first release focused on the core buying and management tasks rather than trying to include too many extras."

### [FR-017] (stated)
The system shall require the customer's name, contact email, and delivery address before an order can be submitted.

**Source Evidence:**
- `[interview_turn:T020]` "We would need the customer’s name, contact email, and a delivery address before the order can be submitted. If we support delivery by phone or need a contact number for follow-up, that would be useful too, but I’d want to confirm whether it’s mandatory or optional. I don’t think we need anything overly complicated at checkout for the first version."

### [FR-018] (stated)
The system shall treat the contact number as optional at checkout.

**Source Evidence:**
- `[interview_turn:T020]` "We would need the customer’s name, contact email, and a delivery address before the order can be submitted. If we support delivery by phone or need a contact number for follow-up, that would be useful too, but I’d want to confirm whether it’s mandatory or optional. I don’t think we need anything overly complicated at checkout for the first version."
- `[interview_turn:T022]` "I’d make the contact number optional at checkout. That keeps the process simpler for first-time customers, and we can still collect it when it’s available for delivery or order follow-up."

### [FR-019] (stated)
The system shall display product name, short description, price, and current availability for each product.

**Source Evidence:**
- `[interview_turn:T024]` "Customers should at least see the product name, a short description, price, and whether it’s currently available. A product image would be very helpful too, if we have one. Search should let them find products by name, and filtering should probably cover basic things like category and price range so they can narrow results without much effort."

### [FR-020] (conditional)
The system shall display a product image when one is available.

**Source Evidence:**
- `[interview_turn:T024]` "Customers should at least see the product name, a short description, price, and whether it’s currently available. A product image would be very helpful too, if we have one. Search should let them find products by name, and filtering should probably cover basic things like category and price range so they can narrow results without much effort."

### [FR-021] (stated)
The system shall allow customers to get immediate confirmation that their purchase was successful.

**Source Evidence:**
- `[interview_turn:T018]` "For a first-time customer, the cart should let them add products, change quantities, remove items, and clearly see the total before they check out. Order placement should be simple enough that they can enter their details, confirm the items, and submit the order without creating too many obstacles. It would also help if they get a clear confirmation right away so they know the purchase was successful."
- `[interview_turn:T012]` "Yes, I think order confirmation notifications should be included as a core feature. Customers should get immediate confirmation after placing an order so they know it went through, and staff should also have visibility that a new order has come in."

## 4. Business Rules and Constraints

### [BR-001] (stated)
The first version shall prioritize order placement, shopping cart, product browsing, and product management.

**Source Evidence:**
- `[interview_turn:T016]` "For the first version, I’d put order placement and the shopping cart at the top, along with product browsing and product management. If customers can find items, add them to a cart, and place an order, and staff can keep products current, that gives us the essential business value right away."

### [BR-002] (stated)
The first release shall stay focused on the core buying and management tasks rather than including too many extras.

**Source Evidence:**
- `[interview_turn:T032]` "That summary sounds right to me. The only thing I’d add is that the system should stay simple enough that someone with little e-commerce experience can use it without training, and we should probably keep the first release focused on the core buying and management tasks rather than trying to include too many extras."

### [BR-003] (stated)
The system should be simple enough that someone with little e-commerce experience can use it without training.

**Source Evidence:**
- `[interview_turn:T032]` "That summary sounds right to me. The only thing I’d add is that the system should stay simple enough that someone with little e-commerce experience can use it without training, and we should probably keep the first release focused on the core buying and management tasks rather than trying to include too many extras."

### [BR-004] (stated)
The system should let a new store owner get the shop running without much technical help.

**Source Evidence:**
- `[interview_turn:T030]` "It would be successful if a new store owner could get the shop running without much technical help, and customers could browse, add items to cart, and place orders without confusion. We’d also want staff to manage products and customer accounts efficiently, with fewer manual steps than they have now. If the system is stable and easy to learn, that would be a big win for us."

### [BR-005] (stated)
The system should be stable and easy to learn.

**Source Evidence:**
- `[interview_turn:T030]` "It would be successful if a new store owner could get the shop running without much technical help, and customers could browse, add items to cart, and place orders without confusion. We’d also want staff to manage products and customer accounts efficiently, with fewer manual steps than they have now. If the system is stable and easy to learn, that would be a big win for us."

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

**Source Evidence:**
- `[interview_turn:T010]` "Yes, a few additional things would be useful if they fit naturally. It would help to have basic search and filtering on products, order history for customers, and some simple admin reporting so staff can see sales activity. We’d also likely want notifications for order confirmation, but I’d need to check how advanced we want that to be."
- `[interview_turn:T012]` "Yes, I think order confirmation notifications should be included as a core feature. Customers should get immediate confirmation after placing an order so they know it went through, and staff should also have visibility that a new order has come in."
