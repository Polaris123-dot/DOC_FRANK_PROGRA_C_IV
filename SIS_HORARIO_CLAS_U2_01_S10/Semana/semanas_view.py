# semanas_view.py
import flet as ft
from conexion import ConexionDB
from acciones.editar_semana_view import EditarSemanaView

class SemanasView(ft.Container):
    def __init__(self, page, volver_atras):
        super().__init__(expand=True)
        self.page = page
        self.volver_atras = volver_atras
        self.conexion = ConexionDB()
        self.titulo = ft.Text("📅 Gestión de Semanas", size=22, weight="bold")
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Número")),
                ft.DataColumn(ft.Text("Fecha Inicio")),
                ft.DataColumn(ft.Text("Fecha Fin")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[]
        )
        self.btn_volver = ft.ElevatedButton("⬅️ Volver", on_click=lambda e: self.volver_atras())
        self.btn_actualizar = ft.ElevatedButton("🔄 Actualizar", on_click=lambda e: self.cargar_semanas())
        self.btn_agregar = ft.ElevatedButton("➕ Agregar", on_click=lambda e: self.mostrar_formulario_nuevo())
        self.content = ft.Column(
            [self.titulo, ft.Row([self.btn_volver, self.btn_actualizar, self.btn_agregar], alignment=ft.MainAxisAlignment.START),
             ft.Container(self.tabla, expand=True, border_radius=10, padding=10, bgcolor=ft.Colors.BLUE_50)],
            spacing=15, expand=True, scroll=ft.ScrollMode.AUTO
        )
        self.cargar_semanas()

    def cargar_semanas(self):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("SELECT semana_id, numero_semana, fecha_inicio, fecha_fin FROM semanas")
                resultados = cursor.fetchall()
                self.tabla.rows.clear()
                for fila in resultados:
                    semana_id = fila[0]

                    def crear_botones(sid):
                        return ft.Row([
                            ft.IconButton(icon=ft.Icons.EDIT, tooltip="Editar", on_click=lambda e, _sid=sid: self.mostrar_formulario_editar(_sid)),
                            ft.IconButton(icon=ft.Icons.DELETE, tooltip="Eliminar", icon_color="red", on_click=lambda e, _sid=sid: self.eliminar_semana(_sid))
                        ])

                    self.tabla.rows.append(ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(semana_id))),
                        ft.DataCell(ft.Text(str(fila[1]) if fila[1] else "")),
                        ft.DataCell(ft.Text(str(fila[2]) if fila[2] else "")),
                        ft.DataCell(ft.Text(str(fila[3]) if fila[3] else "")),
                        ft.DataCell(crear_botones(semana_id))
                    ]))
                self.page.update()
            except Exception as e:
                print(f"❌ Error al cargar semanas: {e}")
            finally:
                self.conexion.cerrar(conexion)

    def mostrar_formulario_nuevo(self):
        txt_numero = ft.TextField(label="Número de Semana")
        txt_fecha_inicio = ft.TextField(label="Fecha Inicio (YYYY-MM-DD)")
        txt_fecha_fin = ft.TextField(label="Fecha Fin (YYYY-MM-DD)")

        def guardar_nuevo(e):
            conexion = self.conexion.conectar()
            if conexion:
                cur = conexion.cursor()
                try:
                    cur.execute("INSERT INTO semanas (numero_semana, fecha_inicio, fecha_fin) VALUES (%s, %s, %s)", (txt_numero.value, txt_fecha_inicio.value, txt_fecha_fin.value))
                    conexion.commit()
                    self.cerrar_dialogo(dlg)
                    self.cargar_semanas()
                except Exception as ex:
                    print(f"❌ Error al insertar semana: {ex}")
                finally:
                    self.conexion.cerrar(conexion)

        dlg = ft.AlertDialog(
            title=ft.Text("➕ Nueva Semana"),
            content=ft.Column([txt_numero, txt_fecha_inicio, txt_fecha_fin], spacing=10),
            actions=[ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg)), ft.TextButton("Guardar", on_click=guardar_nuevo)]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def mostrar_formulario_editar(self, semana_id):
        editar_vista = EditarSemanaView(self.page, self.volver_atras, semana_id)
        self.volver_atras(editar_vista)

    def eliminar_semana(self, semana_id):
        dlg_confirm = ft.AlertDialog(
            title=ft.Text("⚠️ Confirmar eliminación"),
            content=ft.Text("¿Está seguro de que desea eliminar esta semana?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg_confirm)),
                ft.TextButton("Eliminar", style=ft.ButtonStyle(color="white", bgcolor="red"), on_click=lambda e: self.confirmar_eliminar(semana_id, dlg_confirm))
            ]
        )
        self.page.dialog = dlg_confirm
        dlg_confirm.open = True
        self.page.update()

    def confirmar_eliminar(self, semana_id, dlg_confirm):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("DELETE FROM semanas WHERE semana_id = %s", (semana_id,))
                conexion.commit()
                self.cerrar_dialogo(dlg_confirm)
                self.cargar_semanas()
            except Exception as e:
                print(f"❌ Error al eliminar semana: {e}")
            finally:
                self.conexion.cerrar(conexion)

    def cerrar_dialogo(self, dlg):
        dlg.open = False
        self.page.update()


