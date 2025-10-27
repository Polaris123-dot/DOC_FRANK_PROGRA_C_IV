# usuarios_view.py
import flet as ft
from conexion import ConexionDB
from acciones.editar_usuario_view import EditarUsuarioView

class UsuariosView(ft.Container):
    def __init__(self, page, volver_atras):
        super().__init__(expand=True)
        self.page = page
        self.volver_atras = volver_atras
        self.conexion = ConexionDB()

        self.titulo = ft.Text("👤 Gestión de Usuarios", size=22, weight="bold")

        # --- Tabla principal ---
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Usuario")),
                ft.DataColumn(ft.Text("ID Persona")),
                ft.DataColumn(ft.Text("Rol")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[]
        )

        # --- Botones superiores ---
        self.btn_volver = ft.ElevatedButton("⬅️ Volver", on_click=lambda e: self.volver_atras())
        self.btn_actualizar = ft.ElevatedButton("🔄 Actualizar", on_click=lambda e: self.cargar_usuarios())
        self.btn_agregar = ft.ElevatedButton("➕ Agregar", on_click=lambda e: self.mostrar_formulario_nuevo())

        # --- Contenedor principal ---
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

        # --- Cargar datos iniciales ---
        self.cargar_usuarios()

    def cargar_usuarios(self):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("SELECT usuario_id, nombre_usuario, persona_id, rol, activo FROM usuarios")
                resultados = cursor.fetchall()

                self.tabla.rows.clear()
                for fila in resultados:
                    usuario_id = fila[0]

                    def crear_botones(uid):
                        return ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    tooltip="Editar",
                                    on_click=lambda e, _uid=uid: self.mostrar_formulario_editar(_uid)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    tooltip="Eliminar",
                                    icon_color="red",
                                    on_click=lambda e, _uid=uid: self.eliminar_usuario(_uid)
                                )
                            ]
                        )

                    self.tabla.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(usuario_id))),
                                ft.DataCell(ft.Text(fila[1] or "")),
                                ft.DataCell(ft.Text(str(fila[2]) if fila[2] else "")),
                                ft.DataCell(ft.Text(fila[3] or "")),
                                ft.DataCell(ft.Text(fila[4] or "")),
                                ft.DataCell(crear_botones(usuario_id))
                            ]
                        )
                    )
                self.page.update()

            except Exception as e:
                print(f"❌ Error al cargar usuarios: {e}")
            finally:
                self.conexion.cerrar(conexion)

    def mostrar_formulario_nuevo(self):
        txt_usuario = ft.TextField(label="Nombre de Usuario")
        txt_persona_id = ft.TextField(label="ID Persona")
        txt_rol = ft.TextField(label="Rol")
        txt_password = ft.TextField(label="Contraseña", password=True)
        txt_estado = ft.TextField(label="Estado", value="activo")

        def guardar_nuevo(e):
            conexion = self.conexion.conectar()
            if conexion:
                cur = conexion.cursor()
                try:
                    cur.execute("""
                        INSERT INTO usuarios (nombre_usuario, persona_id, rol, hashed_pass, activo)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (txt_usuario.value, txt_persona_id.value, txt_rol.value, txt_password.value, txt_estado.value))
                    conexion.commit()
                    self.cerrar_dialogo(dlg)
                    self.cargar_usuarios()
                except Exception as ex:
                    print(f"❌ Error al insertar usuario: {ex}")
                finally:
                    self.conexion.cerrar(conexion)

        dlg = ft.AlertDialog(
            title=ft.Text("➕ Nuevo Usuario"),
            content=ft.Column([txt_usuario, txt_persona_id, txt_rol, txt_password, txt_estado], spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg)),
                ft.TextButton("Guardar", on_click=guardar_nuevo),
            ]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def mostrar_formulario_editar(self, usuario_id):
        editar_vista = EditarUsuarioView(self.page, self.volver_atras, usuario_id)
        self.volver_atras(editar_vista)

    def eliminar_usuario(self, usuario_id):
        dlg_confirm = ft.AlertDialog(
            title=ft.Text("⚠️ Confirmar eliminación"),
            content=ft.Text("¿Está seguro de que desea eliminar este usuario?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg_confirm)),
                ft.TextButton("Eliminar", style=ft.ButtonStyle(color="white", bgcolor="red"), on_click=lambda e: self.confirmar_eliminar(usuario_id, dlg_confirm))
            ]
        )
        self.page.dialog = dlg_confirm
        dlg_confirm.open = True
        self.page.update()

    def confirmar_eliminar(self, usuario_id, dlg_confirm):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("DELETE FROM usuarios WHERE usuario_id = %s", (usuario_id,))
                conexion.commit()
                self.cerrar_dialogo(dlg_confirm)
                self.cargar_usuarios()
            except Exception as e:
                print(f"❌ Error al eliminar usuario: {e}")
            finally:
                self.conexion.cerrar(conexion)

    def cerrar_dialogo(self, dlg):
        dlg.open = False
        self.page.update()

