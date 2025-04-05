import pandas as pd

def load_scraped_products(filepath = '../scrapers/data/scraped_products.csv'):
    df = pd.read_csv(filepath)
    df['price'] = df['price'].str.replace('Â£', '').astype(float)
    return df

def recommend_top_books(df, top_n=5):
    # Recommend highest rated and cheapest books
    rating_order = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    df['rating_score'] = df['rating'].map(rating_order)
    recommended = df.sort_values(by=['rating_score', 'price'], ascending=[False, True]).head(top_n)
    return recommended[['title', 'price', 'rating', 'product_url']]

if __name__ == "__main__":
    products = load_scraped_products()
    top_recommendations = recommend_top_books(products)

    print("\n📚 Recommended Books:")
    for i, row in top_recommendations.iterrows():
        print(f"- {row['title']} | {row['price']} | Rating: {row['rating']} | Link: {row['product_url']}")
