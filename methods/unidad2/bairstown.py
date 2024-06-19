import flet as ft
import sympy as sp
from sympy import *
from sympy.core.numbers import *
from methods.widgets.widgets import show_alert, open_dlg_modal
name = "Método Bairstown"


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

def es_polinomio(expr):
    try:
        # Obtener los términos de la expresión
        terminos = expr.as_ordered_terms()
        
        # Verificar cada término
        for termino in terminos:
            # Un término es un monomio si es del tipo constante * variable**exponente
            if not termino.is_Mul and not termino.is_Pow and not termino.is_Number:
                return False
            
            if termino.is_Mul:
                # Verificar cada factor del término
                for factor in termino.args:
                    if factor.is_Pow:
                        base, exponente = factor.args
                        if not (base.is_Symbol and exponente.is_Integer and exponente >= 0):
                            return False
                    elif factor.is_Symbol or factor.is_Number:
                        continue
                    else:
                        return False
            elif termino.is_Pow:
                base, exponente = termino.args
                if not (base.is_Symbol and exponente.is_Integer and exponente >= 0):
                    return False
            elif termino.is_Symbol:
                continue
            elif termino.is_Number:
                continue
            else:
                return False
        
        return True
    except (sp.SympifyError, TypeError):
        return False


def solve(expresion, r, s, cifras): # codigo del algoritmo
    rows = []
    x = sp.Symbol('x')
    
     # Función para extrae los coeficientes de la función incluyendo los nulos
    def extraer_coeficientes(fx):
        
        # Convertir la expresión a un polinomio
        polinomio = sp.Poly(fx, x)
        
        # Obtener los coeficientes del polinomio
        coeficientes = polinomio.all_coeffs()
        
        # Invertir el orden de los coeficientes para que estén en orden ascendente
        coeficientes_ascendente = coeficientes[::-1]
        
        return coeficientes_ascendente
    
    # Redondear un número complejo
    def round_complex(num_complejo, decimales):
        # numero_complejo = complex(numero_complejo)
        # numero_complejo = complex(round(numero_complejo.real, decimales), round(numero_complejo.imag, decimales))
        # return numero_complejo

        # Numero complejo de sympy
        num_complejo = sp.sympify(num_complejo)
        parte_real = round(num_complejo.as_real_imag()[0], decimales)
        parte_imaginaria = round(num_complejo.as_real_imag()[1], decimales)
        return sp.sympify(f'{parte_real} + {parte_imaginaria}*I')
    
    # Función método de Bairstown
    def Bairstow(fx, Es, r, s, contador):
        
        # Inicializamos EaR y EaS
        Ea_R = 0 # Error aproximado de R
        Ea_S = 0 # Error aproximado de S
        
        a = extraer_coeficientes(fx)
        b = []
        c = []
        #print("Coefcientes obtenidos An:", a)
        
        n = len(a) - 1
        #n = Grado de la ecuación1, n + 1 = Cantidad de Coeficientes
        
        #Crear Listas de Coeficientes B y C. C0 no se tomará en cuenta.
        for i in range(0, len(a), 1):
            b.append(0)
            c.append(0)
        #print("Listas: ", a, b, c)#Prueba de listas Inicializadas
        """Inicializamos listas para que corresponda el coeficiente con su
        posición en el arreglo en vez de añadirlos uno a uno a la inversa
        con .append, así las ecuaciones son más intuitivas al programarlas"""
        
        # Ahora si el método de Bairstow
        j = 0#Iterador auxiliar
        while (Ea_R > Es and Ea_S > Es) or j == 0:
            
            j += 1
            
            #Calculamos los valodres de los coeficientes Bn y Cn:
            for i in range(n, -1, -1):
                if i == n:
                    b[i] = a[n] #Bn = An 
                    c[i] = b[n] #Cn = Bn
                elif i == (n - 1):
                    b[i] = a[n-1] + (r * b[n]) #B(n-1) = A(n-1) + r*Bn
                    c[i] = b[n-1] + (r * c[n]) #C(n-1) = B(n-1) + r*Cn
                else:
                    b[i] = a[i] + (r * b[i+1]) + (s * b[i+2]) #Bi = Ai + r*B(i+1) + s*B(i+2)
                    c[i] = b[i] + (r * c[i+1]) + (s * c[i+2]) #Ci = Bi + r*C(i+1) + s*C(i+2)
           
            #Calculamos Delta R y Delta S:
            delta_R = ((c[3] * b[0]) - (c[2] * b[1])) / ((c[2]**2) - (c[1] * c[3]))
            delta_S = ((c[1] * b[1]) - (c[2] * b[0])) / ((c[2]**2) - (c[1] * c[3]))

            delta_R = float(delta_R)
            delta_S = float(delta_S)
            
            #Calcular nuevos valores de R y S
            r += delta_R
            s += delta_S
            
            #Calcular error aproximado de R y S
            Ea_R = abs(delta_R / r) * 100
            Ea_S = abs(delta_S / s) * 100
            
            # Añadir a pandas y tabla
            if contador == 1:
                
                rows.append(ft.DataRow(
                            cells=[ft.DataCell(ft.Text(str(cell))) for cell in [j, r, s, delta_R, delta_S, Ea_R, Ea_S]],
                        ))
            else:
                pass
            
            # df.loc[j-1] = [j, r, s, delta_R, delta_S, Ea_R, Ea_S]
            
            # Parada por si no converge
            if j == 100: 
                message = "¡Nivel máximo de iteraciones alcanzado!. Puede que r y s inicial no sean optimos o válidos."
                
                return None, None, message, True
        
        #Calculamos x1 y x2 una vez cumplimos la condición
        x1 = (r + (r**2 + (4*s))**(1/2)) / 2
        x2 = (r - (r**2 + (4*s))**(1/2)) / 2
        
        list_datos = [x1, x2],[r, s]
        
        return list_datos, rows
    
    # Definir la variable simbólica
    x = sp.symbols('x')
    
    # Validar datos
    try:
        fx = sp.sympify(expresion)
    except (sp.SympifyError, AttributeError, TypeError, NameError, SyntaxError) as e:
        message = f'La expresión no es valida. Revise: {fx}'
        
        return None, None, message, True
    
    # Validar datos
    if not (fx is not None and isinstance(fx, (sp.Eq, sp.Poly, sp.Expr)) and fx.free_symbols == {x} and sp.Poly(fx, x).degree()>2):
        # La función no tiene el formato deseado
        message = 'La expresión no puede estar vacía, debe ser únicamente en términos de x y de grado 3 o mayor.'
        
        return None, None, message, True
    
    elif not (cifras is not None and isinstance(cifras, (int, float)) and not isinstance(cifras, bool)):
        # Cifras es None no no tiene el formato deseado
        message = 'La cantidad de cifras significativas debe ser un entero positivo.'
        
        return None, None, message, True
     
    elif not (r is not None and (isinstance(r, (int,float)) and not isinstance(r, bool))):
        # r no cumple con el formato esperado
        message = 'Ingrese valor r0. Debe ser un número.'
        
        return None, None, message, True

    elif not (s is not None and (isinstance(s, (int,float)) and not isinstance(s, bool))):
        # s no cumple con el formato esperado
        message = 'Ingrese valor s0. Debe ser un número.'
        
        return None, None, message, True
    
    # Resolver:
    
    tolerancia = (0.5*(10**(2 - cifras)))#Es
    raices = []# Aquí se guardarán las raíces de Bairstow
    funciones = [fx]# Aquí las funciones a evaluar
    
    # Tabla de pandas    
    
    contador = 0
    while True:
        contador+=1
        
        # Evaluamos la función anterior
        if sp.Poly(funciones[-1], x).degree()>2:
            
            # Enviamos la ultima función a Bairstow si es de grado 3 o más
            resultados, rows = Bairstow(funciones[-1], tolerancia, r, s, contador)
            
            # Añadimos las raíces encontradas
            raices.append(resultados[0][0])
            raices.append(resultados[0][1])
            
            #Cambiamos valores de r y s
            r = resultados[1][0]
            s = resultados[1][1]
            
            #Imprimir la tabla de iteraciones
            
        #Grado 2 o 1
        else:
            # Despeje directo
            soluciones_restantes = sp.solve(funciones[-1], x)
            for raiz in soluciones_restantes:
                raices.append(raiz)
            
            # Fin algoritmo todas las fueron encontradas
            break
        
        #Evaluar si ya hemos resuelto el problema
        
        if len(raices) == sp.Poly(fx, x).degree():
            
            # Fin algoritmo, todas las raíces fueron encontradas
            break
        
        else:
            # Obtenemos en nuevo polinomio con división sintética
            nuevo_poly = sp.div(funciones[-1],(x - raices[-1])*(x - raices[-2]))
            funciones.append(nuevo_poly[0] + nuevo_poly[1])
    
    diccionario_soluciones = {}
   
    i = 1
    for valor in raices:
        if isinstance(valor, (int, float, sp.Integer, sp.Float)):
            redondeo_valor = round(float(valor),cifras)
        
        else:
            redondeo_valor = round_complex(valor, cifras)
        
        if redondeo_valor not in diccionario_soluciones.values():
            #print("No se repite la raíz.")
            diccionario_soluciones[f"x{i}"] = redondeo_valor
            i+=1
        else: 
            pass
    

    return  rows, diccionario_soluciones, None, False
          
 
def show(): # Muestra los resultados 
    def clean(event):
        container_results.visible = False
        table.visible = False
        row.controls[1].value = ''
        row.controls[2].value = ''
        row.controls[3].value = ''      
        row.controls[4].value = ''     
        row.controls[1].autofocus = True
        event.control.page.update()
    
    def get_data(event): # asigna los datos ingresados a la funcion solve()
        x = sp.symbols('x')
    
        try:
            x=sp.symbols('x')
            
            expresion = validar_expresion(row.controls[1].value)
            r = float(row.controls[2].value)
            s = float(row.controls[3].value)
            cifras = int(row.controls[4].value)
            
            es_poli = es_polinomio(expresion)
            
            if es_poli == True:

                rows, raices, message, alert = solve(expresion, r, s, cifras)
                
                if cifras > 0:
                    if alert == True:
                        show_alert(event, message)
                    else:                
                        try:
                            table.rows = rows
                            table.visible = True
                                
                            #Mostrar resultados
                            lbl_root.content = ft.Text(value=f'Raices encontradas: {raices}', weight="bold", size=20, text_align=ft.TextAlign.CENTER)
                            lbl_root.bgcolor = ft.colors.GREEN
                            lbl_root.padding = 10
                            lbl_root.border_radius = 10
                            lbl_results.value = f'{name}'
                            lbl_results.text_align = ft.TextAlign.CENTER
                            container_results.visible=True
                            event.control.page.update()
                                
                        except ValueError as e:
                                    print(f"Error: {e}")
                                    show_alert(event, f'Ingrese una funcion valida {e}')
                else:

                    show_alert(event, 'Las cifras significativas deben ser mayor a cero')
            else:
                show_alert(event, 'La expresion ingresda no es un polinomo\nPor favor ingrese un polinomio')
                
    
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
                label="Polinomio", 
                autofocus=True,
                suffix=ft.IconButton(
                    icon=ft.icons.HELP_OUTLINE_OUTLINED, on_click=open_dlg_modal),
                col={"md": 3}),
            
            ft.TextField(
                label="Valor de r",
                col={"md": 3}),
            
            ft.TextField(
                label="Valor de s", 
                col={"md": 3}),
            
            ft.TextField(
                label="Cifras significativas", 
                col={"md": 3}),
            
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

    # Tabla de flet que almacena los resuultados del algoritmo
    table = ft.DataTable(
        columns=[ft.DataColumn(ft.Text(col)) for col in ["Iteración", "r", "s", "delta_R", "delta_S", "Ea R", "Ea S"]],
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
                            col={"sm": 12, "md": 10, "xl": 10},
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
