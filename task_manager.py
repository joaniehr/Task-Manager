from datetime import date
from _datetime import datetime


def reg_user():
    # creates blank lists to store usernames
    usernames = []

    # opens user text file and appends to username list
    with open("user.txt", "r") as file:
        # appends usernames to username list
        for i in file:
            user_details = i.strip().split(", ")
            usernames.append(user_details[0])

        # continues to prompt user for new username until they enter something not already in user.txt
        while True:
            new_user = input("Please enter new username: ")
            if new_user in usernames:
                print("User already exists.")
            else:
                break

    new_pass = input("Please create a new password: ")
    pass_check = input("Please confirm your password: ")

    # checks if passwords match, if not requests confirmation again
    while new_pass != pass_check:
        print("Passwords do not match.")
        pass_check = input("Please confirm password: ")

    # appends new user info to user.txt
    with open("user.txt", "a") as file:
        file.write(f"\n{new_user}, {new_pass}")

    print("User registration complete.\n")


def add_task():
    # gets user input for required task fields
    user_assign = input("Please enter the username you wish to assign the task to: ")
    task_title = input("What is the title of the task? ")
    description = input("Please enter a description of the task: ")
    due_date = input("What is the due date of the task? ")
    today = input("Please enter today's date: ")

    # writes user input to task file
    with open("tasks.txt", "a") as task_file:
        task_file.write(f"\n{user_assign}, {task_title}, {description}, {due_date}, {today}, No")

    print("Task added.\n")


def view_all():
    # opens tasks file in read mode
    with open("tasks.txt", "r") as task_file:
        for i in task_file:
            task_list = i.split(", ")
            # prints all tasks in readable way
            print(f"""Username: {task_list[0]}
    Task name: {task_list[1]}
    Task description: {task_list[2]}
    Due date: {task_list[3]}
    Date assigned: {task_list[4]}
    Completed? {task_list[5]}\n""")


def view_mine():
    # opens tasks file in read mode
    with open("tasks.txt", "r") as task_file:
        for count, i in enumerate(task_file):
            task_list = i.split(", ")
            # checks username of user and uses this to print their individual tasks
            if task_list[0] == username:
                print(f"""Task {count+1}:
    Username: {task_list[0]}
    Task name: {task_list[1]}
    Task description: {task_list[2]}
    Due date: {task_list[3]}
    Date assigned: {task_list[4]}
    Completed? {task_list[5]}\n""")


def statistics():
    gen_report()

    with open("task_overview.txt", "r") as file:
        for i in file:
            print(i, end="")
        print()

    with open("user_overview.txt", "r") as file:
        for i in file:
            print(i, end="")
        print()


def task_report():
    # opens task file in read mode to access data, gets numbers of tasks
    with open("tasks.txt", "r") as file:
        tasks = len(file.readlines())
        file.seek(0)

        # finds number of complete and incomplete tasks
        complete = 0
        incomplete = 0
        overdue = 0
        for i in file:
            task = i.strip().split(", ")
            if task[5].lower() == "yes":
                complete += 1
            elif task[5].lower() == "no":
                incomplete += 1

            due_date = task[3].strip()

            due_date = datetime.strptime(due_date, '%d %b %Y')

            if due_date < datetime.today() and task[5].lower() == "no":
                overdue += 1

        # calculates percentages of incomplete and overdue tasks
        perc_incomplete = incomplete / tasks * 100
        perc_overdue = overdue / tasks * 100

    # writes information to task overview in readable style
    with open("task_overview.txt", "w") as task_overview:
        task_overview.write(f"""Task Overview:
    Total number of tasks recorded: {tasks}
    Total number of completed tasks: {complete}
    Total number of incomplete tasks: {incomplete}
    Total number of incomplete overdue tasks: {overdue}
    Percentage of tasks incomplete: {perc_incomplete:.2f}%
    Percentage of tasks overdue: {perc_overdue:.2f}%
    """)


def user_report():
    with open("tasks.txt", "r") as file:
        num_tasks = len(file.readlines())

    with open("user.txt", "r") as file:
        num_users = len(file.readlines())
        user_list = []

        file.seek(0)
        for i in file:
            usernames = i.strip().split(", ")
            user_list.append(usernames[0])

        with open("user_overview.txt", "w") as user_overview:
            user_overview.write(f"""User Overview:
    Total number of users: {num_users}
    Total numbers of tasks recorded: {num_tasks}
    """)

    with open("tasks.txt", "r") as task_file:
        tasks = task_file.readlines()

        for user in user_list:
            user_tasks = 0
            complete = 0
            incomplete = 0
            overdue = 0
            for i in tasks:
                task = i.strip().split(", ")
                if user in i:
                    user_tasks += 1

                    if user in i and task[5].lower() == "yes":
                        complete += 1

                    elif user in i and task[5].lower() == "no":
                        incomplete += 1

                    due_date = task[3].strip()

                    due_date = datetime.strptime(due_date, '%d %b %Y')

                    if due_date < datetime.today() and task[5].lower() == "no":
                        overdue += 1

            if user_tasks == 0:
                perc_comp = 0
            else:
                perc_comp = complete/user_tasks*100

            if user_tasks == 0:
                perc_total = 0
            else:
                perc_total = user_tasks/num_tasks*100

            if user_tasks == 0:
                perc_incomp = 0
            else:
                perc_incomp = incomplete/user_tasks*100

            if user_tasks == 0:
                perc_overdue = 0
            else:
                perc_overdue = overdue/user_tasks*100

            with open("user_overview.txt", "a") as f:
                f.write(f"""\nUser: {user}
    Total tasks assigned: {user_tasks}
    Percentage of total tasks: {perc_total:.2f}%
    Percentage of tasks completed: {perc_comp:.2f}%
    Percentage of tasks still to be completed: {perc_incomp:.2f}%
    Percentage of overdue tasks: {perc_overdue:.2f}%
    """)


def gen_report():
    # generates tasks and user reports, creates text files for each
    task_report()
    user_report()

    print("Reports generated.\n")


def edit_item(x):
    complete = input(f"You have selected task {x}. Would you like to mark this task as complete? ").lower()
    if complete == "yes":
        with open("tasks.txt") as file:
            task_list = []
            for i in file:
                task_list.append(i.strip().split(", "))

            task_list[int(x)-1][5] = "Yes"

            with open("tasks.txt", "w") as new_file:
                for i in task_list:
                    tasks = ", ".join(i) + "\n"

                    new_file.write(tasks)
    else:
        edit_num = input(f"""What would you like to edit?
1. Due Date
2. User assignment\n""")
        while edit_num != "1" and edit_num != "2":
            print("Invalid input.")
            edit_num = input(f"""What would you like to edit?
1. Due Date
2. User assignment\n""")

        if edit_num == "1":
            due = input("Please enter new due date: ")
            with open("tasks.txt") as file:
                task_list = []
                for i in file:
                    task_list.append(i.strip().split(", "))

                task_list[int(x) - 1][3] = due

                with open("tasks.txt", "w") as new_file:
                    for i in task_list:
                        tasks = ", ".join(i) + "\n"

                        new_file.write(tasks)

        else:
            user_assign = input("Please enter new user assignment: ")
            with open("tasks.txt") as file:
                task_list = []
                for i in file:
                    task_list.append(i.strip().split(", "))

                task_list[int(x) - 1][0] = user_assign

                with open("tasks.txt", "w") as new_file:
                    for i in task_list:
                        tasks = ", ".join(i) + "\n"

                        new_file.write(tasks)


# ====Login Section====
# gets username from user
username = input("Please enter your username: ")

# creates blank lists to store usernames and passwords
username_list = []
password_list = []

with open("user.txt", "r") as user_file:
    # appends usernames to username list and passwords to password list
    for line in user_file:
        user_info = line.strip().split(", ")
        username_list.append(user_info[0])
        password_list.append(user_info[1])

    # checks if username is in list
    while username not in username_list:
        print("Invalid username.")
        username = input("Please enter your username: ")

    username_location = username_list.index(username)

    password = input("Please enter your password: ")

    # checks if password matches password of username in same list position
    while password != password_list[username_location]:
        print("Invalid passcode.")
        password = input("Please enter your password: ")

    print("Access granted!")


while True:
    if username == "admin":
        # presenting the menu to the admin with additional statistics option and
        # making sure that the user input is converted to lower case.
        menu = input('''Select one of the following Options below:
    r - Register User
    a - Add Task
    va - View All Tasks
    vm - View My Tasks
    s - Statistics
    gr - Generate Report
    e - Exit
    ''').lower()
    else:
        # presenting the menu to the user and
        # making sure that the user input is converted to lower case.
        menu = input('''Select one of the following options below:
    r - Register User
    a - Add Task
    va - View All Tasks
    vm - View My Tasks
    e - Exit
    ''').lower()

    if menu == 'r':
        if username == "admin":
            reg_user()
        else:
            print("Account registration is limited to admin accounts. Please choose another option.\n")

    elif menu == "a":
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()
        edit = input("Enter the task number you would like to edit, or enter -1 to return to main menu: ")
        if edit != "-1":
            edit_item(edit)

    # exits programme
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    # runs statistics function
    elif menu == "s" and username == "admin":
        statistics()

    # runs report function
    elif menu == "gr" and username == "admin":
        gen_report()

    # prints error message
    else:
        print("Invalid menu option. Please try again.")
