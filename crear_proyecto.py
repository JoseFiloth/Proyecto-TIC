import os
import zipfile

# Define the folder structure and files
base_dir = "vm_vs_docker_benchmark"
notebooks_dir = os.path.join(base_dir, "notebooks")
scripts_dir = os.path.join(base_dir, "scripts")
results_dir = os.path.join(base_dir, "results")

# Create directories
os.makedirs(notebooks_dir, exist_ok=True)
os.makedirs(scripts_dir, exist_ok=True)
os.makedirs(results_dir, exist_ok=True)

# Create notebook placeholder
notebook_path = os.path.join(notebooks_dir, "vm_vs_docker_comparison.ipynb")
with open(notebook_path, "w", encoding="utf-8") as f:
    f.write("# Your benchmarking notebook goes here")

# Create shell scripts
vm_script = """#!/bin/bash
echo "🚀 Setting up environment for benchmarking..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip sysbench docker.io git curl procps
pip3 install --upgrade pip
pip3 install jupyter matplotlib psutil
sudo usermod -aG docker $USER
echo "✅ Setup complete! Please restart your VM for Docker permissions to take effect."
echo "➡️ To start Jupyter, run: jupyter notebook"
"""

docker_script = """#!/bin/bash
echo "🐳 Setting up Docker environment for benchmarking..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip sysbench git curl procps
pip3 install --upgrade pip
pip3 install jupyter matplotlib psutil
echo "✅ Docker/WSL2 setup complete!"
echo "➡️ To start Jupyter Notebook, run: jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser"
"""

dockerfile = """FROM python:3.10-slim
RUN apt update && apt install -y sysbench git curl procps \\
    && pip install --upgrade pip \\
    && pip install jupyter matplotlib psutil
WORKDIR /app
COPY . .
EXPOSE 8888
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token=''"]
"""

