import flet as ft
import sympy as sp
from sympy import *
from sympy.core.numbers import *
# from methods.unidad1.grafico import show as show_grafico
from methods.widgets.widgets import show_alert, open_dlg_modal, show_modal_alert
name = "Interpolación Lagrange"


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


def solve(fx, valores_x, valores_y, grade): # codigo del algoritmo
    x = sp.symbols('x')
    f_x = fx
    xv = valores_x
    yv = valores_y
    grado = grade
    
    if grado < 1 or grado >= len(xv):
    #aqui se detendria si pide un grado menor a 1 o un grado mayor/igual al numero de puntos que hay en tablas
        message = f"No es pisible calcular la interpolacion de Lagrange de grado {grado}"
        alert = True
        
        return None, None, message, alert
    #return polinomio, grado, message, alert
    y = 0
    if (len(xv) >= 2 and len(yv) >= 2) and f_x == "" :
        y = 0
        i = 0
        while i < grado+1 :
            agregar = 0
            o = 0
            agregar = agregar + yv[i]

            while o < grado+1:
                if i != o:
                    posible_div0 = (((x - xv[o])/(xv[i] - xv[o])))
                    if posible_div0.is_real == False:
                        message = f"Se genero division entre 0 al calcular el polinomio De Lagrange\n"
                        alert = True
        
                        return None, None, message, alert
                    
                    agregar = agregar*(((x-xv[o])/(xv[i]-xv[o])))
                    
                o = o + 1  
            y = y + agregar      
            i = i + 1
        polinomio = sp.expand(y)
     
        return polinomio, grado, None, False
       
    elif f_x != "" and len(xv) >= 2:

        i = 0
        while i < grado + 1:
            evaluar=f_x.subs({x:xv[i]}).evalf()
            if evaluar.is_real == False:
                message = f"Al evaluar la funcion {f_x} se evaluo un punto fuera de su dominio\n"
                alert = True
        
                return None, None, message, alert
            
            yv.append(f_x.subs({x:xv[i]}).evalf())  
            i = i + 1
        y = 0
        i = 0
        while i < grado + 1 :
            agregar = 0
            o = 0
            agregar = agregar+yv[i]

            while o < grado + 1:
                if i != o:
                    agregar = agregar*(((x - xv[o])/(xv[i] - xv[o])))
                    
                o = o + 1  
            y = y + agregar      
            i = i + 1
        polinomio = sp.expand(y)
     
        return polinomio, grado, None, False
    
    else:
        if  len(xv) >= 2 and f_x == "" and len(yv) == 0:
            message = f"No hay funcion para crear la tabla f(x)"
            alert = True
        
            return None, None, message, alert
            
        elif (len(xv) < 2 or len(yv) < 2) and f_x == "":
            message = f"La tabla de valores x o f(x) no cuenta con los valores necesarios"
            alert = True
        
            return None, None, message, alert
        elif f_x != "" and len(xv) == 0:
            message = f"La tabla de valores x no cuenta con datos"
            alert = True
        
            return None, None, message, alert
        
        
    

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
        lbl_results3.controls[0].value = ''
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
                
                fx = validar_expresion(row.controls[2].value)
                x = row.controls[3].value
                valores_y = row.controls[4].value
                grade = int(row.controls[5].value)
                valores_xstr = x.split(',')
                valores_x = [float(valor.strip()) for valor in valores_xstr]
                valores_y = []
                            
                try:  
                    polinomio, grado, message, alert = solve(fx, valores_x, valores_y, grade)
                    
                    if alert == True:
                        show_alert(event, message)
                    else: 
                        #Mostrar resultados
                        lbl_results.content = ft.Text(value=f'Polinomio interpolacion Lagangre\t\t Grado: {grado}', size=16, text_align=ft.TextAlign.CENTER)
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
                
        if selection_option == 2:
            try:
                x=sp.symbols('x')
                
                fx = row.controls[2].value
                fx = ''
                x = row.controls[3].value
                y = row.controls[4].value
                grade = int(row.controls[5].value)
                valores_xstr = x.split(',')
                valores_x = [float(valor.strip()) for valor in valores_xstr]
                valores_ystr = y.split(',')
                valores_y = [float(valor.strip()) for valor in valores_ystr]
                            
                try:  
                    polinomio, grado, message, alert = solve(fx, valores_x, valores_y, grade)
                    
                    if alert == True:
                        show_alert(event, message)
                    else: 
                        #Mostrar resultados
                        lbl_results.content = ft.Text(value=f'Polinomio interpolacion Lagangre\t\t Grado: {grado}', size=16, text_align=ft.TextAlign.CENTER)
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
        
    
    def update_inputs(event): # Activa o desactiva los inputs
        selection_option = int(select_options.value)
        
        if selection_option == 1:
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
            
        elif selection_option == 2:
            row.controls[2].visible = False
            row.controls[3].visible = True
            row.controls[4].visible = True
            row.controls[5].visible = True
            row.controls[6].visible = True
            row.controls[7].visible = True
            row.controls[3].col = {"md": 3}
            row.controls[4].col = {"md": 3}
            clean(event)
            event.control.page.update()
                 
    # Controles para que el usuario interactue
    select_options = ft.Dropdown(
        label='Opciones para resolver',
        on_change = update_inputs,
        height=60,
        options=[
            ft.dropdown.Option(text='Funcion y valores en x', key=1, on_click=clean ),
            ft.dropdown.Option(text='Tabla de valores x, y', key=2, on_click=clean),
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
                label="Grado", 
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
