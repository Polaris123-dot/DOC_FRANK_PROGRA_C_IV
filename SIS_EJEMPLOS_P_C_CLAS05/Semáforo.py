import threading
import time
import random

# Semáforo con 2 recursos disponibles (2 cajeros)
cajeros = threading.Semaphore(2)

def usar_cajero(nombre):
    print(f"{nombre} está esperando para usar un cajero...")
    with cajeros:  # Solo 2 pueden entrar a la vez
        print(f"{nombre} 💳 está usando un cajero")
        time.sleep(random.randint(1, 3))  # Simula la transacción
        print(f"{nombre} ✅ terminó de usar el cajero")

# Crear varios clientes
clientes = [threading.Thread(target=usar_cajero, args=(f"Cliente-{i}",)) for i in range(6)]

for c in clientes:
    c.start()

for c in clientes:
    c.join()

print("🏁 Todos los clientes han terminado.")
