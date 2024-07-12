import os
import time
from pathlib import Path
import in_place
from copy import deepcopy
# Foundation for "to-do list":
# Have at least one list available to any one user ( >= 1 )
# The lists data needs to be saved in a .txt file
# There should be a folder for each user and an N amount of files(lists) that a user has made
# The lists can be read and edited
    # If the list file is empty, it will be deleted
# Format the list (it can't be just a single continous line of text, it needs to be structured)

# Each list should contain a:
    # - Title(to use as the file name)
    # - Content

# Need to load in all the lists of any existing users(if there are any)
# Do this before asking for any user input
# This will help go through less actions and save time(albeit very little, but we love a little challenge)

class List:
    def __init__(self, title: str, owner: str, content: str, file_path: str, make_with_user: bool) -> None:
        self.owner = owner
        self.title = title
        self.location = file_path
        # Check if we make a List object during User creation, or when loading existing user data
        if make_with_user:
            # The full path to the folder of lists will be the path that is given + the name of the person who's making it
            self.full_path = f'{self.location}\\{self.owner}'
            list_path = f'{self.full_path}\\{self.title}'
            # Make the directory using user given "title" string
            # Check if the directory already exists
            my_dir = Path(f'{self.full_path}')

            if not my_dir.is_dir():
                os.mkdir(f'{self.full_path}')
            
            try:
                # check if the list you're looking for exists
                assert Path(f'{list_path}').is_file(), 'File path already exists'
            except AssertionError:
                # open the list for writing, if it already exists
                self.add_item(list_path, content, 'x')
                print('List created successfully')
            else:
                # make a write to the list, if it doesn't exist
                self.add_item(list_path, content, 'a')
                print('Items added successfully')


    def add_item(self, list_path: str, content: str, action: str):
        # Content strucutre:
        # "-str-str-str"...
        formatted_content = []
        formatted_content.extend("\n- ".join(content.split('-')))
        with open(f'{list_path}.txt', action) as file:
            if action == 'x':
                file.write(f'{list_path.split('\\')[-1]} list:')
            file.writelines(formatted_content)

    def read_list(self, list_path):
        with open(f'{list_path}.txt', 'r') as file:
            content = file.read()
            print("List contents:")
            print('(empty)') if content == '' else print(content)

    def edit_list(self, list_path: str, remove_content: str, substitute_content: str) -> None:
        # 
        edit_list_dict = {}
        # Make arrays from strings passed, to fill a hash table
        remove_items = [r for r in remove_content.split('-')]
        substitute_items = [r for r in substitute_content.split('-')]
        # Populate the hash table
        # if removable content is len == 1, then replacement content goes in the place of that one item
        # if sub_content len == 1 and remove_content is more, then substitues all removes with that one item
        # any other mismatch = don't edit and produce an error message
        if len(remove_items) == len(substitute_items):
        # if removable content and replacement content is equal amounts, replace everything in order
            for i in range(len(remove_items)):
                # map keys to replaceable item names and values to substitute item names
                edit_list_dict[remove_items[i]] = substitute_items[i]
            with in_place.InPlace(f'{list_path}.txt') as file:
                # get file content
                get_content = file.read()
                # get all items from file
                split_content_items: list = [f'\n- {item[:-1]}' if '\n' in item else f'\n- {item}' for item in get_content.split('- ')[1:]]
                # make a copy whose elements we'll change and write to file
                content_items_copy = deepcopy(split_content_items)
                # go through hash table and find values
                for key, value in edit_list_dict.items():
                    for i in range(len(split_content_items)):
                        if key == split_content_items[i][3:]:
                            # make changes to copy that's gonna get written into the file
                            content_items_copy[i] = f'\n- {value}'
                file.write(f'{list_path.split('\\')[-1]} list:')
                file.writelines(content_items_copy)
# -------------------------- Some words get lost along the way, it probably has something to do with non-last words having an 
# -------------------------- "\n- " in the front of the word, when the final array gets made



class User:
    def __init__(self, name):
        self.user_lists = []
        self.name = name

    def create_list(self, title, owner, content, file_path):
        # Every time a new List is made for the User instance, add it to it's list of lists
        new_list = List(title, owner, content, file_path, make_with_user=True)
        self.user_lists.append(new_list)


    def get_lists(self):
        if len(self.user_lists) == 0:
            print("No lists available for this user")
            return
        print("Available Lists:")
        for list in self.user_lists:
            print(f"\t- {list.title}")

def load_users(file_path):
    # We'll run this before asking the user anything during user input
    # to check what lists they already have - 09.07.24

    # Thought about it the next day... this will be harder than I thought
    # but I still want to attempt it - 10.07.24

    # I'll assume all user folders are stored in one place
    # and make User instances based on folders and files found
    # then I append all of the List instances a user has to the appropriate User instance
    user_info = {}
    for (dir_path, sub_folder, files) in os.walk(file_path):
        for folder in sub_folder:
            if folder.isalnum():
                files_in_folder = os.listdir(f'{dir_path}\\{folder}')
                user_info[folder] = User(folder)
                for file in files_in_folder:
                    with open(f'{dir_path}\\{folder}\\{file}', 'r') as doc:
                        list_content = doc.read()
                        # We pass "file[:-4] to get rid of the ".txt" portion of the string
                        # because the user input is purely the name of the list e.g. "blabla", not "blabla.txt"
                        user_info[folder].user_lists.append(List(file[:-4], folder, list_content, dir_path, make_with_user=False))

        return user_info

if __name__ == "__main__":
    running = True
    users_file_path = input("Hello! Enter file path with existing lists, or a new one:\n")
    print('What do you want to do next?')
    while running:
        # Load user data every time an action is done

        # This should be changed later on to only update 
        # if there is any additional data the user passed
        existing_users = load_users(users_file_path)
        try:
            user_input = input('Make a new list(M), Add to an existing list(A),\nRead one of your lists(R), or edit a list(E): ').upper()
            assert user_input in ['M', 'A', 'R', 'E']
        except: 
            print('Wrong input!\nThe answer must be one of the capital letters provided in the parentheses')
            time.sleep(2)
            os.system('cls')
            continue
        else:
            # Things we need to get to a list(file):
            #   - Name of user
            #   - Title of list
            #   - File path
            match user_input:
                case 'M':
                    user_name = input('What directory(folder) name do you want your list to be under?\n(a valid folder name is alphanumeric(no special characters)): ').lower()
                    list_title = input('Choose what is going to be the title of your list: ').lower()
                    user_content = input("What do you want to write in your list?\n(follow the format '-item-item-item...', the dash is used as a seperator):\n")
                    if not Path(users_file_path).is_dir():
                        print(f"Couldn't find path: {users_file_path}\nUsing current directory instead...")
                        users_file_path = os.curdir
                    new_user = User(user_name)
                    new_user.create_list(list_title, user_name, user_content, users_file_path)
                case 'A':
                    # Add items to an existing list
                    user_name = input('What directory(folder) name do you want your list to be under?\n(a valid folder name is alphanumeric(no special characters)): ').lower()
                    try:
                        # Check if user exists
                        assert Path(f'{users_file_path}\\{user_name}').is_dir()
                    except AssertionError as e:
                        print("Folder doesn't exist")
                        print(e)
                    try:
                        list_title = input('Choose what is going to be the title of your list: ').lower()
                        full_file_path = f'{users_file_path}\\{user_name}\\{list_title}'
                        has_list = False
                        # Check if file exists for given user
                        for user_list in existing_users[user_name].user_lists:
                            if user_list.title == list_title:
                                has_list = True
                                active_user_list = user_list
                        user_content = input("What do you want to write in your list?\n(follow the format '-item-item-item...', the dash is used as a seperator):\n")
                        active_user_list.add_item(full_file_path, user_content, 'a')
                    except NameError as e:
                        print(f"\tList '{list_title}' doesn't exist for {user_name}")
                        print(f'{e}', ' NameError')
                    except KeyError as e:
                        print(f"User {user_name} doesn't have any lists in path: {users_file_path}")
                        print(f'{e}', ' KeyError')
                    else: continue
                case 'R':
                    # Read content of existing list
                    user_name = input('What directory(folder) name is your list under?\n(a valid folder name is alphanumeric(no special characters)): ').lower()
                    try:
                        # Check if user exists
                        assert Path(f'{users_file_path}\\{user_name}').is_dir()
                    except AssertionError as e:
                        print("Folder doesn't exist")
                        print(e)
                    list_title = input("The title of the list you're looking for: ").lower()
                    full_file_path = f'{users_file_path}\\{user_name}\\{list_title}'
                    try:
                        has_list = False
                        # Check if file exists for given user
                        for user_list in existing_users[user_name].user_lists:
                            if user_list.title == list_title:
                                has_list = True
                                active_user_list = user_list                        
                        active_user_list.read_list(full_file_path)
                    except NameError as e:
                        print(f"\tList '{list_title}' doesn't exist for {user_name}")
                        print(f'{e}', ' NameError')
                    except KeyError as e:
                        print(f"User {user_name} doesn't have any lists in path: {users_file_path}")
                        print(f'{e}', ' KeyError')
                    else: continue
                case 'E':
                    # Edit an existing list
                    user_name = input('What directory(folder) name do you want your list to be under?\n(a valid folder name is alphanumeric(no special characters)): ').lower()
                    try:
                        # Check if user exists
                        assert Path(f'{users_file_path}\\{user_name}').is_dir()
                    except AssertionError as e:
                        print("Folder doesn't exist")
                        print(e)
                    try:
                        list_title = input('Choose what is going to be the title of your list: ').lower()
                        full_file_path = f'{users_file_path}\\{user_name}\\{list_title}'
                        has_list = False
                        # Check if file exists for given user
                        for user_list in existing_users[user_name].user_lists:
                            if user_list.title == list_title:
                                has_list = True
                                active_user_list = user_list
                        remove_content = input("If you want to replace one or more list items, write them down seperated by a dash '-': ").lower()
                        substitute_content = input("Now, write what do you want to replace them with(this also needs to be seperated by a dash), or leave it blank to remove the previously entered items\n")
                        print('Everything will be replaced in order')
                        time.sleep(2)
                        active_user_list.edit_list(full_file_path, remove_content[1:], substitute_content[1:])
                    except NameError as e:
                        print(f"\tList '{list_title}' doesn't exist for {user_name}")
                        #print(f'{e}', ' NameError')
                    except KeyError as e:
                        print(f"User {user_name} doesn't have any lists in path: {users_file_path}")
                        #print(f'{e}', ' KeyError')
                    else: continue
            stop_script = input("Would you like to make any further changes? (Y\\N)").upper()
            try:
                assert stop_script == 'Y'
            except AssertionError:
                print("Stopping 'To-do list'...")
                running = False
            else: continue
        
        os.system('cls')
        