import flet as ft
from Persona.personas_view import PersonasView
from Usuario.usuarios_view import UsuariosView
from Especialidad.especialidades_view import EspecialidadesView
from Ciclo.ciclos_view import CiclosView
from Curso.cursos_view import CursosView
from Aula.aulas_view import AulasView
from Docente.docentes_view import DocentesView
from Horario.horarios_view import HorariosView
from Semana.semanas_view import SemanasView
from Estructura.estructura_view import EstructuraView
from Asignacion.asignaciones_view import AsignacionesView

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
        elif nombre_tabla == "Usuarios":
            self.abrir_usuarios()
        elif nombre_tabla == "Especialidades":
            self.abrir_especialidades()
        elif nombre_tabla == "Ciclos":
            self.abrir_ciclos()
        elif nombre_tabla == "Cursos":
            self.abrir_cursos()
        elif nombre_tabla == "Aulas":
            self.abrir_aulas()
        elif nombre_tabla == "Docentes":
            self.abrir_docentes()
        elif nombre_tabla == "Horarios_Base":
            self.abrir_horarios()
        elif nombre_tabla == "Semanas":
            self.abrir_semanas()
        elif nombre_tabla == "Estructura_Curricular":
            self.abrir_estructura()
        elif nombre_tabla == "Asignaciones_Semanales":
            self.abrir_asignaciones()
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
    # MÉTODOS PARA ABRIR CADA VISTA
    # ────────────────────────────────────────────────
    def abrir_personas(self):
        def volver_o_navegar(nueva_vista=None):
            if nueva_vista is None:
                self.cambiar_vista(DashboardView(self.page, self.cambiar_vista))
            else:
                self.cambiar_vista(nueva_vista)
        self.cambiar_vista(PersonasView(self.page, volver_atras=volver_o_navegar))

    def abrir_usuarios(self):
        def volver_o_navegar(nueva_vista=None):
            if nueva_vista is None:
                self.cambiar_vista(DashboardView(self.page, self.cambiar_vista))
            else:
                self.cambiar_vista(nueva_vista)
        self.cambiar_vista(UsuariosView(self.page, volver_atras=volver_o_navegar))

    def abrir_especialidades(self):
        def volver_o_navegar(nueva_vista=None):
            if nueva_vista is None:
                self.cambiar_vista(DashboardView(self.page, self.cambiar_vista))
            else:
                self.cambiar_vista(nueva_vista)
        self.cambiar_vista(EspecialidadesView(self.page, volver_atras=volver_o_navegar))

    def abrir_ciclos(self):
        def volver_o_navegar(nueva_vista=None):
            if nueva_vista is None:
                self.cambiar_vista(DashboardView(self.page, self.cambiar_vista))
            else:
                self.cambiar_vista(nueva_vista)
        self.cambiar_vista(CiclosView(self.page, volver_atras=volver_o_navegar))

    def abrir_cursos(self):
        def volver_o_navegar(nueva_vista=None):
            if nueva_vista is None:
                self.cambiar_vista(DashboardView(self.page, self.cambiar_vista))
            else:
                self.cambiar_vista(nueva_vista)
        self.cambiar_vista(CursosView(self.page, volver_atras=volver_o_navegar))

    def abrir_aulas(self):
        def volver_o_navegar(nueva_vista=None):
            if nueva_vista is None:
                self.cambiar_vista(DashboardView(self.page, self.cambiar_vista))
            else:
                self.cambiar_vista(nueva_vista)
        self.cambiar_vista(AulasView(self.page, volver_atras=volver_o_navegar))

    def abrir_docentes(self):
        def volver_o_navegar(nueva_vista=None):
            if nueva_vista is None:
                self.cambiar_vista(DashboardView(self.page, self.cambiar_vista))
            else:
                self.cambiar_vista(nueva_vista)
        self.cambiar_vista(DocentesView(self.page, volver_atras=volver_o_navegar))

    def abrir_horarios(self):
        def volver_o_navegar(nueva_vista=None):
            if nueva_vista is None:
                self.cambiar_vista(DashboardView(self.page, self.cambiar_vista))
            else:
                self.cambiar_vista(nueva_vista)
        self.cambiar_vista(HorariosView(self.page, volver_atras=volver_o_navegar))

    def abrir_semanas(self):
        def volver_o_navegar(nueva_vista=None):
            if nueva_vista is None:
                self.cambiar_vista(DashboardView(self.page, self.cambiar_vista))
            else:
                self.cambiar_vista(nueva_vista)
        self.cambiar_vista(SemanasView(self.page, volver_atras=volver_o_navegar))

    def abrir_estructura(self):
        def volver_o_navegar(nueva_vista=None):
            if nueva_vista is None:
                self.cambiar_vista(DashboardView(self.page, self.cambiar_vista))
            else:
                self.cambiar_vista(nueva_vista)
        self.cambiar_vista(EstructuraView(self.page, volver_atras=volver_o_navegar))

    def abrir_asignaciones(self):
        def volver_o_navegar(nueva_vista=None):
            if nueva_vista is None:
                self.cambiar_vista(DashboardView(self.page, self.cambiar_vista))
            else:
                self.cambiar_vista(nueva_vista)
        self.cambiar_vista(AsignacionesView(self.page, volver_atras=volver_o_navegar))
