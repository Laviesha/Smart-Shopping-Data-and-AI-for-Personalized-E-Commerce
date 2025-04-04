# from flask import Flask, request, jsonify
# from recommendation import find_similar_products

# app = Flask(__name__)

# @app.route("/recommend", methods=["GET"])
# def recommend():
#     query = request.args.get("query", "")
#     recommendations = find_similar_products(query)
#     return jsonify(recommendations)

# if __name__ == "__main__":
#     app.run(debug=True)

# from generate_customer_embeddings import generate_embedding
# import time

# start_time = time.time()

# sample_text = "Test product embedding"
# embedding = generate_embedding(sample_text)


# end_time = time.time()
# print(f"Time taken for one embedding: {end_time - start_time:.2f} seconds")

import ollama

response = ollama.chat(model='orca-mini', messages=[
  {'role': 'user', 'content': 'Hello! Suggest a product for skincare.'}
])

print(response['message']['content'])
