import flet as ft
import sympy as sp
from sympy import *
from sympy.core.numbers import *
# from methods.unidad1.grafico import show as show_grafico
from methods.widgets.widgets import show_alert, open_dlg_modal, show_modal_alert
name = "Diferencia Numerica"


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


def resolver(funcion, derivada, direccion, ecuacion, h_value, x_value, nivel=None): # codigo del algoritmo
    x = sp.symbols('x')
    fx = funcion
    xi = x_value
    h = h_value
    # derivada = option_orden_dx
    # direccion = option_metodo_dx
    # ecuacion = option_tipo_ec
    
    try:
        # Función para evaluar fx de forma compacta
        def f(valor):
            return fx.subs(x, valor).evalf()
        
        #def derivas por diferencias finitas (hi):
        def Dx_Diferencias_Finitas(hi):
            
            calculo = None
            
            # Hacia atrás
            if direccion == 1:
                
                if derivada == 1:
                    
                    if ecuacion == 1:
                        calculo = (f(xi) - f(xi-hi)) / (hi)
                    else:
                        calculo = (3*f(xi) - 4*f(xi-hi) + f(xi-2*hi)) / (2*hi)
                
                elif derivada == 2:
                    
                    if ecuacion == 1:
                        calculo = (f(xi) - 2*f(xi-hi) + f(xi-2*hi)) / (hi**2)
                    else:
                        calculo = (2*f(xi) - 5*f(xi-hi) + 4*f(xi-2*hi) - f(xi-3*hi)) / (hi**2)

                elif derivada == 3:
                    
                    if ecuacion == 1:
                        calculo = (f(xi) - 3*f(xi-hi) + 3*f(xi-2*hi) - f(xi-3*hi)) / (hi**3)
                    else:
                        calculo = (5*f(xi) - 18*f(xi-hi) + 24*f(xi-2*hi) - 14*f(xi-3*hi) + 3*f(xi-4*hi)) / (2*hi**3)
                
                elif derivada == 4:
                    
                    if ecuacion == 1:
                        calculo = (f(xi) - 4*f(xi-hi) + 6*f(xi-2*hi) - 4*f(xi-3*hi) + f(xi-4*hi)) / (h**4)
                    else:
                        calculo = (3*f(xi) - 14*f(xi-hi) + 26*f(xi-2*hi) - 24*f(xi-3*hi) + 11*f(xi-4*hi) - 2*f(xi-5*hi)) / (h**4)
            
            # Hacia adelante
            elif direccion == 2:
                
                if derivada == 1:
                    
                    if ecuacion == 1:# Orden 1
                        calculo = (f(xi+hi) - f(xi)) / (hi)
                    else:# Orden 2 - Taylor
                        calculo = (-f(xi+2*hi) + 4*f(xi+hi) - 3*f(xi)) / (2*h)
                    
                elif derivada == 2:
                    
                    if ecuacion == 1:# Orden 1
                        calculo = (f(xi+2*hi) - 2*f(xi+hi) + f(xi)) / (hi**2)
                    else:# Orden 2 - Taylor
                        calculo = (-f(xi+3*hi) + 4*f(xi+2*hi) - 5*f(xi+hi) + 2*f(xi)) / (hi**2)
                
                elif derivada == 3:
                    
                    if ecuacion == 1:# Orden 1
                        calculo = (f(xi+3*hi) - 3*f(xi+2*hi) + 3*f(xi+hi) - f(xi)) / (h**3)
                    else:# Orden 2 - Taylor
                        calculo = (-3*f(xi+4*hi) + 14*f(xi+3*hi) - 24*f(xi+2*hi) + 18*f(xi+hi) - 5*f(xi)) / (2*h**3)
                
                elif derivada == 4:
                    
                    if ecuacion == 1:# Orden 1
                        calculo = (f(xi+4*hi) - 4*f(xi+3*hi) + 6*f(xi+2*hi) - 4*f(xi+hi) + f(xi)) / (h**4)
                    else:# Orden 2 - Taylor
                        calculo = (-2*f(xi+5*hi) + 11*f(xi+4*hi) - 24*f(xi+3*hi) + 26*f(xi+2*hi) - 14*f(xi+hi) + 3*f(xi)) / (h**4)
            
            # Centrales
            else:
                
                if derivada == 1:
                    
                    if ecuacion == 1:
                        calculo = (f(xi+hi) - f(xi-hi)) / (2*hi)
                    else:
                        calculo = (-f(xi+2*hi) + 8*f(xi+hi) - 8*f(xi-hi) + f(xi-2*hi)) / (12*hi)
                
                elif derivada == 2:
                    
                    if ecuacion == 1:
                        calculo = (f(xi+hi) - 2*f(xi) + f(xi-hi)) / (hi**2)
                    else:
                        calculo = (-f(xi+2*hi) + 16*f(xi+hi) - 30*f(xi) + 16*f(xi-hi) - f(xi-2*hi)) / (12*hi**2)
                
                elif derivada == 3:
                    
                    if ecuacion == 1:
                        calculo = (f(xi+2*hi) - 2*f(xi+hi) + 2*f(xi-hi) - f(xi-2*hi)) / (2*h**3)
                    else:
                        calculo = (-f(xi+3*hi) + 8*f(xi+2*hi) - 13*f(xi+hi) + 13*f(xi-hi) - 8*f(xi-2*hi) + f(xi-3*hi)) / (8*h**3)
                
                elif derivada == 4:
                    
                    if ecuacion == 1:
                        calculo = (f(xi+2*hi) - 4*f(xi+hi) + 6*f(xi) - 4*f(xi-hi) + f(xi-2*hi)) / (h**4)
                    else:
                        calculo = (-f(xi+3*hi) + 12*f(xi+2*hi) + 39*f(xi+hi) + 56*f(xi) - 39*f(xi-hi) + 12*f(xi-2*hi) + f(xi-3*hi)) / (6*h**4)
            
           
            # Devolver el valor obtenido
            if calculo is not None:
                return calculo
            else:
                message = "Escoja un método válido para evaluar."
                
                return None, None, message, True
        
        # Método de Richarson        
        def Richarson(Dh):
            
            D = [Dh]
            
            for k in range(2,nivel+1,1):
                D.append([])
                #print(D)
                for i in range(len(D[k-2])-1):
                    if k == 2:
                        calculo_Richarson = (4/3 * D[k-2][i+1]) - (1/3 * D[k-2][i])
                        D[-1].append(calculo_Richarson) 
                    else:
                        calculo_Richarson = (4**k * D[k-2][i+1] - D[k-2][i]) / (4**k - 1)
                        D[-1].append(calculo_Richarson)
                    #print(calculo_Richarson)
            
            
            # for i,j in zip(D, range(len(D))):
            #     print(f"Nivel {j+1}: {i}")
            
            #print("\n", D[-1][0])        
            return D
        
            
        args = [fx, xi, h, derivada, direccion, ecuacion]
        
        if not all(arg is not None for arg in args):
            message = f"Los argumentos no deben estar vacíos. Revise: {args}"
            
            return None, None, message, True

        elif not (isinstance(fx, (sp.Eq, sp.Poly, sp.Expr))):
            message = "La función no es válida o no ingresó una función."
            
            return None, None, message, True
        
        elif not (fx.free_symbols == {x}):
            message = "La función no es válida. Solo puede estar en términos de x."
            
            return None, None, message, True
        
        elif not (isinstance(xi, (int, float)) and not isinstance(xi, bool)):
            message = "Valor de xi debe ser un número."
            
            return None, None, message, True
        
        elif not (isinstance(h, (int, float)) and not isinstance(h, bool) and h > 0):
            message = "Valor de h debe ser un número positivo."
            
            return None, None, message, True
        
        # Por ahora solo derivada 1 y 2
        elif not (type(derivada) is int and (derivada > 0 and derivada < 3)):
            message = "N° de derivada debe ser entero mayor que 0."
            
            return None, None, message, True
        
        elif not (type(direccion) is int and (direccion > 0 and direccion < 4)):
            message = "La dirección debe ser un número entero tal que: 1 = Atrás, 2 = Adelante, 3 = Central."
            
            return None, None, message, True
        
        elif not (type(ecuacion) is int and (ecuacion > 0 and ecuacion < 3)):
            message = "N° de ecuación debe ser entero entre 1 y 2. 2 = \"Terminos de la serie de Taylor\"."
            
            return None, None, message, True
        
        elif not (nivel is None or (nivel is not None and isinstance(nivel, int) and not isinstance(nivel, bool) and nivel > 0)):
            message = "El nivel debe ser un número entero mayor que 0 si se va a evaluar por el método de Richarson."
            
            return None, None, message, True

        
        # Derivadas Finitas
        if nivel is None:
            
            resultado = Dx_Diferencias_Finitas(h)
        
            
            diff_funcion = sp.diff(funcion, x, derivada)
            vv = diff_funcion.subs(x, xi).evalf()
            
            Ea = (abs((vv - resultado) / vv)*100).evalf()
            
            text="'"
            message = f"Derivada: f{text*derivada}(x) = {diff_funcion}\t\t\t\tValor real: f{text*derivada}({xi}) = {vv} \t\t\t\tError aproximado: {Ea}%"

            return None,  resultado, message, False
        # Derivadas Finitas + Richarson
        else:
            
            lista_h = [h]
            for i in range(nivel-1):
                lista_h.append(lista_h[-1] / 2)
            
            # Evaluamos las derivas de hi
            lista_h_Evaluada = []
            
            for i in lista_h:
                lista_h_Evaluada.append(Dx_Diferencias_Finitas(i))
            
            # LLamada al Método de Richarson

            resultados = Richarson(lista_h_Evaluada)
            
            for i in range(len(resultados)):
                
                if len(resultados[i]) < len(resultados[0]):
                    diferencia = len(resultados[0]) - len(resultados[i])
                    #print(diferencia)
                    resultados[i] = ["-"]*diferencia + resultados[i]
            
            table = ft.DataTable(
                columns=[
                ] + [ft.DataColumn(ft.Text(f'Nivel {i+1}')) for i in range(len(resultados))],
                rows=[
                    ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell))) for cell in fila])
                    for fila in zip(*resultados)
                ]
            )
            tabla = ft.Row([ft.Container(padding=20, content=ft.Row([table]))], scroll=ft.ScrollMode.ALWAYS)
            
            resultado_richardson = resultados[-1][-1]
            
            diff_funcion = sp.diff(funcion, x, derivada)
            vv = diff_funcion.subs(x, xi).evalf()
            
            Ea = (abs((vv - resultado_richardson) / vv)*100).evalf()
            
            text="'"
            message = f"Derivada: f{text*derivada}(x) = {diff_funcion}\t\t\t\tValor real: f{text*derivada}({xi}) = {vv} \t\t\t\tError aproximado: {Ea}%"
        
            return tabla,  resultado_richardson, message, False
        
        
    
    except Exception as e:
        message = f'Error inesperado: {e}'
        
        return None, None, message, True
   
    

   

def show(): # Muestra los resultados 
      
    def clean(event):
        container_results.visible = False
        row.controls[2].value = ''
        row.controls[6].value = '' 
        row.controls[7].value = ''       
        row.controls[8].value = '' 
        row.controls[2].autofocus = True
        tbl.visible = False
        event.control.page.update()
    
    def get_data(event): # asigna los datos ingresados a la funcion solve()
        x = sp.symbols('x')
        
        selection_option = int(select_options.value) 
        option_metodo_dx = int(select_metodo_dx.value)
        option_orden_dx = int(select_orden_dx.value)
        option_tipo_ec = int(select_tipo_ec.value)     
        
        if selection_option == 1: #Diferencia numerica      
            try:
                x=sp.symbols('x')
                
                # en la interfaz no se actualiza cuando se selecciona una opcion de los select
                
                funcion = validar_expresion(row.controls[2].value)
                h_value = float(row.controls[6].value)
                x_value = float(row.controls[7].value)
                nivel = row.controls[8].value
                nivel = None
                derivada = option_orden_dx
                direccion = option_metodo_dx
                ecuacion = option_tipo_ec
                            
                try:  
                    tabla, resultado, message, alert = resolver(funcion, derivada, direccion, ecuacion, h_value, x_value, nivel)
                    
                    if alert == True:
                        show_alert(event, message)
                    else: 
                        #Mostrar resultados
                        lbl_results.content = ft.Text(value=f'{message}', size=16, text_align=ft.TextAlign.CENTER)
                        lbl_results2.content = ft.Text(value=f'Valor aproximado: {resultado}', weight="bold", size=20, text_align=ft.TextAlign.CENTER)
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
                
        elif selection_option == 2: #Richardson
            try:
                x=sp.symbols('x')
                
                funcion = validar_expresion(row.controls[2].value)
                h_value = float(row.controls[6].value)
                x_value = float(row.controls[7].value)
                nivel = int(row.controls[8].value)
                derivada = option_orden_dx
                direccion = option_metodo_dx
                ecuacion = option_tipo_ec
                            
                try:  
                    tabla, resultado, message, alert = resolver(funcion, derivada, direccion, ecuacion, h_value, x_value, nivel)
                    
                    if alert == True:
                        show_alert(event, message)
                    else: 
                        #Mostrar resultados
                        tbl.content = tabla
                        tbl.visible = True
                        lbl_results.content = ft.Text(value=f'{message}', size=16, text_align=ft.TextAlign.CENTER)
                        lbl_results2.content = ft.Text(value=f'Valor aproximado: {resultado}', weight="bold", size=20, text_align=ft.TextAlign.CENTER)
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
            row.controls[0].value = 'Diferencia numerica'
            row.controls[2].visible = True
            row.controls[3].visible = True
            row.controls[4].visible = True
            row.controls[5].visible = True
            row.controls[6].visible = True
            row.controls[7].visible = True
            row.controls[8].visible = False
            row.controls[9].visible = True
            row.controls[10].visible = True
            clean(event)
            event.control.page.update()
            
        elif selection_option == 2:
            row.controls[0].value = 'Diferencia Richardson'
            row.controls[2].visible = True
            row.controls[3].visible = True
            row.controls[4].visible = True
            row.controls[5].visible = True
            row.controls[6].visible = True
            row.controls[7].visible = True
            row.controls[8].visible = True
            row.controls[9].visible = True
            row.controls[10].visible = True
            clean(event)
            event.control.page.update()
    
    def on_change_orden(event):
        option_orden_dx = event.control.value
        
    def on_change_metodo(event):
        option_metodo_dx = event.control.value
        
    def on_change_tipo(event):
        option_tipo_ec = event.control.value
        
        
    
    # Controles para que el usuario interactue
    select_options = ft.Dropdown(
        label='Opciones para derivar',
        on_change=update_inputs,
        height=60,
        options=[
            ft.dropdown.Option(text='Diferencia numerica', key=1, on_click=clean ),
            ft.dropdown.Option(text='Richardson', key=2, on_click=clean),
        ]
    )
    
    select_orden_dx = ft.Dropdown(
        label='Orden de la derivada',
        on_change=on_change_orden,
        height=60,
        options=[
            ft.dropdown.Option(text='Orden 1', key=1 ),
            ft.dropdown.Option(text='Orden 2', key=2),
            ft.dropdown.Option(text='Orden 3', key=3),
            ft.dropdown.Option(text='Orden 4', key=4),
        ]
    )
    
    select_metodo_dx = ft.Dropdown(
        label='Metodo para derivar',
        height=60,
        on_change=on_change_metodo,
        options=[
            ft.dropdown.Option(text='Hacia atras', key=1),
            ft.dropdown.Option(text='Hacia delante', key=2),
            ft.dropdown.Option(text='Central', key=3),
        ]
    )
    
    select_tipo_ec = ft.Dropdown(
        label='Tipo de ecuacion a utilizar',
        on_change=on_change_tipo,
        height=60,
        options=[
            ft.dropdown.Option(text='Tipo 1 (Normal)', key=1,),
            ft.dropdown.Option(text='Tipo 2 (Taylor)', key=2,),
        ]
    )
    
    row = ft.ResponsiveRow(
        [   
            ft.Text(
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
                visible=False,
                suffix=ft.IconButton(
                    icon=ft.icons.HELP_OUTLINE_OUTLINED, on_click=open_dlg_modal),
                col={"md": 3}),
            
            ft.Container(
                        select_metodo_dx,
                        visible=False,
                        col={"md": 3},
                    ),
            
            ft.Container(
                        select_orden_dx,
                        visible=False,
                        col={"md": 3},
                    ),
            
            ft.Container(
                        select_tipo_ec,
                        visible=False,
                        col={"md": 3},
                    ),
            
            ft.TextField(
                height=57,
                visible=False,
                label="Valor de h", 
                col={"md": 3}),
        
            
            ft.TextField(
                height=57,
                visible=False,
                label="Valor de x a evaluar", 
                col={"md": 3}),
            
            ft.TextField(
                height=57,
                visible=False,
                label="Nivel", 
                col={"md": 3}),
            
            ft.ElevatedButton(
                text="Resolver", 
                visible=False,
                on_click=get_data, 
                width=100, 
                height=45, col={"md":2}),
            
            ft.ElevatedButton(
                text="Limpiar", 
                visible=False,
                on_click=clean, 
                width=100, 
                height=45, col={"md":2}),
        ], 
        alignment=ft.MainAxisAlignment.CENTER,  
    )
    
    lbl_results2 = ft.Container()
    lbl_results = ft.Container()
    lbl_eval = ft.Container()
    
    
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
                            col={"sm": 10, "md": 10, "xl": 10},
                        ),                
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
