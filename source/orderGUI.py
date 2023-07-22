import tkinter as tk
import json
from orderBackend import *
from functools import partial

"""
This python file handles the GUI portion of the app
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!This file needs to be on the same level as orderBackend.py and cafeMenu.yml!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""


# Create the top level GUI
topLevelGUI = tk.Tk()

# Set the size of the window
topLevelGUI.geometry("700x350")


# Define a function for switching the frames
def change_to_admin(topLevelGUI):
    """Change the window to admin window"""
    topLevelGUI.destroy()
    admin = tk.Tk()
    admin.geometry("700x350")
    admin.title("管理员选项")
    # Create a Label in New window
    login_screen(admin, "admin")
    admin.mainloop()


def change_to_user(topLevelGUI):
    """Change the window to user window"""
    topLevelGUI.destroy()
    user = tk.Tk()
    user.geometry("700x350")
    user.title("操作员选项")
    # Create a Label in New window
    login_screen(user, "user")


def login_screen(master_window: tk, typeOfOperator: str):
    """GUI for login

    Args:
        master_window (tk): The previous window
        typeOfOperator (str): admin or user
    """
    # username label and text entry box
    usernameLabel = tk.Label(master_window, text="姓名:")
    usernameLabel.pack()
    usernameEntry = tk.Entry(master_window)
    usernameEntry.pack()

    # password label and password entry box
    passwordLabel = tk.Label(master_window, text="Password:")
    passwordLabel.pack()
    passwordEntry = tk.Entry(master_window, show="*")
    passwordEntry.pack()

    # login button
    loginButton = tk.Button(
        master_window,
        text="Login",
        command=lambda: login(
            usernameEntry.get(), passwordEntry.get(), master_window, typeOfOperator
        ),
    )
    loginButton.pack()
    master_window.mainloop()


def login(username, password, master_window, typeOfOperator):
    """validate the login with username and password

    Args:
        username (str): username
        password (str): password
        master_window (tk): THe previous window
        typeOfOperator (str): admin or user
    """
    # Here, you can perform further validation or authentication logic
    validate = validateLogin(username, password)
    if validate:
        optionGUI(master_window, typeOfOperator, username)
    else:
        # TODO: Implement warning here
        pass


def optionGUI(master_window, typeOfOperator, username):
    """Opens the options GUI. The options available depends on the type of operator

    Args:
        master_window (tk): The previous window
        typeOfOperator (str): admin or user
    """
    master_window.destroy()
    option_window = tk.Tk()
    option_window.geometry("700x350")
    option_window.title("用户选项")
    # Create buttons
    orderButton = tk.Button(
        option_window,
        text="点菜",
        command=lambda: order(option_window, username),
    )
    orderButton.pack()
    if typeOfOperator == "admin":
        modifyMenuButton = tk.Button(
            option_window,
            text="菜单维护",
            command=lambda: modifyMenu(option_window),
        )
        modifyMenuButton.pack()
        monthlyStatisticButton = tk.Button(
            option_window,
            text="月统计",
            command=lambda: getStatistics(option_window, "monthly"),
        )
        monthlyStatisticButton.pack()
        yearlyStatisticButton = tk.Button(
            option_window,
            text="年统计",
            command=lambda: getStatistics(option_window, "yearly"),
        )
        yearlyStatisticButton.pack()
        modifyUserButton = tk.Button(
            option_window,
            text="操作员管理",
            command=lambda: modifyUser(option_window),
        )
        modifyUserButton.pack()
    if typeOfOperator == "user":
        changePasswordButton = tk.Button(
            option_window,
            text="修改密码",
            command=lambda: changePassword(option_window),
        )
        changePasswordButton.pack()
    option_window.mainloop()


def order(master_window, user_name):
    """Shows the current menu and allows user/admin to order

    Args:
        master_window (tk): The previous window
        user_name (str): The name for the person ordering
    """

    data = getMenuData()
    master_window.destroy()
    order_window = tk.Tk()
    order_window.title("点菜")

    # Make the rows and columns of the main window resizable
    order_window.grid_rowconfigure(0, weight=1)
    order_window.grid_columnconfigure(0, weight=1)

    # Create a canvas widget
    canvas = tk.Canvas(order_window)
    canvas.grid(row=0, column=0, sticky="nsew")

    # Create a frame to hold the labels
    frame = tk.Frame(canvas)

    def on_configure(event):
        # Update the canvas scroll region to show the entire content
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_scroll(*args):
        # This function will be called whenever the scrollbar is moved.
        # It updates the x-scrollview of the canvas.
        canvas.xview(*args)

    # Construct Menu into a list data structure in the format of [{catagory:<catagory_name>, dishes:<dishes_names>},...]
    for index, category in enumerate(data):
        # Construct first row
        general_id_label_name = tk.Label(frame, text="序号", font=("Arial", 16, "bold"))
        general_id_label_name.grid(row=0, column=index * 4, padx=10, pady=10)
        general_name_label_name = tk.Label(
            frame, text="类别或菜名", font=("Arial", 16, "bold")
        )
        general_name_label_name.grid(row=0, column=index * 4 + 1, padx=10, pady=10)
        general_price_label_name = tk.Label(
            frame, text="单价（元）", font=("Arial", 16, "bold")
        )
        general_price_label_name.grid(row=0, column=index * 4 + 2, padx=10, pady=10)
        general_num_order_label_name = tk.Label(
            frame, text="份数", font=("Arial", 16, "bold")
        )
        general_num_order_label_name.grid(row=0, column=index * 4 + 3, padx=10, pady=10)

        # Construct second row
        id_label = tk.Label(frame, text=category, font=("Arial", 16, "bold"))
        id_label.grid(row=1, column=index * 4, padx=10, pady=10)
        name_label = tk.Label(
            frame, text=data[category]["name"], font=("Arial", 16, "bold")
        )
        name_label.grid(row=1, column=index * 4 + 1, padx=10, pady=10)
        price_label = tk.Label(frame, text=None)
        price_label.grid(row=1, column=index * 4 + 2, padx=10, pady=10)
        num_order_label = tk.Label(frame, text=None)
        num_order_label.grid(row=1, column=index * 4 + 3, padx=10, pady=10)

        # Construct items
        starting_row = 2
        item_lst = []
        for item in data[category]["items"]:
            item_id_label = tk.Label(frame, text=item["id"], font=("Arial", 10))
            item_id_label.grid(row=starting_row, column=index * 4, padx=10, pady=10)
            item_name_label = tk.Label(frame, text=item["name"], font=("Arial", 10))
            item_name_label.grid(
                row=starting_row, column=index * 4 + 1, padx=10, pady=10
            )
            item_price_label = tk.Label(frame, text=item["price"], font=("Arial", 10))
            item_price_label.grid(
                row=starting_row, column=index * 4 + 2, padx=10, pady=10
            )
            num_order = tk.Entry(frame)
            num_order.grid(row=starting_row, column=index * 4 + 3, padx=10, pady=10)
            starting_row += 1
            item_lst.append(
                {
                    "category_name": data[category]["name"],
                    "dish_name": item["name"],
                    "dish_price": item["price"],
                    "num_order": num_order,
                }
            )

    # Make the columns of the main window resizable
    for i in range(len(data) * 4):
        frame.grid_columnconfigure(i, weight=1)

    # Bind the canvas to update the scroll region when resized
    canvas.bind("<Configure>", on_configure)

    # Add the frame to the canvas
    canvas.create_window((0, 0), window=frame, anchor="nw")

    # Create a button right above the scrollbar and make it stay in the middle
    button = tk.Button(order_window, text="确认订餐")
    button.grid(row=1, column=0, sticky="ew")

    # Create a horizontal scrollbar
    scrollbar = tk.Scrollbar(order_window, orient=tk.HORIZONTAL, command=on_scroll)
    scrollbar.grid(row=2, column=0, sticky="ew")

    # Configure the canvas to use the scrollbar
    canvas.configure(xscrollcommand=scrollbar.set)

    # Configure the frame to use the scrollbar
    order_window.mainloop()


def modifyMenu(master_window):
    """Shows the current menu and allows admin to add or remove or modify dishes

    Args:
        master_window (tk): The previous window
    """
    pass


def getStatistics(master_window, frequency):
    """Get the <frequency> statistics

    Args:
        master_window (tk): The previous window
        frequency (str): month or yearly
    """
    pass


def modifyUser(master_window):
    """Allows admin to remove/add users

    Args:
        master_window (tk): The previous window
    """
    pass


def changePassword(master_window):
    """Allows user to change their password

    Args:
        master_window (tk): The previous window
    """
    pass


# Create buttons to select type of operator in a new window
# TODO: Create usertype button class
admin_button = tk.Button(
    topLevelGUI,
    text="管理员选项",
    height=5,
    width=10,
    command=lambda: change_to_admin(topLevelGUI),
).grid(row=0, column=1, padx=100, pady=80)
user_button = tk.Button(
    topLevelGUI,
    text="操作员选项",
    height=5,
    width=10,
    command=lambda: change_to_user(topLevelGUI),
).grid(row=0, column=2, padx=100, pady=80)

topLevelGUI.mainloop()
