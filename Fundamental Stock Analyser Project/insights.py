def stock_insights(con):
    cursor = con.cursor()
    
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



    

def recommend_stocks(con):

    cursor = con.cursor(dictionary=True)
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
