--------------------------------------------------------------------------------
Test Case 1: What is the total monthly spend?
--------------------------------------------------------------------------------

✅ SQL Generated:
SELECT SUM("Monthly_Spend"::INTEGER) as total_monthly_spend FROM tbl_695ff7b55645834edb877af3

📝 Explanation:
This query calculates the total monthly spend by summing the values in the 'Monthly_Spend' column, which is cast to INTEGER for accurate aggregation.

--------------------------------------------------------------------------------
Test Case 2: How many vendors are there for each risk level?
--------------------------------------------------------------------------------

✅ SQL Generated:
SELECT "Risk_Level", COUNT(DISTINCT "Name") as vendor_count FROM tbl_695ff7b55645834edb877af3 GROUP BY "Risk_Level" ORDER BY "Risk_Level"

📝 Explanation:
This query counts the distinct vendors for each risk level by grouping the records based on the Risk Level and counting the unique names of the vendors.

--------------------------------------------------------------------------------
Test Case 3: What is the average outstanding amount by risk level?
--------------------------------------------------------------------------------

✅ SQL Generated:
SELECT "Risk_Level", AVG("Outstanding"::INTEGER) as average_outstanding FROM tbl_695ff7b55645834edb877af3 GROUP BY "Risk_Level" ORDER BY "Risk_Level"

📝 Explanation:
This query calculates the average outstanding amount grouped by risk level, providing insights into the financial status associated with each risk category.

--------------------------------------------------------------------------------
Test Case 4: Which categories are available?
--------------------------------------------------------------------------------

✅ SQL Generated:
SELECT DISTINCT "Category" FROM tbl_695ff7b55645834edb877af3 ORDER BY "Category"

📝 Explanation:
This query retrieves all unique categories from the dataset in alphabetical order.

--------------------------------------------------------------------------------
Test Case 5: Show me top 5 vendors with highest outstanding amounts
--------------------------------------------------------------------------------

✅ SQL Generated:
SELECT "Name", "Outstanding"::INTEGER as outstanding_amount FROM tbl_695ff7b55645834edb877af3 ORDER BY "Outstanding"::INTEGER DESC LIMIT 5

📝 Explanation:
This query retrieves the top 5 vendors with the highest outstanding amounts, sorted in descending order.

--------------------------------------------------------------------------------
Test Case 6: What is the total outstanding for high-risk vendors?
--------------------------------------------------------------------------------

✅ SQL Generated:
SELECT SUM("Outstanding"::INTEGER) as total_outstanding FROM tbl_695ff7b55645834edb877af3 WHERE "Risk Level" = 'high'

📝 Explanation:
This query calculates the total outstanding amount for all vendors classified as high risk.

--------------------------------------------------------------------------------
Test Case 7: List all vendors in the Purchases category
--------------------------------------------------------------------------------

✅ SQL Generated:
SELECT DISTINCT "Name" FROM tbl_695ff7b55645834edb877af3 WHERE "Category" = 'Purchases'

📝 Explanation:
This query retrieves all unique vendors from the dataset that fall under the 'Purchases' category.

--------------------------------------------------------------------------------
Test Case 8: What is the average number of days by category?
--------------------------------------------------------------------------------

✅ SQL Generated:
SELECT "Category", AVG("Days"::INTEGER) as average_days FROM tbl_695ff7b55645834edb877af3 GROUP BY "Category" ORDER BY "Category"

📝 Explanation:
This query calculates the average number of days for each expense category by grouping the records based on the Category column.

--------------------------------------------------------------------------------
Test Case 9: Which vendor has the maximum monthly spend?
--------------------------------------------------------------------------------

✅ SQL Generated:
SELECT "Name", MAX("Monthly Spend"::INTEGER) as max_monthly_spend FROM tbl_695ff7b55645834edb877af3 GROUP BY "Name" ORDER BY max_monthly_spend DESC LIMIT 1

📝 Explanation:
This query retrieves the vendor with the maximum monthly spend by grouping the records by vendor name and selecting the maximum monthly spend, sorted in descending order to get the top result.

--------------------------------------------------------------------------------
Test Case 10: How many sites are managed by each risk level?
--------------------------------------------------------------------------------

✅ SQL Generated:
SELECT "Risk_Level", COUNT("Sites") as site_count FROM tbl_695ff7b55645834edb877af3 GROUP BY "Risk_Level" ORDER BY site_count DESC

📝 Explanation:
This query counts the number of sites managed for each risk level by grouping the records based on the Risk Level and counting the Sites associated with each level.

--------------------------------------------------------------------------------
Test Case 11: What is the total outstanding amount by category?
--------------------------------------------------------------------------------

✅ SQL Generated:
SELECT "Category", SUM("Outstanding"::INTEGER) as total_outstanding FROM tbl_695ff7b55645834edb877af3 GROUP BY "Category" ORDER BY total_outstanding DESC

📝 Explanation:
This query calculates the total outstanding amount for each category by summing the Outstanding amounts, grouping the results by Category, and ordering them in descending order of total outstanding.

--------------------------------------------------------------------------------
Test Case 12: Show vendors with outstanding amount greater than 500000
--------------------------------------------------------------------------------

✅ SQL Generated:
SELECT "Name", "Outstanding"::INTEGER as outstanding_amount FROM tbl_695ff7b55645834edb877af3 WHERE "Outstanding"::INTEGER > 500000

📝 Explanation:
This query retrieves the names of vendors with outstanding amounts greater than 500,000, ensuring the outstanding amounts are treated as integers for accurate comparison.

--------------------------------------------------------------------------------
Test Case 13: What is the distribution of vendors across different categories?
--------------------------------------------------------------------------------

✅ SQL Generated:
SELECT "Category", COUNT(DISTINCT "Name") as vendor_count FROM tbl_695ff7b55645834edb877af3 GROUP BY "Category" ORDER BY vendor_count DESC

📝 Explanation:
This query groups the records by Category and counts the distinct vendors (Name) in each category, providing the distribution of vendors across different categories.

--------------------------------------------------------------------------------
Test Case 14: Calculate the average monthly spend for each category
--------------------------------------------------------------------------------

✅ SQL Generated:
SELECT "Category", AVG("Monthly_Spend"::INTEGER) as avg_monthly_spend FROM tbl_695ff7b55645834edb877af3 GROUP BY "Category" ORDER BY "Category"

📝 Explanation:
This query calculates the average monthly spend for each category by grouping the records based on the Category column and averaging the Monthly Spend.

--------------------------------------------------------------------------------
Test Case 15: Which risk level has the highest total outstanding?
--------------------------------------------------------------------------------

✅ SQL Generated:
SELECT "Risk_Level", SUM("Outstanding"::INTEGER) as total_outstanding FROM tbl_695ff7b55645834edb877af3 GROUP BY "Risk_Level" ORDER BY total_outstanding DESC LIMIT 1

📝 Explanation:
This query groups the records by Risk Level and sums the Outstanding amounts for each risk category, then orders the results in descending order to retrieve the risk level with the highest total outstanding.
