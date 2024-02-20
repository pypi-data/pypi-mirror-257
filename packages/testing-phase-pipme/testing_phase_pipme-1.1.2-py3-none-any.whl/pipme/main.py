import os
from .check_inits import check_all_folders_got_init
from .get_installed_packages import get_user_installed_packages

def run_cli(shell_path:str=os.getcwd()):
    """ 
    this function runs when user runs "pipme" in the shell 
    """
    print("HELLO", shell_path) 

    # ask confirmation if this is the root folder where they want to pip

    # ask if they registered at pypi.org and have an access token ready or not

    # create __init__.py files to each subfolder
    # this creates __init_.py files inside all subfolders if it doesnt already exist
    check_all_folders_got_init(shell_path)


    # get all packages imported into the folder
    packages_installed = get_user_installed_packages(shell_path)
    print(packages_installed)
    # this will go into the requirements array-------->>

    


if __name__=="__main__":
    current_shell_path = os.getcwd()
    run_cli(current_shell_path)