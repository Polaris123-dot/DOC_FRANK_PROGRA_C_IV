import flet as ft
from conexion import ConexionDB

class EditarSemanaView(ft.Container):
    def __init__(self, page, cambiar_vista, semana_id):
        super().__init__(expand=True)
        self.page = page
        self.cambiar_vista = cambiar_vista
        self.semana_id = semana_id
        self.conexion = ConexionDB()
        self.titulo = ft.Text(f"✏️ Editar Semana (ID: {semana_id})", size=22, weight="bold")
        self.column = ft.Column([self.titulo, ft.ProgressRing()], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
        self.content = ft.Container(content=self.column, alignment=ft.alignment.center, padding=20)
        self.cargar_datos_semana()

    def cargar_datos_semana(self):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("SELECT numero_semana, fecha_inicio, fecha_fin FROM semanas WHERE semana_id = %s", (self.semana_id,))
                datos = cur.fetchone()
                if datos:
                    numero, fecha_inicio, fecha_fin = datos
                    self.txt_numero = ft.TextField(label="Número de Semana", value=str(numero), width=350)
                    self.txt_fecha_inicio = ft.TextField(label="Fecha Inicio", value=str(fecha_inicio), width=350)
                    self.txt_fecha_fin = ft.TextField(label="Fecha Fin", value=str(fecha_fin), width=350)
                    btn_guardar = ft.ElevatedButton("💾 Guardar cambios", bgcolor=ft.Colors.GREEN, color="white", on_click=self.guardar_cambios)
                    btn_atras = ft.OutlinedButton("⬅️ Atrás", on_click=lambda e: self.volver_a_semanas())
                    self.column.controls.clear()
                    self.column.controls.extend([self.titulo, ft.Column([self.txt_numero, self.txt_fecha_inicio, self.txt_fecha_fin], spacing=10), ft.Row([btn_guardar, btn_atras], spacing=15)])
                    self.page.update()
                else:
                    self.column.controls.clear()
                    self.column.controls.append(ft.Text("❌ No se encontraron datos.", color="red"))
                    self.page.update()
            except Exception as e:
                print(f"❌ Error al cargar semana: {e}")
            finally:
                self.conexion.cerrar(conexion)

    def guardar_cambios(self, e):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("UPDATE semanas SET numero_semana=%s, fecha_inicio=%s, fecha_fin=%s WHERE semana_id=%s", (self.txt_numero.value, self.txt_fecha_inicio.value, self.txt_fecha_fin.value, self.semana_id))
                conexion.commit()
                self.page.snack_bar = ft.SnackBar(ft.Text("Cambios guardados correctamente ✅", color="white"), bgcolor="green", open=True)
                self.page.update()
            except Exception as ex:
                print(f"❌ Error al guardar cambios: {ex}")
            finally:
                self.conexion.cerrar(conexion)

    def volver_a_semanas(self):
        from Semana.semanas_view import SemanasView
        self.cambiar_vista(SemanasView(self.page, self.cambiar_vista))

