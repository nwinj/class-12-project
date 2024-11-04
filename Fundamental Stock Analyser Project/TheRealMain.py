import mysql.connector
import view
import insights
import classifier
import prosorter as p
import add_and_update as au
# Establish the connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345',
    database='stockanalysis'  
)




while True:
    print("                                   ")
    print("===================================")
    print("       STOCK ANALYZER MENU         ")
    print("===================================")
    print("1. View Stocks ")
    print("2. Top Market Recommendations")
    print("3. Industry Classifier")
    print("4. Pro Stock Sorter")
    print("5. Add and Update Company Data")
    print("6. Search Company By Name")
    print("7. Exit")
    print("===================================")
    print("                                   ")

    c = int(input("Please select an option (1-7): "))

    if c==1:
        insights.stock_insights(conn)
        
    elif c==2:
        insights.recommend_stocks(conn)
    

    elif c==3:
        while True:
            print("                                                   ")
            print("===================================================")
            print("             Industry Classifier                   ")
            print("===================================================")
            print("1. Display Stocks by Industry")
            print("2. Top Stock Recommendations by Industry")
            print("3. Industry Stocks with Lowest Debt-to-Equity")
            print("4. Industry Stocks with Best YoY Growth")
            print("5. Industry Stocks with Best Dividend Yield") 
            print("6. Go Back ")
            print("===================================================")
            print("                                                   ")
                
            c1=int(input("Please select an option (1-5): "))
            if c1 in [1,2,3,4,5]:
                industry_name = input("Enter Industry Name: ")

                if c1==1:
                    classifier.show_stocks_by_industry(conn,industry_name)
                elif c1==2:
                    classifier.recommend_stocks_by_industry(conn,industry_name=None)
                elif c1==3:
                    classifier.stock_insights_industry_least_debt(conn,industry_name)
                elif c1==4:
                    classifier.stock_insights_industry_best_yoy_growth(conn,industry_name)
                elif c1==5:
                    classifier.stock_insights_industry_best_dividend_yield(conn,industry_name)
            elif c1== 6:
                break
            else:
                print("Invalid Choice,Please Enter A Choice From Menu")
                
            
        
        
    elif c==4:
        while True:
            print("                                                   ")
            print("===================================================")
            print("                Pro-Stock-Sorter                   ")
            print("===================================================")
            print("1. Lowest Debt Stocks")
            print("2. Best Performing Growth Stocks")
            print("3. High Dividend Yield Stocks")
            print("4. Go Back ")
            print("===================================================")
            print("                                                   ")
                
            c1=int(input("Please select an option (1-4): "))
            if c1==1:
                p.stock_pro_top_least_debt(conn)
            elif c1==2:
                 p.stock_pro_top_best_yoy_growth(conn)
            elif c1==3:
                p.stock_pro_top_best_dividend_yield(conn)
            elif c1== 4:
                break
            else:
                print("Invalid Choice,Please Enter A Choice From Menu")
                
            
        
        
    elif c==5:
        while True:
            print("                                                   ")
            print("===================================================")
            print("                Add Or Update                      ")
            print("===================================================")
            print("1. Add New Company")
            print("2. Update Company")
            print("3. Go Back ")
            print("===================================================")
            print("                                                   ")
                
            c1=int(input("Please select an option (1-3): "))
            if c1 in [1,2]:
                co= input("Enter Company Name: ")
                m= input("Enter Market Cap: ")
                pe=input("Enter Pe Ratio: ")
                pb=input("Enter Pb Ratio: ")
                d=input("Enter Dividend: ")
                s=input("Enter Sector: ")
                de = input("Enter Debt To Equity Ratio: ")
                yoy = input("Enter Yoy Growth: ")
    
      
                if c1==1:
                    au.add_new_company(conn,co, m, pe, pb, d, s, de, yoy)
                elif c1==2:
                    au.update_company_data(conn,co, m=None, pe=None, pb=None, d=None, s=None, de=None, yoy=None)
            
            elif c1==3:
                break
            else:
                print("Invalid Choice,Please Enter A Choice From Menu")
        
        
    elif c==6:
        company_name=input("Enter Company Name: ").strip().lower()  # Take user input and convert to lowercase
        view.view_stock_detail_by_name(conn,company_name )  # Pass the connection object to the function
    elif c==7:
        exit()

        
    else:
        print("Invalid Choice,Please Enter A Choice From Menu")




# Close the connection after the operation is complete
conn.close()

