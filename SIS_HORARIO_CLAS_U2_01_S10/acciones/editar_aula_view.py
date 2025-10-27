import flet as ft
from conexion import ConexionDB

class EditarAulaView(ft.Container):
    def __init__(self, page, cambiar_vista, aula_id):
        super().__init__(expand=True)
        self.page = page
        self.cambiar_vista = cambiar_vista
        self.aula_id = aula_id
        self.conexion = ConexionDB()
        self.titulo = ft.Text(f"✏️ Editar Aula (ID: {aula_id})", size=22, weight="bold")
        self.column = ft.Column([self.titulo, ft.ProgressRing()], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
        self.content = ft.Container(content=self.column, alignment=ft.alignment.center, padding=20)
        self.cargar_datos_aula()

    def cargar_datos_aula(self):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("SELECT nombre_aula, capacidad FROM aulas WHERE aula_id = %s", (self.aula_id,))
                datos = cur.fetchone()
                if datos:
                    nombre, capacidad = datos
                    self.txt_nombre = ft.TextField(label="Nombre del Aula", value=nombre, width=350)
                    self.txt_capacidad = ft.TextField(label="Capacidad", value=str(capacidad), width=350)
                    btn_guardar = ft.ElevatedButton("💾 Guardar cambios", bgcolor=ft.Colors.GREEN, color="white", on_click=self.guardar_cambios)
                    btn_atras = ft.OutlinedButton("⬅️ Atrás", on_click=lambda e: self.volver_a_aulas())
                    self.column.controls.clear()
                    self.column.controls.extend([self.titulo, ft.Column([self.txt_nombre, self.txt_capacidad], spacing=10), ft.Row([btn_guardar, btn_atras], spacing=15)])
                    self.page.update()
                else:
                    self.column.controls.clear()
                    self.column.controls.append(ft.Text("❌ No se encontraron datos.", color="red"))
                    self.page.update()
            except Exception as e:
                print(f"❌ Error al cargar aula: {e}")
            finally:
                self.conexion.cerrar(conexion)

    def guardar_cambios(self, e):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("UPDATE aulas SET nombre_aula=%s, capacidad=%s WHERE aula_id=%s", (self.txt_nombre.value, self.txt_capacidad.value, self.aula_id))
                conexion.commit()
                self.page.snack_bar = ft.SnackBar(ft.Text("Cambios guardados correctamente ✅", color="white"), bgcolor="green", open=True)
                self.page.update()
            except Exception as ex:
                print(f"❌ Error al guardar cambios: {ex}")
            finally:
                self.conexion.cerrar(conexion)

    def volver_a_aulas(self):
        from Aula.aulas_view import AulasView
        self.cambiar_vista(AulasView(self.page, self.cambiar_vista))

