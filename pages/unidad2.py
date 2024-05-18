import flet as ft

def show():

    def get_data(event):
      event.control.page.update()
        

    row = ft.ResponsiveRow([
        ft.TextField(
            adaptive=True,
            label="Función",
            col={"md": 3}
        ),
        ft.TextField(
            adaptive=True,
            label="Límite Inferior",
            col={"md": 3}
        ),
        ft.TextField(
            adaptive=True,
            label="Límite Superior", 
            col={"md": 3}
        ),
        ft.TextField(
            adaptive=True,
            label="Cifras Significativas",
              col={"md": 3}
        ),
    ])
    
    table = ft.DataTable(
        columns= [ft.DataColumn(ft.Text(colum)) for colum in ["Iteración", "x1", "xU", "xR", "f(x1)", "f(xU)", "f(xR)", "f(x1)f(xR)", "Ea"]],
        rows=[],
        visible=False
    )

    button = ft.ElevatedButton(text="Resolver", on_click=get_data)






    
    return ft.Column([row, button, table])