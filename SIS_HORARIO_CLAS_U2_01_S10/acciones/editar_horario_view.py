import flet as ft
from conexion import ConexionDB

class EditarHorarioView(ft.Container):
    def __init__(self, page, cambiar_vista, horario_id):
        super().__init__(expand=True)
        self.page = page
        self.cambiar_vista = cambiar_vista
        self.horario_id = horario_id
        self.conexion = ConexionDB()
        self.titulo = ft.Text(f"✏️ Editar Horario (ID: {horario_id})", size=22, weight="bold")
        self.column = ft.Column([self.titulo, ft.ProgressRing()], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
        self.content = ft.Container(content=self.column, alignment=ft.alignment.center, padding=20)
        self.cargar_datos_horario()

    def cargar_datos_horario(self):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("SELECT dia_semana, hora_inicio, hora_fin FROM horarios_base WHERE horario_id = %s", (self.horario_id,))
                datos = cur.fetchone()
                if datos:
                    dia, hora_inicio, hora_fin = datos
                    self.txt_dia = ft.TextField(label="Día de la semana", value=dia, width=350)
                    self.txt_hora_inicio = ft.TextField(label="Hora Inicio", value=str(hora_inicio), width=350)
                    self.txt_hora_fin = ft.TextField(label="Hora Fin", value=str(hora_fin), width=350)
                    btn_guardar = ft.ElevatedButton("💾 Guardar cambios", bgcolor=ft.Colors.GREEN, color="white", on_click=self.guardar_cambios)
                    btn_atras = ft.OutlinedButton("⬅️ Atrás", on_click=lambda e: self.volver_a_horarios())
                    self.column.controls.clear()
                    self.column.controls.extend([self.titulo, ft.Column([self.txt_dia, self.txt_hora_inicio, self.txt_hora_fin], spacing=10), ft.Row([btn_guardar, btn_atras], spacing=15)])
                    self.page.update()
                else:
                    self.column.controls.clear()
                    self.column.controls.append(ft.Text("❌ No se encontraron datos.", color="red"))
                    self.page.update()
            except Exception as e:
                print(f"❌ Error al cargar horario: {e}")
            finally:
                self.conexion.cerrar(conexion)

    def guardar_cambios(self, e):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("UPDATE horarios_base SET dia_semana=%s, hora_inicio=%s, hora_fin=%s WHERE horario_id=%s", (self.txt_dia.value, self.txt_hora_inicio.value, self.txt_hora_fin.value, self.horario_id))
                conexion.commit()
                self.page.snack_bar = ft.SnackBar(ft.Text("Cambios guardados correctamente ✅", color="white"), bgcolor="green", open=True)
                self.page.update()
            except Exception as ex:
                print(f"❌ Error al guardar cambios: {ex}")
            finally:
                self.conexion.cerrar(conexion)

    def volver_a_horarios(self):
        from Horario.horarios_view import HorariosView
        self.cambiar_vista(HorariosView(self.page, self.cambiar_vista))

