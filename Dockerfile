FROM nvidia/cuda:12.2.2-runtime-ubuntu20.04

# Install Python 3.10 and necessary components
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    curl \
    software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install --no-install-recommends -y \
    python3.10 \
    python3.10-venv \
    python3.10-dev \
    python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*



# Verify Python and pip installation
RUN python3 --version && \
    python3 -m pip --version

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install necessary Python packages
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install torch torchvision torchaudio

# Copy requirements and install them
COPY ./project_requirements.txt ./requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8080

CMD ["gunicorn", "main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8080", "--timeout", "1800"]
