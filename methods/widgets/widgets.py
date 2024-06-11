import flet as ft 

def close_alert(event):
        event.control.page.banner.open = False
        event.page.update()
       
def show_alert(event, message):
    event.control.page.banner = alert_banner
    text_control =alert_banner.content
    text_control.value = message
    event.control.page.banner.open = True
    event.page.update()
    
alert_banner = ft.Banner(
    bgcolor='#565656',
    leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
    content=ft.Text(),
    actions=[
        ft.TextButton("Ok", on_click=lambda event: close_alert(event)),        
    ],
)
    
def close_dlg(e):
    dlg_modal.open = False
    e.control.page.update()

        
dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Expresiones permitidas"),
        content=ft.Text("Las siguientes expresiones\nson permitidas para evaluar\nuna funcion matematica"),
        actions=[
            ft.TextButton("Ok", on_click=close_dlg),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
         on_dismiss=lambda e: print("Modal dialog dismissed!"),
)
                
def open_dlg_modal(e):
    e.control.page.dialog = dlg_modal
    dlg_modal.open = True
    e.control.page.update()
    
def close_modal_alert(event):
    modal_alert.open = False
    event.control.page.update()        
        
modal_alert = ft.AlertDialog(
        modal=True,
        title=ft.Text("Expresiones permitidas"),
        content=ft.Text(),
        actions=[
            ft.TextButton("Ok", on_click=close_modal_alert),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
         on_dismiss=lambda e: print("Modal dialog dismissed!"),
)
                
def show_modal_alert(event, message):
    event.control.page.dialog = modal_alert
    text_control = modal_alert.content
    text_control.value = message
    modal_alert.open = True
    event.control.page.update()
    
