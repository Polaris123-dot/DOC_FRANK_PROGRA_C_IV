import flet as ft
from conexion import ConexionDB

class EditarUsuarioView(ft.Container):
    def __init__(self, page, cambiar_vista, usuario_id):
        super().__init__(expand=True)
        self.page = page
        self.cambiar_vista = cambiar_vista
        self.usuario_id = usuario_id
        self.conexion = ConexionDB()

        self.titulo = ft.Text(f"✏️ Editar Usuario (ID: {usuario_id})", size=22, weight="bold")

        self.column = ft.Column(
            [
                self.titulo,
                ft.ProgressRing(),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )

        self.content = ft.Container(
            content=self.column,
            alignment=ft.alignment.center,
            padding=20
        )

        self.cargar_datos_usuario()

    def cargar_datos_usuario(self):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("""
                    SELECT nombre_usuario, persona_id, rol, activo 
                    FROM usuarios
                    WHERE usuario_id = %s
                """, (self.usuario_id,))
                datos = cur.fetchone()

                if datos:
                    nombre_usuario, persona_id, rol, estado = datos

                    self.txt_usuario = ft.TextField(label="Nombre de Usuario", value=nombre_usuario, width=350)
                    self.txt_persona_id = ft.TextField(label="ID Persona", value=str(persona_id), width=350)
                    self.txt_rol = ft.TextField(label="Rol", value=rol, width=350)
                    self.txt_estado = ft.TextField(label="Estado", value=estado, width=350)

                    btn_guardar = ft.ElevatedButton(
                        "💾 Guardar cambios",
                        bgcolor=ft.Colors.GREEN,
                        color="white",
                        on_click=self.guardar_cambios
                    )

                    btn_atras = ft.OutlinedButton(
                        "⬅️ Atrás",
                        on_click=lambda e: self.volver_a_usuarios()
                    )

                    self.column.controls.clear()
                    self.column.controls.extend([
                        self.titulo,
                        ft.Column(
                            [self.txt_usuario, self.txt_persona_id, self.txt_rol, self.txt_estado],
                            spacing=10
                        ),
                        ft.Row([btn_guardar, btn_atras], spacing=15)
                    ])
                    self.page.update()
                else:
                    self.column.controls.clear()
                    self.column.controls.append(ft.Text("❌ No se encontraron datos.", color="red"))
                    self.page.update()

            except Exception as e:
                print(f"❌ Error al cargar usuario: {e}")
            finally:
                self.conexion.cerrar(conexion)

    def guardar_cambios(self, e):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("""
                    UPDATE usuarios
                    SET nombre_usuario=%s, persona_id=%s, rol=%s, activo=%s
                    WHERE usuario_id=%s
                """, (
                    self.txt_usuario.value,
                    int(self.txt_persona_id.value) if self.txt_persona_id.value else None,
                    self.txt_rol.value,
                    self.txt_estado.value,
                    self.usuario_id
                ))
                conexion.commit()

                self.page.snack_bar = ft.SnackBar(
                    ft.Text("Cambios guardados correctamente ✅", color="white"),
                    bgcolor="green",
                    open=True
                )
                self.page.update()

            except Exception as ex:
                print(f"❌ Error al guardar cambios: {ex}")
            finally:
                self.conexion.cerrar(conexion)

    def volver_a_usuarios(self):
        from Usuario.usuarios_view import UsuariosView
        self.cambiar_vista(UsuariosView(self.page, self.cambiar_vista))

