##################################################################
#
Basic usage (create environment with Python 3.11)
```python setup_env.py my_project_env```
This will:

Install uv (if not already installed).
Install Python 3.11 (if not already managed by uv).
Create a virtual environment named my_project_env using Python 3.11.
#
Specify a different Python version
```python setup_env.py another_env --python_version 3.9```
This will:

Install uv.
Install Python 3.9.
Create a virtual environment named another_env using Python 3.9.
##################################################################

import subprocess
import sys
import os

def install_uv_and_create_env(env_name, python_version="3.11"):
    """
    Installs uv, installs a specified Python version (defaulting to 3.11),
    and creates a virtual environment with the given name.

    This script is designed to be cross-OS compatible.

    Args:
        env_name (str): The name of the virtual environment to create.
        python_version (str): The Python version to install (e.g., "3.9", "3.11").
                              Defaults to "3.11".
    """
    print("--- Starting environment setup ---")

    # 1. Install uv
    # Using sys.executable -m pip ensures cross-platform compatibility for pip execution
    print("\n--- Installing uv ---")
    try:
        print(f"Running: {sys.executable} -m pip install uv")
        subprocess.run([sys.executable, "-m", "pip", "install", "uv"], check=True)
        print("uv installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing uv: {e}")
        print("Please ensure you have Python and pip installed and accessible.")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Python executable '{sys.executable}' not found.")
        print("Please ensure Python is correctly installed and in your system's PATH.")
        sys.exit(1)


    # 2. Install specified Python version using uv
    # uv commands are generally cross-platform.
    print(f"\n--- Installing Python {python_version} ---")
    try:
        print(f"Running: uv python install {python_version}")
        subprocess.run(["uv", "python", "install", python_version], check=True)
        print(f"Python {python_version} installed successfully (or already present).")
    except subprocess.CalledProcessError as e:
        print(f"Error installing Python {python_version}: {e}")
        print("This might happen if uv cannot find or install the specified Python version.")
        print("Ensure uv is correctly set up to manage Python versions (e.g., using pyenv, or a system-wide Python installation).")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: 'uv' command not found. It might not have been installed correctly or is not in your PATH.")
        print("Please check the 'uv' installation step above.")
        sys.exit(1)

    # 3. Create virtual environment using uv with the specified Python version
    # uv venv commands are generally cross-platform.
    print(f"\n--- Creating virtual environment '{env_name}' with Python {python_version} ---")
    try:
        print(f"Running: uv venv --python {python_version} {env_name}")
        subprocess.run(["uv", "venv", "--python", python_version, env_name], check=True)
        print(f"Virtual environment '{env_name}' created successfully with Python {python_version}.")
        print(f"\nTo activate the environment, run:")
        # Cross-platform activation instructions
        if sys.platform == "win32":
            print(f"  .\\{env_name}\\Scripts\\activate")
        else:
            print(f"  source ./{env_name}/bin/activate")
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment '{env_name}': {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: 'uv' command not found. This should not happen if previous steps were successful.")
        sys.exit(1)

    print("\n--- Environment setup complete ---")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Install uv, install a specific Python version, and create a virtual environment. Designed for cross-OS compatibility.")
    parser.add_argument("env_name", help="The name of the virtual environment to create.")
    parser.add_argument("--python_version", default="3.11",
                        help="The Python version to install and use for the environment (e.g., '3.9', '3.11'). Defaults to 3.11.")

    args = parser.parse_args()

    install_uv_and_create_env(args.env_name, args.python_version)
