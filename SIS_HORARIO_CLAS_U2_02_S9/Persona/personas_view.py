# personas_view.py
import flet as ft
from conexion import ConexionDB

class PersonasView(ft.Container):
    def __init__(self, page, volver_atras):
        super().__init__(expand=True)
        self.page = page
        self.volver_atras = volver_atras
        self.conexion = ConexionDB()

        self.titulo = ft.Text("👥 Gestión de Personas", size=22, weight="bold")

        # --- Tabla principal ---
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombres")),
                ft.DataColumn(ft.Text("Apellidos")),
                ft.DataColumn(ft.Text("DNI")),
                ft.DataColumn(ft.Text("Teléfono")),
                ft.DataColumn(ft.Text("Acciones")),  # nueva columna
            ],
            rows=[]
        )

        # --- Botones superiores ---
        self.btn_volver = ft.ElevatedButton("⬅️ Volver", on_click=lambda e: self.volver_atras())
        self.btn_actualizar = ft.ElevatedButton("🔄 Actualizar", on_click=lambda e: self.cargar_personas())

        # --- Contenedor principal ---
        self.content = ft.Column(
            [
                self.titulo,
                ft.Row([self.btn_volver, self.btn_actualizar], alignment=ft.MainAxisAlignment.START),
                ft.Container(self.tabla, expand=True, border_radius=10, padding=10, bgcolor=ft.Colors.BLUE_50)
            ],
            spacing=15,
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )

        # --- Cargar datos iniciales ---
        self.cargar_personas()

    # =============================
    #   CARGAR PERSONAS
    # =============================
    def cargar_personas(self):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("SELECT persona_id, nombres, apellidos, numero_documento, telefono FROM personas")
                resultados = cursor.fetchall()

                self.tabla.rows.clear()
                for fila in resultados:
                    persona_id = fila[0]
                    self.tabla.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(persona_id))),
                                ft.DataCell(ft.Text(fila[1])),
                                ft.DataCell(ft.Text(fila[2])),
                                ft.DataCell(ft.Text(fila[3])),
                                ft.DataCell(ft.Text(fila[4])),
                                ft.DataCell(
                                    ft.Row(
                                        [
                                            ft.IconButton(
                                                icon=ft.Icons.EDIT,
                                                tooltip="Editar",
                                                on_click=lambda e, id=persona_id: self.mostrar_formulario_editar(id)
                                            ),
                                            ft.IconButton(
                                                icon=ft.Icons.DELETE,
                                                tooltip="Eliminar",
                                                icon_color="red",
                                                on_click=lambda e, id=persona_id: self.eliminar_persona(id)
                                            )
                                        ]
                                    )
                                )
                            ]
                        )
                    )
                self.page.update()

            except Exception as e:
                print(f"❌ Error al cargar personas: {e}")
            finally:
                self.conexion.cerrar(conexion)

    # =============================
    #   FORMULARIO EDITAR PERSONA
    # =============================
    def mostrar_formulario_editar(self, persona_id):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute(
                    "SELECT nombres, apellidos, numero_documento, telefono FROM personas WHERE persona_id = %s",
                    (persona_id,)
                )
                persona = cursor.fetchone()

                if not persona:
                    return

                # Campos de edición
                txt_nombre = ft.TextField(label="Nombres", value=persona[0])
                txt_apellido = ft.TextField(label="Apellidos", value=persona[1])
                txt_dni = ft.TextField(label="DNI", value=persona[2])
                txt_telefono = ft.TextField(label="Teléfono", value=persona[3])

                def guardar_cambios(e):
                    conexion2 = self.conexion.conectar()
                    if conexion2:
                        cur = conexion2.cursor()
                        try:
                            cur.execute("""
                                UPDATE personas
                                SET nombres=%s, apellidos=%s, numero_documento=%s, telefono=%s
                                WHERE persona_id=%s
                            """, (txt_nombre.value, txt_apellido.value, txt_dni.value, txt_telefono.value, persona_id))
                            conexion2.commit()
                            dlg.open = False
                            self.page.update()
                            self.cargar_personas()
                        except Exception as ex:
                            print(f"❌ Error al actualizar persona: {ex}")
                        finally:
                            self.conexion.cerrar(conexion2)

                dlg = ft.AlertDialog(
                    title=ft.Text("✏️ Editar Persona"),
                    content=ft.Column([txt_nombre, txt_apellido, txt_dni, txt_telefono], spacing=10),
                    actions=[
                        ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg)),
                        ft.TextButton("Guardar", on_click=guardar_cambios),
                    ]
                )
                self.page.dialog = dlg
                dlg.open = True
                self.page.update()

            except Exception as e:
                print(f"❌ Error al mostrar formulario: {e}")
            finally:
                self.conexion.cerrar(conexion)

    # =============================
    #   ELIMINAR PERSONA
    # =============================
    def eliminar_persona(self, persona_id):
        dlg_confirm = ft.AlertDialog(
            title=ft.Text("⚠️ Confirmar eliminación"),
            content=ft.Text("¿Está seguro de que desea eliminar esta persona?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg_confirm)),
                ft.TextButton(
                    "Eliminar",
                    style=ft.ButtonStyle(color="white", bgcolor="red"),
                    on_click=lambda e: self.confirmar_eliminar(persona_id, dlg_confirm)
                )
            ]
        )
        self.page.dialog = dlg_confirm
        dlg_confirm.open = True
        self.page.update()

    def confirmar_eliminar(self, persona_id, dlg_confirm):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("DELETE FROM personas WHERE persona_id = %s", (persona_id,))
                conexion.commit()
                dlg_confirm.open = False
                self.cargar_personas()
                self.page.update()
            except Exception as e:
                print(f"❌ Error al eliminar persona: {e}")
            finally:
                self.conexion.cerrar(conexion)

    # =============================
    #   CERRAR DIÁLOGO
    # =============================
    def cerrar_dialogo(self, dlg):
        dlg.open = False
        self.page.update()
