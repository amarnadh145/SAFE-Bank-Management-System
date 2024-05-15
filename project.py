import streamlit as st
import bcrypt
import mysql.connector
import mysql.connector
import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
import pymysql
import random
import base64
import pandas as pd


st.set_page_config(page_title="SAFE BANK")
# Connect to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="amarnadh"
)
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="amarnadh"
)
mycursor = mydb.cursor()

# Authentication functions
def empsignup(authcode,username,password):
    try:
        mycursor.execute("SELECT * FROM das_employee WHERE emp_mail=%s", (username,))
        if mycursor.fetchone():
            return False, "Employee already exists."
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        mycursor.execute("""INSERT INTO das_employee (emp_mail,emp_password) VALUES(%s,%s)""",(username,hashed_password))
        mydb.commit()
        return True, "User created successfully."
    except Exception as e:
        print(e)
        return False, "Failed to create user due to a database error."

def signup(fname,lname,email,password,street,city,state,country,zipcode):
    try:
        mycursor.execute("SELECT * FROM das_cust WHERE cust_email=%s", (email,))
        if mycursor.fetchone():
            return False, "Username already exists."
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        mycursor.execute("""INSERT INTO das_cust (cust_fname, cust_lname, cust_email, cust_password, cust_street, cust_city, cust_state, cust_country, cust_zip) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(fname,lname,email,hashed_password,street,city,state,country,zipcode))
        mydb.commit()
        return True, "User created successfully."
    except Exception as e:
        print(e)
        return False, "Failed to create user due to a database error."

def login(username, password):
    try:
        mycursor.execute("""SELECT cust_password FROM das_cust WHERE cust_email=%s""", (username,))
        user_record = mycursor.fetchone()
        print("Retrieved Hashed Password:", user_record[0])
        if user_record and bcrypt.checkpw(password.encode('utf-8'), user_record[0].encode('utf-8')):
            st.session_state['logged_in'] = True  # Update session state to indicate logged in
            st.session_state['username'] = username
            return True,username
        return False
    except Exception as e:
        print(e)
        return False
def emplogin(username, password):
    try:
        mycursor.execute("""SELECT emp_password FROM das_employee WHERE emp_mail=%s""", (username,))
        user_record = mycursor.fetchone()
        if user_record and bcrypt.checkpw(password.encode('utf-8'), user_record[0].encode('utf-8')):
            st.session_state['emplogged_in'] = True  # Update session state to indicate logged in
            st.session_state['empusername'] = username
            return True,username
        return False
    except Exception as e:
        print(e)
        return False
# set background, use base64 to read local file


def main():
    st.title("SAVE AND FORTUNE EXCELLENCE")
    tab1, tab2=st.tabs(["HOME", "START"])
    with tab1:
        st.image("wallpaper.jpeg", use_column_width=True) 
    with tab2:
        if 'logged_in' and 'emplogged_in' not in st.session_state:
            st.session_state['logged_in'] = False
            st.session_state['emplogged_in'] = False

        if st.session_state['logged_in']:
            user_operations(st.session_state['username']) 
        elif st.session_state['emplogged_in']:
            emp_operations(st.session_state['empusername']) 
        else:
            login_signup_page()

def login_signup_page():
    sel=option_menu(
    menu_title=None,
    options=["LOGIN","FORGOT PASSWORD","SIGN UP"],
    icons=["box-arrow-in-right","x-diamond-fill","r-circle-fill"],
    orientation="horizontal",
)
    sel2=option_menu(
    menu_title="USER TYPE",
    options=["CUSTOMER","EMPLOYEE"],
    icons=["person","person-fill"],
    orientation="horizontal",
)
    if sel=="LOGIN":
        if sel2=="CUSTOMER":
            login_form = st.form(key='login_form')
            username = login_form.text_input("Username")
            password = login_form.text_input("Password", type="password")
            login_btn = login_form.form_submit_button("Login")
            if login_btn:
                if login(username, password):
                    st.session_state['logged_in'] = True
                    st.success("Logged in successfully.")
                    st.experimental_rerun()
                else:
                    st.error("Failed to log in. Check your username and password.")
        elif sel2=="EMPLOYEE":
            emplogin_form = st.form(key='emplogin_form')
            username = emplogin_form.text_input("Username")
            password = emplogin_form.text_input("Password", type="password")
            login_btn = emplogin_form.form_submit_button("Login")
            if login_btn:
                if emplogin(username, password):
                    st.session_state['emplogged_in'] = True
                    st.success("Logged in successfully.")
                    st.experimental_rerun()
                else:
                    st.error("Failed to log in. Check your username and password.")
    elif sel=="FORGOT PASSWORD":
        if sel2=="CUSTOMER":
            email = st.text_input("Enter your email address")
            new_password = st.text_input("Enter your new password", type="password")
            confirm_password = st.text_input("Confirm your new password", type="password")
            mycursor.execute("""select cust_id from das_cust where cust_email=%s""",(email,))
            res=mycursor.fetchone()
            if st.button("RESET"):
                if new_password != confirm_password:
                    st.error("Passwords do not match.")
                if res==None:
                    st.error("No account found on this email")
                else:
                    # Call the function to reset the password
                    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                    mycursor.execute("""UPDATE das_cust SET cust_password = %s WHERE cust_email = %s""", (hashed_password, email))
                    mydb.commit()
                    st.success("PASSWORD CHANGED SUCCESSFULLY")
        elif sel2=="EMPLOYEE":
            authcode = st.number_input("Enter authorization code",step=1,value=None)
            email = st.text_input("Enter your email address")
            new_password = st.text_input("Enter your new password", type="password")
            confirm_password = st.text_input("Confirm your new password", type="password")
            if st.button("RESET"):
                if int(authcode)!=9391521137:
                    st.error("AUTHORIZATION FAILED")
                elif new_password != confirm_password:
                    st.error("PASSWORDS DO NOT MATCH.")
                else:
                    # Call the function to reset the password
                    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                    mycursor.execute("""UPDATE das_employee SET emp_password = %s WHERE emp_mail = %s""", (hashed_password, email))
                    mydb.commit()
                    st.success("PASSWORD CHANGED SUCCESSFULLY")
    elif sel=="SIGN UP":
        if sel2=="CUSTOMER":
            signup_form = st.form(key='signup_form')
            fname=signup_form.text_input("ENTER FIRST NAME",max_chars=40,value=None)
            lname=signup_form.text_input("ENTER LAST NAME",max_chars=40,value=None)
            email=signup_form.text_input("ENTER EMAIL ADDRESS",max_chars=40,value=None)
            password=signup_form.text_input("ENTER PASSWORD",type="password",value=None)
            street=signup_form.text_input("ENTER STREET NAME",max_chars=40,value=None)
            city=signup_form.text_input("ENTER CITY NAME",max_chars=40,value=None)
            state=signup_form.text_input("ENTER STATE NAME",max_chars=40,value=None)
            country=signup_form.text_input("ENTER COUNTRY NAME",max_chars=40,value=None)
            zipcode = signup_form.number_input("ENTER ZIP CODE", format="%d", step=1,min_value=0,max_value=99999)
            signup_btn = signup_form.form_submit_button("Sign Up")
            if signup_btn:
                success, message = signup(fname,lname,email,password,street,city,state,country,zipcode)
                if success:
                    st.success(message)
                else:
                    st.error(message)
        elif sel2=="EMPLOYEE":
            signup_form = st.form(key='empsignup_form')
            authcode = signup_form.number_input("Authorization Code",step=1,value=None)
            username = signup_form.text_input("Username")
            password = signup_form.text_input("Password", type="password")
            signup_btn = signup_form.form_submit_button("SIGNUP")
            if signup_btn:
                if int(authcode)==9391521137:
                    success, message = empsignup(authcode,username,password)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
def fetch_universities(cursor):
    cursor.execute("SELECT univ_id, univ_name FROM das_univ ORDER BY univ_name")
    return cursor.fetchall()

def insert_university(univ_name, cursor):
    cursor.execute("INSERT INTO das_univ (univ_name) VALUES (%s)", (univ_name,))
    cursor.connection.commit()
    return cursor.lastrowid

def get_or_create_university(univ_name, cursor):
    cursor.execute("SELECT univ_id FROM das_univ WHERE univ_name = %s", (univ_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return insert_university(univ_name, cursor)

def user_operations(username):
    st.subheader("USER OPERATIONS")
    st.write(f"WELCOME, {username}! YOU ARE LOGGED IN")
    with st.sidebar:
        selected=option_menu(
            menu_title=None,
            options=["CREATE ACCOUNT","ACCOUNT DETAILS","UPDATE DETAILS","LOG OUT"],
            icons=["briefcase","book","check-square","box-arrow-left"]
            )
    if selected=="CREATE ACCOUNT":
        st.subheader("CREATE BANK ACCOUNT")
        a_name = st.selectbox("ACCOUNT NAME", options=["Checking", "Savings", "Loan"])
        today = datetime.now().date()
        a_date = st.date_input("ACCOUNT OPENING DATE", min_value=today, max_value=today, value=today)
        a_type = 'C' if a_name == "Checking" else 'S' if a_name == "Savings" else 'L' if a_name == "Loan" else 'Unknown'
        try:
            query_cust_id = "SELECT cust_id FROM das_cust WHERE cust_email = %s"
            mycursor.execute(query_cust_id, (username,))
            result = mycursor.fetchone()
            if result is None:
                raise ValueError("INVALID USER ADDRESS OR PASSWORD")
            cust_id = result[0]
    
    # Check if an account of this type already exists for this customer
            query_existing_account = "SELECT COUNT(*) FROM das_account WHERE cust_id = %s AND a_type = %s"
            mycursor.execute(query_existing_account, (cust_id, a_type))
            existing_count = mycursor.fetchone()[0]
            if existing_count > 0:
                raise ValueError("AN ACCOUNT OF THIS TYPE ALREADY EXISTS FOR THIS CUSTOMER")
        
    # Derive a_type based on a_name
            if a_type=='L':
                loan_amount=st.number_input("ENTER LOAN AMOUNT REQUIRED",format="%d", step=1,max_value=9999999,min_value=0)
                loan_months=st.number_input(" ENTER TIME REQUIRED TO REPAY IN MONTHS", format="%d", step=1,value =0,)
                if loan_amount and loan_months:
                    monthly_payment = loan_amount / loan_months
                loan_type = st.radio("SELECT LOAN TYPE", options=["Student Loan", "Home Loan"])
                l_type = 'ST' if loan_type== "Student Loan" else 'H' if loan_type == "Home Loan" else 'Unknown'
                if loan_type == "Home Loan":
                    h_builtyear = st.date_input("BUILT DATE OF HOME",max_value=today)
                    h_iacnumber = st.number_input("INSURANCE ACCOUNT NUMBER OF HOME",format="%d", value=0, step=1)
                    h_iname = st.text_input("INSURANCE COMPANY NAME OF HOME",max_chars=40,value=None)
                    h_iprem = st.number_input("MONTHLY INSURANCE PREMIUM OF HOME", value=0.0, step=0.01)
                    h_istreet = st.text_input("INSURANCE COMPANY STREET NAME",max_chars=40,value=None)
                    h_icity = st.text_input("INSURANCE COMPANY CITY NAME",max_chars=40,value=None)
                    h_istate = st.text_input("INSURANCE COMPANY STATE NAME",max_chars=40,value=None)
                    h_izip = st.number_input("INSURANCE COMPANY ZIP CODE",format="%d", value=0,step=1)
                elif loan_type == "Student Loan":
                    s_id = st.number_input("Student ID", format="%d",value=0, step=1)
                    s_radio = st.radio("SELECT GRADUATION STATUS",options=["GRADUATE","UNDER GRADUATE"])
                    if s_radio=="GRADUATE":
                        s_status="Graduate"
                    else:
                        s_status="Under graduate"
                    s_exgraddate = st.date_input("EXPECTED GRADUATION DATE",min_value=today)
                    cur = conn.cursor()
                    universities = fetch_universities(cur)
                    uni_options = [(u[1], u[0]) for u in universities]  # Creating a list of tuple pairs of names and IDs
                    uni_options.append(("Other", "Other"))  # Add 'Other' option to list
                    univ_selection = st.selectbox("SELECT UNIVERSITY", options=uni_options, format_func=lambda x: x[0])
                    if univ_selection[0] == "Other":
                        new_univ_name = st.text_input("ENTER NEW UNIVERSITY NAME",max_chars=40,value=None)
                        if st.button("ADD NEW UNIVERSITY"):
                            if new_univ_name:
                                univ_id = insert_university(new_univ_name, cur)
                                st.success(f"Added '{new_univ_name}' ")
                            else:
                                st.error("PLEASE ENTER A UNIVERSITY NAME.")
                    else:
                        univ_id = univ_selection[1]
                        cur.close()
            if st.button("CREATE ACCOUNT"):
                existing_a_numbers = set()
                while True:
                    a_number = str(random.randint(10000, 99999)).zfill(5)
                    if a_number not in existing_a_numbers:
                        existing_a_numbers.add(a_number)
                        break
                query_insert_account = """INSERT INTO das_account (a_number,a_name, a_date, a_type, cust_id) VALUES (%s,%s, %s, %s, %s)"""
                mycursor.execute(query_insert_account, (a_number,a_name, a_date, a_type, cust_id))
                try:
                    if a_type == 'C':  # Checking account
                    # Insert into das_check table with predefined service charge
                        query_insert_check_account = """INSERT INTO das_check (a_number,c_scharge) VALUES (%s,%s)"""
                        mycursor.execute("""select c_scharge from das_check limit 1""")
                        res=mycursor.fetchone()
                        if res:
                            c_scharge = res[0] 
                        else:
                            c_scharge=3.5
                        mycursor.execute(query_insert_check_account, (a_number,c_scharge))
                    elif a_type=='S': # Savings account
                # Insert into das_savings table with predefined service charge
                        query_insert_savings_account = """INSERT INTO das_savings(a_number,s_irate) VALUES (%s,%s)"""
                        mycursor.execute("""select s_irate from das_savings limit 1""")
                        res=mycursor.fetchone()
                        if res:
                            s_irate = res[0]  
                        else:
                            s_irate = 5.4
                        mycursor.execute(query_insert_savings_account, (a_number,s_irate))
                    elif a_type=='L':
                        query_insert_loan_account = """INSERT INTO das_loan (a_number,l_lrate, l_lamount, l_lmonths, l_lpayment, l_type)VALUES (%s,%s, %s, %s, %s, %s);"""
                        mycursor.execute("""select l_lrate from das_loan limit 1""")
                        res=mycursor.fetchone()
                        if res:
                            loan_rate = res[0] 
                        else:
                            loan_rate = 11.5
                        mycursor.execute(query_insert_loan_account, (a_number,loan_rate,loan_amount,loan_months,monthly_payment,l_type)) 
                        if l_type == "ST":
                            query_insert_student="""INSERT INTO das_student (a_number, s_id, s_status, s_exgraddate, univ_id) VALUES (%s,%s, %s, %s,%s);"""
                            mycursor.execute(query_insert_student,(a_number,s_id,s_status,s_exgraddate,univ_id))
                        elif l_type == "H":
                            query_insert_home="""INSERT INTO das_home (a_number,h_builtyear, h_iacnumber, h_iname, h_iprem, h_istreet, h_icity, h_istate, h_izip) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s);"""
                            mycursor.execute(query_insert_home,(a_number,h_builtyear,h_iacnumber,h_iname,h_iprem,h_istreet,h_icity,h_istate,h_izip))
                    # For other account types, insert into das_account table
                    mydb.commit()
                    st.success("ACCOUNT CREATED SUCCESSFULLY!")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    elif selected== "ACCOUNT DETAILS":
        st.subheader("ACCOUNT DETAILS")
        if st.button("GET ACCOUNTS"):
            try:
            # Retrieve cust_id based on email
                query_cust_id = "SELECT cust_id FROM das_cust WHERE cust_email = %s"
                mycursor.execute(query_cust_id, (username,))
                result = mycursor.fetchone()
                if result is None and len(email)>0:
                    raise ValueError("INVALID EMAIL ADDRESS OR PASSWORD")
                cust_id = result[0]
            # Retrieve account details using a join
                query_details_account = """SELECT a.cust_id,B.a_number FROM das_cust A JOIN das_account B ON A.cust_id = B.cust_id WHERE A.cust_id = %s"""
                mycursor.execute(query_details_account, (cust_id,))
                results = mycursor.fetchall()
                if not results:
                    st.warning("NO ACCOUNTS FOUND FOR THIS CUSTOMER.")
                else:
                    mycursor.execute("""SELECT cust_fname,cust_lname,cust_email,cust_street,cust_city,cust_state,cust_country,cust_zip from das_cust WHERE cust_id = %s""",(cust_id,))
                    results = mycursor.fetchall()
                    df = pd.DataFrame(results,columns = ['FIRST NAME','LAST NAME','EMAIL ADDRESS','STREET NAME','CITY','STATE','COUNTRY','ZIPCODE'])
                    df_no_index = df.reset_index(drop=True)
                    st.table(df_no_index)
                    mycursor.execute("""SELECT A.A_NUMBER,A.A_NAME,A_DATE,C.C_SCHARGE FROM DAS_ACCOUNT A JOIN DAS_CUST B ON A.CUST_ID=B.CUST_ID JOIN DAS_CHECK C ON A.A_NUMBER=C.A_NUMBER WHERE B.cust_id = %s and A.a_type='C' for update wait 15""",(cust_id,))
                    results = mycursor.fetchall()
                    df = pd.DataFrame(results,columns = ['ACCOUNT  NUMBER','ACCOUNT NAME','OPENING DATE','SERVICE CHARGE'])
                    df_no_index = df.reset_index(drop=True)
                    st.table(df_no_index)
                    mycursor.execute("""SELECT A.A_NUMBER,A.A_NAME,A_DATE,C.S_IRATE FROM DAS_ACCOUNT A JOIN DAS_CUST B ON A.CUST_ID=B.CUST_ID JOIN DAS_SAVINGS C ON A.A_NUMBER=C.A_NUMBER WHERE B.cust_id = %s AND A.A_TYPE='S'for update wait 15""",(cust_id,))
                    results = mycursor.fetchall()
                    df = pd.DataFrame(results,columns = ['ACCOUNT  NUMBER','ACCOUNT NAME','OPENING DATE','INTEREST RATE'])
                    df_no_index = df.reset_index(drop=True)
                    st.table(df_no_index)
                    mycursor.execute("""SELECT A.A_NUMBER,A.A_NAME,A_DATE,C.L_LAMOUNT,C.L_LRATE FROM DAS_ACCOUNT A JOIN DAS_CUST B ON A.CUST_ID=B.CUST_ID JOIN DAS_LOAN C ON A.A_NUMBER=C.A_NUMBER WHERE B.cust_id = %s AND A.A_TYPE='L'for update wait 15""",(cust_id,))
                    results = mycursor.fetchall()
                    df = pd.DataFrame(results,columns = ['ACCOUNT  NUMBER','ACCOUNT NAME','OPENING DATE','LOAN AMOUNT','LOAN RATE'])
                    df_no_index = df.reset_index(drop=True)
                    st.table(df_no_index)
                    st.success("ACCOUNTS RETRIEVED SUCCESSFULLY!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    elif selected == "UPDATE DETAILS":
        st.title("UPDATE PERSONAL DETAILS")
        updated_details = {}
        if st.checkbox("UPDATE FIRST NAME"):
            one=st.text_input("ENTER NEW FIRST NAME",max_chars=40,value=None)
            if one== "":
                st.error("PLEASE ENTER A NEW FIRST NAME",max_chars=40,value=None)
            else:
                updated_details['cust_fname'] =  one
        if st.checkbox("UPDATE LAST NAME"):
            two= st.text_input("ENTER NEW LAST NAME",max_chars=40,value=None)
            if two== "":
                st.error("PLEASE ENTER A NEW LAST NAME",max_chars=40,value=None)
            else:
                updated_details['cust_lname']=two
        if st.checkbox("Update Password"):
            three= st.text_input("Enter new password")
            if three== "":
                st.error("Please enter a new password")
            else:
                updated_details['cust_password'] = three
        if st.checkbox("Update Street"):
            four = st.text_input("Enter new street name",max_chars=40,value=None)
            if four== "":
                st.error("Please enter new street name",max_chars=40,value=None)
            else:
                updated_details['cust_street'] =four
        if st.checkbox("Update City"):
            five = st.text_input("Enter new city name",max_chars=40,value=None)
            if five== "":
                st.error("Please enter a new city name",max_chars=40,value=None)
            else:
                updated_details['cust_city']  = five
        if st.checkbox("Update State"):
            six= st.text_input("Enter new state name",max_chars=40,value=None)
            if six== "":
                st.error("Please enter a new state name",max_chars=40,value=None)
            else:
                updated_details['cust_state']  = six
        if st.checkbox("Update Zip COde"):
            seven= st.number_input("Enter new Zip code",step=1)
            if seven== "":
                st.error("Please enter a new zip code")
            else:
                updated_details['cust_zip']  = seven
    # Add more checkboxes for other details as needed
        if st.button("Update"):
            if not updated_details:
                st.error("Please select at least one detail to update")
            try:
            # Retrieve cust_id based on email
                query_cust_id = "SELECT cust_id FROM das_cust WHERE cust_email = %s"
                mycursor.execute(query_cust_id, (username,))
                result = mycursor.fetchone()
                if result is None:
                    raise ValueError("No customer found with this email address")
                cust_id = result[0]
            
            # Generate SQL update query
                update_query = "UPDATE das_cust SET "
                update_values = []
                for key, value in updated_details.items():
                    update_query += f"{key} = %s, "
                    update_values.append(value)
            # Remove the trailing comma and space
                update_query = update_query[:-2]
                update_query += " WHERE cust_id = %s"
                update_values.append(cust_id)

            # Execute the update query
                mycursor.execute(update_query, update_values)
                mydb.commit()
                st.success("Personal details updated successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    elif selected=="LOG OUT":
        st.write("ARE YOU SURE YOU WANT TO LOGOUT?")
        if st.button("LOG OUT"):
            st.session_state['logged_in'] = False
            st.experimental_rerun()
def emp_operations(empusername):
    st.subheader("EMPLOYEE OPERATIONS")
    st.write(f"Welcome, {empusername}! You are now logged in.")
    with st.sidebar:
        selected=option_menu(
            menu_title=None,
            options=["EMPLOYEE UPDATES","DELETE ACCOUNTS","ANALYSIS","LOG OUT"],
            icons=["check-circle","trash3","bar-chart","box-arrow-left"]
            )
    if selected == "EMPLOYEE UPDATES":
        st.title("UPDATE OFFICIAL DETAILS")
        new_cscharge, new_sirate,new_llrate=None,None,None
        if st.checkbox("UPDATE CHECKING ACCOUNT SERVICE CHARGE"):
            new_cscharge=st.number_input("ENTER NEW SERVICE CHARGE")
        if st.checkbox("UPDATE SAVINGS INTEREST RATE"):
            new_sirate=st.number_input("ENTER NEW SAVINGS INTEREST RATE")
        if st.checkbox("ENTER NEW LOAN RATE"):
            new_llrate=st.number_input("ENTER NEW LOAN RATE")
        if st.button("Update"):
            try:
                # Retrieve cust_id based on email
                query_emp_id = "SELECT * FROM das_employee WHERE emp_mail = %s"
                mycursor.execute(query_emp_id, (empusername,))
                result = mycursor.fetchone()
                if result is None:
                    raise ValueError("AUTHORIZATION FAILED")
                if new_cscharge != None:
                    try:
                        mycursor.execute("CALL updateCSCharge(%s)", (new_cscharge,))
                    except Exception as e:
                        st.error(f"Error updating charge: {e}")
                if new_sirate != None:
                    try:
                        mycursor.execute("CALL updateSIRate(%s)", (new_sirate,))
                    except Exception as e:
                        st.error(f"Error updating charge: {e}")
                if new_llrate != None:
                    try:
                        mycursor.execute("CALL updateLIRate(%s)", (new_llrate,))
                    except Exception as e:
                        st.error(f"Error updating charge: {e}")
                mydb.commit()
                st.success("OFFICIAL DETAILS UPDATED SUCCESSFULLY!")   
            except Exception as e:
                st.error(f"An error occurred: {e}")
    elif selected == "DELETE ACCOUNTS":
        st.title("ACCOUNT DELETES")
        account_number=st.number_input("ENTER ACCOUNT NUMBER",value=None, step=1, format="%d")
        if st.button("DELETE"):
            try:
                # Retrieve cust_id based on email
                query_emp_id = "SELECT * FROM das_employee WHERE emp_mail = %s"
                mycursor.execute(query_emp_id, (empusername,))
                result = mycursor.fetchone()
                if result is None:
                    raise ValueError("AUTHORIZATION FAILED")
                query_delete_account = "DELETE FROM das_check WHERE a_number = %s"
                mycursor.execute(query_delete_account, (account_number,))
                query_delete_savings = "DELETE FROM das_savings WHERE a_number = %s"
                mycursor.execute(query_delete_savings, (account_number,))
                query_delete_home="DELETE from das_home where a_number=%s"
                mycursor.execute(query_delete_home,(account_number,))
                query_delete_student="DELETE from das_student where a_number=%s"
                mycursor.execute(query_delete_student,(account_number,))
                query_delete_loan = "DELETE FROM das_loan WHERE a_number = %s"
                mycursor.execute(query_delete_loan, (account_number,))
                query_delete_account = "DELETE FROM das_account WHERE a_number = %s"
                mycursor.execute(query_delete_account, (account_number,))
                mydb.commit()
                st.success("ACCOUNT DELETED SUCCESSFULLY!")   
            except Exception as e:
                st.error(f"An error occurred: {e}")
    elif selected=="ANALYSIS":
        st.title("ACCOUNT ANALYSIS")
        if st.button("ACCOUNT REPORTS"):
            query_existing_account_count = "SELECT COUNT(*) FROM das_account WHERE  a_type = %s"
            mycursor.execute(query_existing_account_count, ('C',))  # Count existing Checking accounts
            existing_checking_count = mycursor.fetchone()[0]
            
            mycursor.execute(query_existing_account_count, ('S',))  # Count existing Savings accounts
            existing_savings_count = mycursor.fetchone()[0]
            
            mycursor.execute(query_existing_account_count, ('L',))  # Count existing Loan accounts
            existing_loan_count = mycursor.fetchone()[0]

            # Visualization: Count of different account types
            account_types = ["Checking", "Savings", "Loan"]
            account_counts = [existing_checking_count, existing_savings_count, existing_loan_count]
            fig, ax = plt.subplots()
            ax.pie(account_counts, labels=account_types, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            ax.set_title('Distribution of Account Types')
            st.pyplot(fig)
        if st.button("LOAN ANALYSIS"):
            query_loan_type_count = "SELECT (SELECT COUNT(*) FROM das_account a JOIN das_loan b ON a.a_number = b.a_number WHERE a.a_type = %s AND b.l_type = %s);"
            mycursor.execute(query_loan_type_count, ('L', 'ST'))  # Count student loans
            student_loan_count = mycursor.fetchone()[0]

            mycursor.execute(query_loan_type_count, ('L', 'H'))  # Count home loans
            home_loan_count = mycursor.fetchone()[0]

            # Visualization: Bar Chart of Loan Types
            loan_types = ["Student Loan", "Home Loan"]
            loan_counts = [student_loan_count, home_loan_count]
            fig, ax = plt.subplots()
            ax.bar(loan_types, loan_counts, color=['blue', 'green'])
            ax.set_xlabel('Type of Loan')
            ax.set_ylabel('Number of Loans')
            ax.set_title('Distribution of Loan Types')
            ax.set_ylim(0, max(loan_counts) + 10)  # Adjust y-limit for better visualization
            st.pyplot(fig)

    elif selected=="LOG OUT":
        st.write("ARE YOU SURE YOU WANT TO LOGOUT?")
        if st.button("LOG OUT"):
            st.session_state['emplogged_in'] = False
            st.rerun()

if __name__ == "__main__":
    main()
