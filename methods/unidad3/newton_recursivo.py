import flet as ft
import sympy as sp
from sympy import *
from sympy.core.numbers import *
# from methods.unidad1.grafico import show as show_grafico
from methods.widgets.widgets import show_alert, open_dlg_modal, show_modal_alert
name = "Newton Recursivo"


def validar_expresion(expr):
    x = sp.Symbol('x')
    symbolos_permitidos = {x}
    try: 
        exp = sp.sympify(expr)
    except (sp.SympifyError, SyntaxError):
        raise ValueError('La funcion no es valida')
    # Obtener todos los símbolos en la expresión
    symbolos_en_expr = exp.free_symbols
    
    # Verificar que todos los símbolos estén permitidos
    if not symbolos_en_expr.issubset(symbolos_permitidos):
        raise ValueError("La expresión contiene símbolos no permitidos")
    else: 
        return sp.parse_expr(expr)


def solve(fx, valores_x, valores_y, valor_eval): # codigo del algoritmo
    
    def recursivo(x_values, y_values, flag):

        if len(x_values) == 2:
            resultado = (y_values[0] - y_values[1])/(x_values[0] - x_values[1])

            if not flag is None:
                b_valores.append(resultado)
      
            return resultado

        lado_izq = recursivo(x_values[:-1], y_values[:-1], None)
        lado_der = recursivo(x_values[1:], y_values[1:], flag)
        resultado = (lado_izq - lado_der)/(x_values[0] - x_values[-1])

        if flag in x_values:
            b_valores.append(resultado)

        return resultado

    def valores_repetidos(lista):
        return len(lista) != len(set(lista))
    
    
    x = sp.symbols('x')
    f_x = fx
    valores = valores_x
    valoresf_x = valores_y
    x_evaluar = valor_eval
    
    if valores_repetidos(valores):
        message = "En la tabla de valores de X se encuentran valores repetidos" 
          
        return None, message, True
    
    elif valores_repetidos(valoresf_x):
        message = "En la tabla de valores de Y se encuentran valores repetidos" 
        
        return None, message, True

    b_valores=[]
    
    if len(valores) >= 2 and len(valoresf_x) >= 2 and f_x == "" and len(valoresf_x) == len(valores):
        polinomio = 0
        x_evaluar = ''
        b_valores.append(N((valoresf_x[0])).evalf())
        resultado = recursivo(valores[::-1], valoresf_x[::-1], valores[0])  
        
        o = 0
        binomios = 1
        
        while o < len(valores):
            if o > 0:
                binomios=binomios*(x-(valores[o-1]))   
            polinomio=polinomio+b_valores[o]*binomios   
            o = o + 1
        
        poli = sp.expand(polinomio)
        
        return poli, None, False
        # print("El polinomio es:\n",sp.expand(polinomio))
           
        # va = polinomio.subs(x,x_evaluar)
        # print(f"Evaluando el punto {x_evaluar} en el polinomio resultante\np({x_evaluar})={va}")
        
    elif f_x != "" and len(valores) >= 2 and len(valoresf_x) == 0 and len(valoresf_x) == 0: 
        
        polinomio = 0
        i = 0
        
        while i < len(valores):
            posible_fue_dom = f_x.subs(x,valores[i]).evalf()
            
            if not posible_fue_dom.is_real:
                message = f"Error, la funcion se evaluo fuera de su dominio\n"
                
                return None, message, True
            
            valoresf_x.append(f_x.subs(x,valores[i]).evalf())
            
            i = i + 1 
            
        i = 0
        b_valores.append(N((valoresf_x[0])).evalf())
        resultado = recursivo(valores[::-1], valoresf_x[::-1], valores[0])         
        o = 0
        binomios = 1
        
        while o < len(valores):
            if o > 0:
                binomios = binomios*(x-(valores[o-1]))   
            polinomio = polinomio+b_valores[o]*binomios   
            o = o + 1
            
        poli = sp.expand(polinomio)
        # print("El polinomio es:\n",sp.expand(polinomio))
       
        vv = f_x.subs(x,x_evaluar).evalf() 
        
        if vv.is_real == False:
            message = f"Error, la funcion se evaluo fuera de su dominio\nAl calcular el valor verdadero"
            
            return None, message, True
        
        va = polinomio.subs(x,x_evaluar).evalf()
        
        if va.is_real == False:
            message = f"Error, la funcion se evaluo fuera de su dominio\nAl calcular el valor aproximado"
            
            return None, message, True
        
        ep = abs((vv-va)/vv)*100
        
        if ep.is_real==False:
            message = f"Error, division entre 0 \nAl calcular el error porcentual"
            
            return None, message, True
        
        i = 0
        derivadas = f_x
        while i < len(valores):
            derivadas = diff(derivadas)
            i = i + 1
            
        errort = (derivadas/factorial(len(valores)))*binomios 
        et = errort.subs(x,x_evaluar)
        
        if vv.is_real==False:
            message = f"Error, la funcion se evaluo fuera de su dominio\nAl calcular teorico"
            
            return None, message, True
            
        # print("et=",et)  
        
        message = f'Valor verdadero: {vv} \t\t\t\t  Valor aproximado: {va}\nError aproximado: {ep}%\t\t\t\t Error teorico: {et}'
        
        return poli, message, False
           
    else:
        if f_x=="" and len(valoresf_x)!=len(valores):
            message = "Los valores de las tablas no tienen el mismo tamaño"
            
            return None, message, True
            
        elif f_x=="" and (len(valores)<2 or len(valoresf_x)<2):   
            message = "las tablas cuentan con datos insuficientes"
            
            return None, message, True
            
        elif len(valoresf_x)==0 and f_x!="" and len(valores)<2:
            message = f"las tablas de valores x cuenta con datos insuficientes"
            
            return None, message, True
  

def show(): # Muestra los resultados 
      
    def clean(event):
        container_results.visible = False
        row.controls[2].value = ''
        row.controls[3].value = ''
        row.controls[4].value = ''
        row.controls[5].value = ''        
        row.controls[2].autofocus = True
        lbl_results3.controls[0].value = ''
        lbl_eval.visible = False
        event.control.page.update()
    
    def get_data(event): # asigna los datos ingresados a la funcion solve()
        x = sp.symbols('x')
        
        #Limpia los datos del valor a evaluar en el polinomio
        lbl_results3.controls[0].value = row.controls[5].value
        lbl_eval.visible = False
        
        
        def evaluar(event):
            x = sp.symbols('x')
            try:
                num_evaluar = float(lbl_results3.controls[0].value)
                poli_eval  = polinomio.subs(x, num_evaluar)
                lbl_eval.content = ft.Text(f'Polinomio evaluado en X = {num_evaluar}: \nP({num_evaluar}) = {poli_eval}', weight="bold", size=20, text_align = ft.TextAlign.CENTER )
                # lbl_results3.controls[2].size = 16
                # lbl_results3.controls[2].text_align = ft.TextAlign.CENTER 
                lbl_eval.bgcolor = ft.colors.GREEN
                lbl_eval.border_radius = 10
                lbl_eval.padding = 10
                lbl_eval.visible = True
                event.control.page.update()
            except ValueError:
                show_alert(event, 'Por favor, ingrese un número real')
            
        selection_option = int(select_options.value)
        
        if selection_option == 1:
            try:
                x=sp.symbols('x')
                fx = row.controls[2].value
                fx = ''
                x = row.controls[3].value
                y = row.controls[4].value
                valor_eval = row.controls[5].value
                valores_xstr = x.split(',')
                valores_x = [float(valor.strip()) for valor in valores_xstr]
                valores_ystr = y.split(',')
                valores_y = [float(valor.strip()) for valor in valores_ystr]
                            
                try:  
                    polinomio, message, alert = solve(fx, valores_x, valores_y, valor_eval)
                    
                    if alert == True:
                        show_alert(event, message)
                    else: 
                        #Mostrar resultados
                        lbl_results.content = ft.Text(value=f'Polinomio {name}', size=16, text_align=ft.TextAlign.CENTER)
                        lbl_results2.content = ft.Text(value=f'P(x) = {polinomio}', weight="bold", size=20, text_align=ft.TextAlign.CENTER)
                        lbl_results2.bgcolor = ft.colors.BLUE
                        lbl_results2.padding = 10
                        lbl_results2.border_radius = 10
                        lbl_results3.controls[1].on_click = evaluar
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
                
                fx = validar_expresion(row.controls[2].value)
          
                x = row.controls[3].value
                valores_y = row.controls[4].value
                valor_eval = int(row.controls[5].value)
                valores_xstr = x.split(',')
                valores_x = [float(valor.strip()) for valor in valores_xstr]
                valores_y = []
                
                validacion_i = fx.subs(x, valor_eval)
                if validacion_i.is_real == False:
                    show_alert(event, 'La funcion genera numeros imaginarios')
                            
                try:  
                    polinomio, message, alert = solve(fx, valores_x, valores_y, valor_eval)
                    
                    if alert == True:
                        show_alert(event, message)
                    else: 
                        #Mostrar resultados
                        lbl_results.content = ft.Text(value=f'Polinomio {name}\n{message}', size=16, text_align=ft.TextAlign.CENTER)
                        lbl_results2.content = ft.Text(value=f'P(x) = {polinomio}', weight="bold", size=20, text_align=ft.TextAlign.CENTER)
                        lbl_results2.bgcolor = ft.colors.BLUE
                        lbl_results2.padding = 10
                        lbl_results2.border_radius = 10
                        lbl_results3.controls[1].on_click = evaluar
                        container_results.visible = True
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
            row.controls[2].visible = False
            row.controls[3].visible = True
            row.controls[4].visible = True
            row.controls[5].visible = False
            row.controls[6].visible = True
            row.controls[7].visible = True
            row.controls[3].col = {"md": 4}
            row.controls[4].col = {"md": 4}
            clean(event)
            event.control.page.update()
            
        elif selection_option == 2:
            row.controls[2].visible = True
            row.controls[3].visible = True
            row.controls[4].visible = False
            row.controls[5].visible = True
            row.controls[6].visible = True
            row.controls[7].visible = True
            row.controls[2].col = {"md": 3}
            row.controls[3].col = {"md": 3}
            clean(event)
            show_modal_alert(event, 'Ingrese valores separados por coma 1, 2, 3, o 1.000, 2.2222, 3.9999')
            event.control.page.update()
                 
    # Controles para que el usuario interactue
    select_options = ft.Dropdown(
        label='Opciones para resolver',
        on_change = update_inputs,
        height=60,
        options=[
            ft.dropdown.Option(text='Tabla de valores x, y', key=1, on_click=clean ),
            ft.dropdown.Option(text='Funcion y valores en x', key=2, on_click=clean),
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
                        col={"md": 4},
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
            
            ft.TextField(
                height=57,
                visible = False,
                label="Valor a evaluar", 
                col={"md": 2}),
            
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
    lbl_eval = ft.Container()
    
    lbl_results3 = ft.ResponsiveRow(
        [
        ft.TextField(
            label='Valor a evaluar',
            value = row.controls[5].value,
            col={"sm": 10, "md": 10, "xl": 4}  
        ),
        ft.ElevatedButton(
            text = 'Evaluar',
            height=45,
            col={"sm": 10, "md": 10, "xl": 2}
        ),
        ft.Container(
            lbl_eval,
            col={"sm": 10, "md": 8, "xl": 8}
        )
        
        
        ], alignment=ft.MainAxisAlignment.CENTER,  
        # ft.Container(
        #     lbl_results3,
        #     col={"sm": 10, "md": 10, "xl": 10},
        # ),
        
    )
    
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
                        ft.Text(
                            value=('Evaluar un valor de X en el polinomo resultante'), 
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(
                            lbl_results3,
                            col={"sm": 12, "md": 12, "xl": 12},
                        ),
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
