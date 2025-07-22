import os

def setup_venv():
    """
    Sets up a virtual environment for the project.
    """
    os.system("python -m venv venv")
    print("Virtual environment created.")


def activate_venv():
    """
    Prints instructions to activate the virtual environment.
    """
    if os.name == 'nt':
        print("To activate the virtual environment, run: venv\\Scripts\\activate")
    else:
        print("To activate the virtual environment, run: source venv/bin/activate")
    print("Virtual environment activation instructions displayed.")

def install_dependencies():
    """
    Installs the necessary dependencies for the project.
    """
    os.system("venv/bin/pip install -r requirements.txt")
    print("Dependencies installed.")

def main():
    """
    Main function to set up the codespace.
    """
    setup_venv()
    activate_venv()
    install_dependencies()
    print("Codespace setup complete.")

if __name__ == "__main__":
    print("Setting up codespace...")
    main()
    print("Setup script executed successfully.")