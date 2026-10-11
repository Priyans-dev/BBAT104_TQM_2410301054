# System Architecture Flowchart

**Project:** Restaurant Billing System
**Quality Goal:** Q06 - Reduce Duplicate Entries

The flowchart below shows the main flow of the system. The duplicate-prevention checks (Search Before Add, Pre-add Validation, Confirmation Dialog and Unique ID) are part of the Q06 quality goal.

```mermaid
flowchart TD
    A([Start]) --> B[Main Dashboard]
    B --> C[Menu Management]
    B --> D[Billing]
    B --> E[Bill History]
    B --> F([Exit])

    C --> C1[Enter Menu Item Details]
    C1 --> C2[Search Before Add]
    C2 --> C3{Item Already Exists?}
    C3 -->|Yes| C4[Show Duplicate Warning]
    C4 --> C1
    C3 -->|No| C5[Pre-add Validation]
    C5 --> C6{Data Valid?}
    C6 -->|No| C7[Show Error Message]
    C7 --> C1
    C6 -->|Yes| C8[Confirmation Dialog]
    C8 --> C9{User Confirms?}
    C9 -->|No| B
    C9 -->|Yes| DB[("SQLite Database with Unique ID Constraint")]
    DB --> B

    D --> D1[Select Menu Items and Quantity]
    D1 --> D2[Calculate Subtotal, Tax and Total]
    D2 --> D3[Confirmation Dialog before Bill Generation]
    D3 --> D4{User Confirms?}
    D4 -->|No| D1
    D4 -->|Yes| D5[Generate Bill with Unique Bill ID]
    D5 --> DB

    E --> E1[View or Search Past Bills]
    E1 --> DB
    DB --> E2[Display Bill Records]
    E2 --> B
```