import flet as ft
import threading
import time

# --- 1. ESTADO COMPARTIDO Y CANDADO (LOCK) ---

# Datos de los destinos con capacidad (stock) inicial
# Usamos un diccionario para que sea mutable y fácil de acceder por nombre
DESTINATIONS_DATA = {
    "Ciudad Antigua": {"icon": ft.Icons.LANDSCAPE, "color": ft.Colors.TEAL_600, "description": "Descubre ruinas históricas y museos.", "stock": 5},
    "Playas del Sol": {"icon": ft.Icons.BEACH_ACCESS, "color": ft.Colors.YELLOW_600, "description": "Relájate en la arena y disfruta del mar.", "stock": 10},
    "Montaña Escondida": {"icon": ft.Icons.FOREST, "color": ft.Colors.BROWN_600, "description": "Senderismo, aire puro y vistas panorámicas.", "stock": 3},
    "Mercado Local": {"icon": ft.Icons.SHOPPING_BAG, "color": ft.Colors.PURPLE_600, "description": "Gastronomía, artesanías y cultura local.", "stock": 20},
}

# Candado (Lock) global para proteger el acceso concurrente a DESTINATIONS_DATA
# Es vital para evitar que dos hilos actualicen el stock al mismo tiempo.
DATA_LOCK = threading.Lock()

# Diccionario para almacenar las referencias a los controles ft.Text que muestran el stock
# Esto permite que el hilo pueda actualizar el elemento específico en la UI.
STOCK_CONTROLS = {}


def visitante_view(page: ft.Page, role: str, main_app_function):
    """
    Define la interfaz de usuario para el rol de Visitante.
    """
    page.title = f"Explorar Destinos | {role}"

    def logout(e):
        page.clean()
        # Vuelve a la función de login en index.py
        main_app_function(page)

    # --- 2. LÓGICA DE CONCURRENCIA (THREAD-SAFE) ---

    def reserve_spot(destination_name, button_control):
        """
        Función que maneja la reserva en un hilo separado (thread-safe).
        Modifica el stock global y actualiza la UI.
        """
        global DATA_LOCK

        # 1. Simular una tarea de larga duración (ej: llamada a API)
        time.sleep(1.5)

        # 2. Usar el candado para garantizar la concurrencia segura
        with DATA_LOCK:
            current_stock = DESTINATIONS_DATA[destination_name]["stock"]
            
            if current_stock > 0:
                # Modificar el estado compartido de manera segura
                DESTINATIONS_DATA[destination_name]["stock"] -= 1
                new_stock = DESTINATIONS_DATA[destination_name]["stock"]
                
                # Actualizar el control de texto del stock en la UI
                if destination_name in STOCK_CONTROLS:
                    STOCK_CONTROLS[destination_name].value = f"Cupos disponibles: {new_stock}"
                    STOCK_CONTROLS[destination_name].color = ft.Colors.GREEN_600 if new_stock > 0 else ft.Colors.RED_600
                    STOCK_CONTROLS[destination_name].update()
                
                # Actualizar el botón con el estado final
                button_control.text = "¡Cupo Reservado!"
                button_control.bgcolor = ft.Colors.GREEN_400
                button_control.disabled = new_stock == 0 # Deshabilitar si se agotó
                
                print(f"[{threading.current_thread().name}] Reserva exitosa en {destination_name}. Quedan {new_stock} cupos.")
                
            else:
                # No hay stock, pero el botón ya debería estar deshabilitado
                button_control.text = "Sin Cupos"
                button_control.disabled = True
                
            # Siempre actualizar el botón al finalizar el proceso
            button_control.update()


    def on_reserve_clicked(e, destination_name):
        """Inicia la reserva en un hilo separado para no bloquear la UI principal."""
        
        # Mostrar estado de carga y deshabilitar para evitar doble click
        e.control.disabled = True
        e.control.text = "Reservando..."
        e.control.bgcolor = ft.Colors.ORANGE_400
        e.control.update()
        
        # Crear y comenzar el hilo, pasándole el control del botón para su actualización
        thread = threading.Thread(
            target=reserve_spot, 
            args=(destination_name, e.control), 
            name=f"ReserveThread-{destination_name}"
        )
        thread.start()

    # --- 3. ESTRUCTURA DE LA VISTA ---
        
    # El fondo del portal turístico será más brillante
    page.bgcolor = ft.Colors.CYAN_50 
    page.clean()
    
    # Título principal del portal
    welcome_header = ft.Row(
        [
            ft.Icon(ft.Icons.MAP, color=ft.Colors.BLUE_700, size=40),
            ft.Text("Tu Guía Turística", size=30, weight=ft.FontWeight.BOLD),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    
    # Crear tarjetas de destino
    destination_cards = []
    # Iteramos sobre el diccionario para obtener el nombre y los datos del destino
    for name, data in DESTINATIONS_DATA.items():
        
        # 3.1. Texto dinámico del stock (creado antes del card para almacenar su referencia)
        stock_text = ft.Text(
            f"Cupos disponibles: {data['stock']}", 
            size=14, 
            color=ft.Colors.GREEN_600 if data['stock'] > 0 else ft.Colors.RED_600,
            weight=ft.FontWeight.W_600 # Usamos W_600 (Semibold)
        )
        
        # 3.2. Almacenar la referencia en el diccionario global para que el hilo la use
        STOCK_CONTROLS[name] = stock_text
        
        # 3.3. Botón de reserva
        reserve_button = ft.ElevatedButton(
            "Reservar Cupo",
            icon=ft.Icons.CHECK_CIRCLE,
            # Llama a la función que inicia el hilo
            on_click=lambda e, n=name: on_reserve_clicked(e, n),
            disabled=data['stock'] == 0, # Deshabilitar si no hay stock inicial
            bgcolor=ft.Colors.CYAN_700,
            color=ft.Colors.WHITE
        )
        
        card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Icon(data['icon'], color=data['color'], size=30),
                            title=ft.Text(name, weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(data['description']),
                        ),
                        stock_text, # Mostrar el stock dinámico
                        ft.Row(
                            [
                                reserve_button, # El botón de acción
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        )
                    ],
                    spacing=5, # Aumenté el espaciado para mejor legibilidad
                ),
                padding=10,
            ),
            width=350 
        )
        destination_cards.append(card)

    # Contenedor principal de la vista
    view_content = ft.Column(
        [
            welcome_header,
            ft.Text(
                f"¡Hola {role}! Reserva tu cupo con lógica de concurrencia (hilos).", 
                size=16, 
                color=ft.Colors.BLUE_GREY_700
            ),
            ft.Divider(height=15),
            # Las tarjetas de destino en un scroll view
            ft.Container(
                content=ft.Column(
                    destination_cards,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                    # El Column ahora maneja el scroll
                    scroll=ft.ScrollMode.AUTO, 
                ),
                expand=True, 
                width=380,
                padding=ft.padding.only(top=10, bottom=10)
            ),
            
            ft.Container(
                ft.ElevatedButton(
                    "Volver al Portal de Ingreso", 
                    on_click=logout, 
                    icon=ft.Icons.LOGOUT, 
                    bgcolor=ft.Colors.RED_400,
                    color=ft.Colors.WHITE
                ),
                padding=ft.padding.only(bottom=10)
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.START,
        expand=True
    )
    
    page.add(view_content)
    page.update()
