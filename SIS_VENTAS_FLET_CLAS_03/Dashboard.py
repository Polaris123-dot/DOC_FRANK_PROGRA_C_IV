import flet as ft

def main(page: ft.Page):
    # Configuración de la ventana
    page.window.width = 1000
    page.window.height = 700
    page.window.resizable = True
    page.window.center()
    page.title = "Dashboard - Sistema de Ventas"
    page.bgcolor = "#f5f5f5"
    page.padding = 20
    
    # Función para volver al inicio
    def volver_inicio(e):
        page.window.close()
        import subprocess
        import sys
        import os
        ruta_main = os.path.join(os.path.dirname(__file__), "main.py")
        subprocess.Popen([sys.executable, ruta_main])
    
    # Crear cards con iconos y descripciones
    def create_card(icon, title, description, color):
        return ft.Container(
            width=180,
            height=180,
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Icon(icon, size=40, color="white"),
                        alignment=ft.alignment.center,
                        padding=10,
                        bgcolor=color,
                        width=60,
                        height=60,
                        border_radius=10,
                    ),
                    ft.Text(title, weight=ft.FontWeight.BOLD, size=16),
                    ft.Text(description, size=12, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=15,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color=ft.Colors.BLUE_GREY_100,
                offset=ft.Offset(0, 0),
            ),
        )
    
    # Crear sección de estadísticas
    stats_section = ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("12,856", size=28, weight=ft.FontWeight.BOLD, color="#2196F3"),
                            ft.Text("Ventas Totales", size=12),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=15,
                    width=150,
                    height=100,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("₡5.2M", size=28, weight=ft.FontWeight.BOLD, color="#4CAF50"),
                            ft.Text("Ingresos", size=12),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=15,
                    width=150,
                    height=100,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("1,258", size=28, weight=ft.FontWeight.BOLD, color="#FF9800"),
                            ft.Text("Clientes", size=12),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=15,
                    width=150,
                    height=100,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("98%", size=28, weight=ft.FontWeight.BOLD, color="#F44336"),
                            ft.Text("Satisfacción", size=12),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=15,
                    width=150,
                    height=100,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        ),
        margin=ft.margin.only(bottom=30),
    )
    
    # Crear grid de cards
    cards_grid = ft.Row(
        [
            create_card(ft.Icons.BAR_CHART, "Reportes", "Ver reportes detallados de ventas", "#2196F3"),
            create_card(ft.Icons.INVENTORY, "Productos", "Gestionar inventario de productos", "#4CAF50"),
            create_card(ft.Icons.PEOPLE, "Clientes", "Administrar base de clientes", "#FF9800"),
            create_card(ft.Icons.RECEIPT, "Facturas", "Generar y gestionar facturas", "#9C27B0"),
            create_card(ft.Icons.TRENDING_UP, "Estadísticas", "Métricas y análisis de negocio", "#F44336"),
        ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        wrap=True,
    )
    
    # Agregar contenido a la página
    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("🎯 DASHBOARD PRINCIPAL", 
                               size=28, 
                               weight=ft.FontWeight.BOLD, 
                               color="#2196F3"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Divider(height=10, color="transparent"),
                ft.Text("Bienvenido al sistema de gestión de ventas", 
                       size=18, 
                       text_align=ft.TextAlign.CENTER,
                       width=page.window.width),
                ft.Divider(height=30),
                stats_section,
                cards_grid,
                ft.Divider(height=30),
                ft.ElevatedButton(
                    "Volver al Inicio", 
                    on_click=volver_inicio,
                    icon=ft.Icons.ARROW_BACK,
                    style=ft.ButtonStyle(
                        bgcolor={ft.Colors.BLUE: "#2196F3"},
                        color=ft.Colors.WHITE,
                    )
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        )
    )
    
    page.update()

if __name__ == "__main__":
    ft.app(target=main)