def stock_pro_top_least_debt(con):
    cursor = con.cursor()
    
    # Query to select top 5 companies ordered by debt-to-equity ratio
    z = """
        SELECT * 
        FROM stock
        ORDER BY dept_to_equity_ratio ASC
        LIMIT 5
    """
    cursor.execute(z)
    result = cursor.fetchall()

    # Define the headers and add 'Rank'
    headers = ['Rank', 'Company', 'Market Cap', 'PE Ratio', 'PB Ratio', 'Dividend Yield', 'Sector', 'Debt-To-Equity Ratio', 'YoY Growth']
    
    # Calculate maximum lengths for each column, handling rank separately
    max_lengths = [max(len(headers[0]), len(str(len(result))))]  # Max length for 'Rank' column
    max_lengths += [max(len(header), max(len(str(row[i - 1])) for row in result)) for i, header in enumerate(headers[1:], start=1)]

    # Display column headers with padding
    header_row = " | ".join(f"{header: <{max_lengths[i]}}" for i, header in enumerate(headers))
    print("\n" + header_row)
    print("-" * (sum(max_lengths) + 3 * (len(headers) - 1)))  # Underline for headers

    # Display the data with rank
    for idx, row in enumerate(result):
        formatted_row = " | ".join(f"{str(idx + 1): <{max_lengths[0]}}" if i == 0 else f"{str(item): <{max_lengths[i]}}" for i, item in enumerate([idx + 1] + list(row)))
        print(formatted_row)
    
    cursor.close()  # Close the cursor after use

def stock_pro_top_best_yoy_growth(con):
    cursor = con.cursor()
    
    # Query to select top 5 companies ordered by YoY growth in descending order
    z = """
        SELECT * 
        FROM stock
        ORDER BY yoy_growth DESC
        LIMIT 5
    """
    cursor.execute(z)
    result = cursor.fetchall()

    # Define the headers and add 'Rank'
    headers = ['Rank', 'Company', 'Market Cap', 'PE Ratio', 'PB Ratio', 'Dividend Yield', 'Sector', 'Debt-To-Equity Ratio', 'YoY Growth']
    
    # Calculate maximum lengths for each column, handling rank separately
    max_lengths = [max(len(headers[0]), len(str(len(result))))]  # Max length for 'Rank' column
    max_lengths += [max(len(header), max(len(str(row[i - 1])) for row in result)) for i, header in enumerate(headers[1:], start=1)]

    # Display column headers with padding
    header_row = " | ".join(f"{header: <{max_lengths[i]}}" for i, header in enumerate(headers))
    print("\n" + header_row)
    print("-" * (sum(max_lengths) + 3 * (len(headers) - 1)))  # Underline for headers

    # Display data with rank
    for idx, row in enumerate(result):
        formatted_row = " | ".join(f"{str(idx + 1): <{max_lengths[0]}}" if i == 0 else f"{str(item): <{max_lengths[i]}}" for i, item in enumerate([idx + 1] + list(row)))
        print(formatted_row)
    
    cursor.close()  # Close the cursor after use

def stock_pro_top_best_dividend_yield(con):
    cursor = con.cursor()
    
    # Query to select top 5 companies ordered by Dividend Yield in descending order
    z = """
        SELECT * 
        FROM stock
        ORDER BY Divy DESC
        LIMIT 5
    """
    cursor.execute(z)
    result = cursor.fetchall()

    # Define the headers and add 'Rank'
    headers = ['Rank', 'Company', 'Market Cap', 'PE Ratio', 'PB Ratio', 'Dividend Yield', 'Sector', 'Debt-To-Equity Ratio', 'YoY Growth']
    
    # Calculate maximum lengths for each column, handling rank separately
    max_lengths = [max(len(headers[0]), len(str(len(result))))]  # Max length for 'Rank' column
    max_lengths += [max(len(header), max(len(str(row[i - 1])) for row in result)) for i, header in enumerate(headers[1:], start=1)]

    # Display column headers with padding
    header_row = " | ".join(f"{header: <{max_lengths[i]}}" for i, header in enumerate(headers))
    print("\n" + header_row)
    print("-" * (sum(max_lengths) + 3 * (len(headers) - 1)))  # Underline for headers

    # Display data with rank
    for idx, row in enumerate(result):
        formatted_row = " | ".join(f"{str(idx + 1): <{max_lengths[0]}}" if i == 0 else f"{str(item): <{max_lengths[i]}}" for i, item in enumerate([idx + 1] + list(row)))
        print(formatted_row)
    
    cursor.close()  # Close the cursor after use
