import flet as ft
from conexion import ConexionDB

class EditarEspecialidadView(ft.Container):
    def __init__(self, page, cambiar_vista, especialidad_id):
        super().__init__(expand=True)
        self.page = page
        self.cambiar_vista = cambiar_vista
        self.especialidad_id = especialidad_id
        self.conexion = ConexionDB()

        self.titulo = ft.Text(f"✏️ Editar Especialidad (ID: {especialidad_id})", size=22, weight="bold")

        self.column = ft.Column(
            [self.titulo, ft.ProgressRing()],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )

        self.content = ft.Container(
            content=self.column,
            alignment=ft.alignment.center,
            padding=20
        )

        self.cargar_datos_especialidad()

    def cargar_datos_especialidad(self):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("""
                    SELECT nombre_especialidad, descripcion
                    FROM especialidades
                    WHERE especialidad_id = %s
                """, (self.especialidad_id,))
                datos = cur.fetchone()

                if datos:
                    nombre, descripcion = datos

                    self.txt_nombre = ft.TextField(label="Nombre de Especialidad", value=nombre, width=350)
                    self.txt_descripcion = ft.TextField(label="Descripción", value=descripcion, width=350, multiline=True)

                    btn_guardar = ft.ElevatedButton("💾 Guardar cambios", bgcolor=ft.Colors.GREEN, color="white", on_click=self.guardar_cambios)
                    btn_atras = ft.OutlinedButton("⬅️ Atrás", on_click=lambda e: self.volver_a_especialidades())

                    self.column.controls.clear()
                    self.column.controls.extend([
                        self.titulo,
                        ft.Column([self.txt_nombre, self.txt_descripcion], spacing=10),
                        ft.Row([btn_guardar, btn_atras], spacing=15)
                    ])
                    self.page.update()
                else:
                    self.column.controls.clear()
                    self.column.controls.append(ft.Text("❌ No se encontraron datos.", color="red"))
                    self.page.update()

            except Exception as e:
                print(f"❌ Error al cargar especialidad: {e}")
            finally:
                self.conexion.cerrar(conexion)

    def guardar_cambios(self, e):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("""
                    UPDATE especialidades
                    SET nombre_especialidad=%s, descripcion=%s
                    WHERE especialidad_id=%s
                """, (self.txt_nombre.value, self.txt_descripcion.value, self.especialidad_id))
                conexion.commit()

                self.page.snack_bar = ft.SnackBar(ft.Text("Cambios guardados correctamente ✅", color="white"), bgcolor="green", open=True)
                self.page.update()

            except Exception as ex:
                print(f"❌ Error al guardar cambios: {ex}")
            finally:
                self.conexion.cerrar(conexion)

    def volver_a_especialidades(self):
        from Especialidad.especialidades_view import EspecialidadesView
        self.cambiar_vista(EspecialidadesView(self.page, self.cambiar_vista))


