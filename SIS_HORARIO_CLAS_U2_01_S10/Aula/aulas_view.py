# aulas_view.py
import flet as ft
from conexion import ConexionDB
from acciones.editar_aula_view import EditarAulaView

class AulasView(ft.Container):
    def __init__(self, page, volver_atras):
        super().__init__(expand=True)
        self.page = page
        self.volver_atras = volver_atras
        self.conexion = ConexionDB()
        self.titulo = ft.Text("🏫 Gestión de Aulas", size=22, weight="bold")
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Capacidad")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[]
        )
        self.btn_volver = ft.ElevatedButton("⬅️ Volver", on_click=lambda e: self.volver_atras())
        self.btn_actualizar = ft.ElevatedButton("🔄 Actualizar", on_click=lambda e: self.cargar_aulas())
        self.btn_agregar = ft.ElevatedButton("➕ Agregar", on_click=lambda e: self.mostrar_formulario_nuevo())
        self.content = ft.Column(
            [self.titulo, ft.Row([self.btn_volver, self.btn_actualizar, self.btn_agregar], alignment=ft.MainAxisAlignment.START),
             ft.Container(self.tabla, expand=True, border_radius=10, padding=10, bgcolor=ft.Colors.BLUE_50)],
            spacing=15, expand=True, scroll=ft.ScrollMode.AUTO
        )
        self.cargar_aulas()

    def cargar_aulas(self):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("SELECT aula_id, nombre_aula, capacidad FROM aulas")
                resultados = cursor.fetchall()
                self.tabla.rows.clear()
                for fila in resultados:
                    aula_id = fila[0]

                    def crear_botones(aid):
                        return ft.Row([
                            ft.IconButton(icon=ft.Icons.EDIT, tooltip="Editar", on_click=lambda e, _aid=aid: self.mostrar_formulario_editar(_aid)),
                            ft.IconButton(icon=ft.Icons.DELETE, tooltip="Eliminar", icon_color="red", on_click=lambda e, _aid=aid: self.eliminar_aula(_aid))
                        ])

                    self.tabla.rows.append(ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(aula_id))),
                        ft.DataCell(ft.Text(fila[1] or "")),
                        ft.DataCell(ft.Text(str(fila[2]) if fila[2] else "")),
                        ft.DataCell(crear_botones(aula_id))
                    ]))
                self.page.update()
            except Exception as e:
                print(f"❌ Error al cargar aulas: {e}")
            finally:
                self.conexion.cerrar(conexion)

    def mostrar_formulario_nuevo(self):
        txt_nombre = ft.TextField(label="Nombre del Aula")
        txt_capacidad = ft.TextField(label="Capacidad")

        def guardar_nuevo(e):
            conexion = self.conexion.conectar()
            if conexion:
                cur = conexion.cursor()
                try:
                    cur.execute("INSERT INTO aulas (nombre_aula, capacidad) VALUES (%s, %s)", (txt_nombre.value, txt_capacidad.value))
                    conexion.commit()
                    self.cerrar_dialogo(dlg)
                    self.cargar_aulas()
                except Exception as ex:
                    print(f"❌ Error al insertar aula: {ex}")
                finally:
                    self.conexion.cerrar(conexion)

        dlg = ft.AlertDialog(
            title=ft.Text("➕ Nueva Aula"),
            content=ft.Column([txt_nombre, txt_capacidad], spacing=10),
            actions=[ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg)), ft.TextButton("Guardar", on_click=guardar_nuevo)]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def mostrar_formulario_editar(self, aula_id):
        editar_vista = EditarAulaView(self.page, self.volver_atras, aula_id)
        self.volver_atras(editar_vista)

    def eliminar_aula(self, aula_id):
        dlg_confirm = ft.AlertDialog(
            title=ft.Text("⚠️ Confirmar eliminación"),
            content=ft.Text("¿Está seguro de que desea eliminar esta aula?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg_confirm)),
                ft.TextButton("Eliminar", style=ft.ButtonStyle(color="white", bgcolor="red"), on_click=lambda e: self.confirmar_eliminar(aula_id, dlg_confirm))
            ]
        )
        self.page.dialog = dlg_confirm
        dlg_confirm.open = True
        self.page.update()

    def confirmar_eliminar(self, aula_id, dlg_confirm):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("DELETE FROM aulas WHERE aula_id = %s", (aula_id,))
                conexion.commit()
                self.cerrar_dialogo(dlg_confirm)
                self.cargar_aulas()
            except Exception as e:
                print(f"❌ Error al eliminar aula: {e}")
            finally:
                self.conexion.cerrar(conexion)

    def cerrar_dialogo(self, dlg):
        dlg.open = False
        self.page.update()

