import flet as ft
from conexion import ConexionDB

class EditarAsignacionView(ft.Container):
    def __init__(self, page, cambiar_vista, asignacion_id):
        super().__init__(expand=True)
        self.page = page
        self.cambiar_vista = cambiar_vista
        self.asignacion_id = asignacion_id
        self.conexion = ConexionDB()
        self.titulo = ft.Text(f"✏️ Editar Asignación (ID: {asignacion_id})", size=22, weight="bold")
        self.column = ft.Column([self.titulo, ft.ProgressRing()], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
        self.content = ft.Container(content=self.column, alignment=ft.alignment.center, padding=20)
        self.cargar_datos_asignacion()

    def cargar_datos_asignacion(self):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("SELECT docente_id, curso_id, aula_id, semana_id FROM asignaciones_semanales WHERE asignacion_id = %s", (self.asignacion_id,))
                datos = cur.fetchone()
                if datos:
                    docente_id, curso_id, aula_id, semana_id = datos
                    self.txt_docente_id = ft.TextField(label="ID Docente", value=str(docente_id) if docente_id else "", width=350)
                    self.txt_curso_id = ft.TextField(label="ID Curso", value=str(curso_id) if curso_id else "", width=350)
                    self.txt_aula_id = ft.TextField(label="ID Aula", value=str(aula_id) if aula_id else "", width=350)
                    self.txt_semana_id = ft.TextField(label="ID Semana", value=str(semana_id) if semana_id else "", width=350)
                    btn_guardar = ft.ElevatedButton("💾 Guardar cambios", bgcolor=ft.Colors.GREEN, color="white", on_click=self.guardar_cambios)
                    btn_atras = ft.OutlinedButton("⬅️ Atrás", on_click=lambda e: self.volver_a_asignaciones())
                    self.column.controls.clear()
                    self.column.controls.extend([self.titulo, ft.Column([self.txt_docente_id, self.txt_curso_id, self.txt_aula_id, self.txt_semana_id], spacing=10), ft.Row([btn_guardar, btn_atras], spacing=15)])
                    self.page.update()
                else:
                    self.column.controls.clear()
                    self.column.controls.append(ft.Text("❌ No se encontraron datos.", color="red"))
                    self.page.update()
            except Exception as e:
                print(f"❌ Error al cargar asignación: {e}")
            finally:
                self.conexion.cerrar(conexion)

    def guardar_cambios(self, e):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("UPDATE asignaciones_semanales SET docente_id=%s, curso_id=%s, aula_id=%s, semana_id=%s WHERE asignacion_id=%s", 
                           (int(self.txt_docente_id.value) if self.txt_docente_id.value else None,
                            int(self.txt_curso_id.value) if self.txt_curso_id.value else None,
                            int(self.txt_aula_id.value) if self.txt_aula_id.value else None,
                            int(self.txt_semana_id.value) if self.txt_semana_id.value else None,
                            self.asignacion_id))
                conexion.commit()
                self.page.snack_bar = ft.SnackBar(ft.Text("Cambios guardados correctamente ✅", color="white"), bgcolor="green", open=True)
                self.page.update()
            except Exception as ex:
                print(f"❌ Error al guardar cambios: {ex}")
            finally:
                self.conexion.cerrar(conexion)

    def volver_a_asignaciones(self):
        from Asignacion.asignaciones_view import AsignacionesView
        self.cambiar_vista(AsignacionesView(self.page, self.cambiar_vista))

