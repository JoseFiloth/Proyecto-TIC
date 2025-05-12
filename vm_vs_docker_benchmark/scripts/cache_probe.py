import ctypes
import time
import statistics

# Cargar librería
lib = ctypes.CDLL("./shared_code.so")
func = lib.secret_function

# Medir tiempos de acceso
times = []

print("⏱️ Ejecutando prueba de acceso a caché...")

for _ in range(1000):
    start = time.perf_counter()
    func()
    end = time.perf_counter()
    times.append((end - start) * 1e6)  # microsegundos

# Resultados
mean_time = statistics.mean(times)
stdev_time = statistics.stdev(times)

print(f"Media de tiempo: {mean_time:.2f} µs")
print(f"Desviación estándar: {stdev_time:.2f} µs")
