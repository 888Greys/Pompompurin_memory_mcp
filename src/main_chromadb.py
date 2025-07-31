from mcp.server.fastmcp import FastMCP, Context
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from dotenv import load_dotenv
import asyncio
import json
import os

from utils_chromadb import get_chromadb_client, ChromaMemoryClient

load_dotenv()

# Default user ID for memory operations
DEFAULT_USER_ID = "user"

# Create a dataclass for our application context
@dataclass
class ChromaContext:
    """Context for the ChromaDB MCP server."""
    chromadb_client: ChromaMemoryClient

@asynccontextmanager
async def chromadb_lifespan(server: FastMCP) -> AsyncIterator[ChromaContext]:
    """
    Manages the ChromaDB client lifecycle.
    
    Args:
        server: The FastMCP server instance
        
    Yields:
        ChromaContext: The context containing the ChromaDB client
    """
    # Create and return the ChromaDB client
    print("Initializing ChromaDB client...")
    chromadb_client = get_chromadb_client()
    print("ChromaDB client initialized successfully!")
    
    try:
        yield ChromaContext(chromadb_client=chromadb_client)
    finally:
        # No explicit cleanup needed for ChromaDB
        print("ChromaDB client lifecycle ended")

# Initialize FastMCP server with the ChromaDB client as context
mcp = FastMCP(
    "my-personal-chromadb-memory",
    description="My personal AI memory system using ChromaDB - remembers everything across conversations",
    lifespan=chromadb_lifespan,
    host=os.getenv("HOST", "0.0.0.0"),
    port=int(os.getenv("PORT", "8050"))
)        

@mcp.tool()
async def save_memory(ctx: Context, text: str) -> str:
    """Save information to your long-term memory using ChromaDB.

    This tool stores any type of information that might be useful in the future.
    The content will be processed and indexed for later retrieval through semantic search.

    Args:
        ctx: The MCP server provided context which includes the ChromaDB client
        text: The content to store in memory, including any relevant details and context
    """
    try:
        chromadb_client = ctx.request_context.lifespan_context.chromadb_client
        result = chromadb_client.add_memory(text, DEFAULT_USER_ID)
        return result
    except Exception as e:
        return f"Error saving memory: {str(e)}"

@mcp.tool()
async def get_all_memories(ctx: Context) -> str:
    """Get all stored memories from ChromaDB.
    
    Call this tool when you need complete context of all previously stored memories.

    Args:
        ctx: The MCP server provided context which includes the ChromaDB client

    Returns a JSON formatted list of all stored memories, including when they were created
    and their content.
    """
    try:
        chromadb_client = ctx.request_context.lifespan_context.chromadb_client
        memories = chromadb_client.get_all_memories(DEFAULT_USER_ID)
        
        # Extract just the memory content for cleaner output
        flattened_memories = [memory["memory"] for memory in memories]
        return json.dumps(flattened_memories, indent=2)
    except Exception as e:
        return f"Error retrieving memories: {str(e)}"

@mcp.tool()
async def search_memories(ctx: Context, query: str, limit: int = 3) -> str:
    """Search memories using semantic search with ChromaDB.

    This tool finds relevant information from your memory using semantic similarity.
    Results are ranked by relevance. Always search your memories before making decisions
    to ensure you leverage your existing knowledge.

    Args:
        ctx: The MCP server provided context which includes the ChromaDB client
        query: Search query string describing what you're looking for. Can be natural language.
        limit: Maximum number of results to return (default: 3)
    """
    try:
        chromadb_client = ctx.request_context.lifespan_context.chromadb_client
        memories = chromadb_client.search_memories(query, DEFAULT_USER_ID, limit)
        
        # Extract just the memory content for cleaner output
        flattened_memories = [memory["memory"] for memory in memories]
        return json.dumps(flattened_memories, indent=2)
    except Exception as e:
        return f"Error searching memories: {str(e)}"

@mcp.tool()
async def export_memories(ctx: Context, filename: str = None) -> str:
    """Export all memories to a JSON file for backup or transfer to another computer.

    Args:
        ctx: The MCP server provided context which includes the ChromaDB client
        filename: Optional filename for the export (if not provided, auto-generates with timestamp)
    """
    try:
        chromadb_client = ctx.request_context.lifespan_context.chromadb_client
        result = chromadb_client.export_memories_to_json(DEFAULT_USER_ID, filename)
        return result
    except Exception as e:
        return f"Error exporting memories: {str(e)}"

@mcp.tool()
async def import_memories(ctx: Context, filename: str) -> str:
    """Import memories from a JSON file (useful when setting up on a new computer).

    Args:
        ctx: The MCP server provided context which includes the ChromaDB client
        filename: Path to the JSON file containing exported memories
    """
    try:
        chromadb_client = ctx.request_context.lifespan_context.chromadb_client
        result = chromadb_client.import_memories_from_json(filename, DEFAULT_USER_ID)
        return result
    except Exception as e:
        return f"Error importing memories: {str(e)}"

@mcp.tool()
async def get_memory_stats(ctx: Context) -> str:
    """Get statistics about your memory collection.

    Args:
        ctx: The MCP server provided context which includes the ChromaDB client
    """
    try:
        chromadb_client = ctx.request_context.lifespan_context.chromadb_client
        stats = chromadb_client.get_collection_info()
        return json.dumps(stats, indent=2)
    except Exception as e:
        return f"Error getting memory stats: {str(e)}"

async def main():
    transport = os.getenv("TRANSPORT", "sse")
    if transport == 'sse':
        # Run the MCP server with sse transport
        await mcp.run_sse_async()
    else:
        # Run the MCP server with stdio transport
        await mcp.run_stdio_async()

if __name__ == "__main__":
    asyncio.run(main())