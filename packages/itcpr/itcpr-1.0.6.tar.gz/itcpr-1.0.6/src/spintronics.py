import matplotlib.pyplot as plt
import numpy as np
import itertools
import os
import glob


def start():
    f = open("progress.txt","a")
    f.writelines(["# Data:False\n"])
    f.close()
    
    url = 'https://drive.google.com/uc?export=download&id=1kLBuhoDUUvrJOuBOLUGff0JYr8dB_nQJ'
    r = requests.get(url, allow_redirects=True)
    open('vocabulary.txt', 'wb').write(r.content)
    
    print("Welcome to your python GRE preparation tool. Necessary files are created.")
    print("To learn more about GRE use 'gre.about()', and to learn more about this library use 'gre.help()'.")


def plot(file_path, parameter_names):
    """
    Plots specified parameters from a given file.
    
    Args:
    - file_path: Path to the data file.
    - parameter_names: List of parameter names to plot.
    """
    data = []
    axis_names = []
    selected_columns = []
    
    # Open the file and read data
    with open(file_path, "r") as file:
        for line in file:
            if line.startswith("#"):
                # Extracting axis names
                axis_names = line.strip().split('\t')
                # Determine which columns to plot based on parameter_names
                selected_columns = [axis_names.index(name) for name in parameter_names if name in axis_names]
            else:
                values = [float(value) for value in line.split("\t")]
                data.append(values)
    
    if not selected_columns:  # Check if selected_columns is empty
        print("None of the specified parameters were found in the file.")
        return
    
    # Convert the list of lists into a NumPy array for easier slicing
    data = np.array(data)
    
    # Adjust the number of subplots based on selected parameters
    num_parameters = len(selected_columns)
    
    # Creating subplots
    fig, axs = plt.subplots(num_parameters, 1, figsize=(10, num_parameters * 3), squeeze=False)
    
    # Loop over each selected parameter to create a subplot
    for i, column_index in enumerate(selected_columns):
        axs[i, 0].plot(data[:, 0], data[:, column_index], label=f"${axis_names[column_index]}$")
        axs[i, 0].set_xlabel(axis_names[0])
        axs[i, 0].set_ylabel(axis_names[column_index])
        axs[i, 0].legend()
    
    # Adjust layout to prevent overlapping
    plt.tight_layout()
    plt.show()



def m3_commands(base_folder, filename_pattern, ranges):
    """
    Prints mumax3 commands for files based on a pattern with multiple 'cng' placeholders,
    each having different start, end values, and increments, and then prints 'mumax3' at the end.
    
    Args:
    - base_folder: The base folder address where the files are located or will be saved.
    - filename_pattern: The pattern of the filename with 'cng' as placeholders.
    - ranges: A list of tuples, each tuple contains (start_value, end_value, increment) for each 'cng'.
    """
    # Generate all combinations of replacements for 'cng'
    replacement_lists = [list(range(start, end + 1, increment)) for start, end, increment in ranges]
    all_combinations = list(itertools.product(*replacement_lists))
    
    for combination in all_combinations:
        # Start with the initial pattern for each combination
        filename = filename_pattern
        
        # Replace each 'cng' with the corresponding value from the combination
        for value in combination:
            filename = filename.replace('cng', str(value), 1)  # Replace the first occurrence
        
        full_command = f"mumax3 {base_folder}/{filename}"
        print(full_command)
    
    # Print the final 'mumax3' command
    print('mumax3')


def rename_tables(base_dir):
    """
    Renames all 'table.txt' files to match their parent folder names (without the '.out' extension) with '.txt' extension,
    within folders ending with '.out' found anywhere under the specified base directory.
    Automatically converts backslashes in the base directory path to forward slashes to avoid Unicode errors.
    
    Args:
    - base_dir: The base directory to recursively search for '.out' folders.
    """
    # Automatically convert backslashes to forward slashes to avoid Unicode errors
    base_dir = base_dir.replace("\\", "/")

    # Pattern to match all '.out' folders within the base directory, recursively
    out_folders_pattern = os.path.join(base_dir, "**", "*.out")
    
    # Find all folders matching the pattern, recursively
    out_folders = glob.glob(out_folders_pattern, recursive=True)
    
    for folder in out_folders:
        old_file_path = os.path.join(folder, "table.txt")
        if os.path.exists(old_file_path):  # Check if 'table.txt' exists in the folder
            # Extract the folder name without the path and remove '.out' extension
            base_name = os.path.basename(folder).replace(".out", "")
            new_file_name = f"{base_name}.txt"
            new_file_path = os.path.join(folder, new_file_name)
            
            # Rename the file
            os.rename(old_file_path, new_file_path)
            print(f"Renamed '{old_file_path}' to '{new_file_path}'")

def plot_list(file_path):
    """
    Lists the parameters available for plotting from a given file, excluding the independent variable.
    
    Args:
    - file_path: Path to the data file.
    
    Returns:
    - A list of parameter names that can be plotted, excluding the independent variable.
    """
    try:
        with open(file_path, "r") as file:
            for line in file:
                if line.startswith("#"):
                    # Assuming the first line that starts with "#" contains the headers
                    parameters = line.strip("#").strip().split('\t')
                    # Exclude the first parameter (independent variable) and return the rest
                    return [param for param in parameters[1:] if param]  # Skip the first element
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

    # In case no parameters were found or the file couldn't be read
    print("No parameters found or unable to read the file.")
    return []

def help():
    print("start() : builds necessary database for the package")
    print("hello() : gets you started with the package")
    print("about() : GRE basic informations")
    print("new() : adds new word of GRE vocabulary")
    print("meaning() : prints out the meaning of a given word")
    print("set() : prints out all the words in a set")
    print("flash() : flashcard of a set")
    print("exam() : takes a random vocabulary quiz")
    print("progress() : shows data about your preparation progress")
    print("update() : updates database from the internet")
    
    