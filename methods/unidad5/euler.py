import flet as ft
import sympy as sp
from sympy import *
from sympy.core.numbers import *
# from methods.unidad1.grafico import show as show_grafico
from methods.widgets.widgets import show_alert, open_dlg_modal
name = "Método de Euler"


def validar_expresion(expr):
    x, y = sp.symbols('x y')
    symbolos_permitidos = {x,y}
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


def solve(edo, xi, yi, xf, posicion, h): # codigo del algoritmo
    x, y = sp.symbols('x y')
    iteracion = 0
    
    if xi>=xf:
        message = "Error el X inicial debe de ser menor al X final"
        return None, None, message, True

    if h<=0:
        message = "Error el salto(h) debe de ser mayor a 0"
        return None, None, message, True

    if (xi+h)>xf:
        message = "El salto(h) no permite mas de una iteracion"
        return None, None, message, True

    if posicion==1 :
        
        tabla=[[],[],[],[],[]]
        # columnas=["iteracion","xi","yi","y^","yi+1"]
        
        while xi<xf:
            tabla[0].append(iteracion+1)
            tabla[1].append(xi)
            tabla[2].append(yi)
            y_s=yi+h*N(edo,10,subs={x:xi,y:yi}).evalf(n=10)
            if not y_s.is_real:
                message = "En el valor yi+1 se generaron numeros no reales"
                return None, None, message, True
            
            else:
                tabla[3].append(y_s)
                xi=(xi+h)
                yi_sig=yi+h*N(edo,10,subs={x:xi,y:y_s}).evalf(n=10)
                if not yi_sig.is_real:
                    message = "En el valor yi+1 se generaron numeros no reales"
                    return None, None, message, True
                    
                tabla[4].append(yi_sig)
                iteracion=iteracion+1
                yi=yi_sig
                
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Iteracion")),
                ft.DataColumn(ft.Text("Xi")),
                ft.DataColumn(ft.Text("Yi")),
                ft.DataColumn(ft.Text("y^")),
                ft.DataColumn(ft.Text("Yi+1")),
            ],
            rows=[
                ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell))) for cell in fila])
                for fila in zip(*tabla)
            ]
        )
        
        tabla_ft = ft.Row([ft.Container(padding=20, content=ft.Row([table]))], scroll=ft.ScrollMode.ALWAYS)  
             
        solucion = yi_sig
        
        message = 'Hacia atras'
        
        return tabla_ft, solucion, message, False 
        
        
    elif posicion==2:
        
        # print(f"centrado")
        tabla=[[],[],[],[]]
        # columnas=["iteracion","xi","yi","yi+1"]
        
        while xi<xf:
            tabla[0].append(iteracion)
            tabla[1].append(xi)
            tabla[2].append(yi)
            print(iteracion)
            yi_sig=yi+h*N(edo,10,subs={x:xi,y:yi}).evalf(n=10)
            if not yi_sig.is_real:
                message = "En el valor yi+1 se generaron numeros no reales"
                return None, None, message, True
                
            else:
                tabla[3].append(yi_sig)
                iteracion=iteracion+1
                xi=(xi+h)
                yi=yi_sig
                
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
             
        solucion = yi_sig
        
        message = 'Centrado'
        
        return tabla_ft, solucion, message, False 
        
        
    elif posicion==3:
        
        # print(f"hacia adelante")
        tabla=[[],[],[],[]]
        # columnas=["iteracion","xi","yi","yi+1"]
        
        while xi<xf:
            tabla[0].append(iteracion)
            tabla[1].append(xi)
            tabla[2].append(yi)
            print(iteracion)
            yi_sig=yi+h*N(edo,10,subs={x:xi,y:yi}).evalf(n=10)
            if not yi_sig.is_real:
                message = "En el valor yi+1 se generaron numeros no reales"
                return None, None, message, True
        
            else:
                tabla[3].append(yi_sig)
                iteracion=iteracion+1
                xi=(xi+h)
                yi=yi_sig
        
        
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
             
        solucion = yi_sig
        
        message = 'Hacia adelante'
        
        return tabla_ft, solucion, message, False 
        
    elif posicion==4:
        
        # print(f"mejorado")
        tabla=[[],[],[],[],[]]
        # columnas=["iteracion","xi","yi","y^","yi+1"]
        
        while xi<xf:
            tabla[0].append(iteracion)
            tabla[1].append(xi)
            tabla[2].append(yi)
            print(iteracion)
            y_s=yi+h*N(edo,10,subs={x:xi,y:yi}).evalf(n=10)
            if not y_s.is_real:
                message = "En el valor yi+1 se generaron numeros no reales"
                return None, None, message, True
    
            else:
                
                tabla[3].append(y_s)
                yi_sig=yi+(h/2)*(N(edo,10,subs={x:xi,y:yi}).evalf(n=10)+N(edo,10,subs={x:xi+h,y:y_s}).evalf(n=10))
                if not yi_sig.is_real:
                    message = "En el valor yi+1 se generaron numeros no reales"
                    return None, None, message, True
                
                xi=(xi+h)
                tabla[4].append(yi_sig)
                iteracion=iteracion+1
                yi=yi_sig
                
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Iteracion")),
                ft.DataColumn(ft.Text("Xi")),
                ft.DataColumn(ft.Text("Yi")),
                ft.DataColumn(ft.Text("y^")),
                ft.DataColumn(ft.Text("Yi+1")),
            ],
            rows=[
                ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell))) for cell in fila])
                for fila in zip(*tabla)
            ]
        )
        
        tabla_ft = ft.Row([ft.Container(padding=20, content=ft.Row([table]))], scroll=ft.ScrollMode.ALWAYS)  
             
        solucion = yi_sig
        
        message = 'Hacia atras'
        
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
        x, y = sp.symbols('x y')
       
        try:
            # edo, xi, yi, xf, orden, h
            
            edo = validar_expresion(row.controls[1].value)
            xi = float(row.controls[2].value)
            yi= float(row.controls[3].value)
            xf = float(row.controls[4].value)
            h = float(row.controls[5].value)
            paso_select = int(select_metodo.value)
            
            if paso_select == 1:
                posicion = 1
            elif paso_select == 2:
                posicion = 2
            elif paso_select == 3:
                posicion = 3
            elif paso_select == 4:
                posicion = 4

            tabla, solucion, message, alert = solve(edo, xi, yi, xf, posicion, h)
            
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
            print(f"Error: {e}")
            show_alert(event, f'{e}') # me muestra errores si el usuario ingresa caracteres en los textfield 
        
        
    select_metodo= ft.Dropdown(
        label='Metodo',
        # on_change=on_change_orden,
        height=60,
        options=[
            ft.dropdown.Option(text='Hacia atras', key=1 ),
            ft.dropdown.Option(text='Centrada', key=2),
            ft.dropdown.Option(text='Hacia adelante', key=3),
             ft.dropdown.Option(text='Mejorado', key=4)
        ]
    )
        
        
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
            
            ft.Container(
                        select_metodo,
                        col={"md": 2},
                    ),
            
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
