import os
import time
from pathlib import Path
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
                # just add text to it, if it does exist
                self.add_item(list_path, content)
            else:
                # make and open the list for writing, if it doesn't exist
                with open(f'{list_path}.txt', "x") as file:
                    file.write(f"- {content}")


    def add_item(self, list_path: str, content: str):
        # Content strucutre:
        # "-str-str-str"...
        formatted_content = []
        formatted_content.extend("\n- ".join(content.split('-')))
        with open(f'{list_path}.txt', 'a') as file:
                file.writelines(formatted_content)

    def read_list(self, list_path):
        with open(f'{list_path}.txt', 'r') as file:
            file.read()

    def remove_item(self, list_path):
        # Gotta think of a way to be able to remove list items from the .txt file
        with open(f'{list_path}.txt', '') as file:
            file.read()



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
    user_info = {}
    for (dir_path, sub_folder, files) in os.walk(file_path):
        for folder in sub_folder:
            if folder.isalnum():
                files_in_folder = os.listdir(f'{dir_path}\\{folder}')
                #print(folder, 'folder')
                user_info[folder] = User(folder)
                for file in files_in_folder:
                    with open(f'{dir_path}\\{folder}\\{file}') as doc:
                        list_content = doc.read()
                        # We pass "file[:-4] to get rid of the ".txt" portion of the string"
                        # because the user input is purely the name of the list e.g. "blabla", not "blabla.txt"
                        user_info[folder].user_lists.append(List(file[:-4], folder, list_content, dir_path, make_with_user=False))

        return user_info

if __name__ == "__main__":
    users_file_path = input("Before we start, if you have any lists already made, enter their file path here:\n")
    print('Hello! What do you want to do next?')
    while True:
        # Load user data every time an action is done
        # This should be changed later on to only update 
        # if there is any additional data the user passed
        existing_users = load_users(users_file_path)
        print(existing_users)
        try:
            user_input = input('Make a new list(M), Add to an existing list(A),\nRead one of your lists(R), or edit a list(E): ').upper()
            assert user_input in ['M', 'A', 'R', 'E']
        except: 
            print('Wrong input!\nThe answer must be one of the capital letters provided in the parentheses')
            #time.sleep(1.7)
            #os.system('cls')
            continue
        else:
            # Things we need to get to a list(file):
            #   - Name of user
            #   - Title of list
            #   - File path

            user_name = input('What directory(folder) name do you want your list to be under\n(a valid folder name is alphanumeric(no special characters)): ').lower()
            list_title = input('Choose what is going to be the title of your list: ').lower()
            user_content = input("What do you want to write in your list?\n(follow the format '-item-item-item...', the dash is used as a seperator):\n")
            full_file_path = f'{users_file_path}\\{user_name}\\{list_title}'
            match user_input:
                case 'M':
                    if not Path(users_file_path).is_dir() and users_file_path[0] == '.':
                        #  Change the 2nd part of this if statement, it doesn't make sense
                        users_file_path = os.curdir
                    new_user = User(user_name)
                    new_user.create_list(list_title, user_name, user_content, users_file_path)
                case 'A':
                    # Add items to an existing list
                    has_list = False
                    try:
                        # Check if file exists for given user
                        for user_list in existing_users[user_name].user_lists:
                            if user_list.title == list_title:
                                has_list = True
                                active_user_list = user_list
                        assert has_list
                    except AssertionError as e:
                        print(f'List at path: {full_file_path}.txt was not found')
                        print(e, ' Error')
                    else:
                        active_user_list.add_item(full_file_path, user_content)
                case 'R':
                    # Read content of existing list
                    print('R')
                case 'E':
                    # Edit an existing list
                    print('E')
        
        #os.system('cls')
        