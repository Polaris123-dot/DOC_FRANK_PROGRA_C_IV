import flet as ft
import random
from typing import Callable, Dict, Any, List, Tuple

# --- Datos Simulados del Sistema (Compartidos con otros módulos en una app real) ---

# Usuarios y Roles (Duplicados aquí para que el Admin pueda ver las métricas)
# En una aplicación real, esto provendría de index.py o una base de datos.
SIMULATED_USERS = {
    ("admin", "admin123"): "Administrador",
    ("user", "user123"): "Usuario",
    ("client", "client123"): "Cliente",
    ("visit", "visit123"): "Visitante",
    ("jfernandez", "pass1"): "Usuario",
    ("mrodriguez", "pass2"): "Cliente",
    ("testguest", "12345"): "Visitante",
}

# Inventario de Destinos (Duplicado aquí para que el Admin lo pueda manipular)
# En una aplicación real, esto provendría de Usuario.py o una base de datos.
SIMULATED_INVENTORY = [
    {"name": "Tour de Machu Picchu", "cost": 450.00, "discount_percent": 10},
    {"name": "Cataratas del Iguazú", "cost": 320.00, "discount_percent": 5},
    {"name": "Desierto de Atacama", "cost": 500.00, "discount_percent": 0},
    {"name": "Río Amazonas Aventura", "cost": 750.00, "discount_percent": 15},
    {"name": "Playas de Cancún", "cost": 280.00, "discount_percent": 10},
    {"name": "Islas Galápagos", "cost": 900.00, "discount_percent": 20},
]


def admin_view(page: ft.Page, role: str, main_app_function: Callable):
    """
    Función principal para la vista de Administrador que incluye toda la UI y lógica.
    """
    
    # --- Lógica de la Vista ---

    def calculate_user_metrics() -> Dict[str, int]:
        """Calcula el número de usuarios por rol."""
        metrics = {
            "Administrador": 0,
            "Usuario": 0,
            "Cliente": 0,
            "Visitante": 0,
        }
        for _, user_role in SIMULATED_USERS.items():
            metrics[user_role] = metrics.get(user_role, 0) + 1
        return metrics

    def create_summary_card(title: str, value: Any, icon: ft.Icons, color: str):
        """Crea una tarjeta de resumen de métricas."""
        return ft.Card(
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(icon, color=color, size=30),
                        ft.Column(
                            [
                                ft.Text(title, size=14, color=ft.Colors.BLACK54),
                                ft.Text(str(value), size=24, weight=ft.FontWeight.BOLD),
                            ],
                            spacing=0
                        )
                    ],
                    spacing=15,
                    alignment=ft.MainAxisAlignment.START,
                ),
                padding=15,
            ),
            width=200,
            elevation=5
        )

    # --- Generación de Data Table para Inventario ---

    # Inputs para la edición en línea
    cost_fields: List[ft.TextField] = []
    discount_fields: List[ft.TextField] = []
    
    def create_inventory_table(inventory: List[Dict[str, Any]]):
        """Genera la DataTable con campos editables."""
        
        # Limpiar listas para evitar duplicados en la recarga
        cost_fields.clear()
        discount_fields.clear()

        rows = []
        for i, item in enumerate(inventory):
            # Campo de costo (Editable)
            cost_field = ft.TextField(
                value=f"{item['cost']:.2f}",
                width=100,
                text_align=ft.TextAlign.RIGHT,
                input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9\.]"),
                data=i # Almacena el índice para saber qué fila actualizar
            )
            cost_fields.append(cost_field)

            # Campo de descuento (Editable)
            discount_field = ft.TextField(
                value=str(item['discount_percent']),
                width=60,
                text_align=ft.TextAlign.RIGHT,
                input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]"),
                data=i # Almacena el índice para saber qué fila actualizar
            )
            discount_fields.append(discount_field)

            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item['name'])),
                        ft.DataCell(cost_field),
                        ft.DataCell(discount_field),
                    ]
                )
            )

        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Destino", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Costo Base", weight=ft.FontWeight.BOLD), numeric=True),
                ft.DataColumn(ft.Text("Descuento (%)", weight=ft.FontWeight.BOLD), numeric=True),
            ],
            rows=rows,
            border=ft.border.all(1, ft.Colors.BLACK12),
            border_radius=10,
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK12),
        )

    # Inicializar la tabla
    inventory_data_table = create_inventory_table(SIMULATED_INVENTORY)

    # --- Handlers de Eventos ---

    def logout(e):
        """Cierra la sesión y vuelve a la pantalla de login."""
        page.clean()
        main_app_function(page)

    def save_inventory_changes(e):
        """Guarda los cambios de costo y descuento en la SIMULATED_INVENTORY."""
        
        # Actualizar los datos simulados
        for cost_field in cost_fields:
            index = cost_field.data
            try:
                new_cost = float(cost_field.value)
                if new_cost >= 0:
                    SIMULATED_INVENTORY[index]['cost'] = new_cost
            except ValueError:
                print(f"Error de costo en índice {index}. Valor: {cost_field.value}")
        
        for discount_field in discount_fields:
            index = discount_field.data
            try:
                new_discount = int(discount_field.value)
                if 0 <= new_discount <= 100:
                    SIMULATED_INVENTORY[index]['discount_percent'] = new_discount
            except ValueError:
                print(f"Error de descuento en índice {index}. Valor: {discount_field.value}")
        
        # Retroalimentación
        page.snack_bar = ft.SnackBar(ft.Text("Inventario actualizado con éxito."), duration=2000)
        page.snack_bar.open = True
        page.update()


    def add_new_user(e):
        """Agrega un nuevo usuario a la lista SIMULATED_USERS."""
        new_user = new_username_field.value
        new_pass = new_password_field.value
        new_role = new_role_dropdown.value

        if new_user and new_pass and new_role:
            if (new_user, new_pass) not in SIMULATED_USERS:
                SIMULATED_USERS[(new_user, new_pass)] = new_role
                
                # Limpiar campos después de añadir
                new_username_field.value = ""
                new_password_field.value = ""
                new_role_dropdown.value = None

                # Mostrar mensaje de éxito y actualizar métricas
                page.snack_bar = ft.SnackBar(ft.Text(f"Usuario '{new_user}' ({new_role}) agregado."), duration=3000)
                page.snack_bar.open = True
                
                # Re-renderizar métricas de usuario
                update_metrics_row()
                
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Error: Usuario ya existe."), duration=3000, bgcolor=ft.Colors.RED_700)
                page.snack_bar.open = True
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Error: Completa todos los campos."), duration=3000, bgcolor=ft.Colors.RED_700)
            page.snack_bar.open = True

        page.update()

    def create_report(e):
        """Simula la generación de un reporte de ingresos."""
        total_revenue = 0
        for item in SIMULATED_INVENTORY:
            net_cost = item['cost'] * (1 - item['discount_percent'] / 100)
            # Simular que se han vendido entre 5 y 15 paquetes de cada uno
            sales_volume = random.randint(5, 15)
            total_revenue += net_cost * sales_volume
        
        report_text = f"Reporte Global Generado:\nIngresos Netos Estimados: ${total_revenue:,.2f}"
        
        # Muestra el resultado en un diálogo (simulación de reporte)
        page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Reporte de Ventas"),
            content=ft.Text(report_text, weight=ft.FontWeight.BOLD),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: close_dialog(e))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog.open = True
        page.update()

    def close_dialog(e):
        """Cierra cualquier diálogo abierto."""
        page.dialog.open = False
        page.update()

    # --- Inicialización de Componentes de Gestión de Usuarios ---

    new_username_field = ft.TextField(label="Nuevo Usuario", width=250, prefix_icon=ft.Icons.PERSON_ADD)
    new_password_field = ft.TextField(label="Contraseña", width=250, password=True, prefix_icon=ft.Icons.LOCK)
    new_role_dropdown = ft.Dropdown(
        label="Rol",
        width=250,
        options=[
            ft.dropdown.Option("Administrador"),
            ft.dropdown.Option("Usuario"),
            ft.dropdown.Option("Cliente"),
            ft.dropdown.Option("Visitante"),
        ],
    )
    
    # --- Estructura de la Página ---

    # 1. Métrica de Usuarios
    metrics = calculate_user_metrics()
    
    def update_metrics_row():
        """Función para actualizar la fila de métricas (útil después de añadir un usuario)."""
        metrics = calculate_user_metrics()
        metrics_row.controls = [
            create_summary_card("Total Administradores", metrics['Administrador'], ft.Icons.ADMIN_PANEL_SETTINGS, ft.Colors.GREEN_700),
            create_summary_card("Total Usuarios", metrics['Usuario'], ft.Icons.PEOPLE_ALT, ft.Colors.BLUE_700),
            create_summary_card("Total Clientes", metrics['Cliente'], ft.Icons.SHOPPING_CART, ft.Colors.CYAN_700),
            create_summary_card("Total Visitantes", metrics['Visitante'], ft.Icons.VISIBILITY, ft.Colors.AMBER_700),
        ]
        page.update()

    metrics_row = ft.Row(
        [
            create_summary_card("Total Administradores", metrics['Administrador'], ft.Icons.ADMIN_PANEL_SETTINGS, ft.Colors.GREEN_700),
            create_summary_card("Total Usuarios", metrics['Usuario'], ft.Icons.PEOPLE_ALT, ft.Colors.BLUE_700),
            create_summary_card("Total Clientes", metrics['Cliente'], ft.Icons.SHOPPING_CART, ft.Colors.CYAN_700),
            create_summary_card("Total Visitantes", metrics['Visitante'], ft.Icons.VISIBILITY, ft.Colors.AMBER_700),
        ],
        wrap=True,
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # 2. Gestión de Inventario
    inventory_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("Gestión de Costos y Descuentos", size=18, weight=ft.FontWeight.BOLD),
                ft.Text("Modifica los precios base y descuentos por destino.", size=12, color=ft.Colors.BLACK54),
                ft.Divider(),
                ft.Column(
                    [inventory_data_table],
                    height=250,
                    scroll=ft.ScrollMode.ADAPTIVE
                ),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            text="Guardar Cambios", 
                            on_click=save_inventory_changes, 
                            icon=ft.Icons.SAVE,
                            bgcolor=ft.Colors.GREEN_400
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.START, spacing=10),
            padding=20,
        ),
        elevation=5,
        width=700,
    )

    # 3. Gestión de Usuarios
    user_management_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("Añadir Nuevo Usuario al Sistema", size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Row(
                    [
                        new_username_field,
                        new_password_field,
                        new_role_dropdown
                    ],
                    spacing=15,
                    wrap=True
                ),
                ft.Row(
                    [
                        ft.ElevatedButton("Añadir Usuario", on_click=add_new_user, icon=ft.Icons.PERSON_ADD_ALT, bgcolor=ft.Colors.BLUE_400)
                    ],
                    alignment=ft.MainAxisAlignment.END
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.START, spacing=10),
            padding=20,
        ),
        elevation=5,
        width=700,
    )

    # 4. Reportes y Acciones Generales
    reports_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("Acciones Generales y Reportes", size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Row([
                    ft.ElevatedButton(
                        text="Generar Reporte Global",
                        on_click=create_report,
                        icon=ft.Icons.RECEIPT_LONG,
                        bgcolor=ft.Colors.PURPLE_400,
                        color=ft.Colors.WHITE
                    ),
                    ft.ElevatedButton("Cerrar Sesión", on_click=logout, icon=ft.Icons.LOGOUT, color=ft.Colors.RED_600)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ], horizontal_alignment=ft.CrossAxisAlignment.START, spacing=10),
            padding=20,
        ),
        elevation=5,
        width=700,
    )

    # Contenedor principal de la vista
    main_content = ft.Column(
        [
            ft.Text(f"Dashboard Administrativo", size=38, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_800),
            ft.Text(f"Bienvenido, {role} | Acceso Total al Sistema de Viajes", size=16, color=ft.Colors.BLACK54),
            ft.Divider(height=30),
            
            ft.Text("Métricas de Usuarios", size=20, weight=ft.FontWeight.W_600),
            metrics_row,

            ft.Divider(height=20),
            
            ft.Text("Herramientas de Administración", size=20, weight=ft.FontWeight.W_600),
            user_management_card,
            inventory_card,
            reports_card,
            
            ft.Container(height=50) # Espacio inferior
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        scroll=ft.ScrollMode.ADAPTIVE  # <-- Agrega esta línea aquí
    )

    # Configuración de la página
    page.clean()
    page.add(
        ft.Container(
            content=main_content,
            padding=ft.padding.all(30),
            expand=True
        )
    )
    page.update()
