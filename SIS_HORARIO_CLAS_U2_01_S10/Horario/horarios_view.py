# horarios_view.py
import flet as ft
from conexion import ConexionDB
from acciones.editar_horario_view import EditarHorarioView

class HorariosView(ft.Container):
    def __init__(self, page, volver_atras):
        super().__init__(expand=True)
        self.page = page
        self.volver_atras = volver_atras
        self.conexion = ConexionDB()
        self.titulo = ft.Text("⏰ Gestión de Horarios", size=22, weight="bold")
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Día")),
                ft.DataColumn(ft.Text("Hora Inicio")),
                ft.DataColumn(ft.Text("Hora Fin")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[]
        )
        self.btn_volver = ft.ElevatedButton("⬅️ Volver", on_click=lambda e: self.volver_atras())
        self.btn_actualizar = ft.ElevatedButton("🔄 Actualizar", on_click=lambda e: self.cargar_horarios())
        self.btn_agregar = ft.ElevatedButton("➕ Agregar", on_click=lambda e: self.mostrar_formulario_nuevo())
        self.content = ft.Column(
            [self.titulo, ft.Row([self.btn_volver, self.btn_actualizar, self.btn_agregar], alignment=ft.MainAxisAlignment.START),
             ft.Container(self.tabla, expand=True, border_radius=10, padding=10, bgcolor=ft.Colors.BLUE_50)],
            spacing=15, expand=True, scroll=ft.ScrollMode.AUTO
        )
        self.cargar_horarios()

    def cargar_horarios(self):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("SELECT horario_id, dia_semana, hora_inicio, hora_fin FROM horarios_base")
                resultados = cursor.fetchall()
                self.tabla.rows.clear()
                for fila in resultados:
                    horario_id = fila[0]

                    def crear_botones(hid):
                        return ft.Row([
                            ft.IconButton(icon=ft.Icons.EDIT, tooltip="Editar", on_click=lambda e, _hid=hid: self.mostrar_formulario_editar(_hid)),
                            ft.IconButton(icon=ft.Icons.DELETE, tooltip="Eliminar", icon_color="red", on_click=lambda e, _hid=hid: self.eliminar_horario(_hid))
                        ])

                    self.tabla.rows.append(ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(horario_id))),
                        ft.DataCell(ft.Text(fila[1] or "")),
                        ft.DataCell(ft.Text(str(fila[2]))),
                        ft.DataCell(ft.Text(str(fila[3]))),
                        ft.DataCell(crear_botones(horario_id))
                    ]))
                self.page.update()
            except Exception as e:
                print(f"❌ Error al cargar horarios: {e}")
            finally:
                self.conexion.cerrar(conexion)

    def mostrar_formulario_nuevo(self):
        txt_dia = ft.TextField(label="Día de la semana")
        txt_hora_inicio = ft.TextField(label="Hora Inicio (HH:MM)")
        txt_hora_fin = ft.TextField(label="Hora Fin (HH:MM)")

        def guardar_nuevo(e):
            conexion = self.conexion.conectar()
            if conexion:
                cur = conexion.cursor()
                try:
                    cur.execute("INSERT INTO horarios_base (dia_semana, hora_inicio, hora_fin) VALUES (%s, %s, %s)", (txt_dia.value, txt_hora_inicio.value, txt_hora_fin.value))
                    conexion.commit()
                    self.cerrar_dialogo(dlg)
                    self.cargar_horarios()
                except Exception as ex:
                    print(f"❌ Error al insertar horario: {ex}")
                finally:
                    self.conexion.cerrar(conexion)

        dlg = ft.AlertDialog(
            title=ft.Text("➕ Nuevo Horario"),
            content=ft.Column([txt_dia, txt_hora_inicio, txt_hora_fin], spacing=10),
            actions=[ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg)), ft.TextButton("Guardar", on_click=guardar_nuevo)]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def mostrar_formulario_editar(self, horario_id):
        editar_vista = EditarHorarioView(self.page, self.volver_atras, horario_id)
        self.volver_atras(editar_vista)

    def eliminar_horario(self, horario_id):
        dlg_confirm = ft.AlertDialog(
            title=ft.Text("⚠️ Confirmar eliminación"),
            content=ft.Text("¿Está seguro de que desea eliminar este horario?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg_confirm)),
                ft.TextButton("Eliminar", style=ft.ButtonStyle(color="white", bgcolor="red"), on_click=lambda e: self.confirmar_eliminar(horario_id, dlg_confirm))
            ]
        )
        self.page.dialog = dlg_confirm
        dlg_confirm.open = True
        self.page.update()

    def confirmar_eliminar(self, horario_id, dlg_confirm):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("DELETE FROM horarios_base WHERE horario_id = %s", (horario_id,))
                conexion.commit()
                self.cerrar_dialogo(dlg_confirm)
                self.cargar_horarios()
            except Exception as e:
                print(f"❌ Error al eliminar horario: {e}")
            finally:
                self.conexion.cerrar(conexion)

    def cerrar_dialogo(self, dlg):
        dlg.open = False
        self.page.update()


