import flet as ft
import random
import time

# Datos simulados de inventario de viajes (para efectos de demostración)
INVENTORY_DATA = [
    {"name": "Ciudad Antigua", "cost": 550.00, "discount": 0.10, "status": "Activo"},
    {"name": "Playas del Sol", "cost": 899.50, "discount": 0.00, "status": "Activo"},
    {"name": "Montaña Escondida", "cost": 320.00, "discount": 0.25, "status": "Inactivo"},
    {"name": "Mercado Local", "cost": 150.00, "discount": 0.05, "status": "Activo"},
]

def usuario_view(page: ft.Page, role: str, main_app_function):
    """
    Define la interfaz de usuario para el rol de Usuario (Gestor de Inventario de Viajes).
    """
    page.title = f"Gestión de Inventario | {role}"
    page.bgcolor = ft.Colors.BLUE_GREY_50 

    # --- Funciones de Lógica ---

    def logout(e):
        page.clean()
        main_app_function(page)
    
    def calculate_summary():
        """Calcula los totales para el panel de resumen."""
        total_destinations = len(INVENTORY_DATA)
        active_destinations = sum(1 for item in INVENTORY_DATA if item["status"] == "Activo")
        
        # Calcular el valor total de inventario (Costo * (1 - Descuento))
        total_value = sum(item["cost"] * (1 - item["discount"]) for item in INVENTORY_DATA)
        
        return total_destinations, active_destinations, total_value
    
    def add_new_destination(e):
        """Añade un nuevo destino al inventario y actualiza la UI."""
        
        # Validación de campos
        if not new_name.value or not new_cost.value or not new_discount.value:
            feedback_text.value = "Todos los campos son obligatorios para añadir un destino."
            feedback_text.color = ft.Colors.RED_500
            page.update()
            return

        try:
            cost = float(new_cost.value)
            discount = float(new_discount.value) / 100 # Se espera % de 0-100
            
            if discount < 0 or discount > 1:
                raise ValueError("Descuento debe estar entre 0 y 100.")

            new_item = {
                "name": new_name.value.strip().title(),
                "cost": cost,
                "discount": discount,
                "status": "Activo" # Por defecto
            }
            
            INVENTORY_DATA.append(new_item)
            
            # Limpiar formulario y mostrar éxito
            new_name.value = ""
            new_cost.value = ""
            new_discount.value = ""
            
            feedback_text.value = f"✅ Destino '{new_item['name']}' añadido con éxito."
            feedback_text.color = ft.Colors.GREEN_700
            
            # Recalcular y actualizar el resumen y la página
            update_summary()

        except ValueError as ve:
            feedback_text.value = f"Error en datos: {ve}"
            feedback_text.color = ft.Colors.RED_700

        page.update()

    # --- Componentes de Resumen (Paneles informativos) ---

    def create_summary_card(title, value, icon, color):
        """Crea una tarjeta de resumen estilizada."""
        return ft.Card(
            ft.Container(
                content=ft.Column([
                    ft.Icon(icon, size=30, color=color),
                    ft.Text(title, size=14, color=ft.Colors.BLACK54),
                    ft.Text(value, size=24, weight=ft.FontWeight.BOLD),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=15,
                width=page.window_width * 0.28, # Un tercio del ancho
                alignment=ft.alignment.center,
            ),
            elevation=3,
        )

    # Variables de UI que se actualizarán
    total_dest_text = ft.Text("0", size=24, weight=ft.FontWeight.BOLD)
    active_dest_text = ft.Text("0", size=24, weight=ft.FontWeight.BOLD)
    total_value_text = ft.Text("$0.00", size=24, weight=ft.FontWeight.BOLD)
    
    def update_summary():
        """Actualiza los valores de las tarjetas de resumen."""
        total_dest, active_dest, total_value = calculate_summary()
        
        total_dest_text.value = str(total_dest)
        active_dest_text.value = str(active_dest)
        total_value_text.value = f"${total_value:,.2f}"
        
        page.update()

    # Cards del Resumen
    summary_row = ft.Row([
        create_summary_card("Total Destinos", total_dest_text, ft.Icons.MAP, ft.Colors.BLUE_700),
        create_summary_card("Destinos Activos", active_dest_text, ft.Icons.CHECK_CIRCLE_OUTLINE, ft.Colors.GREEN_700),
        create_summary_card("Valor Total (Neto)", total_value_text, ft.Icons.PRICE_CHANGE, ft.Colors.AMBER_700),
    ], alignment=ft.MainAxisAlignment.CENTER)

    # --- Componentes de Formulario (Para agregar nuevos destinos) ---

    new_name = ft.TextField(label="Nombre del Destino", icon=ft.Icons.PLACE, width=300)
    new_cost = ft.TextField(label="Costo Base ($)", icon=ft.Icons.MONEY, width=150, keyboard_type=ft.KeyboardType.NUMBER)
    new_discount = ft.TextField(label="Descuento (%)", icon=ft.Icons.DISCOUNT, width=135, keyboard_type=ft.KeyboardType.NUMBER)

    form_row = ft.Row([new_cost, new_discount], alignment=ft.MainAxisAlignment.CENTER, width=300)
    
    add_button = ft.ElevatedButton(
        "Añadir Nuevo Destino", 
        on_click=add_new_destination, 
        icon=ft.Icons.ADD_LOCATION,
        bgcolor=ft.Colors.BLUE_700,
        color=ft.Colors.WHITE
    )
    
    feedback_text = ft.Text("") # Mensaje de retroalimentación del formulario

    # --- Contenido de la Vista ---

    page.clean()
    
    main_column = ft.Column(
        [
            ft.Text(f"Bienvenido, {role} (Gestor)", size=34, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
            ft.Text("Panel de Inventario de Viajes y Herramientas Operativas.", size=16, color=ft.Colors.BLUE_GREY_600),
            ft.Divider(height=20),
            
            # SECCIÓN 1: Resumen
            ft.Container(
                content=ft.Column([
                    # CORRECCIÓN: ft.FontWeight.W600 -> ft.FontWeight.W_600
                    ft.Text("Resumen Rápido", size=20, weight=ft.FontWeight.W_600), 
                    summary_row
                ]),
                padding=20,
                width=page.window_width,
            ),
            
            # SECCIÓN 2: Formulario de Adición
            ft.Container(
                content=ft.Column([
                    # CORRECCIÓN: ft.FontWeight.W600 -> ft.FontWeight.W_600
                    ft.Text("Añadir Destino y Tarifas", size=20, weight=ft.FontWeight.W_600),
                    new_name,
                    form_row,
                    add_button,
                    feedback_text,
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                padding=25,
                margin=ft.margin.only(top=10, bottom=10),
                border_radius=15,
                bgcolor=ft.Colors.WHITE,
                width=350,
                shadow=ft.BoxShadow(0, 5, ft.Colors.BLACK12)
            ),
            
            ft.Divider(height=20),
            
            ft.ElevatedButton("Cerrar Sesión", on_click=logout, icon=ft.Icons.LOGOUT, color=ft.Colors.RED_600)
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.START,
        scroll=ft.ScrollMode.AUTO, # Permitir scroll si la ventana es pequeña
        expand=True
    )
    
    page.add(main_column)
    update_summary() # Cargar los datos iniciales al mostrar la vista
    page.update()
