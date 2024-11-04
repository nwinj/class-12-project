def show_stocks_by_industry(con,industry_name):
    cursor = con.cursor(dictionary=True)
    
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
def recommend_stocks_by_industry(con,industry_name=None):
    cursor = con.cursor(dictionary=True)
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
 
def stock_insights_industry_least_debt(con,sector_name):
    cursor = con.cursor()
    
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

def stock_insights_industry_best_yoy_growth(con,sector_name):
    cursor = con.cursor()
    
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

def stock_insights_industry_best_dividend_yield(con,sector_name):
    cursor = con.cursor()
    
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
