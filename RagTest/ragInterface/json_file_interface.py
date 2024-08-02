import json
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.neighbors import NearestNeighbors
from hashlib import blake2b

class json_file_interface:
    
    chunk_length = 2000
    n_neighbours = 5
    rag_keys = set()
    rag_vectors = np.array([])
    rag_data = {}
    embedding_model = None
    neighbours = None 

    def __init__(self):
        self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        with open("./RagTest/resources/json_interface_data.json", 'r') as f:
            try:
                saved_data = json.load(f)
                print(len(saved_data))
                if "rag_data" in saved_data:
                    self.rag_keys = set(saved_data["rag_keys"])
                    data = saved_data["rag_data"]
                    print(len(self.rag_data))
                    self.process_chunks(data)
                    self.neighbours = NearestNeighbors(n_neighbors=self.n_neighbours, algorithm='ball_tree').fit(self.rag_vectors)
                    print("Loaded data, vector shape: ", self.rag_vectors.shape)
            except Exception as e: print(e)

    def process_data(self, data):
        for data_pt in data:
            if data[data_pt] == None or not data[data_pt]:
                print("Could not retrieve data")
                return
            if not data_pt in self.rag_keys:
                self.rag_keys.add(data_pt)
                chunks = self.split_into_chunks(data[data_pt])
                self.process_chunks(chunks)
        self.neighbours = NearestNeighbors(n_neighbors=self.n_neighbours, algorithm='ball_tree').fit(self.rag_vectors)
        with open("./RagTest/resources/json_interface_data.json", 'w') as f:
            data = {"rag_keys": list(self.rag_keys), "rag_data": list(self.rag_data.values())}
            json.dump(data, f)
        print("Rag vectors shape: ", self.rag_vectors.shape)
    
    def process_chunks(self, chunks):
        vectors = self.vectorize_chunks(chunks)
        for chunk, vector in zip(chunks, vectors):
            if self.rag_vectors.size == 0:
                self.rag_vectors = vector
            else:
                self.rag_vectors = np.vstack([self.rag_vectors, vector])
            self.rag_data[self.get_vector_key(vector)] = chunk
    
    def split_into_chunks(self, str):
        return [str[idx : idx + self.chunk_length] for idx in range(0, len(str), self.chunk_length)]
    
    def vectorize_chunks(self, chunks):
        return self.embedding_model.encode(chunks)
    
    def get_vector_key(self, vector):
        return blake2b(vector.tobytes(), digest_size=16).hexdigest()
    
    def knn(self, prompt_vector):
        _, indices = self.neighbours.kneighbors(prompt_vector)
        return self.rag_vectors[indices[0]]

    def retrieve_chunks(self, relevant_vectors):
        chunks = []
        print(relevant_vectors.shape)
        for relevant_vector in relevant_vectors:
            chunks.append(self.rag_data[self.get_vector_key(relevant_vector)])
        return chunks
    
    def retrieve_relevant_chunks(self, prompt):
        prompt_vector = self.vectorize_chunks([prompt])
        relevant_vectors = self.knn(prompt_vector)
        relevant_chunks = self.retrieve_chunks(relevant_vectors)
        return relevant_chunks

