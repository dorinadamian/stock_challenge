import os
import pandas as pd
import random

exchange = "LSE"
folder_path = os.path.join(os.getcwd(), exchange)

IDX_ID = 0    # index of Stock-ID column
IDX_TIME = 1  # index of timestamp column
IDX_PRICE = 2 # index of stock price column

def extract_data_points(csv_file_path):
    """
    Extracts 30 consecutive data points from a random timestamp

    Parameter:
        csv_file_path (str): the path of a stock file in CSV format

    Returns:
        The 30 consecutive data points
        None: if errors encountered
    """
    no_data_to_extract = 30
    try:
        # import csv file
        df = pd.read_csv(csv_file_path, header=None)
    except pd.errors.EmptyDataError:
        print(f"Error: {csv_file_path} is empty.")
        return None
    except pd.errors.ParserError:
        print(f"Error: {csv_file_path} contains invalid CSV format.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while reading {csv_file_path}: '{e}'")
        return None
    
    if len(df) < no_data_to_extract:
        raise ValueError(f"{csv_file_path} doesn't have enough data.")

    rand_timestamp = random.randint(0, len(df) - no_data_to_extract)
    consecutive_data = df.iloc[rand_timestamp:rand_timestamp + no_data_to_extract]

    return consecutive_data
# end of extract_data_points

def find_outliers(data_values):
    """
    Searches for outliers in the given data

    Parameter: 
        data_values (DataFrame): the path of a stock file in CSV format

    Returns:
        List of outliers
    """
    mean = round(data_values[IDX_PRICE].mean(), 2)
    standard_dev = round(data_values[IDX_PRICE].std(), 2)
    # create empty list to hold outliers' corresponding rows
    outliers = []

    for idx, data in data_values.iterrows():
        if data[IDX_PRICE] > mean + 2 * standard_dev:
            threshold = mean + 2 * standard_dev
            out_row = [data[IDX_ID], data[IDX_TIME], data[IDX_PRICE], mean, round(data[IDX_PRICE] - mean, 2),
                       round(100 * ((data[IDX_PRICE] - mean - 2 * standard_dev) / threshold), 2)]
            outliers.append(out_row)

        elif data[IDX_PRICE] < mean - 2 * standard_dev:
            threshold = mean - 2 * standard_dev
            out_row = [data[IDX_ID], data[IDX_TIME], data[IDX_PRICE], mean, round(data[IDX_PRICE] - mean, 2),
                       round(100 * ((mean - 2 * standard_dev - data[IDX_PRICE]) / threshold), 2)]
            outliers.append(out_row)

    return outliers
# end of find_outliers

def main(no_of_files):
    if type(folder_path) != str:
        raise TypeError("The 'folder_path' parameter must be a string!")
    if type(no_of_files) != int:
        raise TypeError("The 'no_of_files' parameter must be an integer!")
    elif no_of_files <= 0:
        raise ValueError("The 'no_of_files' parameter must be a positive integer!")
    if not os.path.exists(folder_path):
        raise Exception(f"The path '{folder_path}' doesn't exist.")

    csv_list = [] # list to include the .csv files

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        # check if the item from folder is a valid .csv file 
        if os.path.isfile(item_path) and item.endswith(".csv"):
            csv_list.append(item)
        if len(csv_list) == no_of_files:
            break
    
    # check if there are no csv files
    if not csv_list:
        raise ValueError(f"There is no '.csv' file in {folder_path}.")

    for csv_file in csv_list:
        extracted_data = extract_data_points(os.path.join(folder_path, csv_file))
        # search for outliers only if 30 consecutive data points were found
        if (extracted_data is not None) and (not extracted_data.empty):
            outliers = find_outliers(extracted_data)
            outliers = pd.DataFrame(outliers)
            # create the corresponding '.csv' file in the folder of interest after isolating the outliers
            outliers.to_csv(f"{os.path.join(folder_path, extracted_data[IDX_ID].iloc[0])}_extracted.csv", index=False, header=None)
# end of main

if __name__ == "__main__":
    input_files = 2
    main(input_files)
