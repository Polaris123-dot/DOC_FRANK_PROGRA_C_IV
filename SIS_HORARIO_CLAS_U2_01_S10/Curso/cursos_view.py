# cursos_view.py
import flet as ft
from conexion import ConexionDB
from acciones.editar_curso_view import EditarCursoView

class CursosView(ft.Container):
    def __init__(self, page, volver_atras):
        super().__init__(expand=True)
        self.page = page
        self.volver_atras = volver_atras
        self.conexion = ConexionDB()

        self.titulo = ft.Text("📖 Gestión de Cursos", size=22, weight="bold")
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Créditos")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[]
        )

        self.btn_volver = ft.ElevatedButton("⬅️ Volver", on_click=lambda e: self.volver_atras())
        self.btn_actualizar = ft.ElevatedButton("🔄 Actualizar", on_click=lambda e: self.cargar_cursos())
        self.btn_agregar = ft.ElevatedButton("➕ Agregar", on_click=lambda e: self.mostrar_formulario_nuevo())

        self.content = ft.Column(
            [self.titulo, ft.Row([self.btn_volver, self.btn_actualizar, self.btn_agregar], alignment=ft.MainAxisAlignment.START),
             ft.Container(self.tabla, expand=True, border_radius=10, padding=10, bgcolor=ft.Colors.BLUE_50)],
            spacing=15, expand=True, scroll=ft.ScrollMode.AUTO
        )
        self.cargar_cursos()

    def cargar_cursos(self):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("SELECT curso_id, nombre, creditos FROM cursos")
                resultados = cursor.fetchall()
                self.tabla.rows.clear()
                for fila in resultados:
                    curso_id = fila[0]

                    def crear_botones(cid):
                        return ft.Row([
                            ft.IconButton(icon=ft.Icons.EDIT, tooltip="Editar", on_click=lambda e, _cid=cid: self.mostrar_formulario_editar(_cid)),
                            ft.IconButton(icon=ft.Icons.DELETE, tooltip="Eliminar", icon_color="red", on_click=lambda e, _cid=cid: self.eliminar_curso(_cid))
                        ])

                    self.tabla.rows.append(ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(curso_id))),
                        ft.DataCell(ft.Text(fila[1] or "")),
                        ft.DataCell(ft.Text(str(fila[2]) if fila[2] else "")),
                        ft.DataCell(crear_botones(curso_id))
                    ]))
                self.page.update()
            except Exception as e:
                print(f"❌ Error al cargar cursos: {e}")
            finally:
                self.conexion.cerrar(conexion)

    def mostrar_formulario_nuevo(self):
        txt_nombre = ft.TextField(label="Nombre del Curso")
        txt_creditos = ft.TextField(label="Créditos")

        def guardar_nuevo(e):
            conexion = self.conexion.conectar()
            if conexion:
                cur = conexion.cursor()
                try:
                    cur.execute("INSERT INTO cursos (nombre, creditos) VALUES (%s, %s)", (txt_nombre.value, txt_creditos.value))
                    conexion.commit()
                    self.cerrar_dialogo(dlg)
                    self.cargar_cursos()
                except Exception as ex:
                    print(f"❌ Error al insertar curso: {ex}")
                finally:
                    self.conexion.cerrar(conexion)

        dlg = ft.AlertDialog(
            title=ft.Text("➕ Nuevo Curso"),
            content=ft.Column([txt_nombre, txt_creditos], spacing=10),
            actions=[ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg)), ft.TextButton("Guardar", on_click=guardar_nuevo)]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def mostrar_formulario_editar(self, curso_id):
        editar_vista = EditarCursoView(self.page, self.volver_atras, curso_id)
        self.volver_atras(editar_vista)

    def eliminar_curso(self, curso_id):
        dlg_confirm = ft.AlertDialog(
            title=ft.Text("⚠️ Confirmar eliminación"),
            content=ft.Text("¿Está seguro de que desea eliminar este curso?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg_confirm)),
                ft.TextButton("Eliminar", style=ft.ButtonStyle(color="white", bgcolor="red"), on_click=lambda e: self.confirmar_eliminar(curso_id, dlg_confirm))
            ]
        )
        self.page.dialog = dlg_confirm
        dlg_confirm.open = True
        self.page.update()

    def confirmar_eliminar(self, curso_id, dlg_confirm):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("DELETE FROM cursos WHERE curso_id = %s", (curso_id,))
                conexion.commit()
                self.cerrar_dialogo(dlg_confirm)
                self.cargar_cursos()
            except Exception as e:
                print(f"❌ Error al eliminar curso: {e}")
            finally:
                self.conexion.cerrar(conexion)

    def cerrar_dialogo(self, dlg):
        dlg.open = False
        self.page.update()



