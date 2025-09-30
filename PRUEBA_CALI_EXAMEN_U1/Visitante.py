import flet as ft

# Lista de destinos turísticos con íconos temáticos
DESTINATIONS = [
    ("Ciudad Antigua", ft.Icons.LANDSCAPE, ft.Colors.TEAL_600, "Descubre ruinas históricas y museos."),
    ("Playas del Sol", ft.Icons.BEACH_ACCESS, ft.Colors.YELLOW_600, "Relájate en la arena y disfruta del mar."),
    ("Montaña Escondida", ft.Icons.FOREST, ft.Colors.BROWN_600, "Senderismo, aire puro y vistas panorámicas."),
    ("Mercado Local", ft.Icons.SHOPPING_BAG, ft.Colors.PURPLE_600, "Gastronomía, artesanías y cultura local."),
]

def visitante_view(page: ft.Page, role: str, main_app_function):
    """
    Define la interfaz de usuario para el rol de Visitante con temática turística.
    """
    page.title = f"Explorar Destinos | {role}"

    def logout(e):
        page.clean()
        # Vuelve a la función de login en index.py
        main_app_function(page)
        
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
    for title, icon, color, description in DESTINATIONS:
        card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Icon(icon, color=color, size=30),
                            title=ft.Text(title, weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(description),
                        ),
                        ft.Row(
                            [
                                ft.TextButton(
                                    "Ver Info", 
                                    icon=ft.Icons.INFO_OUTLINE, 
                                    on_click=lambda e, t=title: print(f"Solicitando info de {t}")
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                            # CORRECCIÓN: Se eliminó el 'padding' ya que ft.Row no lo soporta.
                            # El padding se aplica al ft.Container padre (padding=10)
                        )
                    ],
                    spacing=0,
                ),
                padding=10,
            ),
            # Ancho fijo para que se vean bien en el Column
            width=350 
        )
        destination_cards.append(card)

    # Contenedor principal de la vista
    view_content = ft.Column(
        [
            welcome_header,
            ft.Text(f"¡Hola {role}! Elige tu próxima aventura.", size=16, color=ft.Colors.BLUE_GREY_700),
            ft.Divider(height=15),
            # Las tarjetas de destino en un scroll view
            ft.Container(
                content=ft.Column(
                    destination_cards,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                    # CORRECCIÓN: 'scroll' movido del Container al Column.
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
