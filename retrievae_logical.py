import openai
import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# Azure OpenAI setup

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
index = faiss.read_index("chunks.index")
dimension = index.d  # Ensure correct dimension

# Load code metadata
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

def generate_query_vector(query_text):
    """Generate a vector representation of the query using the embedding model."""
    return np.array([model.encode(query_text)], dtype="float32")

def generate_logical_steps(query_text, retrieved_snippets):
    """Use Azure OpenAI to generate logical steps based on retrieved code snippets."""
    
    snippet_text = "\n\n".join([f"Snippet {i+1}:\n{snippet['code']}" for i, snippet in enumerate(retrieved_snippets)])

    prompt = f"""
    The user wants to: "{query_text}".

    Below are some relevant code snippets retrieved from FAISS:

    {snippet_text}

    Based on these code snippets, break down the solution into logical steps.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[
            {"role": "system", "content": "You are an AI that breaks down queries into structured steps based on code snippets."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=700
    )

    return response.choices[0].message.content

def search_code(query, top_k=3):
    """Search FAISS for the top K relevant code snippets and generate logical steps."""
    query_vector = generate_query_vector(query)

    if query_vector.shape[1] != dimension:
        print(f"Error: Query vector dimension mismatch. Expected {dimension}, got {query_vector.shape[1]}")
        return

    distances, indices = index.search(query_vector, top_k)
    
    retrieved_snippets = []
    for j, i in enumerate(indices[0]):
        if i != -1:
            retrieved_snippets.append({"code": chunks[i], "distance": float(distances[0][j])})

    # # Check if the factorial function is present in stored dataset
    # factorial_code = [
    #     chunk for chunk in chunks
    #     if "factorial(" in chunk.get("code", "") and chunk.get("name", "") == "factorial"
    # ]

    # if factorial_code:
    #     print("\n✅ **Factorial function exists in dataset!**")
    #     print("Stored Factorial Code:\n", factorial_code)
    # else:
    #     print("\n❌ **Factorial function NOT found in dataset!**")
    #     print("Skipping nCr code generation.")
    #     return  # Stop execution if factorial function is missing

    logical_steps = generate_logical_steps(query, retrieved_snippets)

    return {"retrieved_snippets": retrieved_snippets, "logical_steps": logical_steps}

# Example usage
query = "I have an array i want to display all of its elements"
result = search_code(query)

if result:
    print("\n🔍 **Retrieved Code Snippets:**")
    contains_factorial = False

    for snippet in result["retrieved_snippets"]:
        code_snippet = snippet["code"]
        print(f"- Code:\n{code_snippet}\n  Distance: {snippet['distance']}\n")
        
        # Check if the retrieved snippet contains the factorial function
        if "factorial(" in code_snippet:
            contains_factorial = True

    print("\n🛠 **Factorial Function Found in Retrieved Snippets:**", contains_factorial)

    print("\n📝 **Logical Breakdown:**")
    print(result["logical_steps"])