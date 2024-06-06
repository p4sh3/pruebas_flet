import flet as ft
import sympy as sp
import pandas as pd
# from methods.unidad1.grafico import show as show_grafico
from methods.widgets.widgets import show_alert, open_dlg_modal
name = "Método de Bisección"


def validar_expresion(expr):
    x = sp.Symbol('x')
    symbolos_permitidos = {x}
    try: 
        exp = sp.sympify(expr)
    except (sp.SympifyError, SyntaxError):
        raise ValueError('La expresion no es valida')
    # Obtener todos los símbolos en la expresión
    symbolos_en_expr = exp.free_symbols
    
    # Verificar que todos los símbolos estén permitidos
    if not symbolos_en_expr.issubset(symbolos_permitidos):
        raise ValueError("La expresión contiene símbolos no permitidos")
    else: 
        return sp.parse_expr(expr)



# def validar_expresion(expr):# valida que se ingrese una funcion en el texfield funcion
#     if not expr.strip():
#         raise ValueError("Ingrese una funcio a resolver")
#     return sp.parse_expr(expr)

def solve(fx, limite_inferior, limite_superior, cifras): # codigo del algoritmo
    rows = []
    x = sp.Symbol('x')
    x1 = limite_inferior
    xU = limite_superior
    xR = 0
    metodo = 'Biseccion'
    
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

    return rows, xR, iteracion, Ea, fx, metodo

def show(): # Muestra los resultados 
    
    def clean(event):
        container_results.visible = False
        table.visible = False
        row.controls[1].value = ''
        row.controls[2].value = ''
        row.controls[3].value = ''
        row.controls[4].value = ''
        
        row.controls[1].autofocus = True
        event.control.page.update()
        
    def get_data(event): # asigna los datos ingresados a la funcion solve()
        try:
            fx = validar_expresion(row.controls[1].value)
            limite_inferior = float(row.controls[2].value)
            limite_superior = float(row.controls[3].value)
            cifras = int(row.controls[4].value)
            x = sp.Symbol('x')
            f_x1 = fx.subs(x, limite_inferior).evalf()
            f_xu = fx.subs(x, limite_superior).evalf()
            
            if (f_x1 > 0 and f_xu < 0 and cifras >= 0) or (f_x1 < 0 and f_xu > 0 and cifras >= 0):
                if(limite_superior > limite_inferior):
                    try: 
                        rows, raiz, iteracion, Ea, fx, metodo = solve(fx, limite_inferior, limite_superior, cifras)
                        table.rows = rows
                        table.visible = True
                        #Mostrar resultados
                        lbl_root.content = ft.Text(value=f'Solucion: {raiz}', weight="bold", size=20, text_align=ft.TextAlign.CENTER)
                        lbl_root.bgcolor = ft.colors.GREEN
                        lbl_root.padding = 10
                        lbl_root.border_radius = 25
                        lbl_root.width = 100
                        lbl_results.value = f'Metodo: {metodo}\nFuncion {fx}\nCon {iteracion} iteraciones\nError porcentual aproximado {Ea}%'
                        container_results.visible=True
                        
                        event.control.page.update()
                    except ValueError as e:
                        print(f"Error: {e}")
                        show_alert(event, f'Ingrese una funcion valida {e}')
                else:
                    show_alert(event, 'El limite inferior no puede ser mayor que el el limite superior')
            else: 
                if cifras < 0:
                    show_alert(event, 'Las cifras significativas deben ser mayor a cero')
                else:   
                    show_alert(event, f'En el intervalo [{limite_inferior}, {limite_superior}] no existe una raiz')
              
        except ValueError as e:
            print(f"Error: {e}")
            show_alert(event, f'{e}') # me muestra errores si el usuario ingresa caracteres en los textfield 
        
    # Controles para que el usuario interactue
    row = ft.ResponsiveRow(
        [   
            ft.Text(
                value=f'{name}',
                col={"md": 12},
                weight="bold",
                size=20,
                text_align=ft.TextAlign.CENTER            
            ),
            
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
                height=45, col={"md":2}),
            
            ft.ElevatedButton(
                text="Limpiar", 
                on_click=clean, 
                width=100, 
                height=45, col={"md":2}),
        ], 
        alignment=ft.MainAxisAlignment.CENTER,  
    )

    # Tabla de flet que almacena los resuultados del algoritmo
    table = ft.DataTable(
        columns=[ft.DataColumn(ft.Text(col)) for col in ["Iteración", "x1", "xU", "xR", "f(x1)", "f(xU)", "f(xR)", "f(x1)f(xR)", "Ea"]],
        rows=[],
        visible=False
    )

    tbl = ft.Row([ft.Container(padding=20, content=ft.Row([table]))], scroll=ft.ScrollMode.ALWAYS) # Diseno de la tabla 

    lbl_root = ft.Container()
    lbl_results = ft.Text()
    
    # contenedor de los controlos que se muestran los resultados
    container_results = ft.Container(
                    visible=False,
                    bgcolor='#565656',  #ft.colors.BLUE_100,
                    border_radius=ft.border_radius.all(20),
                    padding=20,
                    content=ft.ResponsiveRow(
                        [
                        ft.Container(
                            lbl_root,
                            col={"sm": 6, "md": 4, "xl": 3},
                        ),
                        ft.Container(
                            lbl_results,
                            col={"sm": 12, "md": 12, "xl": 12},
                        )
                    ],
                        alignment=ft.MainAxisAlignment.CENTER,
                )
            
    )
    
    # contenedor de los controlos que se muestran en la interfaz
    container_input = ft.Container(
        bgcolor='#565656',
        border_radius=ft.border_radius.all(20),
        padding=20,
        content=row
    )
    
    view_controls = ft.ResponsiveRow(
        controls=[
            container_input, container_results, tbl
        ])

    

    

    return view_controls
