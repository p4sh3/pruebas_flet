import flet as ft
import sympy as sp
from sympy import *
from sympy.core.numbers import *
# from methods.unidad1.grafico import show as show_grafico
from methods.widgets.widgets import show_alert, open_dlg_modal, show_modal_alert
name = "Diferencia Numerica"


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


def resolver(funcion_str, variables_str, limites_str, metodo_str, intervalos_str, error=None): # codigo del algoritmo
    
    fx = funcion_str
    metodo = metodo_str
    
    try:
        
        def f(valor):
            #print("Función: ", funcion, "\nValor: ", valor)
            return funcion.subs(variable,valor)
            
        def ValidarVariables():
            abecedario = 'abcdfghijklmnopqrstuvwxyz'
            #print(abecedario)

            if variables_str is None or not type(variables_str)==list:
                message = 'Ingrese las variables a usar, ejemplo: [x,y,z]'
                return message, True
            
            elif not all(type(variable)==str and len(variable)==1 for variable in variables_str):
                message = 'Las variables deben se letras del abecedario, ejemplo: [x,y,z].'
                return message, True
            
            elif not all((variable.lower() in abecedario) for variable in variables_str):
                message = f'Las variables deben se letras del abecedario(Excepto la e, se tomará como número de euler).'
                return message, True
            
            else:
                variables = set()
                for variable in variables_str:
                    if type(variable) is str and len(variable)==1:
                        variables.add(sp.sympify(variable.lower()))
                
                if len(variables_str) != len(variables):
                    message = 'Ingrese una lista de variables sin repetición. Se integrará en ese orden.'
                    return message, True
                
                elif not (fx.free_symbols == variables):
                    #print(fx.free_symbols)
                    message = 'La función debe tener las variables ingresadas. Se integrará en ese orden.'
                    return message, True
            
            return variables_str, False
        
        def ValidarLimites():
            
            if limites_str is None or not isinstance(limites_str, list):
                message = 'Ingrese limites válidos para cada variable. Ejemplo: [[2,4],[0,1]]'
                return message, True
            
            elif not all((type(limite)==list and len(limite)==2) for limite in limites_str):
                message = 'Cada limite debe tener 2 valores numéricos [a,b]. Ejemplo: [[2,4],[0,1]]'
                return message, True
            
            elif not all((isinstance(limite[0], (int,float)) and isinstance(limite[1], (int,float))) for limite in limites_str):
                message = 'Cada limite debe tener 2 valores numéricos [a,b]. Ejemplo: [[2,4],[0,1]]'
                return message, True
            
            #Simpificamos los limites
            nuevos_limites=[]
            for limite in limites_str:
                nuevos_limites.append([sp.sympify(limite[0]),sp.sympify(limite[1])])
            
            if not len(nuevos_limites) == len(variables):
                message = 'No se ingrasaron los limites correspondientes de cada variable.'
                return message, True
            
            elif not all((limite[0]<limite[1]) for limite in nuevos_limites):
                message = 'Para cada limite [a,b] debe ser a < b. Ejemplo: [[2,4],[0,1]]'
                return message, True
            
            return nuevos_limites, False
        
        def ValidarIntervalos():
            
            if metodo == 'Simpson 1/3 Simple' or metodo == 'Simpson 3/8 Simple' or metodo == 'Trapecio Simple' or metodo == 'Simpson Adaptativo':
                return None, None
                
            else:#Simpson Compuesto(Con intervalos)

                if intervalos_str == None:
                    message = f'El método {metodo} requiere de intervalos.'
                    return message, True
                
                if not (intervalos_str>0):
                    message = 'Ingrese un intervalo válido. Debe ser un entero positivo.'
                    return message, True
                
                else: 
                    return intervalos_str, False
        
        def ResolverIntegral(a, b, n=None):
            
            #Simple y Compuesto, 1/3, 3/8
            #Trapecio Simple y Compuesto
            
            if metodo == 'Simpson 1/3 Simple' or metodo == 'Simpson Adaptativo':
                
                fxm = f(a+(b-a)/2)
                resultado = (b-a)*(f(a) + 4*fxm + f(b))/6
            
            elif metodo == 'Simpson 1/3 Compuesto':
                
                fxi = []
                fxm = []
                h = (b-a)/n
                
                # Valores fxi
                for i in range(0,n+1,1):
                    fxi.append(f(a+i*h))
                    #print(a+i*h)
                #print(fxi)
                
                # Valores fxm
                for i in range(1,n*2,2):
                    fxm.append(f(a+(i*h)/2))
                    #print(a+(i*h)/2)
                #print(fxm)
                
                resultado = (b-a)*(fxi[0] + 4*sum(fxm) + 2*sum(fxi[1:-1]) + fxi[-1])/(6*n)
            
            elif metodo == 'Simpson 3/8 Simple':
                h = (b-a)/3
                
                fx0 = f(a)
                fx1 = f(a+h)
                fx2 = f(a+2*h)
                fx3 = f(b)
                resultado = (b-a)*(fx0 + 3*fx1 + 3*fx2 + fx3)/8
            
            elif metodo == 'Simpson 3/8 Compuesto':
                
                fxi = []
                fxm = []
                h = (b-a)/n
                subh = h/3
                
                # Valores fxi
                for i in range(0,n+1,1):
                    fxi.append((f(a+i*h)))
                    #print(a+i*h)
                #print(fxi)
                
                # Valores fxm
                for i in range(0,n,1):
                    fxm.append(f(a+i*h+subh))
                    fxm.append(f(a+i*h+2*subh))
                    #print(a+i*h+subh)
                    #print(a+i*h+2*subh)
                #print(fxm)
                
                resultado = (b-a)*(fxi[0] + 3*sum(fxm) + 2*sum(fxi[1:-1]) + fxi[-1])/(8*n)
            
            elif metodo == 'Trapecio Simple':
                
                resultado = (b - a)*(f(a) + f(b)) / 2
                
            elif metodo == 'Trapecio Compuesto':
                
                h = (b-a)/n
                fxi = []
                
                for i in range(n+1):
                    fxi.append(f(a+i*h))
                    #print(f(a+i*h))
                #print(fxi)
                
                resultado = (h/2)*(fxi[0] + 2*sum(fxi[1:-1]) + fxi[-1])
                
            elif metodo == 'Cuadratura Gaussiana':
                print(metodo_str)
                if n < 2 or n > 5:
                    message = 'Intervalos fuera de limite(2-5). '
                    
                    return message, True

                zi = [[0.5773502691896257, -0.5773502691896257],
                        [0.7745966692414834,0.0,-0.7745966692414834],
                        [0.8611363115940526,0.3399810435848563,-0.3399810435848563,-0.8611363115940526],
                        [-0.9061798459386640,-0.5384693101056831,0.0,0.5384693101056831,0.9061798459386640]]

                wi = [[1.0,1.0],
                        [0.5555555555555556,0.8888888888888888,0.5555555555555556],
                        [0.3478548451374539,0.6521451548625461,0.6521451548625461,0.3478548451374539],
                        [0.2369268850561891,0.4786286704993665,0.5688888888888889,0.4786286704993665,0.2369268850561891]]

                evaluaciones = []
                                
                for i in range(n):
                    evaluaciones.append(wi[n-2][i]*f(((b-a)/2)*zi[n-2][i]+((a+b)/2)))

                resultado = ((b-a)/2) * sum(evaluaciones)

            
            else:
                message = 'Método inválido.'
                return message, True
            
            # Devolvemos el número o la expresión si es múltiple
            if resultado.is_real:
                return float(resultado)
                
            else:
                return resultado
        
        def Integral_Adaptativa(a, b, error, Raiz):
            I1 = ResolverIntegral(a, b)
            I2 = ResolverIntegral(a, (a + b) / 2)
            I3 = ResolverIntegral((a + b) / 2, b) 
            #print(f"S{I1} --> \tS{I2}\tS{I3}")
            # print(f"[{a}, {b}] =\t[{a}, {(a + b) / 2}]\t[{(a + b) / 2}, {b}]")
            
            Ea = abs(I1 - I2 - I3)
            
            if Ea < 15 * error:
                return I2 + I3 + (I2 + I3 - I1) / 15
            
            else:
                nodo_izquierda = Integral_Adaptativa(a, (a + b) / 2, error / 2, I2)
                nodo_derecha = Integral_Adaptativa((a + b) / 2, b, error / 2, I3)
                return nodo_izquierda + nodo_derecha
            
        # def Validar_Error():
            
        #     if not (isinstance(error, (int,float)) and not isinstance(error,(bool))):
        #         message = 'El error debe ser un número.'
        
               
            
        #     elif not (error > 0 and error<1):
        #         message = 'El error debe ser valores entre 0 y 1.'    
            
        #     return message, True
            
        
        # Validación de datos
        
        variables, error_msg = ValidarVariables()
        
        if error_msg == True:
            message = variables
            return None, message, True
        
    
        limites, error_msg = ValidarLimites()
        
        if error_msg == True:
            message = limites
            return None, message, True
        
        
        intervalos, error_msg = ValidarIntervalos()   
        if error_msg == True:
            message = intervalos
            return None, message, True
        
        if metodo == "Simpson Adaptativo":
            
            x = sp.symbols('x')
            
            # # message, alert = Validar_Error()
            
            # if alert:
            #     return None, message, alert
            
            funcion = fx
            variable = 'x'
            
            if funcion.free_symbols == {x}:
                a = limites[0][0]
                b = limites[0][1]
                # Integral Adaptativa(a, b, error)
                solucion_final = Integral_Adaptativa(a, b, error, ResolverIntegral(a,b))
                
                message = f"funcion = {funcion}\na = {a}\nb = {b}\ne = {error}\nEl resultado de la integración adaptativa de Simpson es: {solucion_final}"
                
                return solucion_final, message, False
            
            else:
                message ='Este metodo solo permite expresiones en términos de x.'
                
                return None, message, True
            
           
            
            
        else: 
            funciones = [fx]
            
            message = ''
            
            for i in range(0,len(variables),1):
                variable = variables[i]
                funcion = funciones[i]
                funciones.append(ResolverIntegral(limites[i][0], limites[i][1], intervalos))
                message += f'\n{i+1}° Integral. Evaluada respecto a {variables[i]}:\nResultado: {funciones[-1]}'
                solucion_final = funciones[-1]
                
            return solucion_final, message, False
    
    except sp.SympifyError:
        message = "Error: No se pudo convertir una de las expresiones a una expresión SymPy válida."
        
        return None, message, True
        
    except ZeroDivisionError:
        message = "Error: Intento de división por cero."
        
        return None, message, True
        
    except TypeError as e:
        message = f"Error de tipo: {e}"
        
        return None, message, True
        
    except ValueError as e:
        message = f"Error de valor: {e}"
        
        return None, message, True
        
    except AttributeError as e:
        message = f"Error de atributo: {e}"
        
        return None, message, True
        
    except Exception as e:
        message = f"Ocurrió un error inesperado: {e}"
        
        return None, message, True
    
   

def show(): # Muestra los resultados 
      
    def clean(event):
        container_results.visible = False
        row.controls[2].value = ''
        row.controls[3].value = '' 
        row.controls[4].value = ''       
        row.controls[5].value = '' 
        row.controls[2].autofocus = True
        event.control.page.update()
    
    def get_data(event): # asigna los datos ingresados a la funcion solve()
        x = sp.symbols('x')
        
        selection_option = int(select_options.value)      
        
        if (selection_option == 1) or (selection_option == 3) or (selection_option == 5) or (selection_option == 8): #Diferencia numerica      
            try:
                x=sp.symbols('x')
                
                funcion_str = validar_expresion(row.controls[2].value)
                
                variables = row.controls[3].value
                variables_str = [(valor.strip()) for valor in variables.split(',')]
                
                limites = row.controls[4].value
                intervalos_str = row.controls[5].value
                intervalos_str = None
                
                
                try:
                    if '#' in limites:
                        limites_integrar = [row.split(",") for row in limites.split("#")]
                        limites_str = [[float(elemento) for elemento in sublista] for sublista in limites_integrar]
                    else: 
                        limites_str = [[float(valor.strip()) for valor in limites.split(',')]]
                        
                except Exception as e:
                    show_alert(event, f'Se ingresaron de manera incorrecta los valores de limites\n{limites_str}')
                
                
                if selection_option == 1:
                    metodo_str = 'Simpson 1/3 Simple'
                    error = None
                elif selection_option == 3:
                    metodo_str = 'Simpson 3/8 Simple'
                    error = None
                elif selection_option == 5:
                    metodo_str = 'Trapecio Simple'
                    error = None
                elif selection_option == 8:
                    error = float(row.controls[6].value)
                    metodo_str = 'Simpson Adaptativo'
                if error == None or (error < 1 and error > 0):
                    try:  
                        resultado, message, alert = resolver(funcion_str, variables_str, limites_str, metodo_str, intervalos_str, error)
                        
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
                else: 
                    show_alert(event, 'El valor de error a ingresar debe ser entre 0 y 1')  
        
            except ValueError as e:
                print(f"Error: {e}")
                show_alert(event, f'{e}') # me muestra errores si el usuario ingresa caracteres en los textfield 
    
        elif (selection_option == 2) or (selection_option == 4) or (selection_option == 6) or (selection_option == 7): #compuestos, cuadratura gausiana   
            try:
                x=sp.symbols('x')
                
                funcion_str = validar_expresion(row.controls[2].value)
                
                variables = row.controls[3].value
                variables_str = [(valor.strip()) for valor in variables.split(',')]
        
                limites = row.controls[4].value
                intervalos_str = int(row.controls[5].value)
                
                try:
                    limites_integrar = [row.split(",") for row in limites.split("#")]
                    limites_str = [[float(elemento) for elemento in sublista] for sublista in limites_integrar]
                    
                except Exception as e:
                    show_alert(event, 'Se ingresaron de manera incorrecta los valores de limites')
                
                if selection_option == 2:
                    metodo_str = 'Simpson 1/3 Compuesto'
                elif selection_option == 4:
                    metodo_str = 'Simpson 3/8 Compuesto'
                elif selection_option == 6:
                    metodo_str = 'Trapecio Compuesto'
                elif selection_option == 7:
                    metodo_str = 'Cuadratura Gaussiana'

                print(metodo_str)
                
                try:  
                    resultado, message, alert = resolver(funcion_str, variables_str, limites_str, metodo_str, intervalos_str)
                    
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
        
        
    
    
    def update_inputs(event): # Activa o desactiva los inputs
        selection_option = int(select_options.value)
        
        if selection_option == 1:
            row.controls[0].value = 'Simpson 1/3 Simple'
            row.controls[2].visible = True
            row.controls[3].visible = True
            row.controls[4].visible = True
            row.controls[5].visible = False
            row.controls[6].visible = False
            row.controls[7].visible = True
            row.controls[8].visible = True
            row.controls[3].col = {"md": 3}
            row.controls[2].col = {"md": 3}
            clean(event)
            event.control.page.update()
            
        elif selection_option == 2:
            row.controls[0].value = 'Simpson 1/3 Compuesto'
            row.controls[2].visible = True
            row.controls[3].visible = True
            row.controls[4].visible = True
            row.controls[5].visible = True
            row.controls[6].visible = False
            row.controls[7].visible = True
            row.controls[8].visible = True
            row.controls[3].col = {"md": 2}
            row.controls[5].col = {"md": 2}
            row.controls[2].col = {"md": 2}
            clean(event)
            event.control.page.update()
            
        elif selection_option == 3:
            row.controls[0].value = 'Simpson 3/8 Simple'
            row.controls[2].visible = True
            row.controls[3].visible = True
            row.controls[4].visible = True
            row.controls[5].visible = False
            row.controls[6].visible = False
            row.controls[7].visible = True
            row.controls[8].visible = True
            row.controls[3].col = {"md": 3}
            row.controls[2].col = {"md": 3}
            clean(event)
            event.control.page.update()
        
        elif selection_option == 4:
            row.controls[0].value = 'Simpson 3/8 Compuesto'
            row.controls[2].visible = True
            row.controls[3].visible = True
            row.controls[4].visible = True
            row.controls[5].visible = True
            row.controls[6].visible = False
            row.controls[7].visible = True
            row.controls[8].visible = True
            row.controls[3].col = {"md": 2}
            row.controls[5].col = {"md": 2}
            row.controls[2].col = {"md": 2}
            clean(event)
            event.control.page.update()
        
        elif selection_option == 5:
            row.controls[0].value = 'Trapecio Simple'
            row.controls[2].visible = True
            row.controls[3].visible = True
            row.controls[4].visible = True
            row.controls[5].visible = False
            row.controls[6].visible = False
            row.controls[7].visible = True
            row.controls[8].visible = True
            row.controls[3].col = {"md": 3}
            row.controls[2].col = {"md": 3}
            clean(event)
            event.control.page.update()
            
        elif selection_option == 6:
            row.controls[0].value = 'Trapecio Compuesto'
            row.controls[2].visible = True
            row.controls[3].visible = True
            row.controls[4].visible = True
            row.controls[5].visible = True
            row.controls[6].visible = False
            row.controls[7].visible = True
            row.controls[8].visible = True
            row.controls[3].col = {"md": 2}
            row.controls[5].col = {"md": 2}
            row.controls[2].col = {"md": 2}
            clean(event)
            event.control.page.update()
            
        elif selection_option == 7:
            row.controls[0].value = 'Cuadratura Gaussiana'
            row.controls[2].visible = True
            row.controls[3].visible = True
            row.controls[4].visible = True
            row.controls[5].visible = True
            row.controls[6].visible = False
            row.controls[7].visible = True
            row.controls[8].visible = True
            row.controls[3].col = {"md": 2}
            row.controls[5].col = {"md": 2}
            row.controls[2].col = {"md": 2}
            clean(event)
            event.control.page.update()
        
        elif selection_option == 8:
            row.controls[0].value = 'Simpson Adaptativo'
            row.controls[2].visible = True
            row.controls[3].visible = True
            row.controls[4].visible = True
            row.controls[5].visible = False
            row.controls[7].visible = True
            row.controls[8].visible = True
            row.controls[6].visible = True
            row.controls[3].col = {"md": 2}
            row.controls[6].col = {"md": 2}
            row.controls[2].col = {"md": 2}
            clean(event)
            event.control.page.update()
    
    # Controles para que el usuario interactue
    select_options = ft.Dropdown(
        label='Opciones para integrar',
        on_change=update_inputs,
        height=60,
        options=[
            ft.dropdown.Option(text='Simpson 1/3 Simple', key=1, on_click=clean ),
            ft.dropdown.Option(text='Simpson 1/3 Compuesto', key=2, on_click=clean),
            ft.dropdown.Option(text='Simpson 3/8 Simple', key=3, on_click=clean),
            ft.dropdown.Option(text='Simpson 3/8 Compuesto', key=4, on_click=clean),
            ft.dropdown.Option(text='Trapecio Simple', key=5, on_click=clean),
            ft.dropdown.Option(text='Trapecio Compuesto', key=6, on_click=clean),
            ft.dropdown.Option(text='Cuadratura Gaussiana', key=7, on_click=clean),
            ft.dropdown.Option(text='Simpson Adaptativo', key=8, on_click=clean),
        ]
    )
    
    
    #(funcion, variables, limites, metodo, intervalos)
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
            
            ft.TextField(
                height=57,
                visible=False,
                label="Variables", 
                col={"md": 3}),
        
            
            ft.TextField(
                height=57,
                visible=False,
                label="Limites", 
                col={"md": 3}),
            
            ft.TextField(
                height=57,
                visible=False,
                label="Intervalos", 
                col={"md": 3}),
            
            ft.TextField(
                height=57,
                visible=False,
                label="Error", 
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
