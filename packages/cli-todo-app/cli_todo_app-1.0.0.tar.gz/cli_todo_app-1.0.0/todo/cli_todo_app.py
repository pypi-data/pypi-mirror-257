from datetime import date
from os.path import exists, expanduser, join
from shelve import open
from os import chdir as change_directory, makedirs as make_directory
from typing import Union
from colorama import Fore, Back, Style
from getpass import getpass

TODO_FILE = ".todo"
DONE_FILE = ".done"
SETTINGS_FILE = ".settings"
TODO_FOLDER = ".cli-todo-app"
HOME_DIR = expanduser("~")
TODO_DIR = join(HOME_DIR, TODO_FOLDER)

BRIGHT_YELLOW = Style.BRIGHT + Fore.YELLOW
BRIGHT_GREEN = Style.BRIGHT + Fore.GREEN
BRIGHT_RED = Style.BRIGHT + Fore.LIGHTRED_EX
BRIGHT_CYAN = Style.BRIGHT + Fore.LIGHTCYAN_EX
BRIGHT_MAGENTA = Style.BRIGHT + Back.MAGENTA + Fore.LIGHTGREEN_EX
RESET = Style.RESET_ALL


def __read_file(filename) -> dict:
    with open(filename) as _file:
        data = dict(_file)
    return data


def __write_file(filename, index=None, data=None, remove=False) -> Union[str, None]:
    with open(filename) as _file:
        if remove:
            return _file.pop(index)
        _file[index] = data


def __get_current_date():
    return date.today().strftime("%Y-%m-%d")


def __upload_files(user):
    if user.find(TODO_FILE):
        print(user.delete(TODO_FILE[0]))
    if user.find(DONE_FILE):
        print("found")
        user.delete(DONE_FILE[0])


def prepare_report(todo, done) -> str:
    date = done[0].split()[1]
    report = "{0} Pending : {1} Completed : {2}".format(date, len(todo), len(done))
    return report


def display_all_commands():
    print(
        f"""
$./todo {BRIGHT_MAGENTA}add "todo item"{RESET}  # Add a new todo
$./todo {BRIGHT_MAGENTA}ls{RESET}               # Show remaining todos
$./todo {BRIGHT_MAGENTA}del NUMBER {RESET}      # Delete a todo
$./todo {BRIGHT_MAGENTA}done NUMBER{RESET}      # Complete a todo
$./todo {BRIGHT_MAGENTA}help{RESET}             # Show usage
$./todo {BRIGHT_MAGENTA}settings{RESET}         # Settings
$./todo {BRIGHT_MAGENTA}push{RESET}             # Save todos to cloud
$./todo {BRIGHT_MAGENTA}report{RESET}           # Statistics"""
    )


def display_pending_tasks() -> None:
    todos = sorted(
        __read_file(TODO_FILE).items(), reverse=SETTINGS.get("last_entry_top", True)
    )
    for index, todo in todos:
        date, todo = todo.get("Entry Date"), todo.get("Todo")
        print(f"[{index}] {BRIGHT_YELLOW}{date} {BRIGHT_GREEN}{todo}{RESET}")


def add(task) -> None:
    todo = __read_file(TODO_FILE)
    last_index = "{0}".format(int(max(list("0" if not todo else todo.keys()))) + 1)
    __write_file(
        TODO_FILE, last_index, data={"Entry Date": __get_current_date(), "Todo": task}
    )
    print(f"{BRIGHT_GREEN}Added:{BRIGHT_YELLOW}{task}{RESET}")


def delete_task(index) -> None:
    try:
        __write_file(TODO_FILE, index, remove=True)
        print(f"{BRIGHT_GREEN}Deleted{BRIGHT_CYAN} todo #{index}.{RESET}")
    except KeyError:
        print(
            f"{BRIGHT_RED}Error:{BRIGHT_YELLOW} todo #{index} does not exist. Nothing deleted.{RESET}"
        )


def mark_done(index) -> None:
    try:
        done_date = __get_current_date()
        removed_todo = __write_file(TODO_FILE, index, remove=True)
        __write_file(
            DONE_FILE, index, data={"Completed Date ": done_date, **removed_todo}
        )
        print(f"{BRIGHT_GREEN}Marked{BRIGHT_CYAN} todo #{index} as done.{RESET}")
    except KeyError:
        print(f"{BRIGHT_RED}Error:{BRIGHT_YELLOW} todo #{index} does not exist.{RESET}")


def display_settings():
    settings = __read_file(SETTINGS_FILE)
    for setting, value in settings:
        print(f"{BRIGHT_GREEN}{setting}{BRIGHT_YELLOW} :  {value}{RESET}")


def save_to_cloud():
    email = input("Enter email-id : ")
    password = getpass("Enter password : ")
    cloud.login(email, password)
    if not (cloud.find(TODO_FILE) and cloud.find(DONE_FILE)):
        cloud.delete(cloud.find(TODO_FILE)[0])
        cloud.delete(cloud.find(DONE_FILE)[0])
    cloud.upload(TODO_FILE)
    cloud.upload(DONE_FILE)


def display_report():
    pending_tasks = __read_file(TODO_FILE)
    done_tasks = __read_file(DONE_FILE)
    # report = prepare_report(pending_tasks, done_tasks)
    print(pending_tasks)
    print(done_tasks)
    # print(report)


def incorrect_argument(argument):
    print(f"{BRIGHT_RED}Incorrect argument passed, unknown option `{argument}`{RESET}")


def display_logo():
    print(
        """
  ______ _ _                  _                            
 / _____) (_)   _            | |                           
| /     | |_   | |_  ___   _ | | ___      ____ ____  ____  
| |     | | |  |  _)/ _ \ / || |/ _ \    / _  |  _ \|  _ \ 
| \_____| | |  | |_| |_| ( (_| | |_| |  ( ( | | | | | | | |
 \______)_|_|   \___)___/ \____|\___/    \_||_| ||_/| ||_/ 
                                              |_|   |_|    """
    )
    print("App Initialized")


try:
    if not exists(TODO_DIR):
        make_directory(TODO_DIR)
        display_logo()
    change_directory(TODO_DIR)
    with open(TODO_FILE) as todo:
        pass
    with open(DONE_FILE) as done:
        pass
    with open(SETTINGS_FILE) as settings_file:
        SETTINGS = dict(settings_file)
except Exception as e:
    print(f"{BRIGHT_RED}Error: {BRIGHT_YELLOW}{e}{RESET}")
