import flet as ft
from datetime import datetime, timedelta

# --- 1. DATOS SIMULADOS ---

# Paquete turistico pagado por el cliente
CLIENT_RESERVATION = {
    "package_name": "Aventura Total 5 Noches",
    "status": "Pago Confirmado",
    "original_destination": "Playas del Sol",
    "current_destination": "Playas del Sol",
    "base_price": 899.50,
    "departure_datetime": datetime.now().replace(hour=10, minute=0) + timedelta(days=7),
    "available_destinations": ["Playas del Sol", "Ciudad Antigua", "Montaña Escondida"]
}

def cliente_view(page: ft.Page, role: str, main_app_function):
    """
    Define la interfaz de usuario para el rol de Cliente.
    Se enfoca en la gestión de su reserva pagada.
    """
    page.title = f"Mi Reserva | {role}"
    page.bgcolor = ft.Colors.CYAN_50
    page.clean()

    # --- 2. FUNCIONES DE LÓGICA ---

    def logout(e):
        page.clean()
        main_app_function(page)

    def update_reservation(e):
        """Función para simular la actualización de la reserva."""
        
        # 1. Obtener los valores de los selectores
        new_destination = destination_dropdown.value
        
        # El DatePicker ya actualiza su valor al seleccionarse (client_date_picker.value)
        # El TimePicker ya actualiza su valor al seleccionarse (client_time_picker.value)
        
        selected_date = client_date_picker.value
        selected_time = client_time_picker.value

        # --- Validación y Actualización ---
        if not new_destination or not selected_date or not selected_time:
             feedback_message.value = "Error: Por favor, selecciona un destino, fecha y hora de salida."
             feedback_message.color = ft.Colors.RED_600
        else:
            try:
                # Convertir los valores a objetos datetime para el estado interno
                # Nota: DatePicker devuelve un objeto datetime.date, no un string, si no se usa format_string.
                # Para simplificar la lógica de simulacion, asumiremos que selected_date es el objeto date.
                
                # Si client_date_picker.value es un objeto datetime, usamos su strftime para obtener la cadena
                # Si el valor viene de un input de texto, se usa strptime.
                # Aquí intentamos obtener la fecha:
                if isinstance(selected_date, datetime):
                    departure_date = selected_date
                else:
                    # Si viene como string, asumimos el formato ISO que usa Flet
                    departure_date = datetime.strptime(selected_date.split(' ')[0], "%Y-%m-%d")
                    
                
                # Suponiendo que el TimePicker devuelve un string HH:MM:SS (ej: 10:00:00)
                # O solo la hora y minuto si Flet lo simplifica (ej: 10:00)
                # Si TimePicker devuelve un objeto time (el caso más probable), lo usamos
                if isinstance(selected_time, ft.Time):
                    time_parts = [selected_time.hour, selected_time.minute]
                else:
                    time_parts = list(map(int, selected_time.split(':')[:2])) 
                
                final_departure = departure_date.replace(hour=time_parts[0], minute=time_parts[1])
                
                # Actualizar el estado simulado
                CLIENT_RESERVATION["current_destination"] = new_destination
                CLIENT_RESERVATION["departure_datetime"] = final_departure
                
                # Actualizar el texto del resumen y el mensaje de feedback
                summary_text.value = f"Destino: {new_destination} | Salida: {final_departure.strftime('%d/%m/%Y a las %H:%M')}"
                feedback_message.value = "✅ Reserva actualizada con éxito. ¡Buen viaje!"
                feedback_message.color = ft.Colors.GREEN_700
                
            except Exception as ex:
                feedback_message.value = f"Error en la actualización: {ex}. Asegúrate de seleccionar Fecha y Hora."
                feedback_message.color = ft.Colors.RED_600

        page.update()

    # --- 3. COMPONENTES INTERACTIVOS (Selectores) ---

    # Selector de Destino (Modificar Lugar de Salida)
    destination_dropdown = ft.Dropdown(
        label="Modificar Destino",
        width=300,
        options=[
            ft.dropdown.Option(dest) for dest in CLIENT_RESERVATION["available_destinations"]
        ],
        value=CLIENT_RESERVATION["current_destination"],
        icon=ft.Icons.FLIGHT_TAKEOFF_OUTLINED
    )
    
    # Selector de Fecha (Reservar Salida)
    client_date_picker = ft.DatePicker(
        # Por defecto, la fecha de la reserva simulada
        value=CLIENT_RESERVATION["departure_datetime"],
        on_change=lambda e: print(f"Fecha seleccionada: {e.control.value}"),
        on_dismiss=lambda e: print("Selector de fecha cerrado"),
        first_date=datetime.now(),
        last_date=datetime.now() + timedelta(days=365*2), # Máximo 2 años
    )
    
    # Selector de Hora (Poner un Horario)
    client_time_picker = ft.TimePicker(
        # Por defecto, la hora de la reserva simulada
        value=CLIENT_RESERVATION["departure_datetime"].time(), 
        on_change=lambda e: print(f"Hora seleccionada: {e.control.value}"),
        on_dismiss=lambda e: print("Selector de hora cerrado"),
    )

    # Botones de apertura de Selectores
    select_date_button = ft.ElevatedButton(
        "Seleccionar Fecha",
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda e: client_date_picker.pick_date(),
        width=145
    )
    select_time_button = ft.ElevatedButton(
        "Seleccionar Hora",
        icon=ft.Icons.ACCESS_TIME,
        on_click=lambda e: client_time_picker.pick_time(),
        width=145
    )
    
    # Añadir los pickers a la página para que puedan ser usados por los botones
    page.overlay.append(client_date_picker)
    page.overlay.append(client_time_picker)


    # --- 4. ESTRUCTURA DE LA VISTA ---
    
    # Resumen de la reserva
    summary_text = ft.Text(
        f"Destino: {CLIENT_RESERVATION['current_destination']} | Salida: {CLIENT_RESERVATION['departure_datetime'].strftime('%d/%m/%Y a las %H:%M')}",
        size=16,
        # CORRECCIÓN: ft.FontWeight.W500 -> ft.FontWeight.W_500
        weight=ft.FontWeight.W_500,
        color=ft.Colors.CYAN_900
    )
    
    # Tarjeta de Reserva (Boarding Pass Style)
    reservation_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Mi Tarjeta de Reserva", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_700),
                    ft.Divider(height=10, color=ft.Colors.BLACK12),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.CARD_TRAVEL, color=ft.Colors.CYAN_500),
                        title=ft.Text(f"Paquete: {CLIENT_RESERVATION['package_name']}"),
                        subtitle=ft.Text(f"Estado: {CLIENT_RESERVATION['status']}", weight=ft.FontWeight.BOLD),
                    ),
                    ft.Divider(height=1, color=ft.Colors.BLACK12),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.PRICE_CHECK, color=ft.Colors.GREEN_600),
                        title=ft.Text(f"Precio Base Pagado: ${CLIENT_RESERVATION['base_price']:.2f}"),
                    ),
                    ft.Divider(height=1, color=ft.Colors.BLACK12),
                    # Aca el error original es SEMI_BOLD, pero dado que W_500 es el error actual,
                    # lo dejo como W_600 (Semibold) para evitar futuros errores en esta linea
                    ft.Text("Detalles de Salida", size=18, weight=ft.FontWeight.W_600, color=ft.Colors.BLUE_GREY_800),
                    summary_text,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.START,
                spacing=5
            ),
            padding=20,
            width=380,
            border_radius=15,
            bgcolor=ft.Colors.WHITE
        ),
        elevation=10
    )

    # Contenedor de Modificación
    modification_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Personaliza tu Viaje", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
                    ft.Divider(height=10),
                    destination_dropdown,
                    ft.Row([select_date_button, select_time_button], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    ft.Divider(height=10),
                    ft.ElevatedButton(
                        "Confirmar Modificaciones",
                        on_click=update_reservation,
                        icon=ft.Icons.CHECK_CIRCLE,
                        bgcolor=ft.Colors.CYAN_700,
                        color=ft.Colors.WHITE,
                        width=300
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=20,
            width=380,
            border_radius=15,
            bgcolor=ft.Colors.WHITE
        ),
        elevation=5
    )
    
    feedback_message = ft.Text(
        "Modifica los detalles de tu reserva según tus preferencias.", 
        color=ft.Colors.BLACK54
    )


    main_column = ft.Column(
        [
            ft.Text("¡Tu Próxima Aventura Te Espera!", size=34, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
            ft.Divider(height=10),
            reservation_card,
            ft.Divider(height=20),
            modification_card,
            feedback_message,
            ft.Divider(height=30),
            ft.ElevatedButton("Cerrar Sesión", on_click=logout, icon=ft.Icons.LOGOUT, color=ft.Colors.RED_600)
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.START,
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )
    
    page.add(main_column)
    page.update()
