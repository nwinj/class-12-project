Mysql Database
![image](https://github.com/user-attachments/assets/944f105c-e2b9-4111-8762-c947f286739a)
![image](https://github.com/user-attachments/assets/ab336bbd-1dea-4737-923b-196326a11d17)
![image](https://github.com/user-attachments/assets/b6519dd5-0d0b-442a-94d4-d5a45ff45207)


## 1. Creating Table
```sql
CREATE TABLE stock (
    company VARCHAR(200) NOT NULL,
    market_cap ENUM('largecap', 'midcap', 'smallcap') NOT NULL,
    PEratio FLOAT NULL,
    PBratio FLOAT NULL,
    Div FLOAT NULL,
    sector VARCHAR(100) NULL,
    dept_to_equity_ratio FLOAT NULL,
    yoy_growth DECIMAL(7,2) NULL
)
