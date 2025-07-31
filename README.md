# 🧠 Pompompurin's Personal AI Memory System

<div align="center">

![Memory System](https://img.shields.io/badge/AI-Memory%20System-blue?style=for-the-badge&logo=brain&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Optimized-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Performance](https://img.shields.io/badge/Build%20Time-85%25%20Faster-green?style=for-the-badge)
![Size](https://img.shields.io/badge/Downloads-90%25%20Smaller-orange?style=for-the-badge)

**Ultra-fast MCP ChromaDB server with Micromamba + UV optimization**

*Personal AI memory that remembers everything across conversations*

</div>

## 🚀 What This Is

This is my **personal AI memory system** built on the [Model Context Protocol (MCP)](https://modelcontextprotocol.io) with **ChromaDB** for vector storage. It gives AI agents persistent memory capabilities, allowing them to remember and recall information across conversations.

### ✨ Key Features

- 🧠 **Persistent Memory**: AI agents remember everything across sessions
- 🔍 **Semantic Search**: Find relevant memories using natural language
- ⚡ **Lightning Fast**: Optimized Docker builds (85% faster than standard setups)
- 🐳 **Production Ready**: Multi-stage Docker with health checks and monitoring
- 📦 **Minimal Size**: CPU-only packages (90% smaller downloads)
- 🔧 **Easy Setup**: One-command deployment with docker-compose

## 📊 Performance Optimizations

This setup includes **major performance improvements** over standard Docker builds:

| Metric | Standard Setup | This Optimized Setup | Improvement |
|--------|---------------|---------------------|-------------|
| **Build Time** | ~20 minutes | ~3 minutes | **85% faster** |
| **Download Size** | 2.2GB | 250MB | **90% smaller** |
| **Image Size** | 1.2GB | 900MB | **25% smaller** |
| **CUDA Packages** | 15+ packages | 0 packages | **100% eliminated** |

## 🛠 Technology Stack

- **🐍 Python 3.12+** - Modern Python with type hints
- **🧬 ChromaDB** - Vector database for semantic search
- **🚀 Micromamba** - Ultra-fast conda package manager (10x faster than conda)
- **⚡ UV** - Lightning-fast Python package installer (10-100x faster than pip)
- **🐳 Docker + BuildKit** - Optimized containerization with parallel builds
- **🔧 MCP Protocol** - Model Context Protocol for AI agent integration

## 🚀 Quick Start

### **Prerequisites**
- Docker installed and running
- Git for cloning the repository

### **1. Clone & Setup**
```bash
# Clone the repository
git clone https://github.com/888Greys/Pompompurin_memory_mcp.git
cd Pompompurin_memory_mcp

# Copy environment template
cp .env.example .env
```

### **2. Configure Environment**
Edit `.env` file with your settings:
```bash
# Basic Configuration
TRANSPORT=sse
HOST=0.0.0.0
PORT=8050

# ChromaDB Configuration (local storage)
CHROMA_DB_PATH=./chroma_db
CHROMA_COLLECTION_NAME=pompompurin_memory

# Optional: Add your LLM provider for enhanced features
# LLM_PROVIDER=openai
# LLM_API_KEY=your-api-key-here
```

### **3. Build & Run (Optimized)**
```bash
# Enable BuildKit for maximum performance
export DOCKER_BUILDKIT=1

# Build with lightning speed (3 minutes vs 20 minutes)
docker build --progress=plain -t pompompurin-memory .

# Run with docker-compose (recommended)
docker-compose up -d

# Check if it's running
curl http://localhost:8050/health
```

### **4. View Logs**
```bash
# Watch logs in real-time
docker-compose logs -f

# Check container status
docker-compose ps
```

## 🔧 Advanced Usage

### **Development Mode**
```bash
# Run with hot-reload for development
docker-compose --profile development up -d

# Access development server
curl http://localhost:8051/health
```

### **Manual Docker Commands**
```bash
# Run container manually with custom settings
docker run -d \
  --name pompompurin-memory \
  -p 8050:8050 \
  -v ./chroma_db:/app/chroma_db \
  -v ./exports:/app/exports \
  -e PYTHONUNBUFFERED=1 \
  -e CHROMA_COLLECTION_NAME=my_custom_memory \
  pompompurin-memory

# Stop and remove
docker stop pompompurin-memory
docker rm pompompurin-memory
```

### **Scaling & Production**
```bash
# Scale to multiple instances
docker-compose up -d --scale mcp-chromadb=3

# Production deployment with resource limits
docker run -d \
  --name pompompurin-memory-prod \
  --restart unless-stopped \
  -p 8050:8050 \
  -v ./chroma_db:/app/chroma_db \
  --memory=2g \
  --cpus=2.0 \
  pompompurin-memory
```

## 🔌 Integration with AI Clients

### **Claude Desktop / Windsurf (SSE)**
Add to your MCP configuration:
```json
{
  \"mcpServers\": {
    \"pompompurin-memory\": {
      \"transport\": \"sse\",
      \"url\": \"http://localhost:8050/sse\"
    }
  }
}
```

### **Local Python Integration (Stdio)**
```json
{
  \"mcpServers\": {
    \"pompompurin-memory\": {
      \"command\": \"docker\",
      \"args\": [\"run\", \"--rm\", \"-i\", \"pompompurin-memory\"],
      \"env\": {
        \"TRANSPORT\": \"stdio\"
      }
    }
  }
}
```

### **n8n Integration**
Use `host.docker.internal` for container-to-container communication:
```
http://host.docker.internal:8050/sse
```

## 🧠 Memory Operations

The system provides three core memory operations:

### **1. Save Memory**
```python
# Store information with automatic semantic indexing
save_memory(\"I prefer dark mode in all applications\")
save_memory(\"My favorite programming language is Python\")
save_memory(\"I'm working on an AI memory system project\")
```

### **2. Search Memories**
```python
# Find relevant memories using natural language
search_memories(\"What are my preferences?\")
search_memories(\"What programming projects am I working on?\")
```

### **3. Get All Memories**
```python
# Retrieve complete memory context
get_all_memories()
```

## 📁 Project Structure

```
Pompompurin_memory_mcp/
├── 🐳 Docker Configuration
│   ├── Dockerfile                     # Optimized multi-stage build
│   ├── docker-compose.yml             # Production-ready setup
│   └── .dockerignore                 # Minimal build context
│
├── 📦 Package Management
│   ├── pyproject.toml                # UV configuration with CPU-only packages
│   ├── uv.lock                       # Reproducible dependency versions
│   └── environment.yml               # Conda environment with scientific packages
│
├── 💻 Source Code
│   ├── src/
│   │   ├── main_chromadb.py          # Main MCP server
│   │   └── utils_chromadb.py         # ChromaDB utilities
│   └── test_setup.py                 # Setup validation
│
├── 📚 Documentation
│   ├── README.md                     # This file
│   ├── DOCKER_BUILDKIT_GUIDE.md      # BuildKit optimization guide
│   ├── BUILD_SPEED_OPTIMIZATION.md   # Performance analysis
│   ├── DOCKERFILE_FIXES.md           # Technical solutions
│   └── CLEANUP_SUMMARY.md           # Project optimization details
│
└── 🔧 Configuration
    ├── .env.example                  # Environment template
    └── run-chromadb.sh              # Helper script
```

## ⚙️ Configuration Options

### **Environment Variables**

| Variable | Default | Description |
|----------|---------|-------------|
| `TRANSPORT` | `sse` | Protocol: `sse` or `stdio` |
| `HOST` | `0.0.0.0` | Server host binding |
| `PORT` | `8050` | Server port |
| `CHROMA_DB_PATH` | `/app/chroma_db` | ChromaDB storage location |
| `CHROMA_COLLECTION_NAME` | `pompompurin_memory` | Memory collection name |
| `PYTHONUNBUFFERED` | `1` | Python output buffering |

### **Performance Tuning**

| Variable | Default | Description |
|----------|---------|-------------|
| `OMP_NUM_THREADS` | `4` | OpenMP thread count |
| `MKL_NUM_THREADS` | `4` | Intel MKL threads |
| `NUMBA_NUM_THREADS` | `4` | Numba compilation threads |

### **Resource Limits**
```yaml
# docker-compose.yml
deploy:
  resources:
    limits:
      memory: 2G      # Maximum memory
      cpus: '2.0'     # Maximum CPU cores
    reservations:
      memory: 1G      # Reserved memory
      cpus: '1.0'     # Reserved CPU cores
```

## 🔧 Technical Architecture

### **Multi-Stage Docker Build**
```dockerfile
# Stage 1: Base environment with micromamba
FROM mambaorg/micromamba:1.5.8 AS base
# - Ultra-fast conda package manager (10x faster than conda)
# - Scientific computing packages (NumPy, SciPy, PyTorch-CPU)
# - System dependencies and build tools

# Stage 2: Builder with UV package management
FROM base AS builder
# - Lightning-fast Python package installer (10-100x faster than pip)
# - CPU-only packages to avoid 2GB CUDA downloads
# - Installs into conda environment for perfect integration

# Stage 3: Production runtime
FROM base AS runtime
# - Minimal final image with only necessary components
# - Proper security and permissions
# - Health checks and monitoring
```

### **Package Manager Synergy**
- **Micromamba**: Handles system dependencies and scientific packages
- **UV**: Manages pure Python packages with incredible speed
- **CPU-only constraint**: Both tools install CPU-optimized packages
- **Single environment**: No virtual environment conflicts or overhead

## 🐛 Troubleshooting

### **Common Issues**

#### **Port Already in Use**
```bash
# Check what's using port 8050
lsof -i :8050

# Use different port
docker run -p 8051:8050 pompompurin-memory
```

#### **Permission Issues**
```bash
# Fix volume permissions
sudo chown -R $(id -u):$(id -g) ./chroma_db ./exports
```

#### **Build Failures**
```bash
# Clear Docker cache
docker builder prune -a

# Rebuild without cache
docker build --no-cache -t pompompurin-memory .
```

#### **Memory Issues**
```bash
# Check container memory usage
docker stats pompompurin-memory

# Increase memory limit
docker run --memory=4g pompompurin-memory
```

### **Health Checks**
```bash
# Test health endpoint
curl -f http://localhost:8050/health

# Check container health
docker inspect pompompurin-memory | grep -A 5 Health

# View detailed logs
docker logs -f pompompurin-memory
```

## 📈 Performance Monitoring

### **Build Performance**
```bash
# Time the build process
time docker build -t pompompurin-memory .

# Monitor build cache usage
docker system df

# Check image layers
docker history pompompurin-memory
```

### **Runtime Performance**
```bash
# Monitor resource usage
docker stats

# Check memory usage
docker exec pompompurin-memory free -h

# Monitor ChromaDB performance
docker exec pompompurin-memory ps aux
```

## 🔒 Security Considerations

- **Non-root user**: Container runs as `mambauser` for security
- **Read-only filesystem**: Application code mounted read-only
- **Resource limits**: CPU and memory constraints prevent resource exhaustion
- **Health monitoring**: Built-in health checks for reliability
- **Network isolation**: Containers run in isolated Docker networks

## 🤝 Contributing

This is my personal memory system, but feel free to:

1. **Fork** the repository for your own use
2. **Submit issues** if you find bugs
3. **Suggest improvements** via pull requests
4. **Share optimizations** you discover

## 📚 Additional Resources

- **[DOCKER_BUILDKIT_GUIDE.md](DOCKER_BUILDKIT_GUIDE.md)** - Complete BuildKit optimization guide
- **[BUILD_SPEED_OPTIMIZATION.md](BUILD_SPEED_OPTIMIZATION.md)** - Detailed performance analysis
- **[DOCKERFILE_FIXES.md](DOCKERFILE_FIXES.md)** - Technical problem solutions
- **[Model Context Protocol](https://modelcontextprotocol.io)** - Official MCP documentation
- **[ChromaDB Documentation](https://docs.trychroma.com/)** - Vector database guide

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align=\"center\">

**Built with ❤️ by Pompompurin**

*Optimized for speed, designed for intelligence*

[![GitHub](https://img.shields.io/badge/GitHub-888Greys-black?style=flat&logo=github)](https://github.com/888Greys)
[![Docker](https://img.shields.io/badge/Docker-Optimized-blue?style=flat&logo=docker)](https://hub.docker.com)

</div>