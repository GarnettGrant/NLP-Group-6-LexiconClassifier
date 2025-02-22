import os
import pandas as pd
import json
import matplotlib.pyplot as plt

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "Software_5.json")

# Read the JSON file line by line into a list
data = []
with open(file_path, "r", encoding="utf-8") as f:
    for line in f:
        data.append(json.loads(line))

# Convert to DataFrame
df = pd.DataFrame(data)

# Display basic info
print(df.info())  
print(df.head())  

# (a) Counts, averages

# Count total number of reviews
total_reviews = len(df)

# Count unique products 
unique_products = df['asin'].nunique() if 'asin' in df.columns else None

# Count unique users 
unique_users = df['reviewerID'].nunique() if 'reviewerID' in df.columns else None

# Compute average reviews per user
avg_reviews_per_user = total_reviews / unique_users if unique_users else None

# Print results
print(f"Total Reviews: {total_reviews}")
print(f"Unique Products: {unique_products}")
print(f"Unique Users: {unique_users}")
print(f"Avg Reviews per User: {avg_reviews_per_user}")

# (b) Distribution of the number of reviews across products
if 'asin' in df.columns:
    review_count_per_product = df.groupby('asin')['reviewerID'].count()
    plt.figure(figsize=(10,5))
    plt.hist(review_count_per_product, bins=50, edgecolor='black')
    plt.xlabel('Number of Reviews per Product')
    plt.ylabel('Frequency')
    plt.title('Distribution of Reviews Across Products')
    plt.show()

# (c) Distribution of reviews per product
if 'asin' in df.columns:
    product_review_distribution = review_count_per_product.describe()
    print("Product Review Distribution Summary:")
    print(product_review_distribution)

# (d) Distribution of Reviews Per User
if 'reviewerID' in df.columns:
    review_count_per_user = df.groupby('reviewerID')['asin'].count()
    user_review_distribution = review_count_per_user.describe()
    print("User Review Distribution Summary:")
    print(user_review_distribution)

    # Visualize user review distribution
    plt.figure(figsize=(10,5))
    plt.hist(review_count_per_user, bins=50, edgecolor='black', log=True)
    plt.xlabel('Number of Reviews per User')
    plt.ylabel('Frequency (Log Scale)')
    plt.title('Distribution of Reviews Per User')
    plt.show()

# (e) Review lengths and outliers
if 'reviewText' in df.columns:
    df['review_length'] = df['reviewText'].apply(lambda x: len(x.split()) if isinstance(x, str) else 0)
    print("Review Length Summary:")
    print(df['review_length'].describe())

    # Plot review length distribution
    plt.figure(figsize=(10,5))
    plt.hist(df['review_length'], bins=50, edgecolor='black', log=True)
    plt.xlabel('Review Length (Word Count)')
    plt.ylabel('Frequency (Log Scale)')
    plt.title('Distribution of Review Lengths')
    plt.show()

# (f) Identify outliers in review length
q1 = df['review_length'].quantile(0.25)
q3 = df['review_length'].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

outliers = df[(df['review_length'] < lower_bound) | (df['review_length'] > upper_bound)]
print(f"Number of Review Length Outliers: {len(outliers)}")

# (g) Check for duplicate reviews
if 'reviewText' in df.columns:
    duplicate_reviews = df.duplicated(subset=['reviewerID', 'asin', 'reviewText'], keep=False)
    num_duplicates = duplicate_reviews.sum()
    print(f"Number of Duplicate Reviews: {num_duplicates}")
    
    # Display some duplicate entries if they exist
    if num_duplicates > 0:
        print(df[duplicate_reviews].head(10))
