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

    return rows, xR

def show():
    
    def get_data(event):
        try:
            fx = validar_expresion(row.controls[0].value)
            limite_inferior = float(row.controls[1].value)
            limite_superior = float(row.controls[2].value)
            cifras = int(row.controls[3].value)

            rows, raiz = solve(fx, limite_inferior, limite_superior, cifras)
            table.rows = rows
            table.visible = True
            event.control.page.update()
        except ValueError as e:
            print(f"Error: {e}")

    row = ft.ResponsiveRow(
        [
            ft.TextField(
                label="Función", 
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


    container_input = ft.Container(
        bgcolor='#565656',
        border_radius=ft.border_radius.all(20),
        padding=20,
        content=row
    )

    view_controls = ft.ResponsiveRow(
        controls=[
            container_input, tbl
        ])

    

    

    return view_controls
