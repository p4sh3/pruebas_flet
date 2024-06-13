import flet as ft
import sympy as sp
from sympy import *
from sympy.core.numbers import *
# from methods.unidad1.grafico import show as show_grafico
from methods.widgets.widgets import show_alert, open_dlg_modal, show_modal_alert
name = "Interpolación Cuadratica"


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


def solve(fx, valores_x, valores_y): # codigo del algoritmo
    x = sp.symbols('x')
    f_x = fx
    x_valores = valores_x
    f = valores_y
    
    def valores_repetidos(lista):
        return len(lista) != len(set(lista))
    if valores_repetidos(x_valores):
            message = "En la tabla se encuentran valores repetidos"   
            return None, message, True
        
    if len(x_valores)>=3 and len(f)>=3 :
        if valores_repetidos(f):
            message = "En la tabla de valores de Y se encuentran valores repetidos"   
            return None, message, True
        
        b0 = f[0]
        b1 = (f[1] - b0)/(x_valores[1] - x_valores[0])
        b2=(((f[2] - f[1])/(x_valores[2] - x_valores[1])) - (b1))/(x_valores[2] - x_valores[0])
        f2x = b0 + b1 * (x - x_valores[0]) + b2*(x - x_valores[0])*(x - x_valores[1]) 
        poli = sp.expand(f2x)
        message = f'B0 = {b0} \t\t\t\tB1 = {b1} \t\t\t\tB2 = {b2}'
        
        return poli, message, False
        
    elif f_x != "" and len(x_valores) >= 3:
        i = 0
        while i < len(x_valores):
            evaluar = f_x.subs({x:x_valores[i]}).evalf()
            
            if evaluar.is_real == False:
                message = f"Al evaluar la funcion {f_x} se evaluo un punto fuera de su dominio\n"
                
                return None, message, True
            
            f.append(f_x.subs({x:x_valores[i]}).evalf())  
            i = i + 1 
         
        # if (x_valores[1] - x_valores[0]) == 0:
        #     message = "En la tabla se encuentran valores repetidos"   
        #     return None, message, True
           
        b0 = f[0]
        b1 = N((f[1]-b0)/(x_valores[1]-x_valores[0])).evalf()
        b2 = (((f[2] - f[1])/(x_valores[2] - x_valores[1])) - (b1))/(x_valores[2] - x_valores[0])
        print(type(b0))
        print(type(b1))
        print(type(b2))
        
        
        f2x = b0 + b1*(x - x_valores[0]) + b2*(x - x_valores[0])*(x - x_valores[1])
        poli = sp.expand(f2x)
        message = f'B0 = {b0} \t\t\t\tB1 = {b1} \t\t\t\tB2 = {b2}'
        
        return poli, message, False
    
    else:
        if  len(x_valores) >= 3 and f_x == "" and len(f) == 0:
            message = f"No hay funcion para crear la tabla f(x)"
            
            return None, message, True
            
        elif (len(x_valores) < 3 or len(f) < 3) and f_x == "" :
            message = f"La tabla de valores x o f(x) no cuenta con los valores necesarios"
            
            return None, message, True
            
        elif f_x != "" and len(x_valores) < 3:
            message = f"La tabla de valores x no cuenta con datos necesarios"
            
            return None, message, True

def show(): # Muestra los resultados 
    def clean(event):
        container_results.visible = False
        row.controls[2].value = ''
        row.controls[3].value = ''
        row.controls[4].value = ''
        
        row.controls[2].autofocus = True
        event.control.page.update()
    
    def get_data(event): # asigna los datos ingresados a la funcion solve()
        x = sp.symbols('x')
        
        selection_option = int(select_options.value)
        
        if selection_option == 1:
            try:
                x=sp.symbols('x')
                
                fx = validar_expresion(row.controls[2].value)
                x = row.controls[3].value
                valores_y = row.controls[4].value
                valores_xstr = x.split(',')
                valores_x = [float(valor.strip()) for valor in valores_xstr]
                valores_y = []
                            
                try:  
                    polinomio, message, alert = solve(fx, valores_x, valores_y)
                    
                    if alert == True:
                        show_alert(event, message)
                    else: 
                        #Mostrar resultados
                        lbl_results.content = ft.Text(value=f'{message}', size=16, text_align=ft.TextAlign.CENTER)
                        lbl_results2.content = ft.Text(value=f'{polinomio}', weight="bold", size=20, text_align=ft.TextAlign.CENTER)
                        lbl_results2.bgcolor = ft.colors.BLUE
                        lbl_results2.padding = 10
                        lbl_results2.border_radius = 10
                        container_results.visible=True
                        event.control.page.update()
                                    
                except ValueError as e:
                    print(f"Error: {e}")
                    show_alert(event, f'Ingrese una funcion valida {e}')       
        
            except ValueError as e:
                print(f"Error: {e}")
                show_alert(event, f'{e}') # me muestra errores si el usuario ingresa caracteres en los textfield 
                
        if selection_option == 2:
            try:
                x=sp.symbols('x')
                
                fx = row.controls[2].value
                fx = ''
                x = row.controls[3].value
                y = row.controls[4].value
                valores_xstr = x.split(',')
                valores_x = [float(valor.strip()) for valor in valores_xstr]
                valores_ystr = y.split(',')
                valores_y = [float(valor.strip()) for valor in valores_ystr]
                            
                try:  
                    polinomio, message, alert = solve(fx, valores_x, valores_y)
                    
                    if alert == True:
                        show_alert(event, message)
                    else: 
                        #Mostrar resultados
                        lbl_results.content = ft.Text(value=f'{message}', size=16, text_align=ft.TextAlign.CENTER)
                        lbl_results2.content = ft.Text(value=f'polinomio interpolacion cuadratico:\n {polinomio}', weight="bold", size=20, text_align=ft.TextAlign.CENTER)
                        lbl_results2.bgcolor = ft.colors.BLUE
                        lbl_results2.padding = 10
                        lbl_results2.border_radius = 10
                        container_results.visible=True
                        event.control.page.update()
                                    
                except ValueError as e:
                    print(f"Error: {e}")
                    show_alert(event, f'Ingrese una funcion valida {e}')       
        
            except ValueError as e:
                print(f"Error: {e}")
                show_alert(event, f'{e}') # me muestra errores si el usuario ingresa caracteres en los textfield 
        
    
    def update_inputs(event): # Activa o desactiva los inputs
        selection_option = int(select_options.value)
        
        if selection_option == 1:
            row.controls[2].visible = True
            row.controls[3].visible = True
            row.controls[4].visible = False
            row.controls[5].visible = True
            row.controls[6].visible = True
            row.controls[2].col = {"md": 4}
            row.controls[3].col = {"md": 4}
            show_modal_alert(event, 'Ingrese valores separados por coma 1, 2, 3, o 1.000, 2.2222, 3.9999')
            event.control.page.update()
            
        elif selection_option == 2:
            row.controls[2].visible = False
            row.controls[3].visible = True
            row.controls[4].visible = True
            row.controls[5].visible = True
            row.controls[6].visible = True
            row.controls[3].col = {"md": 4}
            row.controls[4].col = {"md": 4}
            event.control.page.update()
                 
    # Controles para que el usuario interactue
    select_options = ft.Dropdown(
        label='Opciones para resolver',
        on_change = update_inputs,
        height=60,
        options=[
            ft.dropdown.Option(text='Funcion y valores en x', key=1),
            ft.dropdown.Option(text='Tabla de valores x, y', key=2),
        ]
    )
    
    
            
            
    
    row = ft.ResponsiveRow(
        [   
            ft.Text(
                value=f'{name}',
                col={"md": 12},
                weight="bold",
                size=20,
                text_align=ft.TextAlign.CENTER            
            ),
            
            ft.Container(
                        select_options,
                        col={"md": 3},
                    ),
            
            ft.TextField(
                height=57,
                label="Función", 
                autofocus=True,
                visible = False,
                suffix=ft.IconButton(
                    icon=ft.icons.HELP_OUTLINE_OUTLINED, on_click=open_dlg_modal),
                col={"md": 3}),
            
            ft.TextField(
                height=57,
                visible = False,
                label="Valores de x", 
                col={"md": 3}),
            
            ft.TextField(
                height=57,
                visible = False,
                label="Valores de y", 
                col={"md": 3}),
            
            ft.ElevatedButton(
                text="Resolver", 
                on_click=get_data, 
                width=100, 
                visible = False,
                height=45, col={"md":2}),
            
            ft.ElevatedButton(
                text="Limpiar", 
                on_click=clean, 
                width=100, 
                visible=False,
                height=45, col={"md":2}),
        ], 
        alignment=ft.MainAxisAlignment.CENTER,  
    )
    
    lbl_results2 = ft.Container()
    lbl_results = ft.Container()
    
    # contenedor de los controlos que se muestran los resultados
    container_results = ft.Container(
                    visible=False,
                    bgcolor='#565656',  #ft.colors.BLUE_100,
                    border_radius=ft.border_radius.all(20),
                    padding=20,
                    content=ft.ResponsiveRow(
                        [
                        ft.Container(
                            lbl_results,
                            col={"sm": 12, "md": 12, "xl": 12},
                        ),
                        ft.Container(
                            lbl_results2,
                            col={"sm": 6, "md": 8, "xl": 4},
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
            container_input, container_results
        ],alignment=ft.MainAxisAlignment.CENTER,)

    

    

    return view_controls
