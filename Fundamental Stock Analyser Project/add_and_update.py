def add_new_company(con,company_name, market_cap, pe_ratio, pb_ratio, dividend_yield, sector, debt_to_equity_ratio, yoy_growth):
    cursor = con.cursor()
    
    # SQL query to insert a new company into the stock table
    z = """
        INSERT INTO stock (company, `market_cap`, PEratio, PBratio, Divy, sector, dept_to_equity_ratio, yoy_growth)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    # Execute the query with the provided values
    try:
        cursor.execute(z, (company_name, market_cap, pe_ratio, pb_ratio, dividend_yield, sector, debt_to_equity_ratio, yoy_growth))
        con.commit()  # Commit the changes to the database
        print(f"Successfully added {company_name} to the database.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cursor.close()  # Close the cursor after use

# Call the function correctly

def update_company_data(con,company_name, market_cap=None, pe_ratio=None, pb_ratio=None, dividend_yield=None, sector=None, debt_to_equity_ratio=None, yoy_growth=None):
    cursor = con.cursor()
    
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
        updates.append("`market_cap` = %s")
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
        con.commit()  # Commit the changes to the database
        print(f"Successfully updated data for {company_name}.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cursor.close()  # Close the cursor after use
