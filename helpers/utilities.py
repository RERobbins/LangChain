import os
import importlib
from dotenv import load_dotenv, find_dotenv, dotenv_values

def install_if_needed(package_names):
    """
    Install Python packages if they're not already installed.
    
    Args:
        package_names (str or list): The name of the package(s) to install,
                                    can be a single package name or a list of package names.
    """
    if isinstance(package_names, str):
        package_names = [package_names]
    
    for package_name in package_names:
        try:
            import importlib
            importlib.import_module(package_name)
            print(f"{package_name} is already installed.")
        except ImportError:
            try:
                import subprocess
                subprocess.check_call(['pip', 'install', package_name])
                print(f"Installed {package_name}.")
            except subprocess.CalledProcessError:
                print(f"Failed to install {package_name}.")
                
def running_in_colab():
    """
    Check if the Jupyter Notebook is running in Google Colab.

    Returns:
        bool: True if running in Google Colab, False otherwise.
    """
    try:
        import google.colab
        return True
    except ImportError:
        return False

def check_env_variable(variable_name):
    """
    Check if an environment variable exists.

    Parameters:
        variable_name (str): The name of the environment variable to check.

    Returns:
        bool: True if the environment variable exists, False otherwise.
    """
    if variable_name in os.environ:
        return True
    return False          

def delete_env_variable(variable_name):
    """
    Delete an environment variable if it exists.

    Parameters:
        variable_name (str): The name of the environment variable to delete.

    Returns:
        bool: True if the environment variable was deleted or didn't exist, False if an error occurred.
    """

    if check_env_variable(variable_name):
        try:
            del os.environ[variable_name]
            return True
        except Exception as e:
            print(f"Error deleting environment variable '{variable_name}': {e}")
            return False
    else:
        return True  # Variable didn't exist, so consider it "deleted"
                
def load_keys(env_file=".env"):
    """
    Load environment variables from a specified dotenv file.

    Parameters:
        env_file (str, optional): The name of the dotenv file to load.
            Defaults to ".env".

    Returns:
        None
    """
    load_dotenv(find_dotenv(env_file))
    return

def get_env_file_keys(env_file=".env"):
    """
    Get the key names (variable names) from a dotenv file.

    Parameters:
        env_file (str, optional): The name of the dotenv file to parse.
            Defaults to ".env".

    Returns:
        list: List of key names (variable names) from the dotenv file.
    """
    env_values = dotenv_values(find_dotenv(env_file))
    result = list(env_values.keys())
    return result