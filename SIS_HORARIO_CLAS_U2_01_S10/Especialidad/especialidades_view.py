# especialidades_view.py
import flet as ft
from conexion import ConexionDB
from acciones.editar_especialidad_view import EditarEspecialidadView

class EspecialidadesView(ft.Container):
    def __init__(self, page, volver_atras):
        super().__init__(expand=True)
        self.page = page
        self.volver_atras = volver_atras
        self.conexion = ConexionDB()

        self.titulo = ft.Text("🎓 Gestión de Especialidades", size=22, weight="bold")

        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Descripción")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[]
        )

        self.btn_volver = ft.ElevatedButton("⬅️ Volver", on_click=lambda e: self.volver_atras())
        self.btn_actualizar = ft.ElevatedButton("🔄 Actualizar", on_click=lambda e: self.cargar_especialidades())
        self.btn_agregar = ft.ElevatedButton("➕ Agregar", on_click=lambda e: self.mostrar_formulario_nuevo())

        self.content = ft.Column(
            [
                self.titulo,
                ft.Row([self.btn_volver, self.btn_actualizar, self.btn_agregar], alignment=ft.MainAxisAlignment.START),
                ft.Container(self.tabla, expand=True, border_radius=10, padding=10, bgcolor=ft.Colors.BLUE_50)
            ],
            spacing=15,
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )

        self.cargar_especialidades()

    def cargar_especialidades(self):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("SELECT especialidad_id, nombre_especialidad, descripcion FROM especialidades")
                resultados = cursor.fetchall()

                self.tabla.rows.clear()
                for fila in resultados:
                    especialidad_id = fila[0]

                    def crear_botones(eid):
                        return ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    tooltip="Editar",
                                    on_click=lambda e, _eid=eid: self.mostrar_formulario_editar(_eid)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    tooltip="Eliminar",
                                    icon_color="red",
                                    on_click=lambda e, _eid=eid: self.eliminar_especialidad(_eid)
                                )
                            ]
                        )

                    self.tabla.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(especialidad_id))),
                                ft.DataCell(ft.Text(fila[1] or "")),
                                ft.DataCell(ft.Text(fila[2] or "")),
                                ft.DataCell(crear_botones(especialidad_id))
                            ]
                        )
                    )
                self.page.update()

            except Exception as e:
                print(f"❌ Error al cargar especialidades: {e}")
            finally:
                self.conexion.cerrar(conexion)

    def mostrar_formulario_nuevo(self):
        txt_nombre = ft.TextField(label="Nombre de Especialidad")
        txt_descripcion = ft.TextField(label="Descripción", multiline=True)

        def guardar_nuevo(e):
            conexion = self.conexion.conectar()
            if conexion:
                cur = conexion.cursor()
                try:
                    cur.execute("""
                        INSERT INTO especialidades (nombre_especialidad, descripcion)
                        VALUES (%s, %s)
                    """, (txt_nombre.value, txt_descripcion.value))
                    conexion.commit()
                    self.cerrar_dialogo(dlg)
                    self.cargar_especialidades()
                except Exception as ex:
                    print(f"❌ Error al insertar especialidad: {ex}")
                finally:
                    self.conexion.cerrar(conexion)

        dlg = ft.AlertDialog(
            title=ft.Text("➕ Nueva Especialidad"),
            content=ft.Column([txt_nombre, txt_descripcion], spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg)),
                ft.TextButton("Guardar", on_click=guardar_nuevo),
            ]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def mostrar_formulario_editar(self, especialidad_id):
        editar_vista = EditarEspecialidadView(self.page, self.volver_atras, especialidad_id)
        self.volver_atras(editar_vista)

    def eliminar_especialidad(self, especialidad_id):
        dlg_confirm = ft.AlertDialog(
            title=ft.Text("⚠️ Confirmar eliminación"),
            content=ft.Text("¿Está seguro de que desea eliminar esta especialidad?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg_confirm)),
                ft.TextButton("Eliminar", style=ft.ButtonStyle(color="white", bgcolor="red"), on_click=lambda e: self.confirmar_eliminar(especialidad_id, dlg_confirm))
            ]
        )
        self.page.dialog = dlg_confirm
        dlg_confirm.open = True
        self.page.update()

    def confirmar_eliminar(self, especialidad_id, dlg_confirm):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("DELETE FROM especialidades WHERE especialidad_id = %s", (especialidad_id,))
                conexion.commit()
                self.cerrar_dialogo(dlg_confirm)
                self.cargar_especialidades()
            except Exception as e:
                print(f"❌ Error al eliminar especialidad: {e}")
            finally:
                self.conexion.cerrar(conexion)

    def cerrar_dialogo(self, dlg):
        dlg.open = False
        self.page.update()

