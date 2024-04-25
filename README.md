# Store Management System

## Introduction

This project is a Store Management System developed using MySQL and Python with connectors, featuring a Graphical User Interface (GUI) for enhanced usability. The primary objective is to create a user-friendly, scalable, and secure system to efficiently manage a store's inventory, sales, purchases, and customer data.

## What is Store Management System?

A Store Management System is a crucial tool for store owners to effectively manage various aspects of their business operations, including inventory, sales, purchases, and customer data. By automating processes, this system helps store owners save time, reduce costs, and enhance overall efficiency.

## Technologies Used

- MySQL
- Python
- Python-MySQL connector
- Tkinter Library for Python

## Problem Statement

Manual management of store operations such as inventory, sales, purchases, and customer data can be time-consuming and error-prone. With the increasing complexity of modern stores and the rise in online sales, there's a growing need for a reliable and efficient system to manage these operations effectively. The current manual processes are prone to errors, leading to lost sales, customer dissatisfaction, and increased operational costs. Hence, there's a need for an automated, scalable, and secure Store Management System implemented using MySQL and Python.

## About the Project

This project aims to design and implement a Store Management System using MySQL and Python. The system automates processes related to inventory management, sales, purchases, and customer data, thereby improving efficiency. Key features include inventory management, sales management, purchasing management, user management, and reporting. The system is designed to be scalable, secure, and user-friendly, with real-time reporting and analysis capabilities.

## ER-Diagram

### Entities:
- Customer
- Dealer
- Invoices
- Invoice Details (Weak Entity)
- Purchases
- Purchase Details (Weak Entity)
- Product

### Entity-Relations:
- Customer - Invoices
- Product - Purchase Details
- Invoice – Invoice Details
- Invoice Details – Product
- Dealer – Purchases
- Purchases Details – Purchases

### Relationship Properties:
- Customer - Invoices (One-to-Many)
- Product - Purchase Details (One-to-Many)
- Invoice - Invoice Details (One-to-Many)
- Product - Invoice Details (One-to-Many)
- Dealer - Purchases (One-to-Many)
- Purchases - Purchases Details (One-to-Many)

## Relational Model

The relation is normalized till BCNF, resulting in 7 tables as mentioned in the ER diagram.

## Frontend

[Include details about the GUI here.]

## Setup and Usage

[Include instructions on how to set up and run the application, any prerequisites, and other relevant information for users and developers.]

