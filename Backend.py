import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter.constants import SE
from Databases import *
from ApplyQuery import Query
from datetime import date
import math, json, random


def Validate_Submit(entries):
    error = 0
    for i in range(len(entries)):
        digit, char = Validate(entries[i].get())
        if (i == 0 or i == 2 or i == 3 or i == 7 or i == 5 or i == 6) and ((digit == True and char == False) or (
                digit == False and char == False)):  # checking all entries validity, should not be wrong entry
            if i == 6:
                messagebox.showerror("Password Invalid",
                                     "Password should not be all numeric. It should have alphabet plus numeric digits.")
            else:
                messagebox.showerror("Invalid Input", "Invalid Data entered, Please Enter Correct Data")
            error = 1
        elif (i == 1) and (digit == False and char == True):
            error = 1
            messagebox.showerror("Invalid entry", "Please enter correct phone number. Note: Phone # should be numeric")
        elif ((i == 4)) and (entries[i].get() == "" or digit == False or char == True):
            error = 1
            messagebox.showerror("Invalid Employee ID", "Please enter a valid employee ID")
        return error


# Function to submit registration details
def Submit(entries, key=None):
    error = Validate_Submit(entries)
    if error == 0:

        ans = Query(LoginTable, col=LoginTable['columns'], query=SELECT, where=['Username'], value=[entries[6].get()])
        if not ans:
            final_value = []
            for i in entries:
                final_value.append(i.get())
            if final_value[3] == "Employee" or final_value[3] == "Bill Officer":
                check = Query(assign_IDs_Table, col=['ID'], query=SELECT, where=['Username'], value=[entries[6].get()])
                if check:
                    if check[0] != final_value[4]:
                        error = 1
                        messagebox.showerror("Employee ID Error", "Employee ID mismatched")
                else:
                    id = random.randint(1000, 9999)
                    final_value[4] = "A-" + str(id)
            if error == 0:
                Query(LoginTable, col=LoginTable['columns'], query=INSERT, value=final_value)
                messagebox.showinfo("Account Created",
                                    f"Your Account with username {final_value[6]} has been successfully created for designation of {final_value[3]}")

        else:
            if key == "Update":
                Query(LoginTable, col=LoginTable['columns'], query=UPDATE, where=['Username'], value=[entries[6].get()])
                messagebox.showinfo("Account Updated", "Your account has been updated successfully")
            else:
                messagebox.showerror("Database Error", "This account already exists. Try another username")


def Login_Backend(data, s, pc):
    ans = Query(LoginTable, col=LoginTable['columns'], query=SELECT, where=["Username", "password"],
                value=[data[-2].get(), data[-1].get()])
    if ans:
        status = Query(Remember_Me, col=Remember_Me['columns'], query=SELECT, where=["Username", "pc_name"],
                       value=[data[-2].get(), pc])
        if status:
            Query(Remember_Me, col=["Status"], query=UPDATE, where=["Username", "pc_name"],
                  value=[s.get(), data[-2].get(), pc])
        else:
            Query(Remember_Me, col=Remember_Me['columns'], query=INSERT, value=[data[-2].get(), s.get(), pc])
        return ans[0]
    else:
        messagebox.showerror("Invalid Credentials", "Username/Password is incorrect. Please enter valid details.")
        return "wrong"


def ImportFirm_Settings(data=None):
    data_fetched = Query(pdf_setting, col=pdf_setting['columns'], query=SELECT, where=["Sr"], value=["2"])
    if data_fetched:

        return json.loads(data_fetched[0][1])
    else:
        Query(pdf_setting, col=pdf_setting['columns'], query=INSERT, value=["2", json.dumps(data)])
        return data


def Today_Date():
    today = date.today()
    # Textual month, day and year	
    Date = today.strftime("%B %d, %Y")
    Time = today.strftime("%m/%d/%y")
    return Date, Time


def Validate(value):
    digit = False
    char = False
    for i in value:
        if i.isdigit():
            digit = True
        else:
            char = True
    return digit, char


def Check_Validity(value):
    phoneCount = 0
    phoneCount1 = 0
    validation = 0
    for x in value:
        if (x.isdigit()):
            phoneCount += 1
            if phoneCount == 1:
                if x == "0":
                    validation = 1
            if phoneCount == 2:
                if x == "3":
                    validation = 2

        phoneCount1 += 1
    result = phoneCount1 - phoneCount
    return result, validation, phoneCount


def Get_Employees():
    conn = sqlite3.connect("LoginDetails.db")
    cursor = conn.cursor()
    pos = "EMPLOYEE"
    cursor.execute("SELECT Username FROM LoginTable WHERE Position = ?", (pos,))
    count = 0
    for x in cursor.fetchall():
        count += 1

    pos = "OWNER"
    cursor.execute("SELECT Username FROM LoginTable WHERE Position = ?", (pos,))
    count1 = 0
    for x in cursor.fetchall():
        count1 += 1
    data = [str(count), str(count1)]
    return data


def Get_Profile_Details(name):
    # DataBase Opening
    conn = sqlite3.connect("LoginDetails.db")
    cursor = conn.cursor()
    cursor.execute("SELECT Gender FROM LoginTable WHERE Full_Name =?", (name,))
    gender = cursor.fetchall()
    gender = str(gender[0][0])
    cursor.execute("SELECT Username FROM LoginTable WHERE Full_Name =?", (name,))
    UserName = cursor.fetchall()
    UserName = str(UserName[0][0])
    cursor.execute("SELECT Password FROM LoginTable WHERE Full_Name =?", (name,))
    Pass = cursor.fetchall()
    Pass = str(Pass[0][0])
    data = [UserName, Pass, gender]
    return data


def update(Status, emailEnt, phoneEnt, PassEnt, position, Email, Contact_Number, Pass, name, EmailVarify):
    change = 0
    error = 0
    email = 0

    if emailEnt.get() == "" or phoneEnt.get() == "" or PassEnt == "":
        tk.messagebox.showerror("Fields Empty", "Fill The Fields Properly. Fields Should Not be Empty")
        error = 1
    passCount = 0
    passCount1 = 0
    Password = PassEnt.get()
    for i in Password:
        if (i.isdigit()):
            passCount += 1
        passCount1 += 1
    phoneCount = 0
    phoneCount1 = 0
    Phone = phoneEnt.get()
    validation = 0
    for x in Phone:
        if (x.isdigit()):
            phoneCount += 1
            if phoneCount == 1:
                if x == "0":
                    validation = 1
            if phoneCount == 2:
                if x == "3":
                    validation = 2

        phoneCount1 += 1

    if Status.get() != position:
        change = 1
    if Email != emailEnt.get():
        change = 2
        email = 1
    else:
        if EmailVarify != 1 and email == 1:
            error = 1
            tk.messagebox.showerror("Email Varification Failed", "Please Enter a valid Email Address")
    if phoneEnt.get() != Contact_Number:
        change = 3
    else:
        if phoneCount1 != 11 or phoneCount1 - phoneCount != 0:
            tk.messagebox.showerror("Phone Number Failed",
                                    "Invalid Mobile Number. NOTE: It should contain 11 numeric digits")
            error = 1
        if validation != 2:
            tk.messagebox.showerror("Phone Validation Failed",
                                    "Phone Number should start with 03. Format [03123456789]")
            error = 1
    if PassEnt.get() != Pass:
        change = 4
    else:
        if passCount1 < 6:
            tk.messagebox.showerror("Password Failed", "Password Should contain 6 Charachters minimum")
            error = 1
    if error == 0 and change > 0:
        conn = sqlite3.connect("LoginDetails.db")
        cursor = conn.cursor()
        query = "UPDATE LoginTable SET Password=?,Contact=?,Email=?,Position=? WHERE Full_Name=?"
        cursor.execute(query, (PassEnt.get(), phoneEnt.get(), emailEnt.get(), Status.get(), name))
        conn.commit()
        cursor.close()
        conn.close()
        tk.messagebox.showinfo("Profile Updated", "Profile Updated Successfully")
    elif change == 0:
        tk.messagebox.showerror("NO CHANGES", "You made no changes, Record Remained Same")
    else:
        tk.messagebox.showerror("Data Entry Error", "Unable to save record becaue of your mistakes")


def Login(Data, Status):
    Query(LoginTable, col=["Username TEXT", "Password TEXT", "Full_Name TEXT", "Status TEXT"], query=CREATE)
    # ans = Query(database=LoginTable['database'],table=LoginTable['table'],col=LoginTable['columns'],query=INSERT,
    #       value=["engr.smab","03056842507","Syed Mubashir Azeem","1"])
    ans = Query(LoginTable, col=["Username", "Password"], query=SELECT,
                value=[str(Data[0].get())], where=["Username"])
    if ans:
        return True
    else:
        return False


def Remember_me(Username, value, pc_name):
    ans = Query(Remember_Me, col=Remember_Me['columns'], query=SELECT, where=["pc_name"],
                value=[pc_name])
    if ans:
        Query(Remember_Me, col=['Status'], query=UPDATE, where=["pc_name"], value=[str(value), pc_name])
    else:
        Query(Remember_Me, col=Remember_Me['columns'], query=INSERT,
              value=[Username, value, pc_name])


def Login_Status(pc_name):
    Create_Tables()
    Query(Remember_Me, col=Remember_Me['columns'], query=CREATE)
    ans = Query(Remember_Me, col=['Status', 'Username'], query=SELECT,
                value=[str(pc_name)], where=['pc_name'])
    data = []
    status = False
    for i in ans:
        if str(i[0]) == "1":
            data = Query(LoginTable,
                         col=LoginTable['columns'], query=SELECT, where=['Username'], value=[str(ans[0][1])])
            if data:
                status = True
                data = data[0]
                data = [data[1], data[3], data[4], data[7], data[5]]
            else:
                pass
    return status, data


def Set_Billing_List():
    depart = []
    Firms = ["Azeem Enterprises", "Hadi Enterprises", "Masood Traders", "Muazzam Enterprises", "Zahid Enterprises",
             "Al Jannat Enterprises"]
    Subject = []
    item_names = []
    specs = []
    unit = ["Nos", "Pkt", "Kgs", "gram", "liter"]
    types = ["Engineering", "Lab Equipments", "Chemicals", "Stationary", "Non - Technical", "Crokery"]
    for lists in range(3, 9):
        data = Query(tables[lists], col=tables[lists]['columns'], query=SELECT)
        for rows in data:
            if lists == 3:
                item_names.append(rows[0])
            if lists == 4:
                found = False
                for names in Firms:
                    if names.lower() == rows[0].lower():
                        found = True
                if found == False:
                    Firms.append(rows[0])
            if lists == 5:
                Subject.append(rows[0])
            if lists == 6:
                depart.append(rows[0])
            if lists == 7:
                found == False
                for units in unit:
                    if units.lower() == rows[0].lower():
                        found = True
                if found == False:
                    unit.append(rows[0])
            if lists == 8:
                specs.append(rows[0])

    return depart, Firms, Subject, item_names, specs, unit, types


def search_engine(value, match):
    if match.lower() == value.lower():
        return True
    else:
        return False


def update_lists(fields, table):
    # Matching Firms name in database
    firms = [fields[2].get(), fields[3].get(), fields[4].get()]
    ans = Query(Firms_List_Table, col=Firms_List_Table['columns'], query=SELECT)
    for name in firms:
        result = False
        if ans:
            for rows in ans:
                result = search_engine(rows[0], name)
                if result:
                    break
        if result == False:
            Query(Firms_List_Table, col=Firms_List_Table['columns'], query=INSERT, value=[name])

    # Matching Item Name and rate in database
    ans = Query(Item_List_Table, col=Item_List_Table['columns'], query=SELECT)
    for item in table:
        result = False
        if ans:
            for rows in ans:
                result = search_engine(rows[0], str(item[1]))
                if result == True and str(item[5]) == rows[2] and rows[3] == str(item[4]):
                    break
        if result == False:
            Query(Item_List_Table, col=Item_List_Table['columns'], query=INSERT,
                  value=[str(item[1]), str(item[2]), str(item[5]), str(item[4]), str(fields[7].get())])

    # Matching Department Name in database
    ans = Query(Depart_List_Table, col=Depart_List_Table['columns'], query=SELECT, where=['Department_List'],
                value=[fields[0].get()])
    result = False
    if ans:
        for rows in ans:
            result = search_engine(rows[0], fields[0].get())
            if result:
                break
    if result == False:
        Query(Depart_List_Table, col=Depart_List_Table['columns'], query=INSERT, value=[fields[0].get()])

    # Matching Subject in database
    sub = Query(Subject_List_Table, col=Subject_List_Table['columns'], query=SELECT)
    result = False
    if sub:
        for rows in sub:
            result = search_engine(rows[0], fields[3].get())
            if result:
                break
    if result == False:
        Query(Subject_List_Table, col=Subject_List_Table['columns'], query=INSERT, value=[fields[3].get()])

    # Matching Unit in database
    unit = Query(Unit_List_Table, col=Unit_List_Table['columns'], query=SELECT)
    result = False
    if unit:
        for rows in unit:
            result = search_engine(rows[0], item[2])
            if result:
                break
    if result == False:
        Query(Unit_List_Table, col=Unit_List_Table['columns'], query=INSERT, value=[item[2]])

    # Inserting data into Specification database
    specs = Query(specs_List_Table, col=specs_List_Table['columns'], query=SELECT)
    for item in table:
        result = False
        if specs:
            for rows in specs:
                result = search_engine(rows[0], item[2])
                if result:
                    break
        if result == False:
            Query(specs_List_Table, col=specs_List_Table['columns'], query=INSERT, value=[str(item[2])])


def set_directories(folder, path=None):
    if path == None:
        paths = Query(files_path, col=files_path['columns'], query=SELECT)
        if paths:
            for rows in paths:
                if rows[0] == folder:
                    return rows[1]
            return "None"
        else:
            return "None"
    else:
        Query(files_path, col=files_path['columns'], query=INSERT, value=[folder, path])
        return "Done"


def New_Item_Validation(checkboxes, fields, items):
    error = 0
    for item in range(len(items)):
        digit, char = Validate(items[item].get())
        if (item == 0 or item == 2) and ((digit == True and char == False) or (digit == False and char == False)):
            messagebox.showerror("Invalid Entry", "Please Enter Correct Item Name")
            error = 1
        elif (item == 1 or item == 3) and (char == True or digit == False or int(items[item].get()) == 0):
            messagebox.showerror("Invalid Entry", "Please Enter correct Rate/Quantity")
            error = 1
        elif (item == 5 or item == 4) and (checkboxes[3].get() == 1 and (char == True or digit == False)):
            messagebox.showerror("Invalid Entry", "Please enter valid Amounts")
            error = 1
        elif (checkboxes[6].get() == 1 or checkboxes[0].get() == 1) and item == 5:
            if checkboxes[6].get() == 1:
                v = 6
            else:
                v = 1
            digit, char = Validate(fields[v].get())
            if digit == False or char == True:
                error = 1
                messagebox.showerror("Invalid Entry", "Please enter valid Tax")
    final_list = []
    if error == 0:
        if checkboxes[3].get() == 1 and (
                int(items[3].get()) >= int(items[4].get()) or int(items[3].get()) >= int(items[5].get()) or int(
                items[4].get()) == int(items[5].get())):
            error = 1
            messagebox.showerror("Invalid Price", "Comparitors rates should be greater than selected Firm")
        if error == 0:
            tax = 0
            if checkboxes[6].get() == 1:
                tax = int(fields[6].get())
            elif checkboxes[0].get() == 1:
                tax = int(fields[1].get())
            amount = int(items[1].get()) * int(items[3].get())
            tax_amount = float("{:.1f}".format(float((amount * tax) / 100)))
            total_amount = math.trunc(round(tax_amount, 0) + amount)
            amount_comp1 = int(items[1].get()) * int(items[4].get())
            amount_comp2 = int(items[1].get()) * int(items[5].get())
            tax_comp1 = float("{:.1f}".format(float((amount_comp1 * tax) / 100)))
            tax_comp2 = float("{:.1f}".format(float((amount_comp2 * tax) / 100)))
            total_comp1 = math.trunc(round(tax_comp1, 0) + amount_comp1)
            total_comp2 = math.trunc(round(tax_comp2, 0) + amount_comp2)
            final_list = [items[0].get(), items[6].get(), items[1].get(), items[2].get(), items[3].get(), str(amount),
                          str(tax_amount) + " (" + str(tax) + "%)", str(total_amount), str(total_comp1),
                          str(total_comp2)]
    return error, final_list


def Diary_No(value, diary_no):
    if value == SELECT:
        number = Query(Diary_no_table, col=Diary_no_table['columns'], value=["Bill"], query=value, where=["title"])
        if not number:
            Query(Diary_no_table, col=Diary_no_table['columns'], value=["Bill", diary_no], query=INSERT)
            number = Query(Diary_no_table, col=Diary_no_table['columns'], value=["Bill"], query=value, where=["title"])
        return number[0][1]
    elif value == UPDATE:
        number = Query(Diary_no_table, col=['Diary_no'], value=[diary_no, "Bill"], query=value, where=["title"])


def Validate_Print(fields, print_mode, comparator):
    error1 = 0
    error2 = 0
    for i in range(len(fields)):
        digit, char = Validate(fields[i].get())
        if (i == 0 or i == 2 or i == 3) and ((digit == True and char == False) or (digit == False and char == False)):
            error1 = 1
        elif (i == 5 or i == 4) and comparator == True and (
                (digit == True and char == False) or (digit == False and char == False)):
            error2 = 1
    if error1 == 0:
        if len(print_mode) == 1 and print_mode[0] == "Demand":
            return "Demand", error1
        if error2 == 0:
            return "All", error1
        else:
            messagebox.showerror("Invalid Entries", "Please Enter correct Department/Firm/Subject/Comparators")
            return "None", 1
    else:
        messagebox.showerror("Invalid Entries", "Please Enter correct Department/Firm/Subject")
        return "None", error1


def Create_Tables():
    for table in tables:
        if table['table'] != "pdf_setting_table":
            Query(table, col=table['columns'], query=CREATE)
        else:
            col = [table['columns'][0] + " TEXT", table['columns'][1] + " JSON"]
            Query(table, col=col, query=CREATE)


def Save_Bills(fields, table, diary, group, prints, limit, status, cheque_no):
    ans = Query(Bills_Table, col=Bills_Table['columns'], query=SELECT, where=["Diary_No"], value=[diary])
    if not ans:
        update_lists(fields, table)
        Date, Time = Today_Date()
        v = [str(Date), diary, fields[3].get(), fields[0].get(), fields[2].get(), fields[4].get(), fields[5].get(),
             fields[7].get(), group, limit, status, cheque_no]
        print(v)
        Query(Bills_Table, col=Bills_Table['columns'], query=INSERT, value=v)
        for i in table:
            tax = str(i[7]).split("(")[1]
            tax = tax.split(")")[0]
            data = [diary, i[1], i[2], i[3], i[4], tax, i[9], i[10], ""]
            print(data)
            Query(Bill_Items_Table, col=Bill_Items_Table['columns'], query=INSERT, value=data)
        selected_prints = ""
        for i in prints:
            selected_prints += i[0]
        print(selected_prints)
        data = [diary, selected_prints]
        print(data)
        Query(Bill_Prints_Table, col=Bill_Prints_Table['columns'], query=INSERT, value=data)
        return "Done"
    else:
        return "exists"


def Find_Required_Bills(table_data, entry_data, totals):
    qty = []
    for row in table_data:
        qty.append(int(row[3]))
    no_bills = 0
    final_qty = []
    bill_total_amount = 0.0
    final_above_rates = []
    bill_total_list = []
    while (int(math.trunc(round(bill_total_amount, 0))) < int(totals[2])):
        # print("Bill Total Amount (Used): ",bill_total_amount)
        bill_amount = 0.0
        items_qty = []
        count_row = 0
        above_rates = []

        for row in table_data:
            tax = str(row[7]).split("(")[1]
            tax = int(tax.split("%")[0])

            rate = float(((int(row[5]) * tax) / 100) + int(row[5]))
            item_qty = 0
            # print(rate,qty)

            if entry_data < rate:
                return "", "", row, ""
            while entry_data >= int(math.trunc(round(bill_amount, 0)) + math.trunc(round(rate, 0))):
                if item_qty < qty[count_row] and bill_total_amount < int(totals[2]):
                    item_qty += 1
                    bill_amount += rate
                    bill_total_amount += rate
                else:
                    break
            items_qty.append(item_qty)

            qty[count_row] -= item_qty
            # print("remaining qty: ",qty)
            count_row += 1
        final_above_rates.append(above_rates)
        bill_total_list.append(int(math.trunc(round(bill_amount, 0))))
        final_qty.append(items_qty)
        no_bills += 1
    return no_bills, final_qty, final_above_rates, bill_total_list


def save_firm_settings(data, json_data):
    j = 0
    for key in json_data:
        y_list = [int(y.get()) for y in data[j][0]]
        json_data[key]['y'] = y_list
        json_data[key]['heading_size'] = int(data[j][1].get())
        json_data[key]['border_bg'] = data[j][2].get()
        json_data[key]['border_text'] = data[j][3].get()
        json_data[key]['font'] = data[j][4].get()
        if data[j][4].get() == "Times-Roman":
            bold = "Times-Bold"
        else:
            bold = data[j][4].get() + "-Bold"
        json_data[key]['font_bold'] = bold
        json_data[key]['page_size'] = data[j][5].get()
        j += 1
    try:
        Query(pdf_setting, col=pdf_setting['columns'], query=UPDATE, where=['Sr'],
              value=["2", json.dumps(json_data), "2"])
        messagebox.showinfo("Success Message", "PDF Settings has been successfully Updated")
    except:
        messagebox.showerror("Database Error",
                             "Error In Database. Please contact my owner Engr. Syed Mubashir at engr.smab@azeementerprises.org")
