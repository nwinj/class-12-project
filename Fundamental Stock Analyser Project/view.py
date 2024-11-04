def view_stock_detail_by_name(con, company_name):
    # Create a cursor object
    cursor = con.cursor()

    # Fetch all company names from the table in lowercase
    cursor.execute("SELECT LOWER(company) FROM stock")
    company_names = {item[0] for item in cursor.fetchall()}  # Use a set for faster lookups

    # Convert input company name to lowercase
    company_name_lower = company_name.strip().lower()

    if company_name_lower in company_names:
        # Fetch details of the entered company using case-insensitive comparison
        cursor.execute("SELECT * FROM stock WHERE LOWER(company) = %s", (company_name_lower,))
        company_details = cursor.fetchall()

        # Get column names for printing
        column_names = [desc[0] for desc in cursor.description]

        # Print company details in a descriptive format
        print("\nCompany Details:")
        for detail in company_details:
            for i, value in enumerate(detail):
                print(f"{column_names[i]}: {value}")
            print("\n" + "-" * 50)  # Separator line between entries if there are multiple
    else:
        print("Company Not Found!")

    # Close the cursor
    cursor.close()
