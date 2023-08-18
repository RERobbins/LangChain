import os
import importlib

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

def load_keys():
    install_if_needed("dotenv")
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
    return
            
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
