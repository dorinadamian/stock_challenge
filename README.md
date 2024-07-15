# Coding Challenge
Author: Dorina Damian

Description: This project provides a solution for analyzing stock price data from CSV files. It focuses on extracting a random sequence of data points and identifying outliers based on statistical measures.
# Requirements
- python 3.x
- pandas library

  If pandas not installed, please use the following command:
  - Windows: pip install pandas
  - Linux: pip3 install pandas

# Getting Started
The folder containing the CSV files SHALL be located in the current working directory and should be named according to the stock exchange (e.g., "NASDAQ"). Each CSV file should contain data in the following format:
- Stock-ID (Ticker)
- Timestamp (dd-mm-yyyy)
- Stock price value

The "exchange" variable SHALL hold the name of stock exchange folder.

Set the desired number of input files to be processed ("input_files").

Run the script.

# Notes
Ensure that the CSV files are properly formatted and contain enough data points.

Adjust the "input_files" variable to match the desired number of files to process.

The outliers are saved in the same folder as the original CSV files with the suffix "_extracted.csv".
