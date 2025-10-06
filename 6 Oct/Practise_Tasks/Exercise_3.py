import pandas as pd
import logging

# Setup logging
logging.basicConfig(filename='sales.log', level=logging.INFO,
                    format='%(levelname)s - %(message)s')

filename = 'sales.csv'

try:
    # Read CSV file
    df = pd.read_csv(filename)

    # Ensure 'price' and 'quantity' are numeric
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')

    # Check for missing numeric values
    if df['price'].isnull().any() or df['quantity'].isnull().any():
        raise ValueError("CSV contains non-numeric values in 'price' or 'quantity'.")

    # Calculate total sales
    total_sales = []
    for i in range(len(df)):
        total = df['quantity'].iloc[i] * df['price'].iloc[i]
        total_sales.append(int(total))  # Convert from np.int64 to regular int

    # Print and log the total sales
    print("Total Sales per item:")
    for i in range(len(df)):
        product = df['product'].iloc[i]
        total = total_sales[i]
        print(f"{product} total = {total}")
        logging.info(f"{product} total sales = {total}")

except FileNotFoundError:
    print(f"Error: The file '{filename}' does not exist.")
    logging.error(f"File not found: {filename}")

except ValueError as ve:
    print(f"Invalid data: {ve}")
    logging.error(f"Invalid data in CSV: {ve}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
    logging.error(f"Unexpected error: {e}")