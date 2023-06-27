import os
import subprocess


def create_virtual_environment():
    """
    Creates a new virtual environment called lynch_env and installs the required libraries.
    """
    # Create the virtual environment
    subprocess.run(["python", "-m", "venv", "lynch_env"])

    # Activate the virtual environment
    activate_env_command = os.path.join("lynch_env", "Scripts", "activate")
    subprocess.run(activate_env_command, shell=True)

    # Install the required libraries from the requirements.txt file
    subprocess.run(["pip", "install", "-r", "requirements.txt"])


def load_virtual_environment():
    """
    Loads the existing virtual environment called lynch_env.
    """
    activate_env_command = os.path.join("lynch_env", "Scripts", "activate")
    subprocess.run(activate_env_command, shell=True)


def virtual_environment_loader():
    choice = input("Do you want to generate a new virtual environment (G) or load an existing one (L)? ")

    if choice.upper() == "G":
        create_virtual_environment()
    elif choice.upper() == "L":
        if not os.path.exists("lynch_env"):
            print("The virtual environment 'lynch_env' does not exist.")
            return
        load_virtual_environment()
    else:
        print("Invalid choice. Please choose 'G' to generate a new virtual environment or 'L' to load an existing one.")


if __name__ == "__main__":
    virtual_environment_loader()