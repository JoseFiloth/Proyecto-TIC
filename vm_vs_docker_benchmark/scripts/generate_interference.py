import ctypes
import time

lib = ctypes.CDLL("./shared_code.so")
func = lib.secret_function

print("🚨 Generando interferencia...")
while True:
    func()
    time.sleep(0.001)