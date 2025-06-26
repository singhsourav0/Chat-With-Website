import streamlit as st
import os
from dotenv import load_dotenv
from utils.web_scraper import WebScraper
from utils.embedder import DocumentEmbedder
from utils.retriever import DocumentRetriever

load_dotenv()

def main():
    st.set_page_config(page_title="Chat with Website", page_icon="🌐")
    
    st.title("🌐 Chat with Website")
    st.markdown("Enter a website URL and ask questions about its content!")
    
    # Get API key from environment
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        st.error("❌ Gemini API key not found. Please set GEMINI_API_KEY in .env file")
        return
    
    if api_key:
        # Initialize components
        scraper = WebScraper()
        embedder = DocumentEmbedder(api_key)
        retriever = DocumentRetriever(api_key)
        
        # URL input
        url = st.text_input("Enter Website URL:", placeholder="https://example.com")
        
        if url and st.button("Load Website"):
            with st.spinner("Scraping and processing website..."):
                try:
                    # Scrape website
                    content = scraper.scrape_website(url)
                    title = scraper.get_page_title(url)
                    
                    # Create chunks and embeddings
                    chunks = embedder.create_chunks(content)
                    embeddings = embedder.create_embeddings(chunks)
                    
                    # Save data
                    filepath = embedder.save_data(chunks, embeddings, url)
                    
                    # Store in session state
                    st.session_state.chunks = chunks
                    st.session_state.embeddings = embeddings
                    st.session_state.url = url
                    st.session_state.title = title
                    
                    st.success(f"✅ Successfully loaded: {title}")
                    st.info(f"📄 Created {len(chunks)} text chunks")
                    
                except Exception as e:
                    st.error(f"❌ Error loading website: {str(e)}")
        
        # Chat interface
        if hasattr(st.session_state, 'chunks'):
            st.markdown("---")
            st.subheader(f"💬 Chat with: {st.session_state.title}")
            
            # Initialize chat history
            if "messages" not in st.session_state:
                st.session_state.messages = []
            
            # Display chat messages
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            
            # Chat input
            if prompt := st.chat_input("Ask a question about the website..."):
                # Add user message
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                # Generate response
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        relevant_chunks = retriever.retrieve_relevant_chunks(
                            prompt, 
                            st.session_state.chunks, 
                            st.session_state.embeddings
                        )
                        response = retriever.generate_response(prompt, relevant_chunks)
                        st.markdown(response)
                
                # Add assistant response
                st.session_state.messages.append({"role": "assistant", "content": response})
        
    else:
        st.info("👆 Enter a website URL and click 'Load Website' to start chatting!")

if __name__ == "__main__":
    main()