import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings

class DocumentRetriever:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=api_key
        )
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def retrieve_relevant_chunks(self, query, chunks, embeddings, top_k=3):
        # Get query embedding
        query_embedding = np.array(self.embeddings.embed_query(query))
        
        # Calculate similarities
        similarities = cosine_similarity([query_embedding], embeddings)[0]
        
        # Get top k indices
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        # Return relevant chunks
        relevant_chunks = [chunks[i] for i in top_indices]
        return relevant_chunks
    
    def generate_response(self, query, relevant_chunks):
        context = "\n\n".join(relevant_chunks)
        
        prompt = f"""
        You are a helpful website assistant chatbot. Your role is to provide comprehensive, accurate, and engaging responses based on the website content provided.
        
        Website Content:
        {context}
        
        User Question: {query}
        
        Instructions:
        - Act as an expert on this website's content
        - Provide detailed, helpful responses using the website information
        - If asked about services, products, or features, explain them thoroughly
        - Include relevant details, benefits, and context from the website
        - If information isn't available in the content, politely mention that
        - Maintain a friendly, professional tone as a website representative
        - Format responses clearly with bullet points or sections when helpful
        
        Response:
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"