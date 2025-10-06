import flet as ft

def main(page: ft.Page):
    page.title = "App de Control de Stock Simple"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 30
    
    stock = 5
    texto_stock = ft.Text(
        f"Stock: {stock}", 
        size=30, 
        weight=ft.FontWeight.W_700,
        color=ft.Colors.GREEN_700
    )
    
    boton = ft.ElevatedButton(
        "Restar 1", 
        on_click=lambda e: boton_click(e, boton), 
        icon=ft.Icons.REMOVE_CIRCLE,
        bgcolor=ft.Colors.BLUE_GREY_400,
        color=ft.Colors.WHITE
    )

    def boton_click(e, btn_control):
        nonlocal stock  
        
    
        if stock > 0:
            stock -= 1  
            texto_stock.value = f"Stock: {stock}" 
            
            if stock == 0:
                btn_control.disabled = True
                btn_control.text = "¡Sin Stock!"
                btn_control.bgcolor = ft.Colors.RED_700
                texto_stock.color = ft.Colors.RED_700
            
            elif stock < 3:
                btn_control.bgcolor = ft.Colors.ORANGE_500
                texto_stock.color = ft.Colors.ORANGE_500
            else:
                btn_control.bgcolor = ft.Colors.BLUE_GREY_400
                texto_stock.color = ft.Colors.GREEN_700
        
        page.update() 

    page.add(
        ft.Column(
            [
                ft.Text("Control de Stock", size=40, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                texto_stock, 
                ft.Container(height=20),
                boton
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
