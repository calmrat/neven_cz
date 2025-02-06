
# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install UV package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Install dependencies
RUN uv pip install --system

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose webhook port
EXPOSE 5000

# Start services
CMD ["uv", "pip", "install", "--system"] &&     ["python", "upgates/webhook_server.py"] & ["python", "upgates/scheduler.py"]
