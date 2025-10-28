# docentes_view.py
import flet as ft
from conexion import ConexionDB
from acciones.editar_docente_view import EditarDocenteView

class DocentesView(ft.Container):
    def __init__(self, page, volver_atras):
        super().__init__(expand=True)
        self.page = page
        self.volver_atras = volver_atras
        self.conexion = ConexionDB()
        self.titulo = ft.Text("👨‍🏫 Gestión de Docentes", size=22, weight="bold")
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("ID Persona")),
                ft.DataColumn(ft.Text("ID Especialidad")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[]
        )
        self.btn_volver = ft.ElevatedButton("⬅️ Volver", on_click=lambda e: self.volver_atras())
        self.btn_actualizar = ft.ElevatedButton("🔄 Actualizar", on_click=lambda e: self.cargar_docentes())
        self.btn_agregar = ft.ElevatedButton("➕ Agregar", on_click=lambda e: self.mostrar_formulario_nuevo())
        self.content = ft.Column(
            [self.titulo, ft.Row([self.btn_volver, self.btn_actualizar, self.btn_agregar], alignment=ft.MainAxisAlignment.START),
             ft.Container(self.tabla, expand=True, border_radius=10, padding=10, bgcolor=ft.Colors.BLUE_50)],
            spacing=15, expand=True, scroll=ft.ScrollMode.AUTO
        )
        self.cargar_docentes()

    def cargar_docentes(self):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("SELECT docente_id, persona_id, especialidad_id, activo FROM docentes")
                resultados = cursor.fetchall()
                self.tabla.rows.clear()
                for fila in resultados:
                    docente_id = fila[0]

                    def crear_botones(did):
                        return ft.Row([
                            ft.IconButton(icon=ft.Icons.EDIT, tooltip="Editar", on_click=lambda e, _did=did: self.mostrar_formulario_editar(_did)),
                            ft.IconButton(icon=ft.Icons.DELETE, tooltip="Eliminar", icon_color="red", on_click=lambda e, _did=did: self.eliminar_docente(_did))
                        ])

                    self.tabla.rows.append(ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(docente_id))),
                        ft.DataCell(ft.Text(str(fila[1]) if fila[1] else "")),
                        ft.DataCell(ft.Text(str(fila[2]) if fila[2] else "")),
                        ft.DataCell(ft.Text(fila[3] or "")),
                        ft.DataCell(crear_botones(docente_id))
                    ]))
                self.page.update()
            except Exception as e:
                print(f"❌ Error al cargar docentes: {e}")
            finally:
                self.conexion.cerrar(conexion)

    def mostrar_formulario_nuevo(self):
        txt_persona_id = ft.TextField(label="ID Persona")
        txt_especialidad_id = ft.TextField(label="ID Especialidad")
        txt_estado = ft.TextField(label="Estado", value="activo")

        def guardar_nuevo(e):
            conexion = self.conexion.conectar()
            if conexion:
                cur = conexion.cursor()
                try:
                    cur.execute("INSERT INTO docentes (persona_id, especialidad_id, activo) VALUES (%s, %s, %s)", (txt_persona_id.value, txt_especialidad_id.value, txt_estado.value))
                    conexion.commit()
                    self.cerrar_dialogo(dlg)
                    self.cargar_docentes()
                except Exception as ex:
                    print(f"❌ Error al insertar docente: {ex}")
                finally:
                    self.conexion.cerrar(conexion)

        dlg = ft.AlertDialog(
            title=ft.Text("➕ Nuevo Docente"),
            content=ft.Column([txt_persona_id, txt_especialidad_id, txt_estado], spacing=10),
            actions=[ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg)), ft.TextButton("Guardar", on_click=guardar_nuevo)]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def mostrar_formulario_editar(self, docente_id):
        editar_vista = EditarDocenteView(self.page, self.volver_atras, docente_id)
        self.volver_atras(editar_vista)

    def eliminar_docente(self, docente_id):
        dlg_confirm = ft.AlertDialog(
            title=ft.Text("⚠️ Confirmar eliminación"),
            content=ft.Text("¿Está seguro de que desea eliminar este docente?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg_confirm)),
                ft.TextButton("Eliminar", style=ft.ButtonStyle(color="white", bgcolor="red"), on_click=lambda e: self.confirmar_eliminar(docente_id, dlg_confirm))
            ]
        )
        self.page.dialog = dlg_confirm
        dlg_confirm.open = True
        self.page.update()

    def confirmar_eliminar(self, docente_id, dlg_confirm):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("DELETE FROM docentes WHERE docente_id = %s", (docente_id,))
                conexion.commit()
                self.cerrar_dialogo(dlg_confirm)
                self.cargar_docentes()
            except Exception as e:
                print(f"❌ Error al eliminar docente: {e}")
            finally:
                self.conexion.cerrar(conexion)

    def cerrar_dialogo(self, dlg):
        dlg.open = False
        self.page.update()



