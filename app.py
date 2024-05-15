import mysql.connector
import streamlit as st
from datetime import datetime
import pymysql
import random
a_number = random.randint(10000, 99999) 
mydb= mysql.connector.connect(
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
mycursor=mydb.cursor()
print("connection established")
def main():
    st.title("BANK MANAGEMENT SYSTEM")
    option=st.sidebar.selectbox("select an operation",("REGISTRATION","CREATE BANK ACCOUNT","ACCOUNT DETAILS","UPDATE DETAILS","delete"))
    if option=="REGISTRATION":
        st.subheader("REGISTER FOR BANK ACCOUNT")
        fname=st.text_input("enter first name")
        lname=st.text_input("enter lasst name")
        email=st.text_input("enter  email address")
        password=st.text_input("enter password")
        street=st.text_input("enter street name")
        city=st.text_input("enter city name")
        state=st.text_input("enter state name")
        country=st.text_input("enter country name")
        zip=st.number_input("enter zip code",step=1)
        if st.button("create"):
            sql="INSERT INTO das_cust (cust_fname, cust_lname, cust_email, cust_password, cust_street, cust_city, cust_state, cust_country, cust_zip) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val=(fname,lname,email,password,street,city,state,country,zip)
            mycursor.execute(sql,val)
            st.success("record created successfully")
            mydb.commit()
    elif option == "CREATE BANK ACCOUNT":
        st.subheader("CREATE BANK ACCOUNT")
        email = st.text_input("Enter email address")
        a_name = st.selectbox("Account Name", options=["Checking", "Savings", "Loan"])
        a_date = st.date_input("Account Opening Date", value=datetime.now())
        a_type = 'C' if a_name == "Checking" else 'S' if a_name == "Savings" else 'L' if a_name == "Loan" else 'Unknown'
        try:
            query_cust_id = "SELECT cust_id FROM das_cust WHERE cust_email = %s"
            mycursor.execute(query_cust_id, (email,))
            result = mycursor.fetchone()
            if result is None:
                raise ValueError("No customer found with this email address")
            cust_id = result[0]
    
    # Check if an account of this type already exists for this customer
            query_existing_account = "SELECT COUNT(*) FROM das_account WHERE cust_id = %s AND a_type = %s"
            mycursor.execute(query_existing_account, (cust_id, a_type))
            existing_count = mycursor.fetchone()[0]
            if existing_count > 0:
                raise ValueError("An account of this type already exists for this customer")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    # Derive a_type based on a_name
        if a_type=='L':
            loan_amount=st.number_input("Enter loan amount required", value=0, step=1)
            loan_months=st.number_input(" Enter time rquired to repay loan in months", value =0,step=1)
            if loan_amount and loan_months:
                monthly_payment = loan_amount / loan_months
            loan_type = st.radio("Select Loan Type", options=["Student Loan", "Home Loan"])
            l_type = 'ST' if loan_type== "Student Loan" else 'H' if loan_type == "Home Loan" else 'Unknown'
            if loan_type == "Home Loan":
                h_builtyear = st.date_input("Built Date of Home")
                h_iacnumber = st.number_input("Insurance Account Number of Home", value=0, step=1)
                h_iname = st.text_input("Insurance Company Name of Home", value="")
                h_iprem = st.number_input("Monthly Insurance Premium of Home", value=0.0, step=0.01)
                h_istreet = st.text_input("Insurance Company Street Name", value="")
                h_icity = st.text_input("Insurance Company City Name", value="")
                h_istate = st.text_input("Insurance Company State Name", value="")
                h_izip = st.number_input("Insurance Company ZIP Code", value=0,step=1)
            elif loan_type == "Student Loan":
                s_id = st.number_input("Student ID", value=0, step=1)
                s_status = st.text_input("Student Status (Graduate/Undergraduate)", value="")
                s_exgraddate = st.date_input("Expected Graduation Date")
                cur = conn.cursor()
                universities = fetch_universities(cur)
                uni_options = [(u[1], u[0]) for u in universities]  # Creating a list of tuple pairs of names and IDs
                uni_options.append(("Other", "Other"))  # Add 'Other' option to list
                univ_selection = st.selectbox("Select University", options=uni_options, format_func=lambda x: x[0])
                if univ_selection[0] == "Other":
                    new_univ_name = st.text_input("Enter New University Name")
                    if st.button("Add New University"):
                        if new_univ_name:
                            univ_id = insert_university(new_univ_name, cur)
                            st.success(f"Added '{new_univ_name}' with ID {univ_id}")
                        else:
                            st.error("Please enter a university name.")
                else:
                    univ_id = univ_selection[1]
                    cur.close()
        if st.button("CREATE ACCOUNT"):
            try:
                if a_type == 'C':  # Checking account
                # Insert into das_check table with predefined service charge
                    query_insert_check_account = """INSERT INTO das_check (c_scharge) VALUES (%s)"""
                    c_scharge = 0.05  # Predefined service charge of 5%
                    mycursor.execute(query_insert_check_account, (c_scharge,))
                elif a_type=='S': # Savings account
            # Insert into das_savings table with predefined service charge
                    query_insert_savings_account = """INSERT INTO das_savings(s_irate) VALUES (%s)"""
                    s_irate= 4.5  # Predefined service charge of 5%
                    mycursor.execute(query_insert_savings_account, (s_irate,))
                elif a_type=='L':
                    query_insert_loan_account = """INSERT INTO das_loan (l_lrate, l_lamount, l_lmonths, l_lpayment, l_type)VALUES (%s, %s, %s, %s, %s);"""
                    loan_rate=9.5
                    mycursor.execute(query_insert_loan_account, (loan_rate,loan_amount,loan_months,monthly_payment,l_type)) 
                    if l_type == "ST":
                        query_insert_student="""INSERT INTO das_student (s_id, s_status, s_exgraddate, univ_id) VALUES (%s, %s, %s,%s);"""
                        mycursor.execute(query_insert_student,(s_id,s_status,s_exgraddate,univ_id))
                    elif l_type == "H":
                        query_insert_home="""INSERT INTO das_home (h_builtyear, h_iacnumber, h_iname, h_iprem, h_istreet, h_icity, h_istate, h_izip) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
                        mycursor.execute(query_insert_home,(h_builtyear,h_iacnumber,h_iname,h_iprem,h_istreet,h_icity,h_istate,h_izip))
                query_insert_account = """INSERT INTO das_account (a_name, a_date, a_type, cust_id) VALUES (%s, %s, %s, %s)"""
                mycursor.execute(query_insert_account, (a_name, a_date, a_type, cust_id))

                # For other account types, insert into das_account table
                mydb.commit()
                st.success("Account created successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    elif option == "ACCOUNT DETAILS":
        st.subheader("ACCOUNT DETAILS")
        email = st.text_input("Enter email address")
        if st.button("GET ACCOUNTS"):
            try:
            # Retrieve cust_id based on email
                query_cust_id = "SELECT cust_id FROM das_cust WHERE cust_email = %s"
                mycursor.execute(query_cust_id, (email,))
                result = mycursor.fetchone()
                if result is None:
                    raise ValueError("No customer found with this email address")
                cust_id = result[0]
            # Retrieve account details using a join
                query_details_account = """SELECT A.*, B.* FROM das_cust A JOIN das_account B ON A.cust_id = B.cust_id WHERE A.cust_id = %s"""
                mycursor.execute(query_details_account, (cust_id,))
                results = mycursor.fetchall()
                if not results:
                    st.warning("No accounts found for this customer.")
                else:
                # Display account details
                    for row in results:
                        st.write(row)
                    st.success("Accounts retrieved successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    elif option == "UPDATE DETAILS":
        st.title("Update Personal Details")
        email = st.text_input("Enter email address")
        updated_details = {}
        if st.checkbox("Update First Name"):
            one=st.text_input("Enter new first name")
            if one== "":
                st.error("Please enter a new first name")
            else:
                updated_details['cust_fname'] =  one
        if st.checkbox("Update Last Name"):
            two= st.text_input("Enter new last name")
            if two== "":
                st.error("Please enter a new last name")
            else:
                updated_details['cust_lname']=two
        if st.checkbox("Update Password"):
            three= st.text_input("Enter new password")
            if three== "":
                st.error("Please enter a new password")
            else:
                updated_details['cust_password'] = three
        if st.checkbox("Update Street"):
            four = st.text_input("Enter new street name")
            if four== "":
                st.error("Please enter new street name")
            else:
                updated_details['cust_street'] =four
        if st.checkbox("Update City"):
            five = st.text_input("Enter new city name")
            if five== "":
                st.error("Please enter a new city name ")
            else:
                updated_details['cust_city']  = five
        if st.checkbox("Update State"):
            six= st.text_input("Enter new state name")
            if six== "":
                st.error("Please enter a new state name ")
            else:
                updated_details['cust_state']  = six
        if st.checkbox("Update Zip COde"):
            seven= st.number_input("Enter new Zip code",step=1)
            if seven== "":
                st.error("Please enter a new zip code ")
            else:
                updated_details['cust_zip']  = seven
    # Add more checkboxes for other details as needed
        if st.button("Update"):
            if not updated_details:
                st.error("Please select at least one detail to update")
            try:
            # Retrieve cust_id based on email
                query_cust_id = "SELECT cust_id FROM das_cust WHERE cust_email = %s"
                mycursor.execute(query_cust_id, (email,))
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

if __name__=="__main__":
    main()

