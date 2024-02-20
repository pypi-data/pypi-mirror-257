import os

def run_cli(shell_path:str=os.getcwd()):
    """ 
    this function runs when user runs "pipme" in the shell 
    """
    print("HELLO", shell_path) 
    


if __name__=="__main__":
    current_shell_path = os.getcwd()
    run_cli(current_shell_path)