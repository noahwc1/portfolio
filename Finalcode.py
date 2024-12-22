# user_csv.py
# ENDG 233 F24
# Noah Weir Chaba
# Noah Weir Chaba, N/A
# A terminal-based data analysis and visualization program in Python.
# You must follow the specifications provided in the project description.
# Remember to include docstrings and comments throughout your code.

#PREFACE TO MY CODE:
#When I undertook this idea, I did not expect it to become so complicated but by the 
#nature of garmin csv files it took a lot of debugging to even get errors to not come up
#Obviously it was required to go into concepts out of the scope of this course and I had to use
#chatgpt and online sources as help, however, all code written here is written in not copied and in doing so I learned
#how a lot of the concepts worked. I know understand how dictionaries, try except statements, list ziping and text coloring works
#and implimented them a lot within the code. 


import numpy as np
import matplotlib.pyplot as plt

#functions doing specific tasks
def styled_text(text, color=None, bold=False, underline=False):
    """
    Function to style terminal output text with ANSI escape codes. 
    Function takes color wanted, finds escape code and prints that coloured text on the terminal.

    Parameters:
        text (str): The text to style. In quotations.
        color (str): The color name ('red', 'green', 'blue', etc.).
        bold (bool): Whether to make the text bold. True or False.
        underline (bool): Whether to underline the text.True or False

    Returns:
        str: The styled text. 
    """
    #dictionary defining the ANSI escape codes of different colours
    colors = {
        "red": "31",
        "green": "32",
        "yellow": "33",
        "blue": "34",
        "magenta": "35",
        "cyan": "36",
        "white": "37",
    }

    #reading in what colour text should be and formating output text
    style = []

    if bold:
        style.append("1")
    if underline:
        style.append("4")
    if color and color in colors:
        style.append(colors[color])

    style_code = ";".join(style)
    return f"\033[{style_code}m{text}\033[0m" if style_code else text

def read_csv(file_name, include_headers):
    """
    Reads in a CSV file and stores its contents into a list of lists.
    If include_headers is True, returns the headers separately.
    Otherwise, the headers are removed from the returned data.

    Parameters:
        file_name (str): The name or path of the CSV file.
        include_headers (bool): Whether to include headers in the return.

    Returns:
        tuple: (data, headers)
            data: List of lists representing the CSV rows with meaningful data.
            headers: List of column headers with meaningful data.
        None: If file doesn't exist
    """
    file_path = file_name
    #try function to not give terminal error if file doesnt exist in directory
    try:
            open(file_path, "r")
    except FileNotFoundError:
            print(f"CSV file was not found:\n{file_name}") 
            return None, None


    # Read the file and split into rows
    with open(file_path, "r") as file:
        lines = [line.strip().replace('"', '').split(",") for line in file]  #list comprehension for creation of list from data

    # Separate headers and data
    headers = lines[0]
    data = lines[1:]

    # Transpose data to work with columns
    columns = list(zip(*data)) if data else []    #makes every row a column to easier parse through data, saved as tuple

    # Filter out columns with no meaningful data
    cleaned_headers = []
    cleaned_columns = []

    for i, col in enumerate(columns):
        # Check if the column contains any meaningful data (non-placeholder values)
        has_meaningful_data = any(val.strip() and val.strip() not in ("--", "NA", "null", "") for val in col)
        
        if has_meaningful_data:
            cleaned_headers.append(headers[i])
            cleaned_columns.append(col)

    # Transpose cleaned columns back into rows
    cleaned_data = list(zip(*cleaned_columns)) if cleaned_columns else []

    # Convert tuples to lists
    cleaned_data = [list(row) for row in cleaned_data]

    # If headers are not included, return only data rows
    if not include_headers:
        return cleaned_data, []

    return cleaned_data, cleaned_headers

def headers_to_lowercase(headers):
    """
    Converts list of headers to lowercase.

    Parameters:
        headers(list): Returns all strings in list to lowercase
    
    Returns:
        list: lowercased string within list
    
    """
    return [h.lower() for h in headers]

def clean_headers_and_data(headers, data):
    """
    Remove columns from headers and data that have no meaningful data. To get rid of data within inputed csv file(s) that doesn't contain valuable information.
    'meaningful' data is if it has at leat least one numeric or non-empty value. 

    Parameters:
        headers(list): list of the headers from the file
        data(list): list of data from the file that is not headers

    Returns:
        cleaned_headers(list): headers removed if not associated with relevent data
        cleaned_data(list): data columns removed if not containing relevent data
    """
    
    columns = list(zip(*data)) if data else [] # zip(*data) turns rows into columns, easier to parse through
    
    cleaned_headers = []
    cleaned_columns = []

    for i, h in enumerate(headers):
        col_values = columns[i] if columns else []

        # Check if column has any numeric data or at least one non-empty, non '--' entry
        has_meaningful_data = False
        for val in col_values:
            val = val.strip()
            if val and val != "--":  # Non-empty and not just '--'
                # Try converting to float; if not possible, we still consider it meaningful text
                try:
                    float(val)
                    # If it converts to a float successfully, we have numeric data
                    has_meaningful_data = True
                    break
                except ValueError:
                    # It's non-numeric but still a valid, non-empty string -> meaningful enough
                    has_meaningful_data = True
                    break

        if has_meaningful_data:
            cleaned_headers.append(h)
            cleaned_columns.append(col_values)

    # Convert columns back to rows
    cleaned_data = list(zip(*cleaned_columns)) if cleaned_columns else []

    # Convert tuples back to lists
    cleaned_data = [list(row) for row in cleaned_data]
    
    return cleaned_headers, cleaned_data

def write_csv(all_data_for_plot, output_file='output.csv'):
    '''
    Function to write the create/open a csv file and write in data from the laps wanted.

    Parameters:
        all_data_for_plot (2D list): list containing [[file name, type of data, [data]], [another one...]] .
        output_file (variable name): the name of the csv file created or appended to
    
    Returns:
        A csv file either appended to or created based of the given name and the data
    
    '''
    #try function to not give terminal error if not able to open wanted output csv file
    with open(output_file, mode='w') as file:
        try:
            file.read().strip()
            print(styled_text("Existing file is being appended with laps data. Look for output.csv.", color="blue"))
        except:
            print(styled_text("New csv file is being created to append laps data. Look for output.csv.", color="blue"))
        for entry in all_data_for_plot:
            # Write the name of the file
            file.write(entry[0] + '\n')
            # write the data type and the data on the next line
            line = ', '.join([entry[1]] + entry[3])  #join each entry together with ","
            file.write(line + '\n')

def remove_duplicates(lst):
    """
    Removes duplicate items from a list and prints which items were removed. To get rid of multiple header entrees for analysis.

    Parameters:
        lst(list): List of headers or names
    
    Returns:
        unique_items(list): unique list of the headers given, and prints the headers removed that were dublicates.
    """
    removed_items = []
    unique_items = []
    for item in lst:
        if item not in unique_items:
            unique_items.append(item)
        else:
            removed_items.append(item)

    for item in removed_items:
        print(f"{item} was a duplicate and has been removed from the list")

    return unique_items

def parse_time_to_seconds(time_str):
    """
    Convert the H:MM:SS format of garmin csv files into useful analyzing data (seconds). 

    Parameters:
        time_str(string): The unwanted time format, H:MM:SS

    Returns:
        seconds(int): The associated seconds to input
        float('nan'): If cannot convert to seconds

    """
    time_str = time_str.strip()
    if not time_str or time_str == "--":
        return float('nan')  # or return None if no data

    # Split by colon
    parts = time_str.split(":")
    
    # Handle cases like "H:MM:SS" or just "MM:SS"
    if len(parts) == 3:
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = float(parts[2])
        return hours * 3600 + minutes * 60 + seconds
    elif len(parts) == 2:
        minutes = int(parts[0])
        seconds = float(parts[1])
        return minutes * 60 + seconds
    else:
        # Unexpected format handle without giving terminal error
        return float('nan')

def numpy_averages(data):
    '''
    Outputs of the average and the max of the data collected from the laps wanted in a list to be printed.

    Parameters:
        data(list): data to be sent to display or collected 

    Returns:
        averages(list): list of the averages of each data inputed
        maxes(list): list of the maxes of each data inputed
    '''
    rows = []

    for entry in data:
        numeric_values = entry[3]  
        numeric_values = np.array(numeric_values, dtype=float)
        rows.append(numeric_values)
    
    array = np.array(rows, dtype=object)
    
    averages = []
    maxes = []
    
    for i in range(len(rows)):
        maxes.append(np.max(array[i]))
        averages.append(np.average(array[i]))
    
    return averages, maxes

#functions involving user input
def prompt_for_csv_files():
    """
    Prompts the user to input CSV file names located in the /usercode/data_files/ directory.
    Pressing 'q' returns -1 to indicate quitting. Overall Program ends. 

    Returns:
        list: A list of CSV filenames, or -1 if the user quits.
    """
    names_of_files = []
    paths_of_files = []

    while True:
        file_wanted = input(
            styled_text("Enter the CSV file name (including .csv) or 'q' to quit:\n>> ", color="cyan", bold=True)
        ).strip()
        
        #quits program if "q" entered
        if file_wanted.lower() == "q":
            return -1

        file_path = "C:\\Users\\stree\\Downloads\\virtual environment for vs code\\data files\\" + file_wanted

        #try function to see if file exists within directory
        try:
            with open(file_path, "r"):
                paths_of_files.append("C:\\Users\\stree\\Downloads\\virtual environment for vs code\\data files\\" + file_wanted)
                names_of_files.append(file_wanted)
                another = input(
                    styled_text("Would you like to analyze another file (yes/no)?\n>> ", color="cyan", bold=True)
                ).strip().lower()
                if another == "yes":
                    continue
                else:
                    break
        except FileNotFoundError:
            print(styled_text(f"CSV file not found: {file_wanted}", color="red", bold=False))

    return paths_of_files, names_of_files

def select_data_to_compare(headers, file_name):
    """
    Asks the user which headers they would like to analyze from the given file.

    Parameters:
        headers (list): List of headers from the CSV.
        file_name (str): The CSV file name.

    Returns:
        list: A list of headers that exist in the file and the user wants to analyze.
    """
    styled_text(f"\nAvailable headers in {file_name}:\n{', '.join(headers)}", color="cyan", bold=False)
    data_to_compare = input(
        styled_text("Enter one or multiple headers separated by commas for comparison:\n>> "),
        color="yellow",
        bold=False
        ).strip()

    #creates a list of the selected data to compare
    selected = [item.strip() for item in data_to_compare.split(",") if item.strip()]

    validated = []
    
    #checks to see if input matches headers
    for item in selected:
        if item in headers:
            validated.append(item)
        else:
            print(f"'{item}' not found in {file_name}'s headers. Skipping...")

    validated = remove_duplicates(validated)

    if not validated:
        print("No valid headers selected.")
    return validated

def prompt_for_lap_range(file_name, data_length):
    """
    Prompts user to enter starting lap, ending lap, and step.
    Ensures values are valid and within the data length.

    Parametesrs:
        file_name (str): The name of the CSV file.
        data_length (int): Number of data rows.

    Returns:
        tuple: (start, end, step) if valid input; None otherwise.
    """
    while True:
        laps = input(
    styled_text("\nSpecify laps for ", color="magenta", bold=False) + 
    styled_text(file_name, color="blue", bold=True) +
    styled_text(" as: start_lap,end_lap,step\n>> ", color="magenta", bold=False)
).strip()

        #try function to see if input matches format wanted
        try:
            start_str, end_str, step_str = laps.split(",")
            start, end, step = int(start_str), int(end_str), int(step_str)
            
            #checks if inputs are valid for the data given, eg not a lap that doesn't exist within data
            if start > end:
                print("Error: start lap should not be greater than end lap.")
            elif end > data_length:
                print("Error: end lap exceeds the number of laps in the data.")
            elif step <= 0:
                print("Error: step must be a positive integer.")
            else:
                return (start, end, step)
        except ValueError:
            print("Invalid input format. Example: 1,10,1")

#functions extracting data from different lists and such
def extract_data_for_plot(headers, data, header_specified, file_name, sequence):
    """
    Extracts the wanted data from the data extracted from the CSV file and returns it as a list. 
    So if specifed to analyze avg hr from file1 with all even laps (0,end,2), extacts the avg hr from data under file1, based of the laps wanted and returns it with the parameters.

    Parameters:
        headers(list): The headers from the specified file
        data(list): list of all data associated with the file
        header_specified(str): The header wanted to extract data from
        sequence(list): the list of which laps to pull the data from
    
    Returns:
        list: with the [file_name, header_specified, filtered_laps, filtered_values]
    """
    #try function to see if it can find lap or laps within headers to find laps numbered in data
    try:
        index_lap = headers.index("lap")
    except ValueError:
        try:
            index_lap = headers.index("laps")
        except ValueError:
            print("Error: No 'laps' column found.")
            return None

    data_index = headers.index(header_specified)
    start, end, step = sequence
    numeric_data = []

    #goes through data and appends data wanted if lap number matches laps wanted with that row
    for row in data:
        try:
            lap_val = int(row[index_lap])
            numeric_data.append((lap_val, row[data_index]))
        except ValueError:
            # Skip non-numeric rows, garmin has some rows named as weird names and not laps
            continue

    # Filter by the specified sequence
    filtered_laps = []
    filtered_values = []

    for lap_num in range(start, end + 1, step):
        # Find rows with this correct lap num from the sequence
        matches = [val for (lv, val) in numeric_data if lv == lap_num]

        if matches:
            filtered_laps.append(lap_num)
            filtered_values.append(matches[0])

    if not filtered_values:
        print(f"No data found for laps {start} to {end} in {file_name}.")
        return None

    return [file_name, header_specified, filtered_laps, filtered_values]

def gather_headers_from_plotdata(all_data_for_plot):
    """
    Collects all headers from the full plot data.

    Parameters:
        all_data_for_plot (list): List of [file, header, data_list] entries.

    Returns:
        list: A list of headers corresponding to the data selected.
    """
    #list comprehension for items meeting the criteria, basically if the item exists
    return [item[1] for item in all_data_for_plot if item is not None]

def find_repeated_indexes(headers):
    """
    Finds indexes of repeated headers.

    Parameters:
        headers (list): Headers from all datasets chosen.

    Returns:
        dict: {header: [indexes]} mapping header to the indexes in all_data_for_plot.
    """
    repeated_headers = {}
    for index, header in enumerate(headers):
        repeated_headers.setdefault(header, []).append(index)
    return repeated_headers

#functions to plot data on display
def display_data_one_plot(all_data_for_plot):
    """
    Displays a single graph with all datasets plotted, aligning data on shared laps. Line chart for the data as it's easy to compare on one graph.
    Function parses through the data finding the same laps and then outputs the data on a graph. 
    
    Paremeters:
        all_data_for_plot (list): A list of lists: [filename, header, laps_list, values_list].
    
    Returns:
        plot: a matplotlib of the data on one plot and a file saved under final_plots of data
    """
    # Filter out None data 
    all_data_for_plot = [d for d in all_data_for_plot if d is not None]

    if not all_data_for_plot:
        print("No data to plot.")
        return

    # Collect all unique laps across all datasets
    all_laps = set()
    for data_entry in all_data_for_plot:
        all_laps.update(data_entry[2])  # data_entry[2] is laps_list

    # Sort the laps for a consistent x-axis, same laps
    unified_laps = sorted(all_laps)

    plt.figure(figsize=(12, 6))

    for data_entry in all_data_for_plot:
        file_name = data_entry[0]
        header = data_entry[1]
        laps_list = data_entry[2]
        values_list = data_entry[3]

        # Align values with unified_laps
        y_aligned = []

        for lap in unified_laps:
            if lap in laps_list:
                index = laps_list.index(lap)
                val = values_list[index].strip()

                # Convert time-like data or parse as float
                if ":" in val:
                    y_aligned.append(parse_time_to_seconds(val))
                else:
                    try:
                        y_aligned.append(float(val))
                    except ValueError:
                        y_aligned.append(float('nan'))
            else:
                y_aligned.append(float('nan'))  # No data for this lap

        # Plot the aligned data
        plt.plot(unified_laps, y_aligned, marker='o', label=f"{file_name} - {header}")

    # Add labels, legend, and grid
    plt.title("Comparison of Data Across Laps")
    plt.xlabel("Laps")
    plt.ylabel("Values")
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    
    plt.savefig("C:\\Users\\stree\\Downloads\\virtual environment for vs code\\final_plots\\Currentplot.png")
    print("file saved") 
    plt.tight_layout()
    plt.show()

def display_data_multiple_plots(all_data_for_plot):
    """
    Displays bar plots for the selected data. compares laps that are the same and then ouputs all the data from all_data_for_plot based on similarites.
    So if chosen "avg hr" takes that data out from input data and the multiple files and puts it all on one plot. 

    Paramters:
        all_data_for_plot (list): A list of lists: [filename, header, laps_list, values_list].
    
    Returns:
        plot: mulitple plots of the data wanted to display and saves the plot under final_plots
    """
    headers_from_data = gather_headers_from_plotdata(all_data_for_plot)
    repeated_headers = find_repeated_indexes(headers_from_data)

    if not repeated_headers:
        print("No data to plot.")
        return

    # One plot per unique header
    plots_count = len(repeated_headers)
    fig, axs = plt.subplots(plots_count, figsize=(10, 5 * plots_count))

    if plots_count == 1:
        axs = [axs]

    #sets up the plot based of how many subplots there are
    for ax, (header, indexes) in zip(axs, repeated_headers.items()):
        width = 0.4
        max_len = 0
        for place, idx in enumerate(indexes):
            data_entry = all_data_for_plot[idx]
            if data_entry is None:
                continue

            y_values = data_entry[3]  # values_list
            laps = data_entry[2]      # laps_list

            current_header = data_entry[1]

            # Convert y-values to floats if possible
            float_values = []
            for val in y_values:
                if isinstance(val, str):  # Handle string values
                    if ":" in val:  # If there's a colon, treat it as time-like data, calling converting function
                        parsed_val = parse_time_to_seconds(val)
                        float_values.append(parsed_val)
                    else:
                        # Try to parse as a float, and not give terminal error
                        try:
                            float_values.append(float(val))
                        except ValueError:
                            float_values.append(float('nan'))
                else:
                    # Already a numeric type
                    float_values.append(float(val))

            #sets subplot title and style based of data`
            title = data_entry[0]
            x_values = laps
            adjusted_x = [x + place * width for x in x_values]
            ax.bar(adjusted_x, float_values, width, label=title)
            max_len = max(max_len, len(float_values))
            
        #creates subplots graph
        ax.set_title(f"{header} per Lap")
        ax.set_xlabel("Laps")
        ax.set_ylabel(header)
        ax.set_xticks(range(1, max_len + 1))
        ax.legend()
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
    plt.savefig("C:\\Users\\stree\\Downloads\\virtual environment for vs code\\final_plots\\Currentplot.png")
    print("file saved")    
    plt.tight_layout()
    plt.show()
    
#function putting it all together
def main():
    """
    Main function to run the analysis workflow.
    """

    #get user input for files wanted within data_files
    files_wanted, names_of_files = prompt_for_csv_files()
    
    if files_wanted == -1:
        print("No files selected. Exiting.")
        return


    # Read data from all files
    include_headers = True
    combined_data = []

    for f in files_wanted:
        file_data, file_headers = read_csv(f, include_headers)
        # Convert headers to lowercase for consistency
        file_headers = headers_to_lowercase(file_headers)

        # Clean headers and data
        file_headers, file_data = clean_headers_and_data(file_headers, file_data)

        combined_data.append((f, file_headers, file_data))

    # If no files were successfully read
    if not combined_data:
        print("No data loaded. Exiting.")
        return

    #Compute common headers across all files
    all_headers_sets = [set(d[1]) for d in combined_data]  # d[1] is the headers from each file
    common_headers = set.union(*all_headers_sets) if all_headers_sets else set()

    #Filter out headers that have no actual data across all files
    valid_headers = set()

    for h in common_headers:
        has_real_data = False
        # Check each file for this header
        for f, file_headers, file_data in combined_data:
            if h in file_headers:
                h_index = file_headers.index(h)
                # Check rows for meaningful data
                for row in file_data:
                    val = row[h_index].strip()
                    if val and val.lower() not in ("--", "na", "null", ""):
                        try:
                            # Try to parse as a number
                            float(val)
                            has_real_data = True
                            break
                        except ValueError:
                            # It's meaningful non-numeric data
                            has_real_data = True
                            break
            if has_real_data:
                break
        if has_real_data:
            valid_headers.add(h)

    common_headers = valid_headers

    if not common_headers:
        print("No headers with actual data found after filtering. Exiting.")
        return



    # Ask the user to choose headers from the common set
    valid_headers_list = list(valid_headers)

    #Calculate the number of columns and create rows for headers
    headers_per_row = 4
    header_lines = [valid_headers_list[i:i + headers_per_row] for i in range(0, len(valid_headers_list), headers_per_row)]

    print(styled_text("\nCommon headers available across all files:\n", color="magenta", bold=True))
    for line in header_lines:
        print("  ".join([styled_text(f"{header:<20}", color="cyan") for header in line]))

    data_to_compare = input(styled_text("Enter one or multiple headers separated by commas for comparison:\n>> ", color="magenta", bold=False)).strip()
    selected_headers = [h.strip() for h in data_to_compare.split(",") if h.strip() in common_headers]

    if not selected_headers:
        print("No valid common headers selected. Exiting.")
        return


    # Extract data for each chosen header from each file
    all_data_for_plot = []
    for header in selected_headers:
        count = 0
        # For each file, we ask for a lap range and extract the data for this header
        for f, headers, data in combined_data:
            name_of = names_of_files[count]
            count += 1
            sequence = prompt_for_lap_range(name_of, len(data))
            if sequence is None:
                # User couldn't provide a valid lap range, skip this file
                continue
            plot_data = extract_data_for_plot(headers, data, header, name_of[:-4], sequence)
            if plot_data:
                all_data_for_plot.append(plot_data)
    
    #adds some additional information to termal about functions running and data
    print()
    write_csv(all_data_for_plot, output_file="output.csv")
    print()
    averages, maxes = numpy_averages(all_data_for_plot)
    print(styled_text("The averages and max for the specified data:", color="green"))
    for i in range(len(averages)):
        print(styled_text(f"Data {(i+1)} average is {(averages[i]):0.2f} and max is {(maxes[i]):0.2f}", color="green"))
    print()
    
    # Ask user if they want to display data in one plot or multiple plots
    display_choice = input(styled_text("\nWould you like to display data in one plot or multiple plots (one/multiple)?\n>> ", color="magenta", bold=False)).strip().lower()
    if display_choice == "one":
        display_data_one_plot(all_data_for_plot)
    elif display_choice == "multiple":
        display_data_multiple_plots(all_data_for_plot)
    else:
        print("Invalid choice. Exiting.")



if __name__ == "__main__":
    main()
