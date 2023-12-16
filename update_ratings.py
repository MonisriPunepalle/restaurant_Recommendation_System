import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('instance/users.db')

# Execute the sentiment ratio query for restaurants
restaurant_sentiment_query = """
    SELECT 
        r.restaurant_id,
        ROUND((CAST(SUM(CASE WHEN r.sentiment = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*)) * 5,1) AS sentiment_ratio
    FROM reviews r
    GROUP BY r.restaurant_id;
"""

# Update the 'restaurant' table with sentiment ratios
restaurant_cursor = conn.execute(restaurant_sentiment_query)
for restaurant_row in restaurant_cursor.fetchall():
    restaurant_id, sentiment_ratio = restaurant_row
    restaurant_update_query = f"UPDATE restaurant SET restaurant_rating = {sentiment_ratio} WHERE restaurant_id = '{restaurant_id}';"
    conn.execute(restaurant_update_query)

# Execute the sentiment ratio query for menu items
menu_item_sentiment_query = """
    SELECT 
        r.restaurant_id,
        r.MENU_ITEM_ID,
        ROUND((CAST(SUM(CASE WHEN r.sentiment = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*)) * 5,1) AS sentiment_ratio
    FROM reviews r
    GROUP BY r.restaurant_id, r.menu_item_id;
"""

# Update the 'menu_item_ratings' table with sentiment ratios
menu_item_cursor = conn.execute(menu_item_sentiment_query)
for menu_item_row in menu_item_cursor.fetchall():
    restaurant_id, menu_item_id, sentiment_ratio = menu_item_row
    menu_item_update_query = f"UPDATE menu_item SET menu_item_rating = {sentiment_ratio} WHERE restaurant_id= '{restaurant_id}' and menu_item_id = '{menu_item_id}';"
    conn.execute(menu_item_update_query)

# Commit the changes and close the connection
conn.commit()
conn.close()
