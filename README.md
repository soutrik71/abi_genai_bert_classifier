## __abi_genai_bert_classifier__

* Docker:  24.0.8-1
* CUDA: 12.2
* GPU: GV100GL [Tesla V100 PCIe 16GB]
* Driver: nvidia-driver-535-server
* DOcker Compose: v2.27.1

### __docker-compose__

- docker-compose up build --no-cache
- docker compose up
- docker-compose down --rmi all

### __ CUDA SETUP__
- sudo apt install ubuntu-drivers-common
- ubuntu-drivers devices
- sudo apt install nvidia-driver-535-server
- sudo reboot
- sudo apt install nvidia-cuda-toolkit
- apt info nvidia-cuda-toolkit
- nvcc --version
- nvidia-smi

### __DOCKERCOMPOSE__
- sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
- sudo chmod +x /usr/local/bin/docker-compose
- docker-compose --version

  
### __APP__

- python -m main

### __EXTRAS__
- docker build --no-cache -t fastapi-cuda-app .
- docker run --gpus all -p 8080:8080 fastapi-cuda-app
- sudo docker system prune


