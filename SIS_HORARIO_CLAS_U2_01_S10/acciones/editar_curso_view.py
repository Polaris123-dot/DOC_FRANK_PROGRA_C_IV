import flet as ft
from conexion import ConexionDB

class EditarCursoView(ft.Container):
    def __init__(self, page, cambiar_vista, curso_id):
        super().__init__(expand=True)
        self.page = page
        self.cambiar_vista = cambiar_vista
        self.curso_id = curso_id
        self.conexion = ConexionDB()
        self.titulo = ft.Text(f"✏️ Editar Curso (ID: {curso_id})", size=22, weight="bold")
        self.column = ft.Column([self.titulo, ft.ProgressRing()], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
        self.content = ft.Container(content=self.column, alignment=ft.alignment.center, padding=20)
        self.cargar_datos_curso()

    def cargar_datos_curso(self):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("SELECT nombre, creditos FROM cursos WHERE curso_id = %s", (self.curso_id,))
                datos = cur.fetchone()
                if datos:
                    nombre, creditos = datos
                    self.txt_nombre = ft.TextField(label="Nombre del Curso", value=nombre, width=350)
                    self.txt_creditos = ft.TextField(label="Créditos", value=str(creditos), width=350)
                    btn_guardar = ft.ElevatedButton("💾 Guardar cambios", bgcolor=ft.Colors.GREEN, color="white", on_click=self.guardar_cambios)
                    btn_atras = ft.OutlinedButton("⬅️ Atrás", on_click=lambda e: self.volver_a_cursos())
                    self.column.controls.clear()
                    self.column.controls.extend([self.titulo, ft.Column([self.txt_nombre, self.txt_creditos], spacing=10), ft.Row([btn_guardar, btn_atras], spacing=15)])
                    self.page.update()
                else:
                    self.column.controls.clear()
                    self.column.controls.append(ft.Text("❌ No se encontraron datos.", color="red"))
                    self.page.update()
            except Exception as e:
                print(f"❌ Error al cargar curso: {e}")
            finally:
                self.conexion.cerrar(conexion)

    def guardar_cambios(self, e):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("UPDATE cursos SET nombre=%s, creditos=%s WHERE curso_id=%s", (self.txt_nombre.value, self.txt_creditos.value, self.curso_id))
                conexion.commit()
                self.page.snack_bar = ft.SnackBar(ft.Text("Cambios guardados correctamente ✅", color="white"), bgcolor="green", open=True)
                self.page.update()
            except Exception as ex:
                print(f"❌ Error al guardar cambios: {ex}")
            finally:
                self.conexion.cerrar(conexion)

    def volver_a_cursos(self):
        from Curso.cursos_view import CursosView
        self.cambiar_vista(CursosView(self.page, self.cambiar_vista))

