# Floral-Viewer
## A flexible flower database based on PyQt5

# Installation
This project depends on [PyQt5](https://pypi.org/project/PyQt5/5.6/). We recommend using Python version 3.5 or greater.
To install PyQt5, run the following command:
> pip install PyQt5

From there, you can run python Floral-Viewer.pyw to launch the GUI application.

# User Guide

When you run Floral-Viewer.pyw, you are prompted for credentials. By default, these are `admin` and `password` respectively. 

After successfully being authenticated, you are presented with the main window. This window contains a few things namely:

* **The Search Box**, for entering in values to search
* **The Limit Box**, for specifying the number of results
* **The Select a Flower Button**, which produces a dialog for the user to select from a list of flowers
* **The Create New Entry Button**, which you may press to insert values into the database
* **The Tabbed Sheet**, which presents the results of the user's queries

To run a query of your own, type in the **The Search Box** to filter what results appear in **The Tabbed Sheet**. Alternatively, you could filter by selecting from a list of flowers by pressing **The Select a Flower Button**. You can control the number of results that appear by typing a limit into **The Limit Box**. (If the box is empty, unlimited results are allowed). By default, sightings are sorted in order of descending date. 

**The Tabbed Sheet** contains 3 tabs corresponding to the 3 tables in the database: Sightings, Flowers, and Features. While the Sightings tab is initially selected, you can select another tab to explore entries in that respective table. 

Updating an entry is simple. To update an entry, simply click on a cell in the table. This will produce a dialog box, which allows you to type a new value into that cell. (Each value inside an entry must be changed one-by-one.) We perform a wide-range of error checking, so you will be informed if your proposed update causes an error.

To add an entry to the tables, press **The Create a New Entry Button**. This will produce a dialog box, where you can select the type of entry to create (Sighting, Flower, or Feature). Depending on your selection, you are presented with several fields to fill out before confirming your selection. As with the update dialog box, if any fields are invalid, you will be notified.

All changes will be automatically saved upon a clean exit. If a critical error occurs, your changes to the database will be discarded.

# Implementation Details

All of the SQLite3 calls are made inside FlowerDB.py. Here, we define the FlowerDB class, which acts as a wrapper to our SQLite3 database. Here are a few highlights of our implementation.

## Sanitization
We avoided string formatting / interpolation when writing our SQLite3 queries, instead opting for the safer argument-based approach recommended by Python. This reduces the risk of an SQL injection. 

## Authentication
Before accessing the database, a user must present credentials. This is intended as a proof-of concept. This feature is not secure, since these credentials are tied to the database (which could be read using an outside application).

## Logging
We maintain a log file that logs every query that is executed during a session. We also log all authentication attempts to this log, keeping a record of who has attempted to access the database. (Again, this is insecure and intended as a proof-of-concept). 

## Indexing
We constructed indexes for the Sightings table, in the hopes of facilitating queries.

## Transactions
For the `FlowerDB` class, we implemented context manager functionality. In effect, this means that all build-up and tear-down is automated by using the Python's [with statement](https://docs.python.org/3/reference/compound_stmts.html#with). Thus, when a with statement is used, an instance of `FlowerDB` automatically connects to its database when needed. In our implementation, if a critical error occurs in this with statement, changes will not be saved. Otherwise, if when we exit the with statement normally, the `FlowerDB` instance automatically commits its changes to the database.
