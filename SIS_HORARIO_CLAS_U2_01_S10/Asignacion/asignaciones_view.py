# asignaciones_view.py
import flet as ft
from conexion import ConexionDB
from acciones.editar_asignacion_view import EditarAsignacionView

class AsignacionesView(ft.Container):
    def __init__(self, page, volver_atras):
        super().__init__(expand=True)
        self.page = page
        self.volver_atras = volver_atras
        self.conexion = ConexionDB()
        self.titulo = ft.Text("📝 Gestión de Asignaciones Semanales", size=22, weight="bold")
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("ID Docente")),
                ft.DataColumn(ft.Text("ID Curso")),
                ft.DataColumn(ft.Text("ID Aula")),
                ft.DataColumn(ft.Text("ID Semana")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[]
        )
        self.btn_volver = ft.ElevatedButton("⬅️ Volver", on_click=lambda e: self.volver_atras())
        self.btn_actualizar = ft.ElevatedButton("🔄 Actualizar", on_click=lambda e: self.cargar_asignaciones())
        self.btn_agregar = ft.ElevatedButton("➕ Agregar", on_click=lambda e: self.mostrar_formulario_nuevo())
        self.content = ft.Column(
            [self.titulo, ft.Row([self.btn_volver, self.btn_actualizar, self.btn_agregar], alignment=ft.MainAxisAlignment.START),
             ft.Container(self.tabla, expand=True, border_radius=10, padding=10, bgcolor=ft.Colors.BLUE_50)],
            spacing=15, expand=True, scroll=ft.ScrollMode.AUTO
        )
        self.cargar_asignaciones()

    def cargar_asignaciones(self):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("SELECT asignacion_id, docente_id, curso_id, aula_id, semana_id FROM asignaciones_semanales")
                resultados = cursor.fetchall()
                self.tabla.rows.clear()
                for fila in resultados:
                    asignacion_id = fila[0]

                    def crear_botones(aid):
                        return ft.Row([
                            ft.IconButton(icon=ft.Icons.EDIT, tooltip="Editar", on_click=lambda e, _aid=aid: self.mostrar_formulario_editar(_aid)),
                            ft.IconButton(icon=ft.Icons.DELETE, tooltip="Eliminar", icon_color="red", on_click=lambda e, _aid=aid: self.eliminar_asignacion(_aid))
                        ])

                    self.tabla.rows.append(ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(asignacion_id))),
                        ft.DataCell(ft.Text(str(fila[1]) if fila[1] else "")),
                        ft.DataCell(ft.Text(str(fila[2]) if fila[2] else "")),
                        ft.DataCell(ft.Text(str(fila[3]) if fila[3] else "")),
                        ft.DataCell(ft.Text(str(fila[4]) if fila[4] else "")),
                        ft.DataCell(crear_botones(asignacion_id))
                    ]))
                self.page.update()
            except Exception as e:
                print(f"❌ Error al cargar asignaciones: {e}")
            finally:
                self.conexion.cerrar(conexion)

    def mostrar_formulario_nuevo(self):
        txt_docente_id = ft.TextField(label="ID Docente")
        txt_curso_id = ft.TextField(label="ID Curso")
        txt_aula_id = ft.TextField(label="ID Aula")
        txt_semana_id = ft.TextField(label="ID Semana")

        def guardar_nuevo(e):
            conexion = self.conexion.conectar()
            if conexion:
                cur = conexion.cursor()
                try:
                    cur.execute("INSERT INTO asignaciones_semanales (docente_id, curso_id, aula_id, semana_id) VALUES (%s, %s, %s, %s)", (txt_docente_id.value, txt_curso_id.value, txt_aula_id.value, txt_semana_id.value))
                    conexion.commit()
                    self.cerrar_dialogo(dlg)
                    self.cargar_asignaciones()
                except Exception as ex:
                    print(f"❌ Error al insertar asignación: {ex}")
                finally:
                    self.conexion.cerrar(conexion)

        dlg = ft.AlertDialog(
            title=ft.Text("➕ Nueva Asignación"),
            content=ft.Column([txt_docente_id, txt_curso_id, txt_aula_id, txt_semana_id], spacing=10),
            actions=[ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg)), ft.TextButton("Guardar", on_click=guardar_nuevo)]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def mostrar_formulario_editar(self, asignacion_id):
        editar_vista = EditarAsignacionView(self.page, self.volver_atras, asignacion_id)
        self.volver_atras(editar_vista)

    def eliminar_asignacion(self, asignacion_id):
        dlg_confirm = ft.AlertDialog(
            title=ft.Text("⚠️ Confirmar eliminación"),
            content=ft.Text("¿Está seguro de que desea eliminar esta asignación?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg_confirm)),
                ft.TextButton("Eliminar", style=ft.ButtonStyle(color="white", bgcolor="red"), on_click=lambda e: self.confirmar_eliminar(asignacion_id, dlg_confirm))
            ]
        )
        self.page.dialog = dlg_confirm
        dlg_confirm.open = True
        self.page.update()

    def confirmar_eliminar(self, asignacion_id, dlg_confirm):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("DELETE FROM asignaciones_semanales WHERE asignacion_id = %s", (asignacion_id,))
                conexion.commit()
                self.cerrar_dialogo(dlg_confirm)
                self.cargar_asignaciones()
            except Exception as e:
                print(f"❌ Error al eliminar asignación: {e}")
            finally:
                self.conexion.cerrar(conexion)

    def cerrar_dialogo(self, dlg):
        dlg.open = False
        self.page.update()


