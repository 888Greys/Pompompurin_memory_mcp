"""
ChromaDB utilities for MCP server
Provides local vector storage with semantic search
"""
import chromadb
from sentence_transformers import SentenceTransformer
from datetime import datetime
import uuid
import json
import os
from typing import List, Dict, Any

class ChromaMemoryClient:
    def __init__(self, collection_name: str = "memories", persist_directory: str = "./chroma_db"):
        """Initialize ChromaDB client with local persistence"""
        # Create persistent client
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "MCP server memories"}
        )
        
        # Initialize embedding model (runs locally)
        print("Loading embedding model...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Embedding model loaded successfully!")
    
    def add_memory(self, content: str, user_id: str = "default_user") -> str:
        """Add a new memory with semantic embedding"""
        try:
            memory_id = str(uuid.uuid4())
            
            # Create embedding
            embedding = self.embedding_model.encode(content).tolist()
            
            # Prepare metadata
            metadata = {
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "content_length": len(content)
            }
            
            # Add to ChromaDB
            self.collection.add(
                embeddings=[embedding],
                documents=[content],
                metadatas=[metadata],
                ids=[memory_id]
            )
            
            return f"Successfully saved memory: {content[:100]}..." if len(content) > 100 else f"Successfully saved memory: {content}"
            
        except Exception as e:
            raise Exception(f"Failed to add memory: {str(e)}")
    
    def search_memories(self, query: str, user_id: str = "default_user", limit: int = 3) -> List[Dict[str, Any]]:
        """Search memories using semantic similarity"""
        try:
            # Create query embedding
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Search in ChromaDB with user filter
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=limit,
                where={"user_id": user_id}
            )
            
            # Format results
            memories = []
            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    memory = {
                        "memory": results['documents'][0][i],
                        "id": results['ids'][0][i],
                        "metadata": results['metadatas'][0][i],
                        "similarity_score": 1 - results['distances'][0][i] if results['distances'][0] else 1.0
                    }
                    memories.append(memory)
            
            return memories
            
        except Exception as e:
            raise Exception(f"Failed to search memories: {str(e)}")
    
    def get_all_memories(self, user_id: str = "default_user") -> List[Dict[str, Any]]:
        """Get all memories for a user"""
        try:
            # Get all memories for the user
            results = self.collection.get(
                where={"user_id": user_id}
            )
            
            # Format results
            memories = []
            if results['documents']:
                for i in range(len(results['documents'])):
                    memory = {
                        "memory": results['documents'][i],
                        "id": results['ids'][i],
                        "metadata": results['metadatas'][i]
                    }
                    memories.append(memory)
            
            # Sort by timestamp (newest first)
            memories.sort(key=lambda x: x['metadata'].get('timestamp', ''), reverse=True)
            
            return memories
            
        except Exception as e:
            raise Exception(f"Failed to get memories: {str(e)}")
    
    def export_memories_to_json(self, user_id: str = "default_user", filename: str = None) -> str:
        """Export all memories to JSON file for backup/transfer"""
        try:
            memories = self.get_all_memories(user_id)
            
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"memories_export_{timestamp}.json"
            
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "total_memories": len(memories),
                "memories": memories
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return f"Exported {len(memories)} memories to {filename}"
            
        except Exception as e:
            raise Exception(f"Failed to export memories: {str(e)}")
    
    def import_memories_from_json(self, filename: str, user_id: str = "default_user") -> str:
        """Import memories from JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                export_data = json.load(f)
            
            memories = export_data.get('memories', [])
            imported_count = 0
            
            for memory_data in memories:
                content = memory_data.get('memory', '')
                if content:
                    self.add_memory(content, user_id)
                    imported_count += 1
            
            return f"Imported {imported_count} memories from {filename}"
            
        except Exception as e:
            raise Exception(f"Failed to import memories: {str(e)}")
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection"""
        try:
            count = self.collection.count()
            return {
                "total_memories": count,
                "collection_name": self.collection.name,
                "embedding_model": "all-MiniLM-L6-v2"
            }
        except Exception as e:
            return {"error": str(e)}

def get_chromadb_client() -> ChromaMemoryClient:
    """Create and return ChromaDB client"""
    try:
        # Create ChromaDB client with local storage
        client = ChromaMemoryClient(
            collection_name="mcp_memories",
            persist_directory="./chroma_db"
        )
        return client
    except Exception as e:
        raise Exception(f"Failed to initialize ChromaDB client: {str(e)}")