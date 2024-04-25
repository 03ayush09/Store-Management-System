import mysql.connector

#Replace these deatils 
mysql_host = "localhost"
mysql_user = "root"
mysql_password = "ap0309"
mysql_database = "db"

mycon = mysql.connector.connect(host=mysql_host,user=mysql_user,passwd=mysql_password,database=mysql_database)
cur = mycon.cursor()

cur.execute(
'''CREATE TABLE Product
(PID varchar(4) PRIMARY KEY,
PName varchar(20) NOT NULL,
Brand varchar(20),
Units integer NOT NULL,
Rate Decimal(10,2) NOT NULL)''' 
)

cur.execute('''INSERT INTO Product (PID, PName, Brand, Units, Rate) 
VALUES
('P001', 'iPhone 13 Pro', 'Apple', 10, 1099.00),
('P002', 'Galaxy S21 Ultra', 'Samsung', 20, 1299.99),
('P003', 'MacBook Pro', 'Apple', 5, 1999.00),
('P004', 'Surface Laptop 4', 'Microsoft', 15, 1399.99),
('P005', 'Pixel 6', 'Google', 30, 899.00),
('P006', 'AirPods Pro', 'Apple', 50, 249.00),
('P007', 'Galaxy Watch 4', 'Samsung', 25, 349.99),
('P008', 'Xbox Series X', 'Microsoft', 8, 499.99),
('P009', 'PlayStation 5', 'Sony', 12, 499.99),
('P010', 'Kindle Paperwhite', 'Amazon', 30, 129.99),
('P011', 'Fitbit Charge 5', 'Fitbit', 15, 179.95),
('P012', 'Bose QuietComfort 35', 'Bose', 20, 329.99),
('P013', 'Roomba i7+', 'iRobot', 5, 799.99),
('P014', 'Apple Watch Series 7', 'Apple', 15, 399.00),
('P015', 'Google Nest Hub Max', 'Google', 10, 229.99),
('P016', 'LG OLED65C1PUB', 'LG', 3, 2099.99),
('P017', 'Canon EOS R6', 'Canon', 7, 2499.00),
('P018', 'Sonos Beam', 'Sonos', 10, 399.00),
('P019', 'Microsoft Surface', 'Microsoft', 25, 1099.99),
('P020', 'GoPro HERO10 Black', 'GoPro', 5, 399.99),
('P021', 'JBL Flip 5', 'JBL', 30, 119.95),
('P022', 'DJI Mavic 3 Pro', 'DJI', 2, 1999.00),
('P023', 'Samsung 49" CRG9', 'Samsung', 5, 1499.99),
('P024', 'Logitech MX Master 3', 'Logitech', 20, 99.99),
('P025', 'Sony WH-1000XM4', 'Sony', 15, 349.99)''')


cur.execute('''CREATE TABLE Customer
(CID varchar(4) PRIMARY KEY,
CName varchar(20) NOT NULL,
Address varchar(30),
City varchar(20),
Phone char(10))''')

cur.execute('''INSERT INTO Customer (CID, CName, Address, City, Phone) VALUES
('C001', 'John Smith', '123 Main St', 'New York', '1234567890'),
('C002', 'Jane Doe', '456 Maple Ave', 'Los Angeles', '2345678901'),
('C003', 'Mike Johnson', '789 Oak St', 'Chicago', '3456789012'),
('C004', 'Emily Wilson', '1010 Pine St', 'Houston', '4567890123'),
('C005', 'David Lee', '1212 Elm St', 'Boston', '5678901234'),
('C006', 'Sarah Kim', '1414 Birch Rd', 'Seattle', '6789012345'),
('C007', 'Tom Chen', '1717 Cedar St', 'San Francisco', '7890123456'),
('C008', 'Mary Johnson', '2020 Maple Ave', 'Dallas', '8901234567'),
('C009', 'Alex Rodriguez', '2323 Oak St', 'Miami', '9012345678'),
('C010', 'Lisa Brown', '2626 Pine St', 'Philadelphia', '9985547463'),
('C011', 'Kevin Davis', '2929 Elm St', 'Atlanta', '5247125364'),
('C012', 'Karen Wilson', '3232 Birch Rd', 'Washington D.C.', '7854693215'),
('C013', 'Bob Smith', '3535 Cedar St', 'Denver', '2510365478'),
('C014', 'Linda Lee', '3838 Maple Ave', 'Phoenix', '7854630219'),
('C015', 'Samuel Kim', '4141 Oak St', 'Portland', '3652014897'),
('C016', 'Lucy Chen', '4444 Pine St', 'San Diego', '8546321790'),
('C017', 'Paul Johnson', '4747 Elm St', 'Las Vegas', '9622447530'),
('C018', 'Grace Rodriguez', '5050 Birch Rd', 'Seattle', '4752123698'),
('C019', 'George Brown', '5353 Cedar St', 'San Francisco', '3652147890'),
('C020', 'Cathy Davis', '5656 Maple Ave', 'Dallas', '9654123870'),
('C021', 'Tim Wilson', '5959 Oak St', 'Miami', '1425358790'),
('C022', 'Maggie Smith', '6262 Pine St', 'Philadelphia', '4523698710'),
('C023', 'Frank Lee', '6565 Elm St', 'Atlanta', '7854123690'),
('C024', 'Emma Kim', '6868 Birch Rd', 'Washington D.C.', '5874693210'),
('C025', 'Peter Chen', '7171 Cedar St', 'Denver', '2014536987')''')


cur.execute('''CREATE TABLE Invoices
(InvoiceID varchar(6) PRIMARY KEY,
CID varchar(4) NOT NULL,
InvoiceDate DATE NOT NULL,
CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
TotalAmt DECIMAL(10,2),
FOREIGN KEY (CID) REFERENCES Customer(CID) ON DELETE CASCADE)''')

cur.execute('''INSERT INTO Invoices (InvoiceID, CID, InvoiceDate, TotalAmt)
VALUES
    ('I00001', 'C001', '2023-04-11', 7995.07),
    ('I00002', 'C002', '2023-04-12', 4127.00),
    ('I00003', 'C003', '2023-04-13', 18000.03),
    ('I00004', 'C004', '2023-04-14', 13896.81),
    ('I00005', 'C001', '2023-04-15', 15036.88),
    ('I00006', 'C004', '2023-04-13', 6441.99),
    ('I00007', 'C003', '2022-01-15', 758.90),
    ('I00008', 'C002', '2022-02-02', 1138.86),
    ('I00009', 'C005', '2022-02-21', 5656.96),
    ('I00010', 'C006', '2022-03-05', 3227.98)''')

cur.execute('''CREATE TABLE InvoiceDetails (
  LineID INT AUTO_INCREMENT PRIMARY KEY,
  InvoiceID VARCHAR(6) NOT NULL,
  PID varchar(4) NOT NULL,
  Quantity INT NOT NULL,
  Rate DECIMAL(10,2) NOT NULL,
  Discount DECIMAL(10,2) DEFAULT 0,
  FOREIGN KEY (InvoiceID) REFERENCES Invoices(InvoiceID) ON DELETE CASCADE,
  FOREIGN KEY (PID) REFERENCES Product(PID)
)''')

cur.execute('''INSERT INTO InvoiceDetails (InvoiceID, PID, Quantity, Rate, Discount)
VALUES
('I00001', 'P001', 2, 1099.00, 0.00),
('I00001', 'P005', 1, 899.00, 89.90),
('I00001', 'P003', 2, 1999.00, 0),
('I00001', 'P012', 3, 329.99, 0),
('I00002', 'P001', 1, 1099.00, 0),
('I00002', 'P003', 1, 1999.00, 0.00),
('I00002', 'P007', 2, 349.99, 34.99),
('I00002', 'P018', 1, 399.00, 0.00),
('I00003', 'P002', 2, 1299.99, 50.00),
('I00003', 'P003', 3, 1999.00, 0),
('I00003', 'P004', 1, 1399.99, 0),
('I00003', 'P005', 4, 899.00, 0),
('I00003', 'P008', 1, 499.99, 0),
('I00003', 'P009', 1, 499.99, 0),
('I00003', 'P018', 2, 399.00, 0),
('I00003', 'P015', 2, 229.99, 0.00),
('I00003', 'P017', 1, 2499, 249.90),
('I00004', 'P012', 3, 329.99, 0.00),
('I00004', 'P021', 2, 119.95, 23.99),
('I00004', 'P024', 1, 99.99, 0.00),
('I00004', 'P001', 1, 1099.00, 0),
('I00004', 'P002', 3, 1299.99, 0),
('I00004', 'P003', 1, 1999.00, 0),
('I00004', 'P005', 2, 899.00, 0),
('I00004', 'P012', 4, 329.99, 0),
('I00004', 'P017', 1, 2499.00, 0),
('I00005', 'P001', 2, 1099.00, 100.00),
('I00005', 'P003', 3, 1999.00, 0),
('I00005', 'P007', 1, 349.99, 0),
('I00005', 'P009', 2, 499.99, 0),
('I00005', 'P012', 4, 329.99, 0),
('I00005', 'P018', 1, 399.00, 0),
('I00005', 'P019', 3, 1099.99, 0),
('I00005', 'P025', 2, 349.99, 0),
('I00006', 'P003', 2, 1999.00, 0),
('I00006', 'P006', 3, 249.00, 0),
('I00006', 'P008', 1, 499.99, 0),
('I00006', 'P014', 3, 399.00, 0),
('I00007', 'P011', 2, 179.95, 0),
('I00007', 'P018', 1, 399.00, 0),
('I00008', 'P006', 1, 249.00, 0),
('I00008', 'P021', 2, 119.95, 0),
('I00008', 'P024', 3, 99.99, 0),
('I00008', 'P025', 1, 349.99, 0),
('I00009', 'P002', 1, 1299.99, 100),
('I00009', 'P005', 3, 899.00, 0),
('I00009', 'P010', 2, 129.99, 0),
('I00009', 'P023', 1, 1499.99, 0),
('I00010', 'P001', 2, 1099.00, 0),
('I00010', 'P013', 1, 799.99, 0),
('I00010', 'P015', 1, 229.99, 0)''')

cur.execute('''CREATE TABLE Dealer
(DID varchar(4) PRIMARY KEY,
DName varchar(20) NOT NULL,
Address varchar(30),
City varchar(20),
Phone char(10))''')

cur.execute('''INSERT INTO Dealer (DID, DName, Address, City, Phone) VALUES
('D001', 'ABC Corporation', '123 Main Street', 'New York', '555-5555'),
('D002', 'XYZ Trading Co.', '456 Elm Street', 'Los Angeles', '555-1234'),
('D003', 'EFG Imports', '789 Oak Street', 'Chicago', '555-6789'),
('D004', 'HIJ Distributors', '1010 Pine Street', 'Miami', '555-4321'),
('D005', 'MegaMart', '1234 Main St', 'New York', '2125556789'),
('D006', 'Reliance Mart', '9101 Pine St', 'Mumbai', '0225554567'),
('D007', 'Big Bazaar', '5678 Cedar St', 'Bangalore', '0805551234'),
('D008', 'Wholesale Club', '5678 Elm St', 'Los Angeles', '2135551234'),
('D009', 'Super Mart', '9101 Oak St', 'Chicago', '3125554567'),
('D010', 'Bulk Buy', '1212 Maple St', 'Houston', '7135557890')''')

cur.execute('''CREATE TABLE Purchases
(PurchaseID varchar(6) PRIMARY KEY,
DID varchar(4) NOT NULL,
PurchaseDate DATE NOT NULL,
CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
TotalAmt DECIMAL(10,2),
FOREIGN KEY (DID) REFERENCES Dealer(DID))''')

cur.execute('''INSERT INTO Purchases (PurchaseID, DID, PurchaseDate, TotalAmt)
VALUES
('P00001', 'D001', '2023-01-15', 5000.00),
('P00002', 'D002', '2023-01-18', 8000.00),
('P00003', 'D003', '2023-02-05', 12000.00),
('P00004', 'D001', '2023-02-10', 7000.00),
('P00005', 'D004', '2023-03-01', 15000.00),
('P00006', 'D002', '2023-03-05', 4000.00),
('P00007', 'D005', '2023-03-15', 9000.00),
('P00008', 'D003', '2023-04-02', 11000.00),
('P00009', 'D006', '2023-04-10', 6000.00),
('P00010', 'D004', '2023-05-01', 20000.00)''')

cur.execute('''CREATE TABLE PurchaseDetails (
  LineID INT AUTO_INCREMENT PRIMARY KEY,
  PurchaseID VARCHAR(6) NOT NULL,
  PID varchar(4) NOT NULL,
  Quantity INT NOT NULL,
  Rate DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (PurchaseID) REFERENCES Purchases(PurchaseID) ON DELETE CASCADE,
  FOREIGN KEY (PID) REFERENCES Product(PID)
)''')

cur.execute('''INSERT INTO PurchaseDetails (PurchaseID, PID, Quantity, Rate) VALUES 
('P00001', 'P001', 10, 200.00),
('P00001', 'P001', 10, 25.00),
('P00001', 'P003', 20, 150.00),
('P00001', 'P002', 5, 50.00),
('P00002', 'P001', 20, 24.00),
('P00002', 'P005', 15, 300.00),
('P00002', 'P002', 25, 250.00),
('P00002', 'P003', 15, 35.00),
('P00003', 'P002', 8, 48.00),
('P00003', 'P004', 5, 100.00),
('P00003', 'P006', 30, 180.00),
('P00004', 'P004', 12, 18.50),
('P00004', 'P005', 6, 32.00),
('P00004', 'P006', 4, 70.00),
('P00004', 'P003', 10, 150.00),
('P00004', 'P001', 15, 200.00),
('P00005', 'P006', 20, 180.00),
('P00005', 'P004', 10, 100.00),
('P00006', 'P003', 10, 150.00),
('P00006', 'P005', 15, 120.00),
('P00006', 'P012', 20, 90.00),
('P00007', 'P002', 25, 200.00),
('P00007', 'P008', 30, 150.00),
('P00007', 'P010', 40, 100.00),
('P00008', 'P007', 15, 120.00),
('P00008', 'P015', 20, 90.00),
('P00008', 'P018', 10, 180.00),
('P00009', 'P004', 30, 150.00),
('P00009', 'P006', 40, 100.00),
('P00009', 'P023', 5, 250.00),
('P00010', 'P011', 10, 180.00),
('P00010', 'P016', 15, 120.00),
('P00010', 'P025', 20, 90.00)''')


mycon.commit()