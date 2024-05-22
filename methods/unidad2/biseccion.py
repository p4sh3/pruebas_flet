import flet as ft
import sympy as sp
import pandas as pd
from methods.unidad2.grafico import show as show_grafico
name = "Método de Bisección"

def validar_expresion(expr):
    if not expr.strip():
        raise ValueError("La expresión no puede estar vacía")
    return sp.parse_expr(expr)

def solve(fx, limite_inferior, limite_superior, cifras):
    rows = []
    x = sp.Symbol('x')
    x1 = limite_inferior
    xU = limite_superior
    xR = 0
    Es = 0.5 * 10 ** (2 - cifras)
    iteracion = 1
    df = pd.DataFrame(columns=["Iteración", "x1", "xU", "xR", "f(x1)", "f(xU)", "f(xR)", "f(x1)f(xR)", "Ea"])
    
    while True:
        xR = (x1 + xU) / 2
        fx1 = fx.subs(x, x1).evalf()
        fxu = fx.subs(x, xU).evalf()
        fxr = fx.subs(x, xR).evalf()
        condicion = fx1 * fxr

        if iteracion != 1: 
            Ea = abs((xR - xR_ant) / xR) * 100
            rows.append(ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(cell))) for cell in [iteracion, x1, xU, xR, fx1, fxu, fxr, condicion, Ea]],
            ))
            df.loc[iteracion - 1] = [iteracion, x1, xU, xR, fx1, fxu, fxr, condicion, Ea]
        else:
            Ea = 1000
            rows.append(ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(cell))) for cell in [iteracion, x1, xU, xR, fx1, fxu, fxr, condicion, "--"]],
            ))
            df.loc[iteracion - 1] = [iteracion, x1, xU, xR, fx1, fxu, fxr, condicion, "--"]

        if condicion < 0:
            xU = xR
        elif condicion > 0:
            x1 = xR
        else:
            df.loc[iteracion - 1] = [iteracion, x1, xU, xR, fx1, fxu, fxr, condicion, Ea]
            break

        if Ea < Es:
            break    

        xR_ant = xR
        iteracion += 1

    return rows, xR, iteracion, Ea, fx

def show():
    
    def get_data(event):
        try:
            fx = validar_expresion(row.controls[0].value)
            limite_inferior = float(row.controls[1].value)
            limite_superior = float(row.controls[2].value)
            cifras = int(row.controls[3].value)
            
            print(type(fx))
            print(type(limite_inferior))
            print(type(limite_superior))
            print(type(cifras))
            
            rows, raiz, iteracion, Ea, fx = solve(fx, limite_inferior, limite_superior, cifras)
            table.rows = rows
            table.visible = True
            lbl_resultados.value = f'Funcion {fx}\nSolucion: {raiz}\nCon {iteracion} iteraciones\nError porcentual aproximado {Ea}%'
            container_resultados.visible=True
            event.control.page.update()
        except ValueError as e:
            print(f"Error: {e}")
            show_alert(event, 'Error ingresa datos para calcular')
        
            
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
        
    
    row = ft.ResponsiveRow(
        [
            ft.TextField(
                height=57,
                label="Función", 
                autofocus=True,
                suffix=ft.IconButton(
                    icon=ft.icons.HELP_OUTLINE_OUTLINED, on_click=open_dlg_modal),
                col={"md": 3}),
            ft.TextField(
                label="Límite Inferior",
                col={"md": 3}),
            
            ft.TextField(
                label="Límite Superior", 
                col={"md": 3}),
            ft.TextField(
                label="Cifras Significativas", 
                col={"md": 3}),
            ft.ElevatedButton(
                text="Resolver", 
                on_click=get_data, 
                width=100, 
                height=45, col={"md":3}),
        ], 
        alignment=ft.MainAxisAlignment.CENTER,  
    )

    table = ft.DataTable(
        columns=[ft.DataColumn(ft.Text(col)) for col in ["Iteración", "x1", "xU", "xR", "f(x1)", "f(xU)", "f(xR)", "f(x1)f(xR)", "Ea"]],
        rows=[],
        visible=False
    )

    tbl = ft.Row([ft.Container(padding=20, content=ft.Row([table]))], scroll=ft.ScrollMode.ALWAYS)

    button = ft.ElevatedButton(text="Resolver", on_click=get_data, width=100, height=45)


    lbl_resultados = ft.Text()
    
    container_resultados = ft.Container(
                    visible=False,
                    bgcolor='#565656',  #ft.colors.BLUE_100,
                    border_radius=ft.border_radius.all(20),
                    padding=20,
                    content=ft.ResponsiveRow(
                        [
                        ft.Container(
                            lbl_resultados,
                            col={"sm": 6, "md": 4, "xl": 12},
                        ),
                    ]
                )
            
    )
    
    container_input = ft.Container(
        bgcolor='#565656',
        border_radius=ft.border_radius.all(20),
        padding=20,
        content=row
    )

    view_controls = ft.ResponsiveRow(
        controls=[
            container_input,container_resultados, tbl
        ])

    

    

    return view_controls
