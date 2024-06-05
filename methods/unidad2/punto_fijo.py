import flet as ft
import sympy as sp
import pandas as pd
from sympy import *
from sympy.core.numbers import *
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

def solve(gx, x0, cifras): # codigo del algoritmo
    rows = []
    x = sp.Symbol('x')
    
    metodo = 'Punto fijo'
    Es = 0.5 * 10 ** (2 - cifras)

    xi = x0
    iteracion = 1
    aprox_anterior = 0
    aprox_actual = 0
    
    g_x = gx

    df = pd.DataFrame(columns=["Iteracion", " Xi", "g(X)", "Error Aproximado"])
    
    while True:
        try:
            gxi = g_x.subs(x, xi).evalf()
           # if im(gxi)!=0:
           #     return True, "Se generaron numeros imaginarios, al calcular las iteraciones"
           # else:
            Ea = abs(((gxi - aprox_anterior)/gxi)*100)
            rows.append(ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(cell))) for cell in [iteracion, xi, gxi, Ea]],
            ))
            #df.loc[iteracion-1] = [iteracion, xi, gxi, Ea,]
                
            if Ea < Es or iteracion==100 :
                break
            else:
                xi = gxi
                    
            aprox_anterior = gxi
            iteracion += 1
        except  ZeroDivisionError as e: 
            return True, "Se genero una division entre cero, al calcular las iteraciones"  
        
    return rows, gxi, Ea, metodo, iteracion 


          
 
def show(): # Muestra los resultados 
    def clean(event):
        container_results.visible = False
        table.visible = False
        row.controls[0].value = ''
        row.controls[1].value = ''
        row.controls[2].value = ''
        
        row.controls[0].autofocus = True
        event.control.page.update()
    
    def get_data(event): # asigna los datos ingresados a la funcion solve()
        x = sp.symbols('x')
        
        def comprobar_imaginarios(expr):
            return sp.im(expr) > 0
     
        
        try:
            gx = validar_expresion(row.controls[0].value)
            x0 = float(row.controls[1].value)
            cifras = int(row.controls[2].value)
            x=sp.symbols('x')
            gx_prima = gx.diff(x)
            print(gx_prima)
            convergencia = gx_prima.subs(x, x0).evalf()   
            print(type(convergencia))
            print(convergencia)
            es_ima=sp.im(convergencia)
            if es_ima != 0:
                comprobacion=True
            elif es_ima==0:
                comprobacion=False     
            if cifras > 0:
                if (Abs(convergencia) < 1) and ( comprobacion == False):
                    try:
                       # division_cero, mensaje =solve(gx, x0, cifras)

                        #if division_cero==True:
                           # show_alert(event, mensaje)
                       # else:    
                        rows, gxi, Ea, metodo, iteracion = solve(gx, x0, cifras)
                        table.rows = rows
                        table.visible = True
                        #Mostrar resultados
                        lbl_root.content = ft.Text(value=f'Solucion: {gxi}', weight="bold", size=20, text_align=ft.TextAlign.CENTER)
                        lbl_root.bgcolor = ft.colors.GREEN
                        lbl_root.padding = 10
                        lbl_root.border_radius = 10
                        lbl_results.value = f'Metodo: {metodo}\ng(x) {gx}\nCon {iteracion} iteraciones\nError porcentual aproximado {Ea}%'
                        container_results.visible=True
                        event.control.page.update()
                    except ValueError as e:
                                print(f"Error: {e}")
                                show_alert(event, f'Ingrese una funcion valida {e}')
                   
                else:
                    if isinstance(convergencia,ComplexInfinity)==True:
                        show_alert(event, f'El punto:{x0} genera una division entre') 
                    elif Abs(convergencia)>=1:
                        show_alert(event, f'El punto:{x0} no converge\nCriterio de convergencia:{Abs(convergencia)}')
                    elif comprobacion==True:   
                        show_alert(event, f'El punto:{x0} genera numeros imaginarios\nPor lo tanto no cumple con el criterio de convergencia')
                  

            else:
                 show_alert(event, 'Las cifras significativas deben ser mayor a cero')
    
        except ValueError as e:
            print(f"Error: {e}")
            show_alert(event, f'{e}') # me muestra errores si el usuario ingresa caracteres en los textfield 
        
    # Controles para que el usuario interactue
    row = ft.ResponsiveRow(
        [
            ft.TextField(
                height=57,
                label="g(x)", 
                autofocus=True,
                suffix=ft.IconButton(
                    icon=ft.icons.HELP_OUTLINE_OUTLINED, on_click=open_dlg_modal),
                col={"md": 3}),
            ft.TextField(
                label="Punto X0",
                col={"md": 3}),
          
            ft.TextField(
                label="Cifras Significativas", 
                col={"md": 3}),
            
            ft.ElevatedButton(
                text="Resolver", 
                on_click=get_data, 
                width=100, 
                height=45, col={"md":3}),
            ft.ElevatedButton(
                text="Limpiar", 
                on_click=clean, 
                width=100, 
                height=45, col={"md":3}),
        ], 
        alignment=ft.MainAxisAlignment.CENTER,  
    )

    # Tabla de flet que almacena los resuultados del algoritmo
    table = ft.DataTable(
        columns=[ft.DataColumn(ft.Text(col)) for col in ["Iteración", " Xi", "g(X)", "Error Aproximado"]],
        rows=[],
        visible=False
    )

    tbl = ft.Row([ft.Container(padding=20, content=ft.Row([table]))], scroll=ft.ScrollMode.ALWAYS,) # Diseno de la tabla 

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
                            col={"sm": 6, "md": 4, "xl": 4},
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
        ],alignment=ft.MainAxisAlignment.CENTER,)

    

    

    return view_controls
