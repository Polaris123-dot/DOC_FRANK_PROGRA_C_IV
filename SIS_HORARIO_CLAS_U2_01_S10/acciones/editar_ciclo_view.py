import flet as ft
from conexion import ConexionDB

class EditarCicloView(ft.Container):
    def __init__(self, page, cambiar_vista, ciclo_id):
        super().__init__(expand=True)
        self.page = page
        self.cambiar_vista = cambiar_vista
        self.ciclo_id = ciclo_id
        self.conexion = ConexionDB()

        self.titulo = ft.Text(f"✏️ Editar Ciclo (ID: {ciclo_id})", size=22, weight="bold")
        self.column = ft.Column([self.titulo, ft.ProgressRing()], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
        self.content = ft.Container(content=self.column, alignment=ft.alignment.center, padding=20)
        self.cargar_datos_ciclo()

    def cargar_datos_ciclo(self):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("SELECT numero_ciclo, descripcion FROM ciclos WHERE ciclo_id = %s", (self.ciclo_id,))
                datos = cur.fetchone()

                if datos:
                    numero, descripcion = datos
                    self.txt_numero = ft.TextField(label="Número de Ciclo", value=str(numero), width=350)
                    self.txt_descripcion = ft.TextField(label="Descripción", value=descripcion, width=350, multiline=True)
                    btn_guardar = ft.ElevatedButton("💾 Guardar cambios", bgcolor=ft.Colors.GREEN, color="white", on_click=self.guardar_cambios)
                    btn_atras = ft.OutlinedButton("⬅️ Atrás", on_click=lambda e: self.volver_a_ciclos())

                    self.column.controls.clear()
                    self.column.controls.extend([
                        self.titulo,
                        ft.Column([self.txt_numero, self.txt_descripcion], spacing=10),
                        ft.Row([btn_guardar, btn_atras], spacing=15)
                    ])
                    self.page.update()
                else:
                    self.column.controls.clear()
                    self.column.controls.append(ft.Text("❌ No se encontraron datos.", color="red"))
                    self.page.update()

            except Exception as e:
                print(f"❌ Error al cargar ciclo: {e}")
            finally:
                self.conexion.cerrar(conexion)

    def guardar_cambios(self, e):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("""
                    UPDATE ciclos
                    SET numero_ciclo=%s, descripcion=%s
                    WHERE ciclo_id=%s
                """, (self.txt_numero.value, self.txt_descripcion.value, self.ciclo_id))
                conexion.commit()

                self.page.snack_bar = ft.SnackBar(ft.Text("Cambios guardados correctamente ✅", color="white"), bgcolor="green", open=True)
                self.page.update()
            except Exception as ex:
                print(f"❌ Error al guardar cambios: {ex}")
            finally:
                self.conexion.cerrar(conexion)

    def volver_a_ciclos(self):
        from Ciclo.ciclos_view import CiclosView
        self.cambiar_vista(CiclosView(self.page, self.cambiar_vista))

