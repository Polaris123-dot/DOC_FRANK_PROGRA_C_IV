import flet as ft
from conexion import ConexionDB

class EditarEstructuraView(ft.Container):
    def __init__(self, page, cambiar_vista, estructura_id):
        super().__init__(expand=True)
        self.page = page
        self.cambiar_vista = cambiar_vista
        self.estructura_id = estructura_id
        self.conexion = ConexionDB()
        self.titulo = ft.Text(f"✏️ Editar Estructura Curricular (ID: {estructura_id})", size=22, weight="bold")
        self.column = ft.Column([self.titulo, ft.ProgressRing()], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
        self.content = ft.Container(content=self.column, alignment=ft.alignment.center, padding=20)
        self.cargar_datos_estructura()

    def cargar_datos_estructura(self):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("SELECT curso_id, ciclo_id, especialidad_id FROM estructura_curricular WHERE estructura_id = %s", (self.estructura_id,))
                datos = cur.fetchone()
                if datos:
                    curso_id, ciclo_id, especialidad_id = datos
                    self.txt_curso_id = ft.TextField(label="ID Curso", value=str(curso_id) if curso_id else "", width=350)
                    self.txt_ciclo_id = ft.TextField(label="ID Ciclo", value=str(ciclo_id) if ciclo_id else "", width=350)
                    self.txt_especialidad_id = ft.TextField(label="ID Especialidad", value=str(especialidad_id) if especialidad_id else "", width=350)
                    btn_guardar = ft.ElevatedButton("💾 Guardar cambios", bgcolor=ft.Colors.GREEN, color="white", on_click=self.guardar_cambios)
                    btn_atras = ft.OutlinedButton("⬅️ Atrás", on_click=lambda e: self.volver_a_estructura())
                    self.column.controls.clear()
                    self.column.controls.extend([self.titulo, ft.Column([self.txt_curso_id, self.txt_ciclo_id, self.txt_especialidad_id], spacing=10), ft.Row([btn_guardar, btn_atras], spacing=15)])
                    self.page.update()
                else:
                    self.column.controls.clear()
                    self.column.controls.append(ft.Text("❌ No se encontraron datos.", color="red"))
                    self.page.update()
            except Exception as e:
                print(f"❌ Error al cargar estructura curricular: {e}")
            finally:
                self.conexion.cerrar(conexion)

    def guardar_cambios(self, e):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("UPDATE estructura_curricular SET curso_id=%s, ciclo_id=%s, especialidad_id=%s WHERE estructura_id=%s", 
                           (int(self.txt_curso_id.value) if self.txt_curso_id.value else None,
                            int(self.txt_ciclo_id.value) if self.txt_ciclo_id.value else None,
                            int(self.txt_especialidad_id.value) if self.txt_especialidad_id.value else None,
                            self.estructura_id))
                conexion.commit()
                self.page.snack_bar = ft.SnackBar(ft.Text("Cambios guardados correctamente ✅", color="white"), bgcolor="green", open=True)
                self.page.update()
            except Exception as ex:
                print(f"❌ Error al guardar cambios: {ex}")
            finally:
                self.conexion.cerrar(conexion)

    def volver_a_estructura(self):
        from Estructura.estructura_view import EstructuraView
        self.cambiar_vista(EstructuraView(self.page, self.cambiar_vista))


