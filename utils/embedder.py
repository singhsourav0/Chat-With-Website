import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import numpy as np
import pickle
import os

class DocumentEmbedder:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=api_key
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    
    def create_chunks(self, text):
        chunks = self.text_splitter.split_text(text)
        return chunks
    
    def create_embeddings(self, chunks):
        embeddings = self.embeddings.embed_documents(chunks)
        return np.array(embeddings)
    
    def save_data(self, chunks, embeddings, url, data_dir="data"):
        os.makedirs(data_dir, exist_ok=True)
        
        # Create filename from URL
        filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
        
        data = {
            'chunks': chunks,
            'embeddings': embeddings,
            'url': url
        }
        
        with open(f"{data_dir}/{filename}.pkl", "wb") as f:
            pickle.dump(data, f)
        
        return f"{data_dir}/{filename}.pkl"
    
    def load_data(self, filepath):
        with open(filepath, "rb") as f:
            return pickle.load(f)