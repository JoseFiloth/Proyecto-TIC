
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
```

Compilación:
```bash
gcc -fPIC -shared -o shared_code.so shared_code.c
```

#### 2. Medición de tiempos desde Python

El script `cache_probe.py` accede a la función compilada y mide el tiempo de ejecución 1000 veces:

```python
import ctypes
import time
import statistics

lib = ctypes.CDLL("./shared_code.so")
func = lib.secret_function

times = []

for _ in range(1000):
    start = time.perf_counter()
    func()
    end = time.perf_counter()
    elapsed = (end - start) * 1e6  # microsegundos
    times.append(elapsed)

mean_time = statistics.mean(times)
stdev_time = statistics.stdev(times)

print(f"Media de tiempo: {mean_time:.2f} µs")
print(f"Desviación estándar: {stdev_time:.2f} µs")
```

#### 3. Generación de interferencia externa

Desde el host, se ejecuta `generate_interference.py`, que ejecuta la misma función en bucle para interferir en la caché:

```python
import ctypes
import time

lib = ctypes.CDLL("./shared_code.so")
func = lib.secret_function

print("🚨 Generando interferencia...")
while True:
    func()
    time.sleep(0.001)
```

---

## 🧪 Escenarios de prueba

| Escenario                         | Acción                                                     | Resultado esperado                      |
|----------------------------------|------------------------------------------------------------|------------------------------------------|
| VM en reposo                     | Ejecutar `cache_probe.py` dentro de la VM                 | Tiempo estable, baja desviación          |
| VM con interferencia del host    | Ejecutar `generate_interference.py` en host + `cache_probe.py` en VM | Leve incremento, buena separación      |
| Docker en reposo                 | Ejecutar `cache_probe.py` en contenedor Docker            | Tiempo estable                          |
| Docker con interferencia del host| Ejecutar `generate_interference.py` en host + Docker      | Tiempo más alto y mayor desviación       |

Los resultados se guardan en la carpeta `results/` con los nombres:
- `vm_reposo.txt`
- `vm_con_interferencia.txt`
- `docker_reposo.txt`
- `docker_con_interferencia.txt`

---

## 📊 Visualización de resultados

Se utilizó un notebook Jupyter para analizar los resultados y graficar la media y desviación estándar:

### Notebook: `notebooks/visualizar_resultados.ipynb`

```python
import matplotlib.pyplot as plt

def parse_result_file(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    mean = float(lines[0].split(":")[1].strip().split()[0])
    stdev = float(lines[1].split(":")[1].strip().split()[0])
    return mean, stdev

escenarios = {
    "VM (reposo)": "results/vm_reposo.txt",
    "VM (interferencia)": "results/vm_con_interferencia.txt",
    "Docker (reposo)": "results/docker_reposo.txt",
    "Docker (interferencia)": "results/docker_con_interferencia.txt"
}

labels, means, stdevs = [], [], []

for nombre, archivo in escenarios.items():
    mean, stdev = parse_result_file(archivo)
    labels.append(nombre)
    means.append(mean)
    stdevs.append(stdev)

plt.figure(figsize=(10, 6))
plt.bar(range(len(labels)), means, yerr=stdevs, capsize=5)
plt.xticks(range(len(labels)), labels, rotation=15)
plt.ylabel("Tiempo promedio (µs)")
plt.title("Interferencia de caché en Docker vs VM")
plt.grid(True)
plt.tight_layout()
plt.show()
```

---

## ✅ Conclusiones

- La **máquina virtual** mostró mejor aislamiento: tiempos más estables y baja interferencia.
- El **contenedor Docker** mostró mayor variación y sensibilidad a interferencia externa.
- Docker, al compartir el kernel con el host, puede ser más vulnerable a canales laterales.
- Las máquinas virtuales ofrecen un entorno más aislado, útil para tareas críticas o sensibles.
- Esta metodología se puede extender a otras pruebas de aislamiento: red, disco, procesos.

---

## 📁 Archivos clave

- `scripts/shared_code.c`: Código C de prueba
- `scripts/cache_probe.py`: Script para medir tiempos
- `scripts/generate_interference.py`: Script para generar carga
- `results/*.txt`: Resultados de las pruebas
- `notebooks/visualizar_resultados.ipynb`: Gráfico comparativo
- `scripts/Dockerfile`: Imagen base para entorno Docker
