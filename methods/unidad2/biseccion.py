import flet as ft

name = "Método de Bisección"

def validar_expresion(str):
    import sympy as sp
    return sp.parse_expr(str)

def solve(fx, limite_inferior, limite_superior, cifras):
    import sympy as sp
    import pandas as pd

    rows = []
    x = sp.Symbol('x')
    x1 = limite_inferior
    xU = limite_superior
    xR = 0
    Es = 0.5 * 10 ** (2 - cifras)
    print(f"fx: {fx}, {type(fx)}")
    print(f"x1: {x1}, {type(x1)}")
    print(f"xU: {xU}, {type(xU)}")
    print(f"cifras: {cifras}, {type(cifras)}")
    iteracion = 1
    df = pd.DataFrame(columns=["Iteración", "x1", "xU", "xR", "f(x1)", "f(xU)", "f(xR)", "f(x1)f(xR)", "Ea"])
    while True:
    
        xR = (x1+xU)/2
        print("\n_____________________________________________\n")
        print(f"ITERACION: {iteracion}, {type(iteracion)}")
        print(f"xR: {xR}, {type(xR)}")
        fx1 = fx.subs(x,x1).evalf()
        fxu = fx.subs(x,xU).evalf()
        fxr = fx.subs(x,xR).evalf()
        print(f"fx1: {fx1}, {type(fx1)}")
        print(f"fxu: {fxu}, {type(fxu)}")
        print(f"fxr: {fxr}, {type(fxr)}")
        condicion = fx1*fxr
        print(f"condicion: {condicion}, {type(condicion)}")

    
        if iteracion != 1: 
            Ea = abs((xR-xR_ant)/xR)*100
            print(f"Xr anterior: {xR_ant}, {type(xR_ant)}")
            rows.append(ft.DataRow(
                cells=[ ft.DataCell(ft.Text(cell)) for cell in [iteracion, x1, xU, xR, fx1, fxu, fxr, condicion, Ea]],
            ))
            df.loc[iteracion - 1] = [iteracion, x1, xU, xR, fx1, fxu, fxr, condicion, Ea]
        else:
            Ea = 1000
            rows.append(ft.DataRow(
                cells=[ ft.DataCell(ft.Text(cell)) for cell in [iteracion, x1, xU, xR, fx1, fxu, fxr, condicion, "--"]],
            ))
            df.loc[iteracion - 1] = [iteracion, x1, xU, xR, fx1, fxu, fxr, condicion, "--"]
        
        print(f"Ea: {Ea}, {type(Ea)}")
        
        print("\n_____________________________________________\n")
        if condicion < 0 :
            xU = xR
        elif condicion > 0:
            x1 = xR
        else:
            df.loc[iteracion - 1] = [iteracion, x1, xU, xR, fx1, fxu, fxr, condicion, Ea]
            break

        if (Ea < Es):
            break    

        xR_ant = xR
        iteracion += 1

    print(df)
    print(f"La raíz de la ecuación es {xR}")
    return rows, xR

def show():

    def get_data(event):
        fx = validar_expresion(row.controls[0].value)
        limite_inferior = float(row.controls[1].value)
        limite_superior = float(row.controls[2].value)
        cifras = int(row.controls[3].value)

        rows, raiz = solve(fx, limite_inferior, limite_superior, cifras)
        table.rows = rows
        table.visible = True
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