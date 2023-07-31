import streamlit as st
import csv
import pandas as pd
import os
import tempfile

st.set_page_config(layout="wide", page_icon="🔐")
st.title("Password generator")

st.markdown("""
<style>
.css-eh5xgm.e1ewe7hr3    
{
            visibility : hidden;
}
.css-cio0dv.e1g8pov61
            {
            visibility : hidden;
            }
</style>
""", unsafe_allow_html=True)


def generate(lower, upper, special, number):
    import random
    lowercase_chars = 'abcdefghijklmnopqrstuvwxyz'
    uppercase_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    special_chars = '!@#$%^&*()_+-/.,'
    digit_chars = '0123456789'

    # Create lists for each character type
    lowercase_list = [random.choice(lowercase_chars) for _ in range(lower)]
    uppercase_list = [random.choice(uppercase_chars) for _ in range(upper)]
    special_list = [random.choice(special_chars) for _ in range(special)]
    number_list = [random.choice(digit_chars) for _ in range(number)]

    # Concatenate the lists and shuffle to form the password
    password_list = lowercase_list + uppercase_list + special_list + number_list
    random.shuffle(password_list)
    password = ''.join(password_list)
    return password


def input():
    password=''
    input_form=st.form(key="input",clear_on_submit=True)
    domain=input_form.text_input("Enter your password domain")
    input_form.markdown("---")
    username=input_form.text_input("Enter your domain username")
    input_form.markdown("---")
    input_form.subheader("Desired password length")
    pass_length=input_form.slider("🔐",min_value=8,max_value=100)
    input_form.markdown("---")
    special=input_form.slider("Special characters",min_value=0,max_value=100)
    lower=input_form.slider("Lower case charcters",min_value=0,max_value=100)
    upper=input_form.slider("Upper case characters",min_value=0,max_value=100)
    number=input_form.slider("Numbers",min_value=0,max_value=100)
    verify=input_form.form_submit_button("Generate")
    sum=lower+upper+number+special
    if verify:
        if  domain=='' or username=='':
            input_form.warning("Please verify username and/or domain name input ")
            if sum!=pass_length:
                input_form.error("Please verify password composition",icon="🚨")
        elif sum==pass_length:
            password=generate(lower,upper,special,number)
            input_form.success("Composition done successfully",icon="✅")
            data={
                "Domain": domain,
                "Username": username,
                "Password Length":(sum),
                "Password" : password
            }
            return data




def create_temp_csv(data):
    # Create a temporary file and get its path
    temp_file = tempfile.NamedTemporaryFile(
        mode='w', delete=False, suffix='.csv')
    temp_file_path = temp_file.name

    # Write the data to the temporary CSV file
    with open(temp_file_path, 'w', newline='') as file:
        fieldnames = ["Domain", "Username", "Password", "Password_Length"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({
            "Domain": data['Domain'],
            "Username": data['Username'],
            "Password": data["Password"],
            "Password_Length": data['Password Length']
        })

    # Close the temporary file
    temp_file.close()

    return temp_file_path

# Function to save data to the CSV file


def save(data):
    file_path = "temp_data.csv"
    write_fieldnames(file_path)

    with open(file_path, 'a+', newline='') as file:
        thewriter = csv.writer(file)
        thewriter.writerow([
            "www." + data['Domain'] + ".com",
            data['Username'],
            data["Password"],
            data['Password Length']
        ])

# Function to check if the CSV file is empty


def empty_data(file_path):
    return not os.path.exists(file_path) or os.path.getsize(file_path) == 0

# Function to write fieldnames if the CSV file is empty
def inner_display():
    iner=st.form(key='inner')
    display_data = iner.form_submit_button("Display/Hide data")
    if display_data:
        try:
            df = pd.read_csv('temp_data.csv')
            iner.table(df)
            delete = st.button(
                    "Delete Data table", on_click=lambda: delete_content('temp_data.csv'))
        except pd.errors.EmptyDataError:
            iner.error("No data found to display")

def write_fieldnames(file_path):
    if empty_data(file_path):
        with open(file_path, 'a+', newline='') as file:
            fieldnames = ["Domain", "Username", "Password", "Password_Length"]
            thewriter = csv.DictWriter(file, fieldnames=fieldnames)
            thewriter.writeheader()

def delete_content(csvfile):
    """Delete all content in given CSV File"""
    try:    
        f = open(csvfile,"r+")
        f.truncate(0)
    except Exception as e :
        print ("Error while deleting contents of ",csvfile,", error message:",e )
    
def display():
    # Check if the temporary file exists or not
    temp_file_path = "temp_data.csv"
    if not os.path.exists(temp_file_path):
        # Create a new temporary file if it doesn't exist
        with open(temp_file_path, 'w', newline='') as file:
            pass  # Create an empty file

    # Create two columns to display the forms side by side
    col1, col2 = st.columns(2)

    # Define the "Data Input" form inside the first column
    with col1:
        st.subheader("Data Input")
        data = input()
        if data is not None:
            save(data)

    # Define the "Data Manipulation" form button inside the second column
    with col2:
        st.subheader("Data Manipulation")
        inner_display()





display()
