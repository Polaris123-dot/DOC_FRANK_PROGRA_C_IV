import threading
import time

def tarea(nombre):
    for i in range(3):
        print(f"{nombre} está trabajando en paso {i+1}")
        time.sleep(1)

# Crear hilos
t1 = threading.Thread(target=tarea, args=("Hilo-1",))
t2 = threading.Thread(target=tarea, args=("Hilo-2",))

print("🚀 Iniciando hilos...\n")
t1.start()
t2.start()

t1.join()
t2.join()

print("\n🏁 Hilos finalizados.")
