import flet as ft
from Persona.personas_view import PersonasView  # ← importar aquí

class DashboardView(ft.Container):
    def __init__(self, page, cambiar_vista):
        super().__init__(expand=True)
        self.page = page
        self.cambiar_vista = cambiar_vista

        titulo = ft.Text(
            "📘 Panel Principal – Sistema de Horarios Marello",
            size=24,
            weight="bold"
        )

        tablas = [  
            ("Personas", "Datos básicos (base de la identidad)"),
            ("Usuarios", "Cuentas, credenciales, y roles (enlace a personas)"),
            ("Especialidades", "Campos de estudio (Informática, Contabilidad, etc.)"),
            ("Ciclos", "Los 6 niveles académicos (I, II, III, etc.)"),
            ("Cursos", "Materias que se dictan"),
            ("Aulas", "Recurso físico limitado"),
            ("Docentes", "Quién enseña (enlace a Personas)"),
            ("Horarios_Base", "Slots fijos de tiempo"),
            ("Semanas", "Las 18 semanas del ciclo"),
            ("Estructura_Curricular", "Regla curricular (Curso–Ciclo–Especialidad)"),
            ("Asignaciones_Semanales", "Asignación final Docente + Curso + Aula + Semana")
        ]

        grid = ft.GridView(
            expand=True,
            runs_count=3,
            max_extent=280,
            child_aspect_ratio=1.2,
            spacing=10,
            run_spacing=10
        )

        # 🔧 Aquí se corrige el uso de on_click:
        for nombre, descripcion in tablas:
            card_content = ft.Container(
                content=ft.Column(
                    [
                        ft.Text(nombre, size=18, weight="bold"),
                        ft.Text(descripcion, size=13, color=ft.Colors.GREY)
                    ],
                    spacing=5
                ),
                padding=15,
                border_radius=10,
                bgcolor=ft.Colors.BLUE_50,
                ink=True,  # efecto visual al hacer clic
                on_click=lambda e, n=nombre: self.mostrar_tabla(n)
            )

            grid.controls.append(ft.Card(content=card_content, elevation=3))

        self.content = ft.Column(
            [
                titulo,
                grid
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START
        )

    # ────────────────────────────────────────────────
    # MÉTODO PRINCIPAL PARA ABRIR CADA TABLA
    # ────────────────────────────────────────────────
    def mostrar_tabla(self, nombre_tabla):
        if nombre_tabla == "Personas":
            self.abrir_personas()
        if nombre_tabla == "Usuarios":
            self.abrir_personas()
        else:
            dlg = ft.AlertDialog(
                title=ft.Text("Tabla no implementada"),
                content=ft.Text(f"La vista para '{nombre_tabla}' aún no está disponible."),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: self.page.dialog.close())]
            )
            self.page.dialog = dlg
            dlg.open = True
            self.page.update()

    # ────────────────────────────────────────────────
    # GESTIONAR VISTA DE PERSONAS
    # ────────────────────────────────────────────────
    def abrir_personas(self):
        """
        Carga la vista de Personas con navegación dinámica.
        Si PersonasView solicita cambiar de vista (por ejemplo, abrir el editor),
        el mismo callback manejará ambos casos.
        """
        def volver_o_navegar(nueva_vista=None):
            if nueva_vista is None:
                # Volver al dashboard principal
                self.cambiar_vista(DashboardView(self.page, self.cambiar_vista))
            else:
                # Cambiar a la vista que se pasa (por ejemplo EditarPersonaView)
                self.cambiar_vista(nueva_vista)

        personas_vista = PersonasView(self.page, volver_atras=volver_o_navegar)
        self.cambiar_vista(personas_vista)
        
    def abrir_personas(self):
        """
        Carga la vista de Personas con navegación dinámica.
        Si PersonasView solicita cambiar de vista (por ejemplo, abrir el editor),
        el mismo callback manejará ambos casos.
        """
        def volver_o_navegar(nueva_vista=None):
            if nueva_vista is None:
                # Volver al dashboard principal
                self.cambiar_vista(DashboardView(self.page, self.cambiar_vista))
            else:
                # Cambiar a la vista que se pasa (por ejemplo EditarPersonaView)
                self.cambiar_vista(nueva_vista)

        personas_vista = PersonasView(self.page, volver_atras=volver_o_navegar)
        self.cambiar_vista(personas_vista)
