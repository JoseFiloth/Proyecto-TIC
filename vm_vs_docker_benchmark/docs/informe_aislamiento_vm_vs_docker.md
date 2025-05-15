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

## 📊 Fase 4: Resultados y visualización

Se realizaron pruebas en 4 escenarios:
- VM en reposo
- VM con interferencia externa
- Docker en reposo
- Docker con interferencia externa

Los resultados fueron procesados en `notebooks/visualizar_resultados.ipynb`, donde se graficó el tiempo medio de acceso con barras de desviación estándar.

> Una variación significativa entre estado en reposo y con interferencia indica baja separación a nivel de caché → fuga de información potencial.

Archivos involucrados:
- `scripts/generate_interference.py`
- `results/*_reposo.txt`
- `results/*_con_interferencia.txt`
- `notebooks/visualizar_resultados.ipynb`

## ✅ Conclusión final

Este proyecto ha permitido comparar el nivel de aislamiento entre una máquina virtual (VM) y un contenedor Docker utilizando una prueba avanzada basada en interferencia de caché, un concepto asociado a ataques por canal lateral.

A través del uso de una función compilada en C, accedida repetidamente desde un script en Python, se midieron los tiempos de ejecución en diferentes escenarios (reposo y con interferencia). El comportamiento de la caché de CPU fue clave para detectar si el entorno podía verse afectado por procesos externos.

### Principales hallazgos:

- **La máquina virtual mostró mayor aislamiento**: los tiempos de ejecución fueron estables, con poca variación incluso cuando el host ejecutaba la misma función en paralelo.
- **El contenedor Docker evidenció mayor vulnerabilidad**: los tiempos medios y su desviación aumentaron notablemente bajo interferencia externa, indicando una menor separación de recursos.
- Este resultado **valida que Docker, al compartir el kernel del host**, puede estar más expuesto a canales de fuga pasiva, mientras que las máquinas virtuales ofrecen un entorno más cerrado y protegido a nivel de hardware.

### Consideraciones finales:

- Los contenedores siguen siendo ideales para despliegues rápidos y eficientes, especialmente en entornos CI/CD.
- Las máquinas virtuales siguen siendo preferibles para ejecutar procesos altamente sensibles o que requieran aislamiento fuerte.
- Esta metodología puede ser extendida a otras áreas como red compartida, disco, y contexto del sistema operativo para evaluar aislamiento total.

> En definitiva, este proyecto demuestra que el aislamiento entre entornos no debe asumirse únicamente por su separación lógica, sino también evaluarse a nivel de comportamiento del hardware compartido.

---

