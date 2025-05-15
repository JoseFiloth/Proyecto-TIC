# 🧪 Proyecto: Evaluación de Aislamiento entre Máquina Virtual y Docker

## 🎯 Objetivo del proyecto

Este proyecto tiene como objetivo comparar el **nivel de aislamiento** entre una máquina virtual (VM) y un contenedor Docker, no sólo desde el punto de vista del uso de recursos, sino a través de una prueba más profunda: detectar **posibles interferencias de caché** que permitan inferir actividad del entorno externo, simulando un **ataque por canal lateral**.

---

## 🧱 Estructura del proyecto

- `scripts/`: Código fuente en C, scripts Python y Dockerfile.
- `results/`: Archivos de resultados generados por cada prueba.
- `notebooks/`: Notebook Jupyter para graficar y analizar los resultados.
- `docs/`: Este documento y cualquier otro archivo explicativo.

---

## 🖥️ Entorno del experimento

### 🧰 Máquina anfitriona (host - Windows)

- Sistema operativo: Windows 10 / 11
- Docker Desktop con WSL2 habilitado
- VirtualBox para ejecutar la máquina virtual
- VS Code como entorno de desarrollo

### 💻 Máquina virtual

- Virtualizador: VirtualBox
- Sistema operativo: Ubuntu Server 22.04 (sin entorno gráfico)
- CPU: 2 núcleos
- RAM: 2 GB
- Disco: 10 GB
- Red: NAT
- Herramientas instaladas: `gcc`, `python3`, `pip`, `stress-ng`, `sysbench`

### 🐳 Contenedor Docker

- Imagen base: `python:3.10-slim`
- Herramientas instaladas: `gcc`, `psutil`, `stress-ng`, `sysbench`
- Dockerfile ubicado en `scripts/Dockerfile`
- Carpetas compartidas con el host para guardar resultados

---

## ⚗️ Metodología

### Prueba de interferencia de caché (Flush+Reload simplificado)

#### 1. Compilación de librería compartida

Se creó una función en C llamada `secret_function()` y se compiló como librería compartida (`shared_code.so`):

```c
void secret_function() {
    volatile int a = 0;
    for (int i = 0; i < 100000; i++) {
        a += i;
    }
}
