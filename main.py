import mysql.connector

# Establish the connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345',
    database='stockanalysis'  # Ensure the database exists
)

def stock_insights():
    cursor = conn.cursor()
    
    # Query to select all data from the stock table
    z = "SELECT * FROM stock"  
    cursor.execute(z)
    result = cursor.fetchall()

    # Define the headers
    headers = ['Company Name', 'Market Cap', 'P/E Ratio', 'P/B Ratio', 'Dividend Yield', 'Industry', 'Debt-To-Equity ratio', 'YoY Growth']
    
    # Calculate the maximum lengths for each column
    max_lengths = [max(len(header), max(len(str(row[i])) for row in result)) for i, header in enumerate(headers)]

    # Display column headers with padding
    header_row = " | ".join(f"{header: <{max_lengths[i]}}" for i, header in enumerate(headers))
    print("\n" + header_row)
    print("-" * (sum(max_lengths) + 3 * (len(headers) - 1)))  # Underline for headers

    # Display the data with sufficient spacing
    for row in result:
        formatted_row = " | ".join(f"{str(item): <{max_lengths[i]}}" for i, item in enumerate(row))
        print(formatted_row)
    
    cursor.close()  # Close the cursor after use



    

def recommend_stocks():

    cursor = conn.cursor(dictionary=True)
    recommendations = {}
    
    # Fetch all stock symbols from the 'stock' table
    cursor.execute("SELECT company FROM stock")
    stock_symbols = [row['company'] for row in cursor.fetchall()]
    
    for stock in stock_symbols:
        # Fetch data for each stock
        query = f"SELECT PEratio, PBratio, dept_to_equity_ratio, Divy, yoy_growth FROM stock WHERE company='{stock}'"
        cursor.execute(query)
        data = cursor.fetchone()
        
        if data:
            # Normalization ranges
            pe_min, pe_max = 5, 35
            pb_min, pb_max = 0.5, 5
            de_max = 2
            div_min = 0.5
            yoy_min, yoy_max = -10, 20

            # Normalized values - convert Decimal to float
            normalized_pe = float(data['PEratio'] - pe_min) / (pe_max - pe_min)
            normalized_pb = float(data['PBratio'] - pb_min) / (pb_max - pb_min)
            normalized_de = 1 - min(float(data['dept_to_equity_ratio']) / de_max, 1)
            normalized_div = float(data['Divy'] - div_min) / (5 - div_min)
            normalized_yoy = float(data['yoy_growth'] - yoy_min) / (yoy_max - yoy_min)

            # Weighted score calculation
            total_score = (0.25 * normalized_pe +
                           0.20 * normalized_pb +
                           0.20 * normalized_de +
                           0.15 * normalized_div +
                           0.20 * normalized_yoy)
            
            # Store the score
            recommendations[stock] = total_score

    # Sort stocks by score in descending order
    sorted_stocks = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)

    # Display the top 3 recommendations
    print("\nTop 3 Stock Recommendations (Ranked):")
    for rank, (stock, score) in enumerate(sorted_stocks[:3], start=1):  # Limit to top 3
        print(f"{rank}. {stock} - Score: {score:.2f}")

    cursor.close()



def show_stocks_by_industry(industry_name):
    cursor = conn.cursor(dictionary=True)
    
    # Fetch column names for debugging purposes
    cursor.execute("SHOW COLUMNS FROM stock")
    columns = cursor.fetchall()
    

    # Query to fetch stocks for the specified industry
    query = "SELECT * FROM stock WHERE sector = %s"
    
    cursor.execute(query, (industry_name,))
    result = cursor.fetchall()

    # Check if there are any results
    if not result:
        print(f"No stocks found for the industry: {industry_name}")
    else:
        # Define the headers as per your request
        headers = ['Company Name', 'Market Cap', 'P/E Ratio', 'P/B Ratio', 'Dividend Yield', 'Industry', 'Debt-To-Equity ratio', 'YoY Growth']

        # Calculate maximum lengths for each column for formatting
        max_lengths = [len(header) for header in headers]  # Start with header lengths

        for row in result:
            # Map actual column names to the headers
            column_mapping = {
                'company': 'Company Name',
                'market cap': 'Market Cap',
                'PEratio': 'P/E Ratio',
                'PBratio': 'P/B Ratio',
                'Divy': 'Dividend Yield',
                'sector': 'Industry',
                'dept_to_equity_ratio': 'Debt-To-Equity ratio',
                'yoy_growth': 'YoY Growth'
            }
            for i, header in enumerate(headers):
                actual_column_name = list(column_mapping.keys())[list(column_mapping.values()).index(header)]
                max_lengths[i] = max(max_lengths[i], len(str(row[actual_column_name])))  # Update lengths based on row data

        # Display column headers with padding
        header_row = " | ".join(f"{header: <{max_lengths[i]}}" for i, header in enumerate(headers))
        print("\n" + header_row)
        print("-" * (sum(max_lengths) + 3 * (len(headers) - 1)))  # Underline for headers

        # Display the stock details with sufficient spacing
        for row in result:
            formatted_row = " | ".join(f"{str(row[actual_column_name]): <{max_lengths[i]}}" 
                                        for i, header in enumerate(headers) 
                                        for actual_column_name in [list(column_mapping.keys())[list(column_mapping.values()).index(header)]])
            print(formatted_row)
    
    cursor.close()  # Close the cursor after use
def recommend_stocks_by_industry(industry_name=None):
    cursor = conn.cursor(dictionary=True)
    recommendations = {}

    # Modify query to filter by industry if an industry_name is provided
    if industry_name:
        cursor.execute("SELECT company FROM stock WHERE sector = %s", (industry_name,))
    else:
        cursor.execute("SELECT company FROM stock")
    
    stock_symbols = [row['company'] for row in cursor.fetchall()]
    
    for stock in stock_symbols:
        # Fetch data for each stock
        query = f"SELECT PEratio, PBratio, dept_to_equity_ratio, Divy, yoy_growth FROM stock WHERE company='{stock}'"
        cursor.execute(query)
        data = cursor.fetchone()
        
        if data:
            # Normalization ranges
            pe_min, pe_max = 5, 35
            pb_min, pb_max = 0.5, 5
            de_max = 2
            div_min = 0.5
            yoy_min, yoy_max = -10, 20

            # Normalized values - convert Decimal to float
            normalized_pe = float(data['PEratio'] - pe_min) / (pe_max - pe_min)
            normalized_pb = float(data['PBratio'] - pb_min) / (pb_max - pb_min)
            normalized_de = 1 - min(float(data['dept_to_equity_ratio']) / de_max, 1)
            normalized_div = float(data['Divy'] - div_min) / (5 - div_min)
            normalized_yoy = float(data['yoy_growth'] - yoy_min) / (yoy_max - yoy_min)

            # Weighted score calculation
            total_score = (0.25 * normalized_pe +
                           0.20 * normalized_pb +
                           0.20 * normalized_de +
                           0.15 * normalized_div +
                           0.20 * normalized_yoy)
            
            # Store the score
            recommendations[stock] = total_score

    # Sort stocks by score in descending order
    sorted_stocks = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)

    # Display the top 3 recommendations
    if sorted_stocks:
        print(f"\nTop 3 Stock Recommendations for {industry_name if industry_name else 'all industries'} (Ranked):")
        for rank, (stock, score) in enumerate(sorted_stocks[:3], start=1):  # Limit to top 3
            print(f"{rank}. {stock} - Score: {score:.2f}")
    else:
        print(f"No stocks found for the industry: {industry_name}")

    cursor.close()
 
def stock_insights_industry_least_debt(sector_name):
    cursor = conn.cursor()
    
    # Query to select data from the stock table for companies in the specified sector, ordered by debt-to-equity ratio
    z = """
        SELECT * 
        FROM stock
        WHERE sector = %s
        ORDER BY dept_to_equity_ratio ASC
    """
    cursor.execute(z, (sector_name,))
    result = cursor.fetchall()

    # Define the headers according to your table structure and add 'Rank'
    headers = ['Rank', 'Company', 'Market Cap', 'PE Ratio', 'PB Ratio', 'Dividend Yield', 'Sector', 'Debt-To-Equity Ratio', 'YoY Growth']
    
    # Calculate the maximum lengths for each column, handling rank separately
    max_lengths = [max(len(headers[0]), len(str(len(result))))]  # Max length for 'Rank' column
    max_lengths += [max(len(header), max(len(str(row[i - 1])) for row in result)) for i, header in enumerate(headers[1:], start=1)]

    # Display column headers with padding
    header_row = " | ".join(f"{header: <{max_lengths[i]}}" for i, header in enumerate(headers))
    print("\n" + header_row)
    print("-" * (sum(max_lengths) + 3 * (len(headers) - 1)))  # Underline for headers

    # Display the data with sufficient spacing and rank
    for idx, row in enumerate(result):
        formatted_row = " | ".join(f"{str(idx + 1): <{max_lengths[0]}}" if i == 0 else f"{str(item): <{max_lengths[i]}}" for i, item in enumerate([idx + 1] + list(row)))
        print(formatted_row)
    
    cursor.close()  # Close the cursor after use

def stock_insights_industry_best_yoy_growth(sector_name):
    cursor = conn.cursor()
    
    # Query to select data from the stock table for companies in the specified sector, ordered by YoY growth in descending order
    z = """
        SELECT * 
        FROM stock
        WHERE sector = %s
        ORDER BY yoy_growth DESC
    """
    cursor.execute(z, (sector_name,))
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

def stock_insights_industry_best_dividend_yield(sector_name):
    cursor = conn.cursor()
    
    # Query to select data from the stock table for companies in the specified sector, ordered by Dividend Yield in descending order
    z = """
        SELECT * 
        FROM stock
        WHERE sector = %s
        ORDER BY Divy DESC
    """
    cursor.execute(z, (sector_name,))
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

def stock_pro_top_least_debt():
    cursor = conn.cursor()
    
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

def stock_pro_top_best_yoy_growth():
    cursor = conn.cursor()
    
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

def stock_pro_top_best_dividend_yield():
    cursor = conn.cursor()
    
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



def add_new_company(company_name, market_cap, pe_ratio, pb_ratio, dividend_yield, sector, debt_to_equity_ratio, yoy_growth):
    cursor = conn.cursor()
    
    # SQL query to insert a new company into the stock table
    z = """
        INSERT INTO stock (company, `market cap`, PEratio, PBratio, Divy, sector, dept_to_equity_ratio, yoy_growth)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    # Execute the query with the provided values
    try:
        cursor.execute(z, (company_name, market_cap, pe_ratio, pb_ratio, dividend_yield, sector, debt_to_equity_ratio, yoy_growth))
        conn.commit()  # Commit the changes to the database
        print(f"Successfully added {company_name} to the database.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cursor.close()  # Close the cursor after use

# Call the function correctly

def update_company_data(company_name, market_cap=None, pe_ratio=None, pb_ratio=None, dividend_yield=None, sector=None, debt_to_equity_ratio=None, yoy_growth=None):
    cursor = conn.cursor()
    
    # Check if the company exists
    check_query = "SELECT COUNT(*) FROM stock WHERE company = %s"
    cursor.execute(check_query, (company_name,))
    company_exists = cursor.fetchone()[0] > 0

    if not company_exists:
        print(f"Company '{company_name}' not found.")
        cursor.close()  # Close the cursor before returning
        return

    # Start building the update query
    updates = []
    params = []

    # Prepare the SQL query with dynamic columns to update
    if market_cap is not None:
        updates.append("`market cap` = %s")
        params.append(market_cap)
    
    if pe_ratio is not None:
        updates.append("PEratio = %s")
        params.append(pe_ratio)
    
    if pb_ratio is not None:
        updates.append("PBratio = %s")
        params.append(pb_ratio)

    if dividend_yield is not None:
        updates.append("Divy = %s")
        params.append(dividend_yield)
    
    if sector is not None:
        updates.append("sector = %s")
        params.append(sector)

    if debt_to_equity_ratio is not None:
        updates.append("dept_to_equity_ratio = %s")
        params.append(debt_to_equity_ratio)

    if yoy_growth is not None:
        updates.append("yoy_growth = %s")
        params.append(yoy_growth)

    # Ensure there's at least one column to update
    if not updates:
        print("No data provided to update.")
        cursor.close()  # Close the cursor before returning
        return

    # Combine updates into a single string
    update_string = ", ".join(updates)
    
    # SQL query to update the company data
    z = f"""
        UPDATE stock
        SET {update_string}
        WHERE company = %s
    """
    params.append(company_name)  # Append the company name to the parameters

    # Execute the query
    try:
        cursor.execute(z, params)
        conn.commit()  # Commit the changes to the database
        print(f"Successfully updated data for {company_name}.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cursor.close()  # Close the cursor after use

def view_stock_detail_by_name ():
    # Create a cursor object
    mycursor = conn.cursor()

    # Fetch all company names from the table in lowercase
    mycursor.execute("SELECT LOWER(company) FROM stock")
    company_names = {item[0] for item in mycursor.fetchall()}  # Use a set for faster lookups

    while True:
        # Take user input and convert to lowercase
        company_name = input("Enter Company Name: ").strip().lower()

        if company_name in company_names:
            # Fetch details of the entered company using case-insensitive comparison
            mycursor.execute("SELECT * FROM stock WHERE LOWER(company) = %s", (company_name,))
            company_details = mycursor.fetchall()

            # Get column names for printing
            column_names = [desc[0] for desc in mycursor.description]

            # Print company details in a descriptive format
            print("\nCompany Details:")
            for detail in company_details:
                for i, value in enumerate(detail):
                    print(f"{column_names[i]}: {value}")
                print("\n" + "-" * 50)  # Separator line between entries if there are multiple

            break  # Exit the loop if the company is found
        else:
            print("Company Not Found! Please try again.")

    # Close the cursor and connection
    mycursor.close()
    conn.close()