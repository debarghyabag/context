from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from cpp_chunks import extract_cpp_blocks

# 🔥 Load an Open-Source Embedding Model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")  # Replaceable with other models

# 📝 Extract C++ code chunks
cpp_file = "test1.cpp"
chunks = extract_cpp_blocks(cpp_file)

# 🏗 Convert text to embeddings
embeddings = model.encode(chunks)

# 🛠 Create FAISS Index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# ✅ Save FAISS Index
faiss.write_index(index, "faiss_cpp.index")
print("FAISS index saved successfully!")
