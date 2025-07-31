# Multi-stage Dockerfile using micromamba and uv for optimal package management
# Stage 1: Base image with micromamba
FROM mambaorg/micromamba:1.5.8 AS base

# Set up micromamba environment
USER root

# Install system dependencies required for building packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Switch to micromamba user for conda operations
USER $MAMBA_USER

# Copy conda environment file
COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /tmp/environment.yml

# Create conda environment with micromamba
# This handles system-level dependencies and scientific packages efficiently
RUN micromamba install -y -n base -f /tmp/environment.yml && \
    micromamba clean --all --yes

# Activate the environment
ARG MAMBA_DOCKERFILE_ACTIVATE=1

# Stage 2: Add uv for fast Python package management
FROM base AS builder

# Switch back to root for uv installation and directory setup
USER root

# Install uv for fast Python package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory and fix permissions
WORKDIR /app
RUN chown -R $MAMBA_USER:$MAMBA_USER /app

# Switch to micromamba user for application setup
USER $MAMBA_USER

# Copy Python project files
COPY --chown=$MAMBA_USER:$MAMBA_USER pyproject.toml uv.lock ./

# Set environment variables to use system Python (conda environment)
# UV_SYSTEM_PYTHON=1 tells UV to use the system Python instead of creating a venv
# UV_PROJECT_ENVIRONMENT points UV to the conda environment
# UV_EXTRA_INDEX_URL forces CPU-only PyTorch packages
ENV UV_SYSTEM_PYTHON=1
ENV UV_PROJECT_ENVIRONMENT=/opt/conda
ENV UV_EXTRA_INDEX_URL="https://download.pytorch.org/whl/cpu"
ENV PIP_EXTRA_INDEX_URL="https://download.pytorch.org/whl/cpu"

# Use uv to install Python dependencies directly into the conda environment
# The eval command activates the conda environment, then UV installs packages
# --no-install-project prevents installing the project itself as a package
RUN eval "$(micromamba shell hook --shell bash)" && \
    micromamba activate base && \
    uv sync --frozen --no-dev --no-install-project

# Stage 3: Final runtime image
FROM base AS runtime

# Switch to root for setup
USER root

# Copy uv from builder stage
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory and fix permissions
WORKDIR /app
RUN chown -R $MAMBA_USER:$MAMBA_USER /app

# Copy installed packages from builder stage first
COPY --from=builder --chown=$MAMBA_USER:$MAMBA_USER /opt/conda /opt/conda

# Create necessary directories with proper permissions
RUN mkdir -p /app/chroma_db /app/exports && \
    chown -R $MAMBA_USER:$MAMBA_USER /app/chroma_db /app/exports /app

# Switch to micromamba user
USER $MAMBA_USER

# Copy the application code
COPY --chown=$MAMBA_USER:$MAMBA_USER . .

# Set environment variables for optimal performance
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH="/app"
ENV UV_SYSTEM_PYTHON=1
ENV UV_PROJECT_ENVIRONMENT=/opt/conda

# Expose port
ARG PORT=8050
ENV PORT=${PORT}
EXPOSE ${PORT}

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Set the entrypoint to activate conda environment and run the application
ENTRYPOINT ["/usr/local/bin/_entrypoint.sh"]

# Command to run the MCP server using the activated conda environment
CMD ["python", "src/main_chromadb.py"]