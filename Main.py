from tkinter import *
from tkinter import messagebox
import mysql.connector
from datetime import date



mysql_host = "localhost"
mysql_user = "root"
mysql_password = "ap0309"
mysql_database = "db"

def Display_Invoice():
    mydb = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )

    cust = Tk()
    cust.title("Invoice Details")
    cust.geometry("800x600")

    InvoiceID_label = Label(cust,text="Invoice ID:")
    InvoiceID_label.grid(column=1, row = 0)

    InvoiceID_entry = Entry(cust)
    InvoiceID_entry.grid(column=2, row = 0)

    labels = []
    def clean():
        while(labels!=[]):
            i = labels.pop()
            i.config(text="")

    def display():
        clean()
        cur = mydb.cursor()
        InvoiceID = InvoiceID_entry.get()
        InvoiceID_entry.delete(0,END)
        cur.execute("SELECT InvoiceID FROM Invoices")
        l = cur.fetchall()
        if (InvoiceID,) not in l:
            messagebox.showerror("Error", "Invoice Not Found")
            return
        cur.execute(f"SELECT * FROM Invoices WHERE InvoiceID='{InvoiceID}'")
        l = cur.fetchone()
        cur.execute(f"SELECT CName from Customer WHERE CID='{l[1]}'")
        x = cur.fetchone()
        InvoiceID_label = Label(cust,text=f"Invoice ID: {l[0]}")
        CID_label = Label(cust,text=f"Customer ID: {l[1]}")
        CName_label = Label(cust, text=f"Customer Name: {x[0]}")
        Date_label = Label(cust, text=f"Invoice Date: {l[2]}")
        Amt_label = Label(cust, text=f"Total Amount: {l[4]}")
        InvoiceID_label.grid(row=2)
        CID_label.grid(row=3)
        CName_label.grid(row=4)
        Date_label.grid(row=5)
        Amt_label.grid(row=6)

        cur.execute(f"SELECT Product.PID,PName,Brand, Quantity, InvoiceDetails.Rate, Discount FROM InvoiceDetails,Product WHERE InvoiceDetails.InvoiceID='{InvoiceID}' and InvoiceDetails.PID = Product.PID")
        l = cur.fetchall()
        if(len(l)==0):
            x = Label(cust,text="No Invoices found in the record for the customer")
            x.grid(row=7,column=2)
            labels.append(x)
            return
        
        head2 = Label(cust, text="PID")
        head2a = Label(cust, text="Product Name")
        head2b = Label(cust, text="Brand")
        head3 = Label(cust, text="Quantity")
        head4 = Label(cust, text="Rate")
        head5 = Label(cust, text="Discount")
        head2.grid(row = 7,pady=2,column=1)
        head2a.grid(row = 7,pady=2,column=2)
        head2b.grid(row = 7,pady=2,column=3)
        head3.grid(row = 7,pady=2,column=4)
        head4.grid(row = 7,pady=2,column=5)
        head5.grid(row = 7,pady=2,column=6)
        labels.extend([CName_label,CID_label,InvoiceID_label,Date_label,Amt_label,head2,head3,head4,head5,head2a,head2b,])
        for i in range(len(l)):
            pid = Label(cust, text=f"{l[i][0]}")
            pname = Label(cust, text=f"{l[i][1]}")
            brand = Label(cust, text=f"{l[i][2]}")
            qty = Label(cust, text=f"{l[i][3]}")
            rate = Label(cust, text=f"{l[i][4]}")
            discount = Label(cust, text=f"{l[i][5]}")

            labels.extend([pid,pname,brand,qty,rate,discount])
            pid.grid(row=8+i,column=1)
            pname.grid(row=8+i,column=2)
            brand.grid(row=8+i,column=3)
            qty.grid(row=8+i,column=4)
            rate.grid(row=8+i,column=5)
            discount.grid(row=8+i,column=6)

    
    search_button = Button(cust, text="Search", command = display, width=12)
    search_button.grid(column=3, row=0, padx=10, pady=10)


def Add_a_Purchase():
    global cnt
    mydb = mysql.connector.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_password,
    database=mysql_database
    )

    cur = mydb.cursor()

    def generate_purchase_id():
        cur.execute("SELECT MAX(PurchaseID) FROM Purchases")
        result = cur.fetchone()
        if result[0] is None:
            purchase_id = 'P00001'
        else:
            purchase_num = int(result[0][1:]) + 1
            purchase_id = 'P' + str(purchase_num).zfill(5)
        return purchase_id

    aprscr = Tk()
    aprscr.title("Add Purchase")
    aprscr.geometry("900x600")

    cnt = 1

    def fetch_details():
        cur.execute("SELECT PID FROM PRODUCT")
        l = cur.fetchall()
        for i in range(len(product_list)):
            product = product_list[i].get()
            if (product,) not in l:
                messagebox.showerror("Error","ProductID Not Found")
                return
            cur.execute(f"SELECT pname from product where pid='{product}'")
            x = cur.fetchone()
            pname_list[i].config(text = str(x[0]))
            
    def add_purchase():
        global PurchaseID
        fetch_details()
        total_amt = 0
        did = DID_entry.get()
        cur.execute("SELECT DID FROM Dealer")
        deal = cur.fetchall()
        if (did,) not in deal:
            messagebox.showerror("Error","Dealer doesn't exist")
            return
        if(len(product_list)==0):
            messagebox.showerror("Error","No Entries")
            return
        for i in range(len(rate_list)):
            product = product_list[i].get()
            if product=="": continue
            try:
                quantity = int(quantity_list[i].get())
                rate = float(rate_list[i].get())
                total_amt += rate*quantity
            except:
                messagebox.showerror("Error","Invalid Input!")
                return

        cur.execute(f"INSERT INTO Purchases (PurchaseID,DID,PurchaseDate,TotalAmt) VALUES ('{PurchaseID}','{did}','{date.today()}',{total_amt})")
        for i in range(len(product_list)):
            product = product_list[i].get()
            quantity = int(quantity_list[i].get())
            rate = float(rate_list[i].get())
            if product=="": continue
            cur.execute(f"INSERT INTO PurchaseDetails (PurchaseID,PID,Quantity,Rate) VALUES ('{PurchaseID}','{product}',{quantity},{rate})")
            cur.execute(f"UPDATE Product SET Units = Units+{quantity} WHERE PID = '{product}'")

        mydb.commit()
        while(cnt>1):
            delete_field()
        DID_entry.delete(0, END)
        PurchaseID = generate_purchase_id()
        Purchase.config(text=PurchaseID)
        messagebox.showinfo("Success", "Purchase added successfully")

    def create_field():
        global cnt
        if cnt==20:
            messagebox.showinfo("Error", "Cannot add more products!")
            return
        product_id_label = Label(aprscr, text="Product ID:")
        product_id_label.grid(column=0, row=cnt)

        product_id_entry = Entry(aprscr)
        product_id_entry.grid(column=1, row=cnt)

        pname_label = Label(aprscr, text="Name:")
        pname_label.grid(column=2, row=cnt)

        pname_entry = Label(aprscr,text="")
        pname_entry.grid(column=3, row=cnt)

        quantity_label = Label(aprscr, text="Quantity:")
        quantity_label.grid(column=4, row=cnt)

        quantity_entry = Entry(aprscr)
        quantity_entry.grid(column=5, row=cnt)

        rate_label = Label(aprscr, text="Rate:")
        rate_label.grid(column=6, row=cnt)

        rate_entry = Entry(aprscr)
        rate_entry.grid(column=7, row=cnt)

        label_list.append((product_id_label,pname_label,quantity_label,rate_label))
        product_list.append(product_id_entry)
        quantity_list.append(quantity_entry)
        rate_list.append(rate_entry)
        pname_list.append(pname_entry)
        cnt+=1

    def delete_field():
        global cnt
        if cnt==1:
            messagebox.showinfo("Error", "No Entries!")
            return
        x = product_list.pop()
        x.destroy()
        x = quantity_list.pop()
        x.destroy()
        x = rate_list.pop()
        x.destroy()
        x = pname_list.pop()
        x.destroy()
        x = label_list.pop()
        for i in x:
            i.destroy()
        cnt-=1

    product_list,pname_list,quantity_list,rate_list,label_list = [],[],[],[],[]

    PurchaseID = generate_purchase_id()
    Purchase = Label(aprscr,text=PurchaseID)
    Purchase.grid(column = 0,row=0)

    DID_label = Label(aprscr,text="Dealer ID:")
    DID_label.grid(column=1, row = 0)

    DID_entry = Entry(aprscr)
    DID_entry.grid(column=2, row = 0)

    create_field_button = Button(aprscr, text="Add Entry", command=create_field)
    create_field_button.grid(column=0, row=20)

    create_field_button = Button(aprscr, text="Delete Entry", command=delete_field)
    create_field_button.grid(column=1, row=20)

    fetch_details_button = Button(aprscr, text="Fetch Details", command=fetch_details)
    fetch_details_button.grid(column=2, row=20)

    add_button = Button(aprscr, text="Submit", command=add_purchase)
    add_button.grid(column=3, row=20)

    aprscr.mainloop()



def Add_a_Dealer():
    mydb = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )

    cur = mydb.cursor()

    adscr = Tk()
    adscr.title("Add Dealer")
    adscr.geometry("300x300")

    def generate_dealer_id():
        cur.execute("SELECT MAX(DID) FROM Dealer")
        result = cur.fetchone()
        if result[0] is None:
            dealer_id = 'D001'
        else:
            dealer_num = int(result[0][1:]) + 1
            dealer_id = 'D' + str(dealer_num).zfill(3)
        return dealer_id

    def add_dealer():
        try:
            DID = generate_dealer_id()
            DName = DName_entry.get()
            Address = Address_entry.get()
            City = City_entry.get()
            Phone = Phone_entry.get()

            cur.execute(f"INSERT INTO Dealer (DID, DName, Address, City, Phone) VALUES ('{DID}', '{DName}', '{Address}', '{City}', '{Phone}')")
            mydb.commit()
            messagebox.showinfo("Success", "Dealer added successfully")
            DID_entry.config(text=generate_dealer_id())
            DName_entry.delete(0, END)
            Address_entry.delete(0, END)
            City_entry.delete(0, END)
            Phone_entry.delete(0, END)
        except:
            messagebox.showerror("Error","Invalid Input!")
            return

    DID_label = Label(adscr, text="Dealer ID:")
    DID_label.grid(column=0, row=0)
    DID_entry = Label(adscr, text=generate_dealer_id())
    DID_entry.grid(column=1, row=0)

    DName_label = Label(adscr, text="Dealer Name:")
    DName_label.grid(column=0, row=1)
    DName_entry = Entry(adscr)
    DName_entry.grid(column=1, row=1)

    Address_label = Label(adscr, text="Address:")
    Address_label.grid(column=0, row=2)
    Address_entry = Entry(adscr)
    Address_entry.grid(column=1, row=2)

    City_label = Label(adscr, text="City:")
    City_label.grid(column=0, row=3)
    City_entry = Entry(adscr)
    City_entry.grid(column=1, row=3)

    Phone_label = Label(adscr, text="Phone:")
    Phone_label.grid(column=0, row=4)
    Phone_entry = Entry(adscr)
    Phone_entry.grid(column=1, row=4)

    add_button = Button(adscr, text="Add Dealer", command=add_dealer)
    add_button.grid(row=5)

    adscr.mainloop()

def Add_an_Invoice():
    global cnt
    global InvoiceID
    mydb = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )

    cur = mydb.cursor()

    def generate_invoice_id():
        cur.execute("SELECT MAX(InvoiceID) FROM Invoices")
        result = cur.fetchone()
        if result[0] is None:
            invoice_id = 'I00001'
        else:
            invoice_num = int(result[0][1:]) + 1
            invoice_id = 'I' + str(invoice_num).zfill(5)
        return invoice_id

    aiscr = Tk()
    aiscr.title("Add Invoice")
    aiscr.geometry("900x600")

    cnt = 1

    def validate_quantity():
        cur.execute("SELECT PID, Units FROM PRODUCT")
        d = dict(cur.fetchall())
        for i in range(len(product_list)):
            d[product_list[i].get()] -= int(quantity_list[i].get())
            if(d[product_list[i].get()]<0):
                return False
        return True

    def fetch_details():
        cur.execute("SELECT PID FROM PRODUCT")
        l = cur.fetchall()
        for i in range(len(product_list)):
            product = product_list[i].get()
            if (product,) not in l:
                messagebox.showerror("Error","ProductID Not Found")
                return
            cur.execute(f"SELECT rate from product where pid='{product}'")
            x = cur.fetchone()
            rate_list[i].config(text = str(x[0]))
            cur.execute(f"SELECT pname from product where pid='{product}'")
            x = cur.fetchone()
            pname_list[i].config(text = str(x[0]))
            

    def add_invoice():
        global InvoiceID
        fetch_details()
        flag = validate_quantity()
        if flag==False:
            messagebox.showerror("Quantity Insufficient!")
            return
        total_amt = 0
        cid = CID_entry.get()
        cur.execute("SELECT CID FROM Customer")
        cust = cur.fetchall()
        if (cid,) not in cust:
            messagebox.showerror("Error","Customer doesn't exist")
            return
        if(len(product_list)==0):
            messagebox.showerror("Error","No Entries")
            return
        for i in range(len(rate_list)):
            product = product_list[i].get()
            if product=="": continue
            try:
                quantity = int(quantity_list[i].get())
                cur.execute(f"SELECT rate from product where pid='{product}'")
                x = cur.fetchone()
                rate = float(str(x[0]))
                discount = float(discount_list[i].get())
                total_amt += (rate-discount)*quantity
            except:
                messagebox.showerror("Error","Invalid Input!")
                return

        cur.execute(f"INSERT INTO Invoices (InvoiceID,CID,InvoiceDate,TotalAmt) VALUES ('{InvoiceID}','{cid}','{date.today()}',{total_amt})")
        for i in range(len(product_list)):
            product = product_list[i].get()
            quantity = int(quantity_list[i].get())
            cur.execute(f"SELECT rate from product where pid='{product}'")
            x = cur.fetchone()
            rate = x[0]
            discount = float(discount_list[i].get())

            if product=="": continue
            cur.execute(f"INSERT INTO InvoiceDetails (InvoiceID,PID,Quantity,Rate,Discount) VALUES ('{InvoiceID}','{product}',{quantity},{rate},{discount})")
            cur.execute(f"UPDATE Product SET Units = Units-{quantity} WHERE PID = '{product}'")

        mydb.commit()
        while(cnt>1):
            delete_field()
        CID_entry.delete(0, END)
        InvoiceID = generate_invoice_id()
        Invoice.config(text=InvoiceID)
        messagebox.showinfo("Success", "Invoice added successfully")

    def create_field():
        global cnt
        if cnt==20:
            messagebox.showinfo("Error", "Cannot add more products!")
            return
        product_id_label = Label(aiscr, text="Product ID:")
        product_id_label.grid(column=0, row=cnt)

        product_id_entry = Entry(aiscr)
        product_id_entry.grid(column=1, row=cnt)

        pname_label = Label(aiscr, text="Name:")
        pname_label.grid(column=2, row=cnt)

        pname_entry = Label(aiscr,text="")
        pname_entry.grid(column=3, row=cnt)

        quantity_label = Label(aiscr, text="Quantity:")
        quantity_label.grid(column=4, row=cnt)

        quantity_entry = Entry(aiscr)
        quantity_entry.grid(column=5, row=cnt)

        rate_label = Label(aiscr, text="Rate:")
        rate_label.grid(column=6, row=cnt)

        rate_entry = Label(aiscr,text="")
        rate_entry.grid(column=7, row=cnt)

        discount_label = Label(aiscr, text="Discount:")
        discount_label.grid(column=8, row=cnt)

        discount_entry = Entry(aiscr)
        discount_entry.grid(column=9, row=cnt)

        label_list.append((product_id_label,pname_label,quantity_label,rate_label,discount_label))
        product_list.append(product_id_entry)
        quantity_list.append(quantity_entry)
        rate_list.append(rate_entry)
        pname_list.append(pname_entry)
        discount_list.append(discount_entry)
        cnt+=1

    def delete_field():
        global cnt
        if cnt==1:
            messagebox.showinfo("Error", "No Entries!")
            return
        x = product_list.pop()
        x.destroy()
        x = quantity_list.pop()
        x.destroy()
        x = rate_list.pop()
        x.destroy()
        x = pname_list.pop()
        x.destroy()
        x = discount_list.pop()
        x.destroy()
        x = label_list.pop()
        for i in x:
            i.destroy()
        cnt-=1

    product_list,pname_list,quantity_list,rate_list,discount_list,label_list = [],[],[],[],[],[]

    InvoiceID = generate_invoice_id()
    Invoice = Label(aiscr,text=InvoiceID)
    Invoice.grid(column = 0,row=0)

    CID_label = Label(aiscr,text="Customer ID:")
    CID_label.grid(column=1, row = 0)

    CID_entry = Entry(aiscr)
    CID_entry.grid(column=2, row = 0)

    create_field_button = Button(aiscr, text="Add Entry", command=create_field)
    create_field_button.grid(column=0, row=20)

    create_field_button = Button(aiscr, text="Delete Entry", command=delete_field)
    create_field_button.grid(column=1, row=20)

    fetch_details_button = Button(aiscr, text="Fetch Details", command=fetch_details)
    fetch_details_button.grid(column=2, row=20)

    add_button = Button(aiscr, text="Submit", command=add_invoice)
    add_button.grid(column=3, row=20)

    aiscr.mainloop()


def Add_a_Customer():
    mydb = mysql.connector.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_password,
    database=mysql_database
    )

    cur = mydb.cursor()

    acscr = Tk()
    acscr.title("Add Customer")
    acscr.geometry("300x300")

    def generate_customer_id():
        cur.execute("SELECT MAX(CID) FROM Customer")
        result = cur.fetchone()
        if result[0] is None:
            customer_id = 'C001'
        else:
            customer_num = int(result[0][1:]) + 1
            customer_id = 'C' + str(customer_num).zfill(3)
        return customer_id

    def add_customer():
        try:
            CID = generate_customer_id()
            CName = Cname_entry.get()
            Address = Address_entry.get()
            City = City_entry.get()
            Phone = Phone_entry.get()

            cur.execute(f"INSERT INTO CUSTOMER (CID, CName, Address, City, Phone) VALUES ('{CID}', '{CName}', '{Address}', '{City}', '{Phone}')")
            mydb.commit()
            messagebox.showinfo("Success", "Customer added successfully")
            CID_entry.config(text=generate_customer_id())
            Cname_entry.delete(0, END)
            Address_entry.delete(0, END)
            City_entry.delete(0, END)
            Phone_entry.delete(0, END)
        except:
            messagebox.showerror("Error","Invalid Input!")
            return

    CID_label = Label(acscr, text="Customer ID:")
    CID_label.grid(column=0, row=0)
    CID_entry = Label(acscr, text=generate_customer_id())
    CID_entry.grid(column=1, row=0)

    Cname_label = Label(acscr, text="Customer Name:")
    Cname_label.grid(column=0, row=1)
    Cname_entry = Entry(acscr)
    Cname_entry.grid(column=1, row=1)

    Address_label = Label(acscr, text="Address:")
    Address_label.grid(column=0, row=2)
    Address_entry = Entry(acscr)
    Address_entry.grid(column=1, row=2)

    City_label = Label(acscr, text="City:")
    City_label.grid(column=0, row=3)
    City_entry = Entry(acscr)
    City_entry.grid(column=1, row=3)

    Phone_label = Label(acscr, text="Phone:")
    Phone_label.grid(column=0, row=4)
    Phone_entry = Entry(acscr)
    Phone_entry.grid(column=1, row=4)

    add_button = Button(acscr, text="Add Customer", command=add_customer)
    add_button.grid(row=5)

    acscr.mainloop()

def Add_a_Product():
    mydb = mysql.connector.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_password,
    database=mysql_database)

    cur = mydb.cursor()

    apscr = Tk()
    apscr.title("Add Product")
    apscr.geometry("300x300")

    def generate_product_id():
        cur.execute("SELECT MAX(PID) FROM Product")
        result = cur.fetchone()
        if result[0] is None:
            product_id = 'P001'
        else:
            product_num = int(result[0][1:]) + 1
            product_id = 'P' + str(product_num).zfill(3)
        return product_id

    def add_product():
        try:
            PID = generate_product_id()
            PName = Pname_entry.get()
            Brand = Brand_entry.get()
            Units = int(Units_entry.get())
            Rate = float(Rate_entry.get())

            cur.execute(f"INSERT INTO PRODUCT (PID, PName, Brand, Units, Rate) VALUES ('{PID}', '{PName}', '{Brand}', {Units}, {Rate})")
            mydb.commit()
            messagebox.showinfo("Success", "Product added successfully")
            PID_entry.config(text=generate_product_id())
            Pname_entry.delete(0, END)
            Brand_entry.delete(0, END)
            Units_entry.delete(0, END)
            Rate_entry.delete(0, END)
        except:
            messagebox.showerror("Error","Invalid Input!")
            return

    PID_label = Label(apscr, text="Product ID:")
    PID_label.grid(column=0, row=0)
    PID_entry = Label(apscr, text=generate_product_id())
    PID_entry.grid(column=1, row=0)

    Pname_label = Label(apscr, text="Product Name:")
    Pname_label.grid(column=0, row=1)
    Pname_entry = Entry(apscr)
    Pname_entry.grid(column=1, row=1)

    Brand_label = Label(apscr, text="Brand Name:")
    Brand_label.grid(column=0, row=2)
    Brand_entry = Entry(apscr)
    Brand_entry.grid(column=1, row=2)

    Units_label = Label(apscr, text="Units:")
    Units_label.grid(column=0, row=3)
    Units_entry = Entry(apscr)
    Units_entry.grid(column=1, row=3)

    Rate_label = Label(apscr, text="Rate:")
    Rate_label.grid(column=0, row=4)
    Rate_entry = Entry(apscr)
    Rate_entry.grid(column=1, row=4)

    add_button = Button(apscr, text="Add Product", command=add_product)
    add_button.grid(row=5)

    apscr.mainloop()

def display_stock():
    mydb = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )

    cur = mydb.cursor()

    dispstock = Tk()
    dispstock.geometry("600x600")
    dispstock.title("Stock")

    cur.execute("SELECT * FROM Product ORDER BY PName")
    l = cur.fetchall()
    head1 = Label(dispstock,text="PID")
    head1.grid(row=0, column=0)
    head2 = Label(dispstock,text="PName")
    head2.grid(row=0, column=1)
    head3 = Label(dispstock,text="Brand")
    head3.grid(row=0, column=2)
    head4 = Label(dispstock,text="Units")
    head4.grid(row=0, column=3)
    head5 = Label(dispstock,text="Rate")
    head5.grid(row=0, column=4)
    c = 1
    for i in l:
        lab0 = Label(dispstock,text=f"{i[0]}")
        lab1 = Label(dispstock,text=f"{i[1]}")
        lab2 = Label(dispstock,text=f"{i[2]}")
        lab3 = Label(dispstock,text=f"{i[3]}")
        lab4 = Label(dispstock,text=f"{i[4]}")
        lab0.grid(row=c, column=0)
        lab1.grid(row=c, column=1)
        lab2.grid(row=c, column=2)
        lab3.grid(row=c, column=3)
        lab4.grid(row=c, column=4)
        c+=1

    dispstock.mainloop()

def update_product():
    mydb = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )
    upprod = Tk()
    upprod.title("Update Product Details")
    upprod.geometry("300x300")

    cur = mydb.cursor()
    PID_label = Label(upprod,text="Product ID:")
    PID_label.grid(column=0, row = 0)

    PID_entry = Entry(upprod)
    PID_entry.grid(column=1, row = 0)

    def display():
        PID = PID_entry.get()
        cur.execute(f"SELECT * FROM Product WHERE PID='{PID}'")
        l = cur.fetchone()
        if(l==None):
            messagebox.showerror("Error","ProductID Not Found!")
            return
        
        PName_label = Label(upprod,text="Product Name:")
        PName_label.grid(row=1,column=0)
        PName_entry = Entry(upprod)
        PName_entry.grid(row=1,column=1)
        PName_entry.insert(0,f"{l[1]}")
        
        Brand_label = Label(upprod,text="Brand:")
        Brand_label.grid(row=2,column=0)
        Brand_entry = Entry(upprod)
        Brand_entry.grid(row=2,column=1)
        Brand_entry.insert(0,f"{l[2]}")
        
        Units_label = Label(upprod,text="Units:")
        Units_label.grid(row=3,column=0)
        Units_entry = Entry(upprod)
        Units_entry.grid(row=3,column=1)
        Units_entry.insert(0,f"{l[3]}")
        
        Rate_label = Label(upprod,text="Rate:")
        Rate_label.grid(row=4,column=0)
        Rate_entry = Entry(upprod)
        Rate_entry.grid(row=4,column=1)
        Rate_entry.insert(0,f"{l[4]}")
        
        def update():
            try:
                PName = PName_entry.get()
                Brand = Brand_entry.get()
                Units = Units_entry.get()
                Rate = Rate_entry.get()
                cur.execute(f"UPDATE Product SET PName = '{PName}', Brand = '{Brand}', Units = {Units}, Rate = {Rate} WHERE PID = '{PID}'")
                mydb.commit()
                messagebox.showinfo("Success","Product Details Updated Successfully")
            except:
                messagebox.showerror("Error","Invalid Input")

        update_button = Button(upprod,text="Update",command=update)
        update_button.grid(row=5, column=0)


    search_button = Button(upprod,text="Search",command=display)
    search_button.grid(row=0, column=2)

    upprod.mainloop()

def update_customer():
    mydb = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )
    upcust = Tk()
    upcust.title("Update Customer Details")
    upcust.geometry("300x300")

    cur = mydb.cursor()
    CID_label = Label(upcust,text="Customer ID:")
    CID_label.grid(column=0, row = 0)

    CID_entry = Entry(upcust)
    CID_entry.grid(column=1, row = 0)

    def display():
        CID = CID_entry.get()
        cur.execute(f"SELECT * FROM Customer WHERE CID='{CID}'")
        l = cur.fetchone()
        if(l==None):
            messagebox.showerror("Error","CustomerID Not Found!")
            return
        
        CName_label = Label(upcust,text="Customer Name:")
        CName_label.grid(row=1,column=0)
        CName_entry = Entry(upcust)
        CName_entry.grid(row=1,column=1)
        CName_entry.insert(0,f"{l[1]}")
        
        Address_label = Label(upcust,text="Address:")
        Address_label.grid(row=2,column=0)
        Address_entry = Entry(upcust)
        Address_entry.grid(row=2,column=1)
        Address_entry.insert(0,f"{l[2]}")
        
        City_label = Label(upcust,text="City:")
        City_label.grid(row=3,column=0)
        City_entry = Entry(upcust)
        City_entry.grid(row=3,column=1)
        City_entry.insert(0,f"{l[3]}")
        
        Phone_label = Label(upcust,text="Phone:")
        Phone_label.grid(row=4,column=0)
        Phone_entry = Entry(upcust)
        Phone_entry.grid(row=4,column=1)
        Phone_entry.insert(0,f"{l[4]}")
        
        def update():
            try:
                CName = CName_entry.get()
                Address = Address_entry.get()
                City = City_entry.get()
                Phone = Phone_entry.get()
                cur.execute(f"UPDATE Customer SET CName = '{CName}', Address = '{Address}', City = '{City}', Phone = '{Phone}' WHERE CID = '{CID}'")
                mydb.commit()
                messagebox.showinfo("Success","Customer Details Updated Successfully")
            except:
                messagebox.showerror("Error","Invalid Input")

        update_button = Button(upcust,text="Update",command=update)
        update_button.grid(row=5, column=0)


    search_button = Button(upcust,text="Search",command=display)
    search_button.grid(row=0, column=2)

    upcust.mainloop()

def update_dealer():
    mydb = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )
    cur = mydb.cursor()
    updeal = Tk()
    updeal.title("Update Dealer Details")
    updeal.geometry("300x300")

    DID_label = Label(updeal,text="Dealer ID:")
    DID_label.grid(column=0, row = 0)

    DID_entry = Entry(updeal)
    DID_entry.grid(column=1, row = 0)

    def display():
        DID = DID_entry.get()
        cur.execute(f"SELECT * FROM Dealer WHERE DID='{DID}'")
        l = cur.fetchone()
        if(l==None):
            messagebox.showerror("Error","DealerID Not Found!")
            return
        
        DName_label = Label(updeal,text="Dealer Name:")
        DName_label.grid(row=1,column=0)
        DName_entry = Entry(updeal)
        DName_entry.grid(row=1,column=1)
        DName_entry.insert(0,f"{l[1]}")
        
        Address_label = Label(updeal,text="Address:")
        Address_label.grid(row=2,column=0)
        Address_entry = Entry(updeal)
        Address_entry.grid(row=2,column=1)
        Address_entry.insert(0,f"{l[2]}")
        
        City_label = Label(updeal,text="City:")
        City_label.grid(row=3,column=0)
        City_entry = Entry(updeal)
        City_entry.grid(row=3,column=1)
        City_entry.insert(0,f"{l[3]}")
        
        Phone_label = Label(updeal,text="Phone:")
        Phone_label.grid(row=4,column=0)
        Phone_entry = Entry(updeal)
        Phone_entry.grid(row=4,column=1)
        Phone_entry.insert(0,f"{l[4]}")
        
        def update():
            try:
                DName = DName_entry.get()
                Address = Address_entry.get()
                City = City_entry.get()
                Phone = Phone_entry.get()
                cur.execute(f"UPDATE Dealer SET DName = '{DName}', Address = '{Address}', City = '{City}', Phone = '{Phone}' WHERE DID = '{DID}'")
                mydb.commit()
                messagebox.showinfo("Success","Dealer Details Updated Successfully")
            except:
                messagebox.showerror("Error","Invalid Input")

        update_button = Button(updeal,text="Update",command=update)
        update_button.grid(row=5, column=0)


    search_button = Button(updeal,text="Search",command=display)
    search_button.grid(row=0, column=2)

    updeal.mainloop()

def delete_invoice():
    mydb = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )
    cur = mydb.cursor()
    delinv = Tk()
    delinv.title("Delete Invoice")
    delinv.geometry("350x300")

    InvoiceID_label = Label(delinv,text="Enter Invoice ID to be deleted: ")
    InvoiceID_label.grid(column=1, row = 0)

    InvoiceID_entry = Entry(delinv)
    InvoiceID_entry.grid(column=2, row = 0)
    
    def display():
        InvoiceID = InvoiceID_entry.get()
        InvoiceID_entry.delete(0,END)
        cur.execute("Select InvoiceID FROM Invoices")
        l = cur.fetchall()
        if (InvoiceID,) not in l:
            messagebox.showerror("Error", "Invoice Not Found")
            return

        cur.execute(f"DELETE FROM Invoices WHERE InvoiceID='{InvoiceID}'")
        mydb.commit()
        messagebox.showinfo("Successful", "The Invoice Deleted Succcessfully.")
        delinv.destroy()
        return 

    
    delete_button = Button(delinv, text="Delete", command = display, width=12)
    delete_button.grid(column=2, row=1, padx=10, pady=10)
    delinv.mainloop()

def delete_purchase():
    mydb = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )

    cur = mydb.cursor()
    delpur = Tk()
    delpur.title("Delete Purchase")
    delpur.geometry("350x300")

    PurchaseID_label = Label(delpur,text="Enter Purchase ID to be deleted: ")
    PurchaseID_label.grid(column=1, row = 0)

    PurchaseID_entry = Entry(delpur)
    PurchaseID_entry.grid(column=2, row = 0)
    
    def display():
        PurchaseID = PurchaseID_entry.get()
        PurchaseID_entry.delete(0,END)
        cur.execute("Select PurchaseID FROM Purchases")
        l = cur.fetchall()
        if (PurchaseID,) not in l:
            messagebox.showerror("Error", "Purchase Not Found")
            return

        cur.execute(f"DELETE FROM Purchases WHERE PurchaseID='{PurchaseID}'")
        mydb.commit()
        messagebox.showinfo("Successfull", "The Purchase Deleted Succcessfully.")
        delpur.destroy()
        return 

    
    delete_button = Button(delpur, text="Delete", command = display, width=12)
    delete_button.grid(column=2, row=1, padx=10, pady=10)
    delpur.mainloop()

def search_db():
    mydb = mysql.connector.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_password,
    database=mysql_database
    )

    cur = mydb.cursor()

    searchscr = Tk()
    searchscr.geometry("1000x1000")
    searchscr.title("Search Database")

    search_entry = Entry(searchscr)
    search_entry.grid(row=0,column=0)

    labels = []

    def search():
        cnt = 0
        while(labels!=[]):
            i = labels.pop()
            i.destroy()
        sword = search_entry.get()
        cur.execute(f"SELECT * FROM PRODUCT WHERE PID LIKE '%{sword}%' OR PName LIKE '%{sword}%' OR Brand LIKE '%{sword}%' OR Units LIKE '%{sword}%' OR Rate LIKE '%{sword}%'")
        l = cur.fetchall()
        if l != []:
            label = Label(searchscr, text = "")
            label.grid(row=cnt, column=0)
            cnt+=1
            head1 = Label(searchscr, text = "PID")
            head1.grid(row=cnt, column=1)
            head2 = Label(searchscr, text = "PName")
            head2.grid(row=cnt, column=2)
            head3 = Label(searchscr, text = "Brand")
            head3.grid(row=cnt, column=3)
            head4 = Label(searchscr, text = "Units")
            head4.grid(row=cnt, column=4)
            head5 = Label(searchscr, text = "Rate")
            head5.grid(row=cnt, column=5)
            labels.extend([head1,head2,head3,head4,head5])
            cnt+=1
            for i in l:
                label1 = Label(searchscr, text = f"{i[0]}")
                label1.grid(row=cnt, column=1)
                label2 = Label(searchscr, text = f"{i[1]}")
                label2.grid(row=cnt, column=2)
                label3 = Label(searchscr, text = f"{i[2]}")
                label3.grid(row=cnt, column=3)
                label4 = Label(searchscr, text = f"{i[3]}")
                label4.grid(row=cnt, column=4)
                label5 = Label(searchscr, text = f"{i[4]}")
                label5.grid(row=cnt, column=5)
                labels.extend([label1,label2,label3,label4,label5])
                cnt+=1

        cur.execute(f"SELECT * FROM CUSTOMER WHERE CID LIKE '%{sword}%' OR CName LIKE '%{sword}%' OR Address LIKE '%{sword}%' OR City LIKE '%{sword}%' OR Phone LIKE '%{sword}%'")
        l = cur.fetchall()
        if l != []:
            label = Label(searchscr, text = "")
            label.grid(row=cnt, column=0)
            cnt+=1
            head1 = Label(searchscr, text = "CID")
            head1.grid(row=cnt, column=1)
            head2 = Label(searchscr, text = "CName")
            head2.grid(row=cnt, column=2)
            head3 = Label(searchscr, text = "Address")
            head3.grid(row=cnt, column=3)
            head4 = Label(searchscr, text = "City")
            head4.grid(row=cnt, column=4)
            head5 = Label(searchscr, text = "Phone")
            head5.grid(row=cnt, column=5)
            labels.extend([head1,head2,head3,head4,head5])
            cnt+=1
            for i in l:
                label1 = Label(searchscr, text = f"{i[0]}")
                label1.grid(row=cnt, column=1)
                label2 = Label(searchscr, text = f"{i[1]}")
                label2.grid(row=cnt, column=2)
                label3 = Label(searchscr, text = f"{i[2]}")
                label3.grid(row=cnt, column=3)
                label4 = Label(searchscr, text = f"{i[3]}")
                label4.grid(row=cnt, column=4)
                label5 = Label(searchscr, text = f"{i[4]}")
                label5.grid(row=cnt, column=5)
                labels.extend([label1,label2,label3,label4,label5])
                cnt+=1

        cur.execute(f"SELECT * FROM DEALER WHERE DID LIKE '%{sword}%' OR DName LIKE '%{sword}%' OR Address LIKE '%{sword}%' OR City LIKE '%{sword}%' OR Phone LIKE '%{sword}%'")
        l = cur.fetchall()
        if l != []:
            label = Label(searchscr, text = "")
            label.grid(row=cnt, column=0)
            cnt+=1
            head1 = Label(searchscr, text = "DID")
            head1.grid(row=cnt, column=1)
            head2 = Label(searchscr, text = "DName")
            head2.grid(row=cnt, column=2)
            head3 = Label(searchscr, text = "Address")
            head3.grid(row=cnt, column=3)
            head4 = Label(searchscr, text = "City")
            head4.grid(row=cnt, column=4)
            head5 = Label(searchscr, text = "Phone")
            head5.grid(row=cnt, column=5)
            labels.extend([head1,head2,head3,head4,head5])
            cnt+=1
            for i in l:
                label1 = Label(searchscr, text = f"{i[0]}")
                label1.grid(row=cnt, column=1)
                label2 = Label(searchscr, text = f"{i[1]}")
                label2.grid(row=cnt, column=2)
                label3 = Label(searchscr, text = f"{i[2]}")
                label3.grid(row=cnt, column=3)
                label4 = Label(searchscr, text = f"{i[3]}")
                label4.grid(row=cnt, column=4)
                label5 = Label(searchscr, text = f"{i[4]}")
                label5.grid(row=cnt, column=5)
                labels.extend([label1,label2,label3,label4,label5])
                cnt+=1

        cur.execute(f"SELECT * FROM INVOICES WHERE InvoiceID LIKE '%{sword}%' OR CID LIKE '%{sword}%' OR InvoiceDate LIKE '%{sword}%' OR TotalAmt LIKE '%{sword}%'")
        l = cur.fetchall()
        if l != []:
            label = Label(searchscr, text = "")
            label.grid(row=cnt, column=0)
            cnt+=1
            head1 = Label(searchscr, text = "InvoiceID")
            head1.grid(row=cnt, column=1)
            head2 = Label(searchscr, text = "CID")
            head2.grid(row=cnt, column=2)
            head3 = Label(searchscr, text = "InvoiceDate")
            head3.grid(row=cnt, column=3)
            head4 = Label(searchscr, text = "TotalAmt")
            head4.grid(row=cnt, column=4)
            labels.extend([head1,head2,head3,head4])
            cnt+=1
            for i in l:
                label1 = Label(searchscr, text = f"{i[0]}")
                label1.grid(row=cnt, column=1)
                label2 = Label(searchscr, text = f"{i[1]}")
                label2.grid(row=cnt, column=2)
                label3 = Label(searchscr, text = f"{i[2]}")
                label3.grid(row=cnt, column=3)
                label4 = Label(searchscr, text = f"{i[4]}")
                label4.grid(row=cnt, column=4)
                labels.extend([label1,label2,label3,label4])
                cnt+=1

        cur.execute(f"SELECT * FROM PURCHASES WHERE PurchaseID LIKE '%{sword}%' OR DID LIKE '%{sword}%' OR PurchaseDate LIKE '%{sword}%' OR TotalAmt LIKE '%{sword}%'")
        l = cur.fetchall()
        if l != []:
            label = Label(searchscr, text = "")
            label.grid(row=cnt, column=0)
            cnt+=1
            head1 = Label(searchscr, text = "PurchaseID")
            head1.grid(row=cnt, column=1)
            head2 = Label(searchscr, text = "DID")
            head2.grid(row=cnt, column=2)
            head3 = Label(searchscr, text = "PurchaseDate")
            head3.grid(row=cnt, column=3)
            head4 = Label(searchscr, text = "TotalAmt")
            head4.grid(row=cnt, column=4)
            labels.extend([head1,head2,head3,head4])
            cnt+=1
            for i in l:
                label1 = Label(searchscr, text = f"{i[0]}")
                label1.grid(row=cnt, column=1)
                label2 = Label(searchscr, text = f"{i[1]}")
                label2.grid(row=cnt, column=2)
                label3 = Label(searchscr, text = f"{i[2]}")
                label3.grid(row=cnt, column=3)
                label4 = Label(searchscr, text = f"{i[4]}")
                label4.grid(row=cnt, column=4)
                labels.extend([label1,label2,label3,label4])
                cnt+=1
        
    search_button = Button(searchscr, text="Search", command=search)
    search_button.grid(row=0, column=1)
    searchscr.mainloop()

root = Tk()
root.title("Store Management System")
root.geometry("550x350")

add_product_button = Button(root, text="Add a Product", command = Add_a_Product, height=2, width=20)
add_product_button.grid(column=0, row=0, padx=10, pady=10)

add_customer_button = Button(root, text="Add a Customer", command = Add_a_Customer, height=2, width=20)
add_customer_button.grid(column=1, row=0, padx=10, pady=10)

add_invoice_button = Button(root, text="Add an Invoice", command = Add_an_Invoice, height=2, width=20)
add_invoice_button.grid(column=2, row=0, padx=10, pady=10)

display_invoice_button = Button(root, text="Display Invoice", command = Display_Invoice, height=2, width=20)
display_invoice_button.grid(column=0, row=1, padx=10, pady=10)

add_dealer_button = Button(root, text="Add a Dealer", command = Add_a_Dealer, height=2, width=20)
add_dealer_button.grid(column=1, row=1, padx=10, pady=10)

add_purchase_button = Button(root, text="Add a Purchase", command = Add_a_Purchase, height=2, width=20)
add_purchase_button.grid(column=2, row=1, padx=10, pady=10)

display_stock_button = Button(root, text="Display Stock", command = display_stock, height=2, width=20)
display_stock_button.grid(column=0, row=2, padx=10, pady=10)

delete_invoice_button = Button(root, text="Delete Invoice", command = delete_invoice, height=2, width=20)
delete_invoice_button.grid(column=1, row=2, padx=10, pady=10)

delete_purchase_button = Button(root, text="Delete Purchase Record", command = delete_purchase, height=2, width=20)
delete_purchase_button.grid(column=2, row=2, padx=10, pady=10)

update_product_button = Button(root, text="Update Product Details", command = update_product, height=2, width=20)
update_product_button.grid(column=0, row=3, padx=10, pady=10)

update_customer_button = Button(root, text="Update Customer Details", command = update_customer, height=2, width=20)
update_customer_button.grid(column=1, row=3, padx=10, pady=10)

update_dealer_button = Button(root, text="Update Dealer Details", command = update_dealer, height=2, width=20)
update_dealer_button.grid(column=2, row=3, padx=10, pady=10)

search_db_button = Button(root, text="Search in Database", command = search_db, height=2, width=20)
search_db_button.grid(column=0, row=4, padx=10, pady=10, columnspan=3)

root.mainloop()