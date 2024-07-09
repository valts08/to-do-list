import os
import time
from pathlib import Path
from string import ascii_letters
from string import digits
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

class List:
    def __init__(self, title: str, owner: str, content: str, file_path=os.curdir):
        self.owner = owner
        self.title = title
        self.location = file_path
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
        except:
            # make and open the list for writing, if it doesn't exist
            with open(f'{list_path}.txt', "x") as file:
                file.write(content)
        else:
            # just add text to it, if it does exist
            self.add_item(list_path, content)


    def add_item(self, list_path: str, content: str):
        # Content strucutre:
        # "str-str-str"...
        formatted_content = []
        # Extend or append to the 'formatted_content' array depending on if there are one or more 'list items'
        formatted_content.extend(content.split('-')) if '-' in content else formatted_content.append(content)
        with open(f'{list_path}.txt', 'a') as file:
            if len(formatted_content) > 1:
                file.writelines(formatted_content)
            else:
                file.write(formatted_content)

    def read_list(self, list_path):
        with open(f'{list_path}.txt', 'r') as file:
            file.read()

    def remove_item(self, list_path):
        # Gotta think of a way to be able to remove list items from the .txt file
        with open(f'{list_path}.txt', '') as file:
            file.read()

    

class User:
    def __init__(self):
        self.user_lists = []

    def create_list(self, title, owner, content, file_path):
        # Every time a new List is made for the User instance, add it to it's list of lists
        new_list = List(title, owner, content, file_path)
        self.user_lists.append(new_list)

    def get_lists(self):
        if len(self.user_lists) == 0:
            print("No lists available for this user")
            return
        print("Available Lists:")
        for list in self.user_lists:
            print(f"\t- {list.title}")


if __name__ == "__main__":
    print('Hello! What do you want to do?')
    while True:
        try:
            user_input = input('Make a new list(M), Add to an existing list(A),\nRead one of your lists(R), or edit a list(E): ').upper()
            assert user_input in ['M', 'A', 'R', 'E']
        except: 
            print('Wrong input!\nThe answer must be one of the capital letters provided in the parentheses')
            time.sleep(1.7)
            os.system('cls')
            continue
        else:
            match user_input:
                case 'M':
                    print("To make a new list you'll have to answer a few questions: ")
                    user_name = input('What directory(folder) name do you want your list to be under: ').lower()
                    list_title = input('Choose what is going to be the title of your list: ').lower()
                    user_content = input("What do you want to write in your list?\n(you need to follow the format 'item-item-item...', the dash is used as a seperator):\n")
                    file_path = input('Lastly, choose the file path, where you want to store your folder of lists(full file path): ')
                    if digits not in file_path and ascii_letters not in file_path:
                        file_path = os.curdir
                    new_user = User()
                    new_user.create_list(list_title, user_name, user_content, file_path)
                case 'A':
                    print('A')
                case 'R':
                    print('R')
                case 'E':
                    print('E')
        