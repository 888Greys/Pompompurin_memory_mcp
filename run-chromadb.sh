#!/bin/bash

# MCP-ChromaDB Docker Runner Script

echo "🚀 Starting MCP-ChromaDB Memory System..."

# Create necessary directories
mkdir -p chroma_db
mkdir -p exports

# Build the Docker image
echo "📦 Building ChromaDB Docker image..."
docker build -f Dockerfile.chromadb -t mcp/chromadb --build-arg PORT=8050 .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
    
    # Run the container
    echo "🏃 Starting ChromaDB container..."
    docker run --name mcp-chromadb-memory \
        -p 8050:8050 \
        -v "$(pwd)/chroma_db:/app/chroma_db" \
        -v "$(pwd)/exports:/app/exports" \
        -e TRANSPORT=sse \
        -e HOST=0.0.0.0 \
        -e PORT=8050 \
        --rm \
        mcp/chromadb
else
    echo "❌ Failed to build Docker image"
    exit 1
fi