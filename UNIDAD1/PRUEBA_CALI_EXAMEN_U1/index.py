import flet as ft
# Importamos las vistas de cada archivo modular
import Administrador
import Usuario
import Cliente
import Visitante

# 1. Definición de credenciales y roles
CREDENTIALS = {
    ("admin", "admin123"): "Administrador",
    ("user", "user123"): "Usuario",
    ("client", "client123"): "Cliente",
    ("visit", "visit123"): "Visitante",
}

def main(page: ft.Page):
    """Función principal que renderiza la vista de Login con estilo Viajes."""
    
    # Configuraciones de la página con estilo de viaje
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 400
    page.window_height = 550
    page.window_resizable = False
    page.title = "Portal de Viajes - Login"
    
    # FONDO DE LA PÁGINA: Azul claro para el cielo/océano
    page.bgcolor = ft.Colors.LIGHT_BLUE_50 

    # Componente para mostrar mensajes de retroalimentación
    feedback_message = ft.Text(
        "Ingresa tus credenciales para tu próximo destino", 
        color=ft.Colors.BLUE_GREY_600,
        size=14
    )

    # Función que se ejecuta al hacer clic en el botón de inicio de sesión
    def login_clicked(e):
        username = username_field.value
        password = password_field.value
        role = CREDENTIALS.get((username, password))

        # Limpiar campos después del intento
        username_field.value = ""
        password_field.value = ""

        # --- Lógica de Navegación Protegida por Roles ---
        if role == "Administrador":
            # Pasamos la función 'main' para permitir el logout
            Administrador.admin_view(page, role, main)
        
        elif role == "Usuario":
            Usuario.usuario_view(page, role, main)
        
        elif role == "Cliente":
            Cliente.cliente_view(page, role, main)
        
        elif role == "Visitante":
            Visitante.visitante_view(page, role, main)
        
        else:
            # Si el login falla
            feedback_message.value = "Error: Credenciales no válidas. ¡Verifica tu boleto!"
            feedback_message.color = ft.Colors.RED_600
            page.update()


    # --- Componentes del Login ---

    # Campos de entrada con íconos de usuario y llave
    username_field = ft.TextField(
        label="Ticket de Usuario (Usuario)", 
        width=300, 
        prefix_icon=ft.Icons.PERSON_PIN_CIRCLE_ROUNDED # Icono temático
    )
    password_field = ft.TextField(
        label="Código de Seguridad (Contraseña)", 
        password=True, 
        can_reveal_password=True, 
        width=300, 
        prefix_icon=ft.Icons.KEY # Icono temático
    )
    
    # Botón de inicio de sesión con estilo y color de acción (como un sol o arena)
    login_button = ft.ElevatedButton(
        text="¡Empezar el Viaje!", 
        width=300, 
        icon=ft.Icons.AIRPLANE_TICKET_ROUNDED, # Icono de billete/vuelo
        on_click=login_clicked,
        bgcolor=ft.Colors.AMBER_600, # Color de destino/sol
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )

    # Encabezado temático
    travel_title = ft.Row(
        [
            ft.Icon(ft.Icons.TRAVEL_EXPLORE, color=ft.Colors.BLUE_700, size=30),
            ft.Text("Portal de Destinos", size=30, weight=ft.FontWeight.BOLD),
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Contenedor que agrupa los elementos del formulario
    login_container = ft.Column(
        [
            travel_title,
            ft.Divider(height=20, color="transparent"),
            username_field,
            password_field,
            ft.Divider(height=10, color="transparent"),
            login_button,
            ft.Divider(height=10, color="transparent"),
            feedback_message,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    
    # ENVOLVEMOS EL FORMULARIO en un contenedor tipo CARD (ticket de embarque)
    login_card = ft.Container(
        login_container,
        width=350,
        padding=ft.padding.all(30),
        border_radius=ft.border_radius.all(20), # Esquinas redondeadas
        bgcolor=ft.Colors.WHITE,
        # Sombra para dar efecto flotante (como un mapa o boleto)
        shadow=ft.BoxShadow(
            0, 15, ft.Colors.BLUE_GREY_200, # Sombra suave
            blur_style=ft.ShadowBlurStyle.NORMAL
        )
    )


    # Limpiamos la página y añadimos la card del login
    page.clean() 
    page.add(login_card)

# Iniciar la aplicación
ft.app(target=main)
