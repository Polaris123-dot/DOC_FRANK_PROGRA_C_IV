import flet as ft
from conexion import ConexionDB

class EditarDocenteView(ft.Container):
    def __init__(self, page, cambiar_vista, docente_id):
        super().__init__(expand=True)
        self.page = page
        self.cambiar_vista = cambiar_vista
        self.docente_id = docente_id
        self.conexion = ConexionDB()
        self.titulo = ft.Text(f"✏️ Editar Docente (ID: {docente_id})", size=22, weight="bold")
        self.column = ft.Column([self.titulo, ft.ProgressRing()], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
        self.content = ft.Container(content=self.column, alignment=ft.alignment.center, padding=20)
        self.cargar_datos_docente()

    def cargar_datos_docente(self):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("SELECT persona_id, especialidad_id, estado FROM docentes WHERE docente_id = %s", (self.docente_id,))
                datos = cur.fetchone()
                if datos:
                    persona_id, especialidad_id, estado = datos
                    self.txt_persona_id = ft.TextField(label="ID Persona", value=str(persona_id) if persona_id else "", width=350)
                    self.txt_especialidad_id = ft.TextField(label="ID Especialidad", value=str(especialidad_id) if especialidad_id else "", width=350)
                    self.txt_estado = ft.TextField(label="Estado", value=estado, width=350)
                    btn_guardar = ft.ElevatedButton("💾 Guardar cambios", bgcolor=ft.Colors.GREEN, color="white", on_click=self.guardar_cambios)
                    btn_atras = ft.OutlinedButton("⬅️ Atrás", on_click=lambda e: self.volver_a_docentes())
                    self.column.controls.clear()
                    self.column.controls.extend([self.titulo, ft.Column([self.txt_persona_id, self.txt_especialidad_id, self.txt_estado], spacing=10), ft.Row([btn_guardar, btn_atras], spacing=15)])
                    self.page.update()
                else:
                    self.column.controls.clear()
                    self.column.controls.append(ft.Text("❌ No se encontraron datos.", color="red"))
                    self.page.update()
            except Exception as e:
                print(f"❌ Error al cargar docente: {e}")
            finally:
                self.conexion.cerrar(conexion)

    def guardar_cambios(self, e):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("UPDATE docentes SET persona_id=%s, especialidad_id=%s, estado=%s WHERE docente_id=%s", 
                           (int(self.txt_persona_id.value) if self.txt_persona_id.value else None, 
                            int(self.txt_especialidad_id.value) if self.txt_especialidad_id.value else None, 
                            self.txt_estado.value, self.docente_id))
                conexion.commit()
                self.page.snack_bar = ft.SnackBar(ft.Text("Cambios guardados correctamente ✅", color="white"), bgcolor="green", open=True)
                self.page.update()
            except Exception as ex:
                print(f"❌ Error al guardar cambios: {ex}")
            finally:
                self.conexion.cerrar(conexion)

    def volver_a_docentes(self):
        from Docente.docentes_view import DocentesView
        self.cambiar_vista(DocentesView(self.page, self.cambiar_vista))

