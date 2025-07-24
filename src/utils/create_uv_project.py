##################################################################

##
#Basic usage (create project my_new_app with Python 3.11)
#```python create_uv_project.py my_new_app```\

#This will:
#Create a directory named my_new_app.
#Change into my_new_app.
#Install uv (if not already installed).
#Run uv init inside my_new_app (creating pyproject.toml).
#Install Python 3.11 (if not already managed by uv).
#Create a virtual environment named .venv inside my_new_app/.
#Change back to your original directory.

##
#Specify a different Python version
#```python create_uv_project.py my_data_tool --python_version 3.9```

#This will:
#Create a directory named my_data_tool.
#Change into my_data_tool.
#Install uv (if not already installed).
#Run uv init inside my_data_tool (creating pyproject.toml).
#Install Python 3.9 (if not already managed by uv).
#Create a virtual environment named .venv inside my_data_tool/.
#Change back to your original directory.
##
##################################################################
    
import subprocess
import sys
import os

def setup_uv_project(project_name, python_version="3.11"):
    """
    Creates a project directory, initializes uv within it, installs a specified
    Python version, and creates a virtual environment named '.venv' inside
    the project directory.

    This script is designed to be cross-OS compatible.

    Args:
        project_name (str): The name of the project directory to create.
        python_version (str): The Python version to install and use for the
                              environment (e.g., "3.9", "3.11"). Defaults to "3.11".
    """
    print("--- Starting project and environment setup ---")

    # 1. Create the project directory
    print(f"\n--- Creating project directory: {project_name} ---")
    try:
        os.makedirs(project_name, exist_ok=True)
        print(f"Directory '{project_name}' created successfully (or already exists).")
    except OSError as e:
        print(f"Error creating directory '{project_name}': {e}")
        sys.exit(1)

    # Change into the project directory
    original_cwd = os.getcwd() # Store original current working directory
    try:
        os.chdir(project_name)
        print(f"Changed current directory to: {os.getcwd()}")
    except OSError as e:
        print(f"Error changing to directory '{project_name}': {e}")
        sys.exit(1)

    # 2. Install uv (if not already installed)
    print("\n--- Installing uv ---")
    try:
        # Using sys.executable -m pip ensures cross-platform compatibility for pip execution
        print(f"Running: {sys.executable} -m pip install uv")
        subprocess.run([sys.executable, "-m", "pip", "install", "uv"], check=True)
        print("uv installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing uv: {e}")
        print("Please ensure you have Python and pip installed and accessible.")
        # Revert CWD before exiting
        os.chdir(original_cwd)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Python executable '{sys.executable}' not found.")
        print("Please ensure Python is correctly installed and in your system's PATH.")
        # Revert CWD before exiting
        os.chdir(original_cwd)
        sys.exit(1)

    # 3. Initialize uv in the project directory
    print(f"\n--- Initializing uv in '{project_name}' ---")
    try:
        # uv init creates pyproject.toml
        print(f"Running: uv init")
        subprocess.run(["uv", "init"], check=True)
        print("uv project initialized (pyproject.toml created).")
    except subprocess.CalledProcessError as e:
        print(f"Error initializing uv: {e}")
        # Revert CWD before exiting
        os.chdir(original_cwd)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: 'uv' command not found. It might not have been installed correctly or is not in your PATH.")
        # Revert CWD before exiting
        os.chdir(original_cwd)
        sys.exit(1)

    # 4. Install specified Python version using uv
    print(f"\n--- Installing Python {python_version} ---")
    try:
        # uv commands are generally cross-platform.
        print(f"Running: uv python install {python_version}")
        subprocess.run(["uv", "python", "install", python_version], check=True)
        print(f"Python {python_version} installed successfully (or already present).")
    except subprocess.CalledProcessError as e:
        print(f"Error installing Python {python_version}: {e}")
        print("This might happen if uv cannot find or install the specified Python version.")
        print("Ensure uv is correctly set up to manage Python versions (e.g., using pyenv, or a system-wide Python installation).")
        # Revert CWD before exiting
        os.chdir(original_cwd)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: 'uv' command not found. This should not happen if uv was installed correctly.")
        # Revert CWD before exiting
        os.chdir(original_cwd)
        sys.exit(1)

    # 5. Create virtual environment named '.venv' using uv with the specified Python version
    print(f"\n--- Creating virtual environment '.venv' with Python {python_version} inside '{project_name}' ---")
    try:
        # Create the environment as .venv in the current directory (which is the project_name dir)
        print(f"Running: uv venv --python {python_version} .venv")
        subprocess.run(["uv", "venv", "--python", python_version, ".venv"], check=True)
        print(f"Virtual environment '.venv' created successfully with Python {python_version}.")
        print(f"\nTo activate the environment, navigate into your project directory and run:")
        # Cross-platform activation instructions
        if sys.platform == "win32":
            print(f"  cd {project_name}")
            print(f"  .\\.venv\\Scripts\\activate")
        else:
            print(f"  cd {project_name}")
            print(f"  source ./.venv/bin/activate")
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment '.venv': {e}")
        # Revert CWD before exiting
        os.chdir(original_cwd)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: 'uv' command not found. This should not happen if previous steps were successful.")
        # Revert CWD before exiting
        os.chdir(original_cwd)
        sys.exit(1)
    finally:
        # Always change back to the original current working directory
        os.chdir(original_cwd)
        print(f"\nChanged back to original directory: {os.getcwd()}")


    print("\n--- Project and environment setup complete ---")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Create a new project directory, initialize uv, install a specific Python version, and create a .venv environment inside it."
    )
    parser.add_argument("project_name", help="The name of the new project directory to create.")
    parser.add_argument("--python_version", default="3.11",
                        help="The Python version to install and use for the environment (e.g., '3.9', '3.11'). Defaults to 3.11.")

    args = parser.parse_args()

    setup_uv_project(args.project_name, args.python_version)
