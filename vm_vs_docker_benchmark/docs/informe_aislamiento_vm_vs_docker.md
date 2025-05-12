## ⚙️ Entorno en Windows

### 🖥️ Máquina anfitriona (host - Windows)
- Sistema operativo: Windows 10 / 11
- Docker Desktop instalado con WSL2
- VirtualBox 7.x con Ubuntu Server 22.04

### 💻 Máquina virtual (VirtualBox)
- Ubuntu Server sin entorno gráfico
- 2 CPU, 2 GB de RAM
- Red NAT
- Herramientas: gcc, python3, stress-ng, sysbench

### 🐳 Docker sobre WSL2
- Usa contenedor basado en `python:3.10-slim`
- Misma configuración que en la VM

## 🐳 Configuración del contenedor Docker

Se ha construido un contenedor basado en `python:3.10-slim`, replicando el entorno de la VM.

### Dockerfile usado:
```dockerfile
FROM python:3.10-slim
RUN apt update && apt install -y build-essential gcc curl git stress-ng sysbench procps \
    && pip install --upgrade pip \
    && pip install psutil
WORKDIR /app
COPY . .

## 🧪 Prueba 2: Acceso a función compartida (Flush+Reload simplificado)

**Objetivo:** Detectar variaciones de tiempo al acceder repetidamente a una misma función de una librería compartida, simulando un ataque por canal lateral tipo Flush+Reload.

**Procedimiento:**
1. Se compila una función en C (`shared_code.c`) como librería compartida.
2. Se llama desde Python y se mide el tiempo de ejecución 1000 veces.
3. Se compara el promedio y la desviación estándar para detectar interferencia externa.

**Archivos usados:**
- `scripts/shared_code.c`
- `scripts/cache_probe.py`
- `results/cache_probe_vm.txt`
- `results/cache_probe_docker.txt`

**Indicador de fuga:** Aumento inesperado de tiempo medio o desviación indica interferencia en la caché → posible falta de aislamiento.

---
