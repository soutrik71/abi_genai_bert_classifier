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
    wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pip for Python 3.10
RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python3.10 get-pip.py && \
    rm get-pip.py

# Create symbolic links for python3.10 and pip3.10
RUN ln -sf /usr/bin/python3.10 /usr/bin/python && \
    ln -sf /usr/local/bin/pip3.10 /usr/bin/pip

# Verify Python and pip installation
RUN python3.10 --version && \
    python3.10 -m pip --version

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install necessary Python packages
RUN python3.10 -m pip install --no-cache-dir --upgrade pip && \
    python3.10 -m pip install torch==2.2.1 torchvision==0.17.1

# Copy requirements and install them
COPY ./project_requirements.txt ./requirements.txt
RUN python3.10 -m pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8080

CMD ["gunicorn", "main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8080", "--timeout", "1800"]
