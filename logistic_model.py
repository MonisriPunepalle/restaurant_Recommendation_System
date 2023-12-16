import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Connect to SQLite database
conn = sqlite3.connect('instance/users.db')

# Query labeled data with not null sentiment column
labeled_data_query = "SELECT * FROM reviews WHERE sentiment IS NOT NULL;"
labeled_df = pd.read_sql_query(labeled_data_query, conn)

# Split labeled data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    labeled_df['reviews'], labeled_df['sentiment'], test_size=0.2, random_state=42
)

# TF-IDF vectorization for training data
tfidf_vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)

# Train the logistic regression model
logreg_model = LogisticRegression()
logreg_model.fit(X_train_tfidf, y_train)

# Query unlabeled data
unlabeled_data_query = "SELECT * FROM reviews WHERE sentiment IS NULL;"

unlabeled_df = pd.read_sql_query(unlabeled_data_query, conn)
#print(unlabeled_df)
# Check if there are unlabeled data
if not unlabeled_df.empty:
    # TF-IDF vectorization for unlabeled data
    X_unlabeled_tfidf = tfidf_vectorizer.transform(unlabeled_df['reviews'])

    # Make predictions on unlabeled data
    unlabeled_predictions = logreg_model.predict(X_unlabeled_tfidf)
    
    # Update the SQLite database with the predicted sentiments for unlabeled data
    conn.execute("BEGIN TRANSACTION;")
    for index, prediction in enumerate(unlabeled_predictions):
        review_id1 = unlabeled_df.at[index, 'id']  # Assuming 'id' is the primary key column
        conn.execute(f"UPDATE reviews SET SENTIMENT = {int(prediction)} WHERE id = '{review_id1}';")
    conn.execute("COMMIT;")
else:
    print("No unlabeled data present.")

# Close the database connection
conn.close()
