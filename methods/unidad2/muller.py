import flet as ft
import sympy as sp
from sympy import *
from sympy.core.numbers import *
# from methods.unidad1.grafico import show as show_grafico
from methods.widgets.widgets import show_alert, open_dlg_modal
name = "Método de Muller"


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


def solve(fx, punto0, punto1, punto2, cifras): # codigo del algoritmo
    rows = []
    x = sp.Symbol('x')

    Es = 0.5 * 10 ** (2 - cifras)
    
    X0 = punto0
    X1 = punto1
    X2 = punto2
    
    iteracion = 1

    while True:

        fx0 = fx.subs(x, X0)
        fx1 = fx.subs(x, X1)
        fx2 = fx.subs(x, X2)
        if  fx0.is_real==False:
            alert = True
            message = f"La función {fx} en el punto X0={X0} se esta evaluando fuera de su dominio"
            return rows, None, None, iteracion, alert, message #necesita tirar el mensaje
        elif  fx1.is_real==False:
            alert = True
            amessage = "La función {fx} en el punto X1={X1} se esta evaluando fuera de su dominio"
            return rows, None, None, iteracion, alert, message #necesita tirar el mensaje     
           
        elif  fx2.is_real==False:
            alert = True
            message = f"La función {fx} en el punto X2={X2} se esta evaluando fuera de su dominio"
            return rows, None, None, iteracion, alert, message #necesita tirar el mensaje
        else:
            h0 = X1 - X0
            h1 = X2 - X1

            #et0 = &0, et1 = &1
            et0 = (fx1 - fx0)/h0
            if et0.is_real==False:
                alert = True
                message = f"Se genero division entre cero al calcular el &0, en la iteracion {iteracion}"
                return rows, None, None, iteracion, alert, message
            
            et1 = (fx2- fx1)/h1
            if et1.is_real==False:
                alert = True
                message = f"Se genero division entre cero al calcular el &1, en la iteracion {iteracion}"
                return rows, None, None, iteracion, alert, message
            
            a = (et1 - et0)/(h1 + h0)
            b = (a * h1) + et1
            c = fx2
            
            D = sqrt((b ** 2) - (4 * a * c))
            if D.is_real==False:
                alert = True
                message = f"Se genero numeros imaginarios al calcular el D, en la iteracion {iteracion}"
                return rows, None, None, iteracion, alert, message

            if abs(b + D) > abs(b - D):
                Xr = N(X2 + ((-2*c)/((b) + D)),13)
                if Xr.is_real==False:
                    alert = True
                    message = f"Se genero una indeterminacion o numero imaginarios\nAl calcular el xr"
                    return rows, None, None, iteracion, alert, message
                
            else:
                Xr = N(X2 + ((-2*c)/((b) - D)),13)
                if Xr.is_real==False:
                    alert = True
                    message = f"Se genero una indeterminacion o numero imaginarios\nAl calcular el xr"
                    return rows, None, None, iteracion, alert, message

            Ea = abs(((Xr - X2)/Xr)*100)
            if Ea.is_real==False:
                alert = True
                message = f"Se genero division entre cero al calcular el Ea, en la iteracion {iteracion}"
                return rows, None, None, iteracion, alert, message
            
            rows.append(ft.DataRow(
                    cells=[ft.DataCell(ft.Text(str(cell))) for cell in [iteracion, X0, X1, X2, Xr, Ea]],
            ))
            
            if(Ea < Es):
                break
            else:
                X0 = X1
                X1 = X2
                X2 = Xr
                
        iteracion += 1
   
        
    return rows, Xr, Ea, iteracion, False, None


          
 
def show(): # Muestra los resultados 
    def clean(event):
        container_results.visible = False
        table.visible = False
        row.controls[1].value = ''
        row.controls[2].value = ''
        row.controls[3].value = ''
        row.controls[4].value = ''
        row.controls[5].value = ''
        
        row.controls[1].autofocus = True
        event.control.page.update()
    
    def get_data(event): # asigna los datos ingresados a la funcion solve()
        x = sp.symbols('x')
        
        # def comprobar_imaginarios(expr):
        #     return sp.im(expr) > 0
        
        try:
            x=sp.symbols('x')
            
            fx = validar_expresion(row.controls[1].value)
            punto0 = float(row.controls[2].value)
            punto1 = float(row.controls[3].value)
            punto2 = float(row.controls[4].value)
            cifras = int(row.controls[5].value)

            
            
            if cifras > 0:
                try:
                    rows, Xr, Ea, iteracion, alert, message = solve(fx, punto0, punto1, punto2, cifras)
                
                    if alert == True:
                        show_alert(event, message)
                    else:                
                        rows, Xr, Ea, iteracion, alert, message = solve(fx, punto0, punto1, punto2, cifras)
                        table.rows = rows
                        table.visible = True
                                    
                        #Mostrar resultados
                        lbl_root.content = ft.Text(value=f'Solucion: {Xr}', weight="bold", size=20, text_align=ft.TextAlign.CENTER)
                        lbl_root.bgcolor = ft.colors.GREEN
                        lbl_root.padding = 10
                        lbl_root.border_radius = 10
                        lbl_results.value = f'Metodo: {name}\nf(x) {fx}\nCon {iteracion} iteraciones\nError porcentual aproximado {Ea}%'
                        container_results.visible=True
                        event.control.page.update()
                            
                except ValueError as e:
                    print(f"Error: {e}")
                    show_alert(event, f'Ingrese una funcion valida {e}')
            else:

                show_alert(event, 'Las cifras significativas deben ser mayor a cero')
    
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
                label="Funcion", 
                autofocus=True,
                suffix=ft.IconButton(
                    icon=ft.icons.HELP_OUTLINE_OUTLINED, on_click=open_dlg_modal),
                col={"md": 4}),
            ft.TextField(
                label="Punto 1",
                col={"md": 2}),
            ft.TextField(
                label="Punto 2",
                col={"md": 2}),
            ft.TextField(
                label="Punto 3",
                col={"md": 2}),
          
            ft.TextField(
                label="Cifras Significativas", 
                col={"md": 2}),
            
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
        columns=[ft.DataColumn(ft.Text(col)) for col in ["Iteracion", " X0", "X1", "X2", "Xr", "Error Aproximado"]],
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
