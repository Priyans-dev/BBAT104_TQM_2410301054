# FMEA - Failure Mode and Effects Analysis

**Project:** Restaurant Billing System
**Quality Goal:** Q06 - Reduce Duplicate Entries
**Student:** Priyanshu Negi (Roll No. 2410301054)

**Formula:** RPN = Severity x Occurrence x Detection (each rated from 1 to 10)

## 1. Rating Scales

| Rating | Severity (S) | Occurrence (O) | Detection (D) |
|---|---|---|---|
| 1-2 | Barely noticeable | Almost never happens | Always caught before the user sees it |
| 3-4 | Minor annoyance | Happens rarely | Usually caught |
| 5-6 | Wrong data or confusion for the user | Happens sometimes | Caught only by careful checking |
| 7-8 | Wrong bills or lost business data | Happens often | Rarely caught in time |
| 9-10 | Financial loss or complete data loss | Happens almost every time | Cannot be caught |

**Priority rule:** RPN 150 or more = High risk, 100 to 149 = Medium risk, below 100 = Low risk.

## 2. FMEA Matrix (sorted by RPN, highest risk first)

The "Before" columns show the risk without the improvement. The "After" columns show the risk after the improvement was built into the system.

| ID | Failure Mode | Effect | Cause | S | O | D | RPN (Before) | Priority | Mitigation (Action Taken) | S | O | D | RPN (After) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FM-01 | Duplicate menu item is added | Same dish appears twice with different prices, confusing billing | No check for existing items | 6 | 7 | 5 | 210 | High | Unique constraint on item name and Search Before Add with live warning | 6 | 2 | 2 | 24 |
| FM-02 | Item added, updated or deleted by mistake | Menu data becomes wrong or is lost | No confirmation before changes | 6 | 5 | 6 | 180 | High | Confirmation Dialogs for add, update and delete | 6 | 2 | 2 | 24 |
| FM-03 | Invalid data saved (empty name, negative price, text in price) | Wrong bills or application errors | No input validation | 7 | 6 | 4 | 168 | High | Pre-add Validation for name, category and price | 7 | 2 | 2 | 28 |
| FM-04 | Duplicate Bill ID generated | Bill record rejected or overwritten | Bill number taken from a count instead of the highest number | 8 | 3 | 5 | 120 | Medium | Bill ID taken from highest existing number and enforced as PRIMARY KEY | 8 | 1 | 2 | 16 |
| FM-05 | Billing shows an old price or a deleted item | Customer charged a wrong price | Menu list not refreshed after changes | 6 | 4 | 5 | 120 | Medium | Billing menu list refreshes every time the Billing page is opened | 6 | 1 | 2 | 12 |
| FM-06 | Wrong subtotal, tax or total | Customer overcharged or undercharged | Manual calculation or rounding error | 9 | 3 | 4 | 108 | Medium | Automatic calculation with rounding to 2 decimals | 9 | 1 | 3 | 27 |
| FM-07 | Database file missing or damaged | All menu and bill data lost | File deleted or corrupted | 9 | 2 | 6 | 108 | Medium | Tables are recreated automatically at startup. Regular manual backup of restaurant.db is recommended (planned) | 9 | 2 | 4 | 72 |
| FM-08 | Invalid quantity entered (0, negative or text) | Wrong bill amount | No quantity validation | 5 | 5 | 3 | 75 | Low | Quantity must be a whole number of at least 1 | 5 | 1 | 1 | 5 |
| FM-09 | Empty bill generated | Blank bill stored in history | No check for an empty bill | 4 | 4 | 3 | 48 | Low | System blocks Generate Bill when no item is added | 4 | 1 | 1 | 4 |

## 3. Summary

| Measure | Value |
|---|---|
| Total failure modes analysed | 9 |
| High risk before mitigation (RPN 150 or more) | 3 (FM-01, FM-02, FM-03) |
| Highest RPN before mitigation | 210 (FM-01, duplicate menu item) |
| Highest RPN after mitigation | 72 (FM-07, database loss) |
| Failure modes with all actions implemented | 8 of 9 |

## 4. Remaining Risk

FM-07 still has the highest remaining RPN. The system cannot stop a user from deleting the database file. The planned mitigation is a regular manual backup of `restaurant.db`.

## 5. Note

Occurrence ratings are estimates based on how the system behaves without the control. Real defect counts are recorded in the Defect Log and Checksheet (Review 4) and are used in the Pareto chart.