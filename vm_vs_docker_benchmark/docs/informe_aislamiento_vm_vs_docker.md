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
