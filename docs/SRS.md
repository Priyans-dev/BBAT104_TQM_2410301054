# Software Requirements Specification (SRS)

**Project:** Restaurant Billing System
**Course:** BBAT104 - Fundamentals of TQM (Session 2026-27)
**Student:** Priyanshu Negi (Roll No. 2410301054)
**Version:** 1.0 (Draft)

## 1. Introduction

### 1.1 Purpose
This document describes the requirements of the Restaurant Billing System, a desktop application that manages menu items and generates bills. The project applies TQM principles, with the quality goal of reducing duplicate entries.

### 1.2 Scope
The system lets restaurant staff manage the menu, create customer bills with automatic tax calculation, and view past bills. It prevents duplicate records using validation checks, unique IDs and confirmation dialogs.

**In scope:** menu management, billing, bill history, duplicate prevention.
**Out of scope:** online ordering, payment gateway, multi-branch support, mobile app.

### 1.3 Definitions
- **CRUD:** Create, Read, Update, Delete
- **CTQ:** Critical to Quality
- **Q06:** Assigned quality goal - Reduce Duplicate Entries

## 2. Overall Description

### 2.1 Product Perspective
A standalone desktop application. Data is stored locally in an SQLite database.

### 2.2 User Classes
- **Cashier / Staff:** creates bills and searches menu items.
- **Admin / Manager:** manages the menu and views bill history.

### 2.3 Operating Environment
- Windows laptop or PC
- Python 3.x with CustomTkinter and SQLite3

## 3. Functional Requirements

| ID | Requirement |
|---|---|
| FR-01 | The system shall allow adding a new menu item (name, category, price). |
| FR-02 | The system shall display all menu items in a table. |
| FR-03 | The system shall allow updating a menu item. |
| FR-04 | The system shall allow deleting a menu item. |
| FR-05 | The system shall allow creating a bill by selecting items and quantities. |
| FR-06 | The system shall calculate subtotal, tax and total automatically. |
| FR-07 | The system shall store every bill with a unique Bill ID. |
| FR-08 | The system shall allow viewing and searching past bills. |

## 4. Quality Goal Requirements (Q06 - Reduce Duplicate Entries)

| ID | Feature | Requirement |
|---|---|---|
| Q06-01 | Unique ID Constraints | The database shall enforce unique IDs for menu items and bills. |
| Q06-02 | Pre-add Validation | The system shall validate all fields before saving a new record. |
| Q06-03 | Search Before Add | The system shall search for an existing item before adding a new one and warn the user if found. |
| Q06-04 | Confirmation Dialogs | The system shall ask for confirmation before adding, updating or deleting a record. |
| Q06-05 | Duplicate Attempt Log (proposed 5th feature) | The system shall record every blocked duplicate attempt with date and time. This feature is pending faculty confirmation. |

## 5. Non-Functional Requirements

- **Performance:** a bill shall be generated in less than 3 seconds.
- **Usability:** a modern, clean interface that a new user can learn in under 2 minutes.
- **Reliability:** the system shall not crash on invalid input.
- **Data Integrity:** no duplicate menu items or bill IDs shall exist in the database.
- **Maintainability:** code shall be modular, with separate files for database and interface.

## 6. Constraints

- Developed in Python using free tools only.
- Data stored in SQLite (no internet required).
- Project follows the BBAT104 course guidelines.