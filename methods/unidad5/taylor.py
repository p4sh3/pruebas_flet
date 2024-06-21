import flet as ft
import sympy as sp
from sympy import *
from sympy.core.numbers import *
# from methods.unidad1.grafico import show as show_grafico
from methods.widgets.widgets import show_alert, open_dlg_modal
name = "Método de Taylor"


def validar_expresion(expr):
    x = sp.Symbol("x")
    y = sp.Function("y")(x)
    print(type(x), type(y))

    symbolos_permitidos = {x}
    
    try: 
        exp = sp.sympify(expr, locals={
        "x": x,
        "y": y
        })
        print(type(expr))
        
    except (sp.SympifyError, SyntaxError) as e:
        
        print('Error al convertir')
        raise ValueError('La expresion no es valida')
    
    # Obtener todos los símbolos en la expresión
    symbolos_en_expr = exp.free_symbols
    
    # Verificar que todos los símbolos estén permitidos
    if not symbolos_en_expr.issubset(symbolos_permitidos):
        
        raise ValueError("La expresión contiene símbolos no permitidos")
    else: 
        return exp 


def solve(edo, xi, yi, xf, grado, h): # codigo del algoritmo
    x = sp.Symbol("x")
    y = sp.Function("y")(x)
    
    iteracion = 0
    if xi >= xf:
        message = "Error el X inicial debe de ser menor al X final"
        return None, message, True

    elif h<=0:
        message = "Error el salto(h) debe de ser mayor a 0"
        return None, message, True

    elif (xi+h)>xf:
        message = "El salto(h) no permite mas de una iteracion"
        return None, message, True

    elif grado<=0:
        message = "El grado {grado} no puede calcular, recomendarion grado mayor o igual a 1"
        return None, message, True
    
    else:
        complemento_funcion=0
        if grado>=2:
            derivada=1
            derivada_funcion=edo
            complemento_funcion=0
            while derivada<grado:
                derivada_funcion= derivada_funcion.diff().subs(y.diff(), edo)
                derivada=derivada+1
                complemento_funcion=complemento_funcion+((h**derivada)/(factorial(derivada)))*(derivada_funcion)
            
        tabla=[[],[],[],[]]   
        while xi<xf:
            funcion_final=h*edo+complemento_funcion 
            tabla[0].append(iteracion+1)
            tabla[1].append(xi)
            tabla[2].append(yi)
           
            y_sig=yi+N(funcion_final,10,subs={x:xi,y:yi}).evalf(n=10)

            if not y_sig.is_real:
               
                break
            else:
                tabla[3].append(y_sig)
                xi=(xi+h)
                iteracion=iteracion+1
                yi=y_sig
                
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Iteracion")),
                ft.DataColumn(ft.Text("Xi")),
                ft.DataColumn(ft.Text("Yi")),
                ft.DataColumn(ft.Text("Yi+1")),
            ],
            rows=[
                ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell))) for cell in fila])
                for fila in zip(*tabla)
            ]
        )
        
        tabla_ft = ft.Row([ft.Container(padding=20, content=ft.Row([table]))], scroll=ft.ScrollMode.ALWAYS)
        
        
        message = f"Con Taylor grado {grado}\nLa respuesta es: y({xf})={y_sig}"
        
        solucion = y_sig
        
        return tabla_ft, solucion, message, False
          
 
def show(): # Muestra los resultados 
    def clean(event):
        container_results.visible = False
        tbl.visible = False
        row.controls[1].value = ''
        row.controls[2].value = ''
        row.controls[3].value = '' 
        row.controls[4].value = ''
        row.controls[5].value = ''
        row.controls[6].value = ''       
        row.controls[1].autofocus = True
        event.control.page.update()
    
    def get_data(event): # asigna los datos ingresados a la funcion solve()
       
        try:
            # edo, xi, yi, xf, orden, h
            
            edo = validar_expresion(row.controls[1].value)
            xi = float(row.controls[2].value)
            yi= float(row.controls[3].value)
            xf = float(row.controls[4].value)
            h = float(row.controls[5].value)
            grado = int(row.controls[6].value)

            tabla, solucion, message, alert = solve(edo, xi, yi, xf, grado, h)
            
            if alert == True:
                show_alert(event, message)
            else: 
                   
                try:
                    tbl.content = tabla
                    tbl.visible = True
                        
                    #Mostrar resultados
                    lbl_root.content = ft.Text(value=f'Solucion: {solucion}', weight="bold", size=20, text_align=ft.TextAlign.CENTER)
                    lbl_root.bgcolor = ft.colors.GREEN
                    lbl_root.padding = 10
                    lbl_root.border_radius = 10
                    lbl_results.value = f'{message}'
                    lbl_results.text_align = ft.TextAlign.CENTER
                    container_results.visible=True
                    event.control.page.update()
                            
                except ValueError as e:
                    print(f"Error: {e}")
                    show_alert(event, f'Ingrese una funcion valida {e}')
                    
        except ValueError as e:
            show_alert(event, f'Error al ingresar datos {e}') # me muestra errores si el usuario ingresa caracteres en los textfield 
        
    # Controles para que el usuario interactue
    row = ft.ResponsiveRow(
        [   ft.Text(
            value=f'{name}',
            col={"md": 12},
            weight="bold",
            size=20,
            text_align=ft.TextAlign.CENTER            
            ),
         
            ft.TextField(
                height=57,
                label="EDO", 
                autofocus=True,
                suffix=ft.IconButton(
                    icon=ft.icons.HELP_OUTLINE_OUTLINED, on_click=open_dlg_modal),
                col={"md": 2}),
            
            ft.TextField(
                label="Valor x inicial",
                col={"md": 2}),
            
            ft.TextField(
                label="Valor y inicial", 
                col={"md": 2}),
            
            ft.TextField(
                label="Valor x final", 
                col={"md": 2}),
            
            ft.TextField(
                label="Valor de salto (h)", 
                col={"md": 2}),
            
            ft.TextField(
                label="Grado (Hasta grado n)", 
                col={"md": 2}),
            
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
    
    tbl = ft.Container(
        visible=False
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
