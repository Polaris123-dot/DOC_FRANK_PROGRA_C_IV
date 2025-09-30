import threading
import time

saldo = 200
lock = threading.Lock()

def retirar(dinero, nombre):
    global saldo
    for _ in range(2):
        with lock:  # Bloquea el acceso al recurso
            if saldo >= dinero:
                print(f"{nombre} retira {dinero}")
                saldo -= dinero
                time.sleep(1)
                print(f"{nombre} finalizó. Saldo: {saldo}")
            else:
                print(f"{nombre} no pudo retirar. Saldo insuficiente: {saldo}")

t1 = threading.Thread(target=retirar, args=(100, "Hilo-1"))
t2 = threading.Thread(target=retirar, args=(100, "Hilo-2"))

print("🏦 Iniciando operaciones...\n")
t1.start()
t2.start()

t1.join()
t2.join()

print("\n🏁 Operaciones finalizadas. Saldo final:", saldo)
