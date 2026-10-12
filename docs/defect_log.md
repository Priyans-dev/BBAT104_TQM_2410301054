# Defect Log and Checksheet

**Project:** Restaurant Billing System
**Quality Goal:** Q06 - Reduce Duplicate Entries
**Student:** Priyanshu Negi (Roll No. 2410301054)

## 1. Test Set (19 checks)

The same 19 checks are run on two versions of the system.

- **Round 1:** the version before the Q06 features (commit "Add bill history page with search and receipt view"). Found by code review of that version.
- **Round 2:** the current version, after all Q06 features. Found by manual testing.

Setup: the menu already contains the item `Paneer Tikka` (price 250) and one more item `Veg Pulao`.

| TC | Module | Check (what to do) | Expected result | Round 1 | Round 2 |
|---|---|---|---|---|---|
| TC-01 | Add Item | Add name `Paneer Tikka` again | Blocked as duplicate | Fail | Pass |
| TC-02 | Add Item | Add name `paneer tikka` (small letters) | Blocked as duplicate | Fail | Pass |
| TC-03 | Add Item | Add name `Paneer Tikka ` (extra space at the end) | Blocked as duplicate | Fail | Pass |
| TC-04 | Add Item | Add name `Paneer   Tikka` (extra spaces inside) | Blocked as duplicate | Fail | Pass |
| TC-05 | Edit Item | Edit `Veg Pulao` and change its name to `Paneer Tikka` | Blocked as duplicate | Fail | Pass |
| TC-06 | Add Item | Name `@@@` | Rejected, invalid name | Fail | Pass |
| TC-07 | Add Item | Name `123` (no letter) | Rejected, invalid name | Fail | Pass |
| TC-08 | Add Item | Name `A` (one character) | Rejected, too short | Fail | Pass |
| TC-09 | Add Item | Name of 60 characters (type `Abcdefghij` six times) | Rejected, too long | Fail | Pass |
| TC-10 | Add Item | Valid name, price `250.999` | Rejected, more than 2 decimals | Fail | Pass |
| TC-11 | Add Item | Valid name, price `99999` | Rejected, above maximum | Fail | Pass |
| TC-12 | Add Item | Valid name, price `nan` | Rejected, not a valid amount | Fail | Pass |
| TC-13 | Add Item | Valid name, price `1e5` | Rejected, not a valid amount | Fail | Pass |
| TC-14 | Add Item | Valid name, price `abc` | Rejected | Pass | Pass |
| TC-15 | Add Item | Valid name, price `-50` | Rejected | Pass | Pass |
| TC-16 | Add Item | Valid name, price `0` | Rejected | Pass | Pass |
| TC-17 | Add Item | Empty name | Rejected | Pass | Pass |
| TC-18 | Add Item | Fill a valid new item and press Save | Confirmation question appears before saving | Fail | Pass |
| TC-19 | Edit Item | Change the price of an item and press Save | Confirmation question appears before saving | Fail | Pass |

| Result | Round 1 | Round 2 |
|---|---|---|
| Checks run | 19 | 19 |
| Passed | 4 | 19 |
| Failed | 15 | 0 |

## 2. Defect Log

| Defect ID | Module | Description | Test checks | Occurrences | Severity | Found in | Found by | Status | Fixed by | FMEA link |
|---|---|---|---|---|---|---|---|---|---|---|
| DF-01 | Menu | Duplicate item accepted (same name, different case or extra spaces) | TC-01 to TC-04 | 4 | High | Before Q06 version | Code review | Closed | Unique Constraint and Search Before Add | FM-01 |
| DF-02 | Menu | Item renamed to the name of another item (creates a duplicate) | TC-05 | 1 | High | Before Q06 version | Code review | Closed | Unique Constraint | FM-01 |
| DF-03 | Menu | Invalid item name accepted (symbols only, digits only, one character, 60 characters) | TC-06 to TC-09 | 4 | Medium | Before Q06 version | Code review | Closed | Pre-add Validation | FM-03 |
| DF-04 | Menu | Invalid price accepted (3 decimals, above 10000, nan, 1e5) | TC-10 to TC-13 | 4 | High | Before Q06 version | Code review | Closed | Pre-add Validation | FM-03 |
| DF-05 | Menu | Item added without a confirmation question | TC-18 | 1 | Medium | Before Q06 version | Code review | Closed | Confirmation Dialogs | FM-02 |
| DF-06 | Menu | Item updated without a confirmation question | TC-19 | 1 | Medium | Before Q06 version | Code review | Closed | Confirmation Dialogs | FM-02 |
| DF-07 | Application | Running src/menu_page.py directly gives ModuleNotFoundError: No module named 'src' | Observed during development | 1 | Low | During development | Manual run | Open until README is updated | Run only main.py (to be written in README and User Manual) | None |
| DF-08 | Billing | Bill ID was taken from a row count, so it could repeat if a bill record was ever removed | Not triggered in testing | 0 | Medium | Before Q06 version | Code review | Closed | Bill ID taken from the highest existing number | FM-04 |

DF-08 is a latent defect. It did not occur during testing, so it is not counted in the checksheet.

## 3. Checksheet (defect occurrences by category, Round 1)

| Defect Category | Defects included | Tally | Count |
|---|---|---|---|
| Duplicate entries accepted | DF-01, DF-02 | IIIII | 5 |
| Invalid item name accepted | DF-03 | IIII | 4 |
| Invalid price accepted | DF-04 | IIII | 4 |
| Missing confirmation | DF-05, DF-06 | II | 2 |
| Wrong way of running the application | DF-07 | I | 1 |
| **Total** | | | **16** |

## 4. Pareto Data (sorted from highest to lowest)

| Rank | Category | Count | Percentage | Cumulative % |
|---|---|---|---|---|
| 1 | Duplicate entries accepted | 5 | 31.25% | 31.25% |
| 2 | Invalid item name accepted | 4 | 25.00% | 56.25% |
| 3 | Invalid price accepted | 4 | 25.00% | 81.25% |
| 4 | Missing confirmation | 2 | 12.50% | 93.75% |
| 5 | Wrong way of running the application | 1 | 6.25% | 100.00% |

The first three categories cause 13 of 16 defects (81.25%). These are the "vital few" and match the 80/20 rule.

## 5. Result After Fixes (Round 2)

All 19 checks pass in the current version. The duplicate count in the Duplicate Attempt Log shows how many duplicate entries are now blocked instead of being stored.