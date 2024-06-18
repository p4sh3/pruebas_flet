import flet as ft
import sympy as sp
from sympy import *
from sympy.core.numbers import *
# from methods.unidad1.grafico import show as show_grafico
from methods.widgets.widgets import show_alert, open_dlg_modal
name = "Método de Rugen Kutta"


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


def solve(edo, xi, yi, xf, orden, h): # codigo del algoritmo
    x, y = sp.symbols('x y')
    iteracion = 0
    if orden == 2:
        tabla = [[],[],[],[],[],[]]
        
        while xi < xf:
            tabla[0].append(iteracion+1)
            tabla[1].append(xi)
            tabla[2].append(yi)
            k_1 = N(edo,8,subs={x:xi}).evalf(n=6)
            k1 = N(k_1,8,subs={y:yi}).evalf(n=6)
            k_2 = N(edo,8,subs={x:xi+h}).evalf(n=6)
            k2 = N(k_2,8,subs={y:yi+k1*h}).evalf(n=6)
            
            if k1.is_real == False:
                message = "En el valor k1 se generaron numeros no reales"
                return None, None, message, True
                
            elif k2.is_real==False:
                message = "En el valor k2 se generaron numeros no reales"
                return None, None, message, True
                
            else:
                yi_sig = N(yi + (1/2)*h*(k1 + k2),8)
                tabla[3].append(k1)
                tabla[4].append(k2)
                tabla[5].append(yi_sig)
                iteracion = iteracion + 1
                xi = (xi + h)
                yi = yi_sig
        
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Iteracion")),
                ft.DataColumn(ft.Text("Xi")),
                ft.DataColumn(ft.Text("Yi")),
                ft.DataColumn(ft.Text("K1")),
                ft.DataColumn(ft.Text("K2")),
                ft.DataColumn(ft.Text("Yi+1")),
            ],
            rows=[
                ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell))) for cell in fila])
                for fila in zip(*tabla)
            ]
        )
        
        tabla_ft = ft.Row([ft.Container(padding=20, content=ft.Row([table]))], scroll=ft.ScrollMode.ALWAYS)
        
        solucion = tabla[5][len(tabla[5])-1]
        
        message = f'Iteraciones: {iteracion}'
        
        return tabla_ft, solucion, message, False

    
    elif orden == 3:
        tabla=[[],[],[],[],[],[],[]]
        
        while xi < xf:
            
            tabla[0].append(iteracion+1)
            tabla[1].append(xi)
            tabla[2].append(yi)
            k_1 = N(edo,8,subs={x:xi}).evalf(n=6)
            k1 = N(k_1,8,subs={y:yi}).evalf(n=6)
            k_2 = N(edo,8,subs={x:xi+(h/2)}).evalf(n=6)
            k2 = N(k_2,8,subs={y:yi+(h/2)*k1}).evalf(n=6)
            k_3 = N(edo,8,subs={x:xi+(h)}).evalf(n=6)
            k3 = N(k_3,8,subs={y:yi-k1*h+2*k2*h}).evalf(n=6)
            if k1.is_real == False:
                message =  "En el valor k1 se generaron numeros no reales"
                return None, None, message, True
                
            elif k2.is_real==False:
                message = "En el valor k2 se generaron numeros no reales"
                return None, None, message, True
            elif k3.is_real==False:
                message = "En el valor k2 se generaron numeros no reales"
                return None, None, message, True
    
            else:
                yi_sig = N(yi + (1/6)*h*(k1 + 4*k2 + k3),8)
                tabla[3].append(k1)
                tabla[4].append(k2)
                tabla[5].append(k3)
                tabla[6].append(yi_sig)
                iteracion = iteracion + 1
                xi = xi + h
                yi = yi_sig
                
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Iteracion")),
                ft.DataColumn(ft.Text("Xi")),
                ft.DataColumn(ft.Text("Yi")),
                ft.DataColumn(ft.Text("K1")),
                ft.DataColumn(ft.Text("K2")),
                ft.DataColumn(ft.Text("K3")),
                ft.DataColumn(ft.Text("Yi+1")),
            ],
            rows=[
                ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell))) for cell in fila])
                for fila in zip(*tabla)
            ]
        )
        
        tabla_ft = ft.Row([ft.Container(padding=20, content=ft.Row([table]))], scroll=ft.ScrollMode.ALWAYS)
        
        solucion = tabla[6][len(tabla[6])-1]
        
        message = f'Iteraciones: {iteracion}'
        
        return tabla_ft, solucion, message, False

    
    elif orden == 4:
        tabla=[[],[],[],[],[],[],[],[]]
        columnas=["iteracion","xi","yi","k1","k2","k3","k4","yi+1"]
        
        while xi < xf:
            
            tabla[0].append(iteracion+1)
            tabla[1].append(xi)
            tabla[2].append(yi)
            
            k_1 = N(edo,8,subs={x:xi}).evalf(n=8)
            k1 = N(k_1,8,subs={y:yi}).evalf(n=6)
            k_2 = N(edo,8,subs={x:xi+(h/2)}).evalf(n=6)
            k2 = N(k_2,8,subs={y:yi+(h/2)*k1}).evalf(n=6)
            k_3 = N(edo,8,subs={x:xi+(h/2)}).evalf(n=6)
            k3 = N(k_3,8,subs={y:yi+k2*(h/2)}).evalf(n=6)
            k_4 = N(edo,8,subs={x:xi+(h)}).evalf(n=6)
            k4 = N(k_4,8,subs={y:yi+k3*h}).evalf(n=6)
            
            if k1.is_real == False:
                message = "En el valor k1 se generaron numeros no reales"
                return None, None, message, True
            
            elif k2.is_real == False:
                message = "En el valor k2 se generaron numeros no reales"
                return None, None, message, True
            
            elif k3.is_real == False:
                message = "En el valor k2 se generaron numeros no reales"
                return None, None, message, True
                
            elif k4.is_real == False:
                message = "En el valor k2 se generaron numeros no reales"
                return None, None, message, True
                
            else:
                    yi_sig=N(yi + (1/6)*h*(k1 + 2*k2 + 2*k3 + k4),8)
                    tabla[3].append(k1)
                    tabla[4].append(k2)
                    tabla[5].append(k3)
                    tabla[6].append(k4)
                    tabla[7].append(yi_sig)
                    iteracion=iteracion+1
                    xi=xi+h
                    yi=yi_sig
        
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Iteracion")),
                ft.DataColumn(ft.Text("Xi")),
                ft.DataColumn(ft.Text("Yi")),
                ft.DataColumn(ft.Text("K1")),
                ft.DataColumn(ft.Text("K2")),
                ft.DataColumn(ft.Text("K3")),
                ft.DataColumn(ft.Text("K4")),
                ft.DataColumn(ft.Text("Yi+1")),
            ],
            rows=[
                ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell))) for cell in fila])
                for fila in zip(*tabla)
            ]
        )
        
        tabla_ft = ft.Row([ft.Container(padding=20, content=ft.Row([table]))], scroll=ft.ScrollMode.ALWAYS)
        
        solucion = tabla[7][len(tabla[7])-1]
        
        message = f'Iteraciones: {iteracion}'
        
        return tabla_ft, solucion, message, False
        
    else:
        message = f"el orden {orden} no esta disponible en el algoritmo"
        
        return None, None, message, True
   


          
 
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
            orden = int(row.controls[6].value)

            tabla, solucion, message, alert = solve(edo, xi, yi, xf, orden, h)
            
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
                    lbl_results.value = f'Orden: {orden}\t\t\t\t{message}'
                    lbl_results.text_align = ft.TextAlign.CENTER
                    container_results.visible=True
                    event.control.page.update()
                            
                except ValueError as e:
                    print(f"Error: {e}")
                    show_alert(event, f'Ingrese una funcion valida {e}')
                    
        except ValueError as e:
            print(f"Error: {e}")
            show_alert(event, f'{e}') # me muestra errores si el usuario ingresa caracteres en los textfield 
        
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
                label="Orden (Hasta orden 4)", 
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
