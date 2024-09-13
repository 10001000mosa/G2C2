import os

def create_directory_structure(base_dir):
    """
    Create the directory structure for the project.

    Args:
        base_dir (str): The base directory where the structure will be created.
    """
    directories = [
        os.path.join(base_dir, "data"),
        os.path.join(base_dir, "data/raw"),
        os.path.join(base_dir, "data/processed"),
        os.path.join(base_dir, "models"),
        os.path.join(base_dir, "notebooks"),
        os.path.join(base_dir, "scripts"),
        os.path.join(base_dir, "output"),
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def main():
    # Define the base directory (current working directory)
    base_dir = os.getcwd()
    
    # Create the directory structure
    create_directory_structure(base_dir)

if __name__ == "__main__":
    main()

