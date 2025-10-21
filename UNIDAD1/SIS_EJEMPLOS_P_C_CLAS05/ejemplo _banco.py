import threading
import time

# Recurso compartido
saldo = 90
lock = threading.Lock()

def retirar(dinero, nombre):
    global saldo
    for i in range(3):  # 3 operaciones por cada hilo
        print(f"[{nombre}] Intentando retirar {dinero} (operación {i+1})...")

        # Bloquea el acceso con 'with', se libera automáticamente al salir
        with lock:
            print(f"[{nombre}] 🚪 Entró a la sección crítica.")

            if saldo >= dinero:
                print(f"[{nombre}] ✅ Retirando {dinero}...")
                saldo -= dinero
                time.sleep(1)  # Simula la transacción
                print(f"[{nombre}] 💰 Operación finalizada. Saldo actual: {saldo}")
            else:
                print(f"[{nombre}] ❌ Fondos insuficientes. Saldo actual: {saldo}")

            print(f"[{nombre}] 🚪 Saliendo de la sección crítica.")

        time.sleep(1)  # Pausa para que los hilos se alternen

# Crear dos hilos que intentan retirar dinero a la vez
t1 = threading.Thread(target=retirar, args=(90, "Hilo-1"))
t2 = threading.Thread(target=retirar, args=(50, "Hilo-2"))

print("🏦 Iniciando operaciones bancarias...\n")

t1.start()
t2.start()

t1.join()
t2.join()

print("\n🏁 Todas las operaciones han finalizado. Saldo final:", saldo)
