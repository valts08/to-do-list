import os
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

class List:
    def __init__(self, title, owner, content, file_path=os.curdir):
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


    def add_item(self, list_path, content):
        with open(f'{list_path}.txt', 'w') as file:
            file.write(content)

    def read_list(self):
        pass

    def remove_item(self):
        pass

    

class User:
    def __init__(self):
        self.lists = []
        pass

    def create_list(self, title, owner, content, file_path):
        List(title, owner, content, file_path)


if __name__ == "__main__":
    pass