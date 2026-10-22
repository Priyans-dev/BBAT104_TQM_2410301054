# PDCA Log (Plan - Do - Check - Act)

**Project:** Restaurant Billing System
**Quality Goal:** Q06 - Reduce Duplicate Entries
**Student:** Priyanshu Negi (Roll No. 2410301054)

PDCA is the continuous improvement cycle of TQM (Kaizen). Each cycle below starts from measured data, makes a change, checks the result with the same measure, and then makes the improvement a standard.

---

## Cycle 1: Reduce duplicate and invalid menu entries (Status: Completed and verified)

### PLAN

| Item | Details |
|---|---|
| Problem | The Pareto chart shows that 13 of 16 defects (81.25%) come from three categories: duplicate entries, invalid item name and invalid price. The largest single category is "Duplicate entries accepted" (5 defects, 31.25%). |
| Root causes | From the Fishbone diagram: no unique constraint, no search before add, no input validation, names not cleaned (capitals and spaces), no confirmation before saving. |
| Target | 0 duplicate items accepted, 0 invalid entries accepted, and all 19 checks in the Defect Log passing. |
| Planned actions | Build the five Q06 features: Unique ID Constraints, Search Before Add, Pre-add Validation, Confirmation Dialogs and Duplicate Attempt Log. |

### DO

| Q06 Feature | What was built | GitHub commit message |
|---|---|---|
| Unique ID Constraints | Unique index on item name (ignoring capitals and extra spaces) and unique Bill IDs | Add unique constraint to prevent duplicate menu items |
| Search Before Add | Menu search box and a live "item already exists" warning while typing | Add search before add for menu items |
| Pre-add Validation | Rules for name, category and price checked before saving | Add pre-add validation for menu items |
| Confirmation Dialogs | "Are you sure?" question before add, update, delete and bill generation | Add confirmation dialogs for adding and updating items |
| Duplicate Attempt Log | Every blocked duplicate attempt is stored with date, time and action | Add duplicate attempt log as fifth Q06 feature |

### CHECK

The same 19 checks (see `defect_log.md`) were run before and after the changes. The "before" result comes from a code review of the earlier version, the "after" result from manual testing of the current version.

| Measure | Before | After | Change |
|---|---|---|---|
| Checks passed (out of 19) | 4 | 19 | +15 |
| Checks failed | 15 | 0 | -15 |
| Defects found in the test set | 16 | 0 | -16 |
| Total RPN of all 9 failure modes (FMEA) | 1137 | 212 | -81.4% |
| Highest single RPN (FMEA) | 210 (FM-01, duplicate item) | 72 (FM-07, database loss) | -138 |

| CTQ | Target | Result |
|---|---|---|
| CTQ-01 Duplicate menu items | 0 | Met (TC-01 to TC-05 pass) |
| CTQ-05 Invalid entries accepted | 0 | Met (TC-06 to TC-13 pass) |
| CTQ-06 Changes without confirmation | 0 | Met (TC-18 and TC-19 pass) |

Remaining risk: FM-07 (database file loss) still has RPN 72, and DF-07 (wrong way of running the application) is still open.

### ACT

- The unique constraint, validation rules and confirmation dialogs are now the standard for the menu form. Every new input form must use the same three controls.
- The 19 checks are kept as a regression test set and are repeated after every future change.
- The Duplicate Attempt Log is kept so that the number of blocked duplicates can be monitored over time.
- Open issues are moved to Cycle 2.

---

## Cycle 2: Close the remaining risks (Status: In progress)

### PLAN

| Item | Details |
|---|---|
| Problem | DF-07 is open: running `src/menu_page.py` directly gives `ModuleNotFoundError`. FM-07 (database loss) has the highest remaining RPN of 72. |
| Root cause | The user does not know that the application must be started from `main.py`. There is no backup routine for `restaurant.db`. |
| Target | DF-07 closed, and FM-07 RPN reduced to 36 or lower. |
| Planned actions | Write clear run instructions in README.md and the User Manual (run only `python main.py` from the project folder). Add a backup instruction for `restaurant.db`. |

### DO

Planned: the instructions will be written in the README.md and User Manual commits.

### CHECK

To be completed after the README and User Manual are committed. The check is: a new user follows only the README and starts the application on the first attempt, and the backup steps work.

### ACT

To be completed after the check. If the check passes, DF-07 is marked Closed in `defect_log.md` and the FM-07 ratings in `FMEA.md` are updated.

---

## Summary of Continuous Improvement

| Cycle | Focus | Status |
|---|---|---|
| 1 | Duplicate and invalid entries (Q06) | Completed, verified with data |
| 2 | Wrong way of running the application and database backup | In progress |