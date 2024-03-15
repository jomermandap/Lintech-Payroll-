from flask import Flask, request, render_template, redirect, url_for, jsonify, send_from_directory
from datetime import datetime, timedelta
import sqlite3
import random
import string
import uuid
import os

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')


# Function to establish database connection -----------------------------------------------------
def get_db_connection():
    connection = sqlite3.connect('test.db')
    connection.row_factory = sqlite3.Row
    return connection


# Loggers ---------------------------------------------------------------------------------------

def login_log(user_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Generate a unique login activity ID
        user_act_id = generate_act_id()

        # Log the login activity
        cursor.execute(
            "INSERT INTO user_activity (user_act_id, act_id, user_id, details, date_time) VALUES (?, ?, ?, ?, ?)",
            (user_act_id, "Login", user_id, "Logged in", datetime.now()))

        connection.commit()
    except Exception as e:
        # Handle any errors that occur during logging
        print("Error logging login activity:", e)
    finally:
        connection.close()


# ID GENERATORS ----------------------------------------------------------------

# Function to generate a unique random employee ID
def generate_emp_id():
    id = str(uuid.uuid4())
    random.seed(id)
    initial = "EMP"
    random_chars = ''.join(random.choices(string.digits, k=10))
    emp_id = initial + random_chars
    return emp_id

def generate_ps_id():
    id = str(uuid.uuid4())
    random.seed(id)
    initial = "PS"
    random_chars = ''.join(random.choices(string.digits, k=10))
    ps_id = initial + random_chars
    return ps_id
def generate_ts_id():
    id = str(uuid.uuid4())
    random.seed(id)
    initial = "TS"
    random_chars = ''.join(random.choices(string.digits, k=10))
    ts_id = initial + random_chars
    return ts_id

def generate_act_id():
    id = str(uuid.uuid4())
    random.seed(id)
    initial = "ACT"
    random_chars = ''.join(random.choices(string.digits, k=10))
    act_id = initial + random_chars
    return act_id


def generate_emp_proj_id():
    id = str(uuid.uuid4())
    random.seed(id)
    initial = "EPR"
    random_chars = ''.join(random.choices(string.digits, k=10))
    emp_proj_id = initial + random_chars
    return emp_proj_id


# Function to generate a unique random timecard ID
def generate_tc_id():
    id = str(uuid.uuid4())
    random.seed(id)
    initial = "TC"
    random_chars = ''.join(random.choices(string.digits, k=10))
    tc_id = initial + random_chars
    return tc_id


def generate_cl_id():
    id = str(uuid.uuid4())
    random.seed(id)
    initial = "CL"
    random_chars = ''.join(random.choices(string.digits, k=10))
    cl_id = initial + random_chars
    return cl_id


def generate_pr_id():
    id = str(uuid.uuid4())
    random.seed(id)
    initial = "PR"
    random_chars = ''.join(random.choices(string.digits, k=10))
    pr_id = initial + random_chars
    return pr_id


# Function to generate a unique payroll period ID
def generate_pp_id():
    id = str(uuid.uuid4())
    random.seed(id)
    initial = "PP"
    random_chars = ''.join(random.choices(string.digits, k=10))
    pp_id = initial + random_chars
    return pp_id


# Function to generate a unique random user ID
def generate_user_id():
    id = str(uuid.uuid4())
    random.seed(id)
    initial = "USER"
    random_chars = ''.join(random.choices(string.digits, k=10))
    user_id = initial + random_chars
    return user_id


# Route to generate user ID --------------------------------------------------------------------
@app.route('/generate_user_id')
def generate_user_id_route():
    user_id = generate_user_id()  # Replace with your actual function for generating user IDs
    return user_id


@app.route('/generate_pr_id')
def generate_pr_id_route():
    pr_id = generate_pr_id()  # Replace with your actual function for generating project IDs
    return pr_id


@app.route('/generate_cl_id')
def generate_cl_id_route():
    cl_id = generate_cl_id()  # Replace with your actual function for generating user IDs
    return cl_id


# Route to generate employee ID
@app.route('/generate_emp_id')
def generate_emp_id_route():
    emp_id = generate_emp_id()
    return emp_id


@app.route('/generate_emp_proj_id')
def generate_emp_proj_id_route():
    emp_proj_id = generate_emp_proj_id()  # Replace with your actual function for generating user IDs
    return emp_proj_id


# Add record functions ---------------------------------------------------------------------
# Route to add a position
@app.route('/n_add_pos', methods=['GET', 'POST'])
def add_position():
    if request.method == 'POST':
        posType = request.form['posType']
        print(posType)
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM position")
            # Fetch the result
            count = cursor.fetchone()[0]
            id = count + 1
            print(id)
            cursor.execute("INSERT INTO position (posID, type) VALUES (?, ?)", (id, posType))
            connection.commit()
            positions = get_emp_positions()  # Fetch positions from the database
            return render_template('n_add_emp.html', positions=positions, message="Position added successfully!")
        except Exception as e:
            return render_template('n_add_emp.html', message="Error adding position: {}".format(e))
        finally:
            connection.close()

    return render_template('n_add_emp.html')

def get_gender_id_by_type(gender_type):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT gender_id FROM gender WHERE type = ?", (gender_type,))
    row = cursor.fetchone()
    connection.close()
    if row:
        return row['gender_id']
    else:
        raise ValueError("Gender type '{}' not found".format(gender_type))


def is_pr_id_valid(pr_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT pr_id FROM project WHERE pr_id = ?", (pr_id,))
    existing_pr_id = cursor.fetchone()
    connection.close()
    return existing_pr_id is not None


def get_genders():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT type FROM gender")
    genders = cursor.fetchall()
    connection.close()
    return genders


# Function to get positions from the database
def get_emp_positions():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM position")
    positions = cursor.fetchall()
    connection.close()
    return positions


# Route to delete an employee
@app.route('/delete/<emp_id>', methods=['POST'])
def delete_employee(emp_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM employee WHERE empID=?", (emp_id,))
        connection.commit()
        return redirect(url_for('view_employees'))
    except Exception as e:
        return render_template('n_employee.html', message="Error deleting employee: {}".format(e))
    finally:
        connection.close()


# Route to delete a client
@app.route('/cl_delete/<cl_id>', methods=['POST'])
def delete_client(cl_id):
    print(cl_id)
    try:
        if request.method == 'POST':
            print(cl_id)
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM client WHERE cl_id=?", (cl_id,))
            connection.commit()
            return redirect(url_for('view_clients'))
    except Exception as e:
        return render_template('n_client.html', message="Error deleting client: {}".format(e))
    finally:
        connection.close()

# Route to delete a project
@app.route('/delete_project/<pr_id>', methods=['POST'])
def delete_project(pr_id):
    try:
        if request.method == 'POST':
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM project WHERE pr_id=?", (pr_id,))
            connection.commit()
            return redirect(url_for('view_projects'))
    except Exception as e:
        return render_template('n_project.html', message="Error deleting project: {}".format(e))
    finally:
        connection.close()





# NEW Route to view all employees
@app.route('/n_employee')
def view_employees():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM EmployeeInfo")
        employees = cursor.fetchall()
        return render_template('n_employee.html', employees=employees)
    except Exception as e:
        return render_template('n_employee.html', message="Error fetching employees: {}".format(e))
    finally:
        connection.close()


# Route to view all employees
# @app.route('/view')
# def view_employees():
#     try:
#         connection = get_db_connection()
#         cursor = connection.cursor()
#         cursor.execute("SELECT * FROM employee")
#         employees = cursor.fetchall()
#         return render_template('view.html', employees=employees)
#     except Exception as e:
#         return render_template('view.html', message="Error fetching employees: {}".format(e))
#     finally:
#         connection.close()

# NEW Route to view all clients
@app.route('/n_client')
def view_clients():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM client")
        clients = cursor.fetchall()
        return render_template('n_client.html', clients=clients)
    except Exception as e:
        return render_template('n_client.html', message="Error fetching clients: {}".format(e))
    finally:
        if connection:
            connection.close()


@app.route('/n_project')
def view_projects():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM project")
        projects = cursor.fetchall()
        return render_template('n_project.html', projects=projects)
    except Exception as e:
        return render_template('n_project.html', message="Error fetching projects: {}".format(e))
    finally:
        if connection:
            connection.close()

# @app.route('/n_attendance_project')
# def show_projects():
#     try:
#         connection = get_db_connection()
#         cursor = connection.cursor()
#         cursor.execute("SELECT * FROM project")
#         projects = cursor.fetchall()
#         return render_template('n_attendance_project.html', projects=projects)
#     except Exception as e:
#         return render_template('n_attendance_project.html', message="Error fetching projects: {}".format(e))
#     finally:
#         if connection:
#             connection.close()


# Flask route for adding a user
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    userID = generate_user_id() if request.method == 'POST' else ''
    if request.method == 'POST':
        empID = request.form['empID']
        username = request.form['username']
        password = request.form['password']
        statusID = request.form['statusID']

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Check if the username already exists
            cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
            existing_user = cursor.fetchone()
            if existing_user:
                return render_template('n_add_user.html',
                                       message="Username already taken. Please choose a different one.",
                                       statuses=get_statuses())

            # Check if the empID exists in the employee table
            if not is_emp_id_valid(empID):
                return render_template('n_add_user.html', message="Invalid Employee ID. Please provide a valid one.",
                                       statuses=get_statuses())

            if is_emp_id_used(empID):
                return render_template('n_add_user.html',
                                       empID_error="Employee ID already used. Please choose a different one.",
                                       statuses=get_statuses())
            # If username is unique and empID is valid, insert the new user
            cursor.execute(
                "INSERT INTO user (user_id, user_status_id, emp_id, username, password) VALUES (?, ?, ?, ?, ?)",
                (userID, statusID, empID, username, password))
            connection.commit()
            return render_template('n_add_user.html', message="User added successfully!", statuses=get_statuses())
        except Exception as e:
            return render_template('n_add_user.html', message="Error adding user: {}".format(e), statuses=get_statuses())
        finally:
            connection.close()

    return render_template('n_add_user.html', statuses=get_statuses())  # Pass statuses to the template context


def is_emp_id_used(empID):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT emp_id FROM user WHERE emp_id = ?", (empID,))
    existing_emp_id = cursor.fetchone()
    connection.close()
    return existing_emp_id is not None


def is_emp_id_valid(empID):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT empID FROM employee WHERE empID = ?", (empID,))
    existing_emp_id = cursor.fetchone()
    connection.close()
    return existing_emp_id is not None


def is_username_taken(username):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user WHERE username=?", (username,))
    existing_user = cursor.fetchone()
    connection.close()
    return existing_user is not None


# Function to get user statuses from the database
def get_statuses():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_status")
    statuses = cursor.fetchall()
    connection.close()
    return statuses


# NEW Route to input employee data
@app.route('/n_add_emp', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'GET':
        empID = generate_emp_id()
        positions = get_emp_positions()  # Fetch positions from the database
        genders = get_genders()  # Fetch genders from the database
        return render_template('n_add_emp.html', empID=empID, positions=positions, genders=genders)
    elif request.method == 'POST':
        print("post")
        empID = request.form.get('empID')
        posID = request.form.get('posID')
        empFName = request.form.get('empFName')
        empLName = request.form.get('empLName')
        empInitial = request.form.get('empInitial')
        gender_type = request.form.get('gender')  # Get the gender type from the form
        birthdate = request.form.get('birthdate')
        age = request.form.get('age')
        contact = request.form.get('contact')
        email = request.form.get('email')
        gender_id = get_gender_id_by_type(gender_type)

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO employee (empID, posID, empFName, empLName, empInitial, gender, birthdate, age, contact, email) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (empID, posID, empFName, empLName, empInitial, gender_id, birthdate, age, contact, email))
            connection.commit()
            success_message = "Employee added successfully!"
            positions = get_emp_positions()  # Fetch positions from the database
            genders = get_genders()  # Fetch genders from the database
            return render_template('n_add_emp.html', empID=empID, positions=positions, genders=genders,
                                   success_message=success_message)
        except Exception as e:
            error_message = "Error adding employee: {}".format(e)
            positions = get_emp_positions()  # Fetch positions from the database
            genders = get_genders()  # Fetch genders from the database
            return render_template('n_add_emp.html', empID=empID, positions=positions, genders=genders,
                                   error_message=error_message)
        finally:
            connection.close()


# NEW Route to add a client
# @app.route('/n_add_client', methods=['GET', 'POST'])
# def add_client():
#     clID = generate_cl_id() if request.method == 'POST' else ''
#     if request.method == 'POST':
#         cl_fname = request.form['cl_fname']
#         cl_lname = request.form['cl_lname']
#         cl_contact = request.form['cl_contact']
#         cl_email = request.form['cl_email']
#
#         try:
#             connection = get_db_connection()
#             cursor = connection.cursor()
#             cursor.execute(
#                 "INSERT INTO client (cl_id, cl_fname, cl_lname, cl_contact, cl_email) VALUES (?, ?, ?, ?, ?)",
#                 (clID, cl_fname, cl_lname, cl_contact, cl_email))
#             connection.commit()
#             return render_template('n_add_client.html', message="Client added successfully!")
#         except Exception as e:
#             return render_template('n_add_client.html', message="Error adding client: {}".format(e))
#         finally:
#             connection.close()
#
#     return render_template('n_add_client.html')


# Route to add a project
@app.route('/n_add_client', methods=['GET', 'POST'])
def add_client():
    clID = generate_cl_id() if request.method == 'POST' else ''
    if request.method == 'POST':
        cl_fname = request.form['cl_fname']
        cl_lname = request.form['cl_lname']
        cl_contact = request.form['cl_contact']
        cl_email = request.form['cl_email']

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO client (cl_id, cl_fname, cl_lname, cl_contact, cl_email) VALUES (?, ?, ?, ?, ?)",
                           (clID, cl_fname, cl_lname, cl_contact, cl_email))
            connection.commit()
            return render_template('n_add_client.html', message="Client added successfully!")
        except Exception as e:
            return render_template('n_add_client.html', message="Error adding client: {}".format(e))
        finally:
            connection.close()

    return render_template('n_add_client.html')

# Route to add a project
@app.route('/n_add_project', methods=['GET', 'POST'])
def add_project():
    prID = generate_pr_id() if request.method == 'POST' else ''
    if request.method == 'POST':
        cl_id = request.form['cl_id']
        pr_name = request.form['pr_name']
        pr_address = request.form['pr_address']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO project (pr_id, cl_id, pr_name, pr_address, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?)",
                (prID, cl_id, pr_name, pr_address, start_date, end_date))
            connection.commit()
            return render_template('n_add_project.html', message="Project added successfully!")
        except Exception as e:
            return render_template('n_add_project.html', message="Error adding project: {}".format(e))
        finally:
            connection.close()

    # Fetch client information to populate the combo box
    clients = get_clients()
    return render_template('n_add_project.html', clients=clients)


# Function to fetch client information
def get_clients():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT cl_id, cl_fname, cl_lname FROM client")
    clients = cursor.fetchall()
    connection.close()
    return clients


@app.route('/n_dashboard')
def n_dashboard():
    return render_template('n_dashboard.html')


@app.route('/')
def login_page():
    return render_template('login.html')


# Route to handle login form submission
@app.route('/login', methods=['POST'])
def login():
    # username = request.form['username']
    # password = request.form['password']
    username = "daniel"
    password = "djhs1216"

    # Check if username and password match a record in the user table
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT user_id FROM user WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()

    print("Imong username: " + username)
    print("Imong Password: " + password)

    if user:
        print("Logged in successfully! Woah Woah!!")
        user_id = user['user_id']
        login_log(user_id)  # Log the login activity

        # Redirect to dashboard route if login is successful
        return redirect(url_for('n_dashboard'))
    else:
        # Redirect back to login page with error message if login fails
        print("Patakag credentials bogo man deay")
        return render_template('login.html', error_message="Invalid username or password")


@app.route('/add_payroll_period')
def add_payroll_period_form():
    return render_template('add_payroll_period.html')


# Route to add a new payroll period
@app.route('/add_payroll_period', methods=['GET', 'POST'])
def add_payroll_period():
    if request.method == 'POST':
        pp_start = request.form['pp_start']
        pp_end = request.form['pp_end']

        id = generate_pp_id()
        print("ID: " + id)

        # Convert into one variable
        period = pp_start + " to " + pp_end
        print("Period: " + period)

        # Generates the timecards for the date
        dates = generate_tc_dates(id, pp_start, pp_end)

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO payroll_period (pp_id, period) VALUES (?, ?)", (id, period))
            connection.commit()
            return render_template('n_attendance_project.html', success_message="Payroll period added successfully!")
        except Exception as e:
            return render_template('n_attendance_project.html', error_message="Error adding payroll period: {}".format(e))
        finally:
            connection.close()
    else:
        return 'Method not allowed', 405


# To generate timecard dates
def generate_tc_dates(id, pp_start, pp_end):
    pp_id = id
    print("pp id: " + id)

    start_dt = datetime.strptime(pp_start, "%Y-%m-%d").date()
    end_dt = datetime.strptime(pp_end, "%Y-%m-%d").date()

    # difference between current and previous date
    delta = timedelta(days=1)

    # store the dates between two dates in a list
    dates = []

    while start_dt <= end_dt:
        # add current date to list by converting  it to iso format
        dates.append(start_dt.isoformat())
        # increment start date by timedelta
        start_dt += delta

    # Add records to the timecard_period table for each date in the dates array
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        for date in dates:
            # Here, day_type_id should be the foreign key reference to the day_type table
            tc_id = generate_tc_id()
            cursor.execute("INSERT INTO timecard_period (tc_id, pp_id, day_type, tc_date) VALUES (?, ?, ?, ?)",
                           (tc_id, pp_id, 1, date))  # Assuming day_type_id is the default day type

        connection.commit()
        return True  # Return True if records are successfully inserted
    except Exception as e:
        print("Error adding timecard periods:", e)
        return False  # Return False if there's an error inserting records
    finally:
        connection.close()


# Function to fetch position names from the database
def get_positions():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT posType, posName FROM projectPosition")
    positions = cursor.fetchall()
    connection.close()
    return positions


# Route to render the form with day_name as a combo box
@app.route('/select_day_name')
def select_day_name():
    day_names = get_all_day_names()
    return render_template('select_day_name.html', day_names=day_names)


def get_all_day_names():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT day_name FROM day")
    day_names = [row['day_name'] for row in cursor.fetchall()]
    connection.close()
    return day_names


@app.route('/add_employee_project', methods=['GET', 'POST'])
def add_employee_project():
    if request.method == 'POST':
        # Extract data from the form submission
        emp_proj_id = request.form['emp_proj_id']
        emp_name = request.form['emp_name']
        pr_id = request.form['pr_name']
        pos_type = request.form['pos_name']

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Fetch emp_id based on emp_name
            cursor.execute("SELECT empID FROM employee WHERE empFName = ?", (emp_name,))
            result = cursor.fetchone()
            if result is not None:
                emp_id = result[0]

                # Insert into employee_project table
                cursor.execute(
                    "INSERT INTO employee_project (emp_proj_id, emp_id, pr_id, pos_type) VALUES (?, ?, ?, ?)",
                    (emp_proj_id, emp_id, pr_id, pos_type))
                connection.commit()

                success_message = "Employee project added successfully!"
                return render_template('n_add_employee_project.html', success_message=success_message,
                                       projects=get_projects(), positions=get_positions(),
                                       generate_emp_proj_id=generate_emp_proj_id())

            else:
                error_message = f"No employee found with name '{emp_name}'"
                return render_template('n_add_employee_project.html', error_message=error_message,
                                       projects=get_projects(), positions=get_positions(),
                                       generate_emp_proj_id=generate_emp_proj_id())

        except Exception as e:
            error_message = "Error adding employee project: {}".format(e)
            return render_template('n_add_employee_project.html', error_message=error_message, projects=get_projects(),
                                   positions=get_positions(), generate_emp_proj_id=generate_emp_proj_id())

        finally:
            connection.close()

    # Fetch project names and positions to populate the combo boxes
    projects = get_projects()
    positions = get_positions()
    # Render the template with project names, positions, and generated employee project ID
    return render_template('n_add_employee_project.html', projects=projects, positions=positions,
                           generate_emp_proj_id=generate_emp_proj_id())
#---- zan project ------

def generate_text_content(emp_id, period, gross_pay, total_deductions, net_pay):
    content = f"""BPB PLANNERS AND BUILDERS

            Period: {period}
            
            Employee ID: {emp_id}
            
            Gross: {gross_pay}
            
            Total Deductions: {total_deductions}
            
            Net: {net_pay}
            """
    return content

@app.route('/generate_payroll', methods=['POST'])
def generate_payroll():

    # Generate a unique payroll summary ID
    ps_id = generate_ps_id()
    # Get the current date and time
    date = datetime.now()
    # Format the date to display only YYYY-MM-DD
    formatted_date = date.strftime("%Y-%m-%d")

    # Extract data from the form submission
    emp_id = request.form['emp_id']
    basic_pay = float(request.form['basic_pay'])  # Convert to float
    equipment_deduction = float(request.form['eq_deductions'])  # Convert to float
    # statutory_deductions_type = request.form['statutory_deductions'] # Will be used soon
    statutory_deductions = float(request.form['statutory_deductions_input'])  # Convert to float
    allowance = float(request.form['allowance'])  # Convert to float
    period = request.form['period']

    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor()

    # Queries to fetch data from the database
    cursor.execute("SELECT pp_id FROM payroll_period WHERE period = ?", (period,))
    pp_id = cursor.fetchone()[0]
    print(pp_id)

    cursor.execute("SELECT Regular_Workday, OT_Regular_Workday FROM employee_payperiod_summary_view WHERE empID = ?", (emp_id,))
    data = cursor.fetchone()
    days_worked = data['Regular_Workday']
    total_ot = data['OT_Regular_Workday']

    # calculate net pay


    total_ot_salary = total_ot * (basic_pay / 8) * 1.25
    total_deductions = equipment_deduction + statutory_deductions
    total_allowance = allowance * days_worked + (total_ot * (allowance / 8 ))

    r_total_ot_salary = round(total_ot_salary, 2)
    r_total_deductions = round(total_deductions, 2)
    r_total_allowance = round(total_allowance, 2)



    gross_pay = basic_pay * days_worked + total_ot_salary + total_allowance
    r_gross_pay = round(gross_pay, 2)
    net_pay = r_gross_pay - r_total_deductions
    r_net_pay = round(net_pay, 2)


    # Insert the payroll data into the database
    cursor.execute(
        "INSERT INTO payslip (pay_slip_id, emp_id, pp_id, status_id, total_allowance, total_deductions, total_leave_pay, overtime, gross, net, receive_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (ps_id, emp_id, pp_id, 1, r_total_allowance, r_total_deductions, 0, r_total_ot_salary, r_gross_pay, r_net_pay,
         formatted_date))

    connection.commit()
    cursor.close()
    connection.close()

    text_content = generate_text_content(emp_id, period, gross_pay, total_deductions, net_pay)

    # Generate a unique filename
    filename = f"payslip_{ps_id}_{emp_id}.txt"

    # Specify the directory where you want to save the file
    directory = r"C:\Users\ADMIN\Desktop\python -payroll\payroll_1\payslip"

    # Write the content to the text file
    with open(os.path.join(directory, filename), "w") as f:
        f.write(text_content)

    return redirect(url_for('n_dashboard'))



@app.route('/process_payslip/<string:emp_id>', methods=['GET', 'POST'])
def process_payslip(emp_id):
    id = emp_id

    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch data for the employee from the database
    cursor.execute("SELECT * FROM employee_payperiod_summary_view WHERE empID = ?", (id,))
    payslip_data = cursor.fetchone()
    period = payslip_data['period']

    if payslip_data:

        statutory_deductions = get_statutory_deductions()

        # Extract relevant data from the payslip data
        regular_workday = payslip_data['Regular_Workday']
        ot_regular_workday = payslip_data['OT_Regular_Workday']

        # Calculate basic pay
        basic_pay = calculate_basic_pay(regular_workday, ot_regular_workday)

        # Perform further processing or return the result as needed
        return render_template('n_payroll.html', emp_id=id, period=period, basic_pay=basic_pay, statutory_deductions=statutory_deductions)
    else:
        return "Employee not found"  # Handle case when employee data is not found

def get_statutory_deductions():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM statutory_deductions")
    statutory_deductions = cursor.fetchall()
    connection.close()
    return statutory_deductions

#Calculate basic pay
def calculate_basic_pay(regular_workday, ot_regular_workday):
    base_wage = 427

    # Calculate OT salary for regular workdays
    ot_salary_regular_workday = (ot_regular_workday * (base_wage / 8)) * 1.25
    print(ot_salary_regular_workday)

    # Calculate total OT salary
    total_ot_salary = ot_salary_regular_workday
    print(total_ot_salary)

    # Calculate total working days
    total_working_days = regular_workday
    print(total_working_days)

    # Calculate basic pay
    pay = (base_wage * total_working_days ) + total_ot_salary

    basic_pay = round(pay, 2)

    return basic_pay


# Route to fetch employee payslip data
@app.route('/n_payslip')
def emp_slip_view():
    # Call a function to fetch data from the database
    payslip_rows = fetch_payslip_data()
    return render_template('n_payslip.html', payslip_rows=payslip_rows)


# Function to fetch payslip data from the database
def fetch_payslip_data():
    # Establish a connection to the database
    connection = get_db_connection()
    cursor = connection.cursor()

    # Execute the query to fetch data from the view
    cursor.execute("SELECT * FROM employee_payperiod_summary_view")

    # Fetch all rows from the result set
    payslip_rows = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Return the fetched data
    return payslip_rows

@app.route('/view_project/<string:project_id>', methods=['GET'])
def view_project(project_id):
    # Fetch data from the database based on the project ID
    # Example:
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT "
        "emp.empID, "
        "emp.empFName, "
        "emp.empLName, "
        "ep.emp_proj_id, "
        "pos.posName "
        "FROM employee emp "
        "JOIN employee_project ep ON emp.empID = ep.emp_id "
        "JOIN projectPosition pos ON ep.pos_Type = pos.posType "
        "WHERE ep.pr_id = ?", (project_id,))
    project_data = cursor.fetchall()

    connection.close()
    # Render the project_data.html template with the fetched data
    return render_template('n_project_data.html', project_data=project_data)

@app.route('/n_project_data')
def n_project_data():
    return render_template('n_project_data.html')

@app.route('/search_employee', methods=['POST'])
def search_employee():
    emp_name = request.form['emp_name']
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM employee WHERE empFName LIKE ? OR empLName LIKE ?",
                       ('%' + emp_name + '%', '%' + emp_name + '%'))
        employees = cursor.fetchall()
        return jsonify({'success': True, 'employees': [dict(row) for row in employees]})
    except Exception as e:
        return jsonify({'success': False, 'error_message': "Error searching employees: {}".format(e)})
    finally:
        connection.close()

#
@app.route('/n_emp_proj')
def index():
    projects = get_projects()
    return render_template('n_emp_proj.html', projects=projects)


# Function to fetch project names from the database
def get_projects():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT pr_id, pr_name FROM project")
    projects = cursor.fetchall()
    connection.close()
    return projects




# Function to fetch employees involved in a project DAN
def get_employees_in_project(project_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT emp.empID, emp.empFName, emp.empLName, ep.emp_proj_id,pp.posName \
                    FROM employee emp \
                    JOIN employee_project ep ON emp.empID = ep.emp_id \
                    JOIN projectPosition pp ON ep.pos_type = pp.posType \
                    WHERE ep.pr_id = ?", (project_id,))
    employees = cursor.fetchall()
    connection.close()
    return employees

# Add route to fetch employee details by ID
@app.route('/get_employee_details/<emp_id>')
def get_employee_details(emp_id):
    employee_details = fetch_employee_details(emp_id)
    return jsonify(employee_details)


# Function to fetch employee details from the database
def fetch_employee_details(emp_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT empID, empFName, empLName FROM employee WHERE empID = ?", (emp_id,))
    employee_details = cursor.fetchone()
    connection.close()
    return employee_details

@app.route('/n_attendance_project')
def n_attendance():
    print("n_attendance_project")
    periods = get_payroll_periods()  # Call the function to fetch payroll periods
    return render_template('n_attendance_project.html', payrollPeriods=periods)

# Route to handle the search for timecard dates for a selected payroll period
@app.route('/search_payroll_periods', methods=['POST'])
def search_payroll_periods():
    payroll_period_id = request.form.get('payrollPeriod')
    print(payroll_period_id)
    timecard_dates = get_timecard_dates_for_period(payroll_period_id)
    return render_template('n_attendance_project.html', projects=get_projects(), employees=get_employees(),
                           payrollPeriods=get_payroll_periods(), timecardDates=timecard_dates)

@app.route('/insert_timestamp', methods=['POST'])
def calculate_hours():
    try:
        # SET
        connection = get_db_connection()
        cursor = connection.cursor()

        # Generate a unique timestamp ID
        ts_id = generate_ts_id()

        # Retrieve the timecard ID for the selected date
        date_form = request.form['timecard']
        date = datetime.strptime(date_form, "%Y-%m-%d").date()
        cursor.execute("SELECT tc_id FROM timecard_period WHERE tc_date = ?", (date,))
        tc_id_result = cursor.fetchone()
        if tc_id_result:
            tc_id = tc_id_result[0]
        else:
            # Handle the case where no timecard ID is found for the selected date
            raise ValueError("No timecard ID found for the selected date")

        # Retrieve form data
        EPRID = request.form['emp_proj_id']
        am_in = request.form['amIn']
        am_out = request.form['amOut']
        pm_in = request.form['pmIn']
        pm_out = request.form['pmOut']

        # Parse start and end time strings into datetime objects
        am_start = datetime.strptime(am_in.strip(), '%H:%M')
        am_end = datetime.strptime(am_out.strip(), '%H:%M')
        pm_start = datetime.strptime(pm_in.strip(), '%H:%M')
        pm_end = datetime.strptime(pm_out.strip(), '%H:%M')

        # Calculate the duration in hours
        am_duration = (am_end - am_start).total_seconds() / 3600
        pm_duration = (pm_end - pm_start).total_seconds() / 3600

        if pm_duration > 3:
            ovt = pm_duration - 3
            ot = round(ovt, 2)
            total_hours = (am_duration + pm_duration) - ovt
        else:
            ot = 0
            total_hours = am_duration + pm_duration

        total = round(total_hours, 2)

        # Insert timestamp data into the database
        cursor.execute(
            "INSERT INTO timestamp (ts_id, tc_id, emp_proj_id, am_in, am_out, pm_in, pm_out, total, ot, present) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (ts_id, tc_id, EPRID, am_in, am_out, pm_in, pm_out, total, ot, "YES"))

        connection.commit()
        return render_template('n_attendance_project.html')

    except Exception as e:
        # Handle errors gracefully
        error_message = f"Error inserting timestamp data: {str(e)}"
        print(error_message)  # Log the error message
        return render_template('n_attendance_project.html', error_message=error_message)

    finally:
        # Always close the connection in the finally block
        if connection:
            connection.close()


# Function to fetch employees from the database
def get_employees():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT empID, empFName, empLName FROM employee")
    employees = cursor.fetchall()
    connection.close()
    return employees


# Function to fetch timecard dates for a selected payroll period from the database
def get_timecard_dates_for_period(payroll_period_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT tc_date FROM timecard_period WHERE pp_id = ?", (payroll_period_id,))
    timecard_dates = [record[0] for record in cursor.fetchall()]
    connection.close()
    return timecard_dates


# Function to fetch payroll periods from the database
def get_payroll_periods():
    print("get_payroll_periods")
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT pp_id, period FROM payroll_period")
    payroll_periods = cursor.fetchall()
    connection.close()
    return payroll_periods

# Route to handle the AJAX request for getting emp_proj_id
@app.route('/get_emp_proj_id', methods=['POST'])
def get_emp_proj_id():
    emp_id = request.form.get('emp_id')
    emp_proj_id = fetch_emp_proj_id(emp_id)
    return jsonify({'emp_proj_id': emp_proj_id})

# Function to fetch emp_proj_id from the database
def fetch_emp_proj_id(emp_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT emp_proj_id FROM employee_project WHERE emp_id = ?", (emp_id,))
        emp_proj_id = cursor.fetchone()[0] if cursor.rowcount > 0 else None
    except Exception as e:
        print(f"Error fetching emp_proj_id: {e}")
        emp_proj_id = None
    finally:
        connection.close()
    return emp_proj_id

@app.route('/n_payslip')
def n_payslip():
    return render_template('n_payslip.html')

# Timecard and Calendar
@app.route('/dates')
def view_dates():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT "
        "t.tc_id, "
        "d.day_name, "
        "t.tc_date "
        "FROM timecard_period t "
        "JOIN day d ON t.day_type = d.day_type"
    )

    timecard_periods = cursor.fetchall()  # Fetch all rows from the query result
    connection.close()
    return render_template('n_dates.html', timecard_periods=timecard_periods)


@app.route('/edit_day/<string:tc_id>', methods=['GET'])
def edit_day_func(tc_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM timecard_period WHERE tc_id = ?", (tc_id,))
    date = cursor.fetchone()
    day = get_day_type()
    return render_template('n_edit_day.html', day=day, date=date)

def get_day_type():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM day")
    day = cursor.fetchall()
    return day


@app.route('/update_timecard_day', methods=['POST'])
def update_timecard_day():
    # Extract data from the form
    tc_id = request.form['tc_id']
    day_type = request.form['day_type']

    # Update the row in the database
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE timecard_period SET day_type = ? WHERE tc_id = ?", (day_type, tc_id))
    connection.commit()
    connection.close()

    # Redirect to a success page or another route
    return redirect(url_for('view_dates'))



if __name__ == '__main__':
    app.run(debug=True)
