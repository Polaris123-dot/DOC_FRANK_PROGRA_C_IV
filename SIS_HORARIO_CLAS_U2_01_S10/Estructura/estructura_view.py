# estructura_view.py
import flet as ft
from conexion import ConexionDB
from acciones.editar_estructura_view import EditarEstructuraView

class EstructuraView(ft.Container):
    def __init__(self, page, volver_atras):
        super().__init__(expand=True)
        self.page = page
        self.volver_atras = volver_atras
        self.conexion = ConexionDB()
        self.titulo = ft.Text("📋 Gestión de Estructura Curricular", size=22, weight="bold")
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("ID Curso")),
                ft.DataColumn(ft.Text("ID Ciclo")),
                ft.DataColumn(ft.Text("ID Especialidad")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[]
        )
        self.btn_volver = ft.ElevatedButton("⬅️ Volver", on_click=lambda e: self.volver_atras())
        self.btn_actualizar = ft.ElevatedButton("🔄 Actualizar", on_click=lambda e: self.cargar_estructura())
        self.btn_agregar = ft.ElevatedButton("➕ Agregar", on_click=lambda e: self.mostrar_formulario_nuevo())
        self.content = ft.Column(
            [self.titulo, ft.Row([self.btn_volver, self.btn_actualizar, self.btn_agregar], alignment=ft.MainAxisAlignment.START),
             ft.Container(self.tabla, expand=True, border_radius=10, padding=10, bgcolor=ft.Colors.BLUE_50)],
            spacing=15, expand=True, scroll=ft.ScrollMode.AUTO
        )
        self.cargar_estructura()

    def cargar_estructura(self):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("SELECT estructura_id, curso_id, ciclo_id, especialidad_id FROM estructura_curricular")
                resultados = cursor.fetchall()
                self.tabla.rows.clear()
                for fila in resultados:
                    estructura_id = fila[0]

                    def crear_botones(eid):
                        return ft.Row([
                            ft.IconButton(icon=ft.Icons.EDIT, tooltip="Editar", on_click=lambda e, _eid=eid: self.mostrar_formulario_editar(_eid)),
                            ft.IconButton(icon=ft.Icons.DELETE, tooltip="Eliminar", icon_color="red", on_click=lambda e, _eid=eid: self.eliminar_estructura(_eid))
                        ])

                    self.tabla.rows.append(ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(estructura_id))),
                        ft.DataCell(ft.Text(str(fila[1]) if fila[1] else "")),
                        ft.DataCell(ft.Text(str(fila[2]) if fila[2] else "")),
                        ft.DataCell(ft.Text(str(fila[3]) if fila[3] else "")),
                        ft.DataCell(crear_botones(estructura_id))
                    ]))
                self.page.update()
            except Exception as e:
                print(f"❌ Error al cargar estructura curricular: {e}")
            finally:
                self.conexion.cerrar(conexion)

    def mostrar_formulario_nuevo(self):
        txt_curso_id = ft.TextField(label="ID Curso")
        txt_ciclo_id = ft.TextField(label="ID Ciclo")
        txt_especialidad_id = ft.TextField(label="ID Especialidad")

        def guardar_nuevo(e):
            conexion = self.conexion.conectar()
            if conexion:
                cur = conexion.cursor()
                try:
                    cur.execute("INSERT INTO estructura_curricular (curso_id, ciclo_id, especialidad_id) VALUES (%s, %s, %s)", (txt_curso_id.value, txt_ciclo_id.value, txt_especialidad_id.value))
                    conexion.commit()
                    self.cerrar_dialogo(dlg)
                    self.cargar_estructura()
                except Exception as ex:
                    print(f"❌ Error al insertar estructura curricular: {ex}")
                finally:
                    self.conexion.cerrar(conexion)

        dlg = ft.AlertDialog(
            title=ft.Text("➕ Nueva Estructura Curricular"),
            content=ft.Column([txt_curso_id, txt_ciclo_id, txt_especialidad_id], spacing=10),
            actions=[ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg)), ft.TextButton("Guardar", on_click=guardar_nuevo)]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def mostrar_formulario_editar(self, estructura_id):
        editar_vista = EditarEstructuraView(self.page, self.volver_atras, estructura_id)
        self.volver_atras(editar_vista)

    def eliminar_estructura(self, estructura_id):
        dlg_confirm = ft.AlertDialog(
            title=ft.Text("⚠️ Confirmar eliminación"),
            content=ft.Text("¿Está seguro de que desea eliminar esta estructura curricular?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg_confirm)),
                ft.TextButton("Eliminar", style=ft.ButtonStyle(color="white", bgcolor="red"), on_click=lambda e: self.confirmar_eliminar(estructura_id, dlg_confirm))
            ]
        )
        self.page.dialog = dlg_confirm
        dlg_confirm.open = True
        self.page.update()

    def confirmar_eliminar(self, estructura_id, dlg_confirm):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("DELETE FROM estructura_curricular WHERE estructura_id = %s", (estructura_id,))
                conexion.commit()
                self.cerrar_dialogo(dlg_confirm)
                self.cargar_estructura()
            except Exception as e:
                print(f"❌ Error al eliminar estructura curricular: {e}")
            finally:
                self.conexion.cerrar(conexion)

    def cerrar_dialogo(self, dlg):
        dlg.open = False
        self.page.update()


