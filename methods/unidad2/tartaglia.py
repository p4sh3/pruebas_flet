import flet as ft
import sympy as sp
from sympy import *
from sympy.core.numbers import *
# from methods.unidad1.grafico import show as show_grafico
from methods.widgets.widgets import show_alert, open_dlg_modal
name = "Método de Tartaglia"


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

def solve(polinomio): # codigo del algoritmo
    x = sp.symbols('x')
    
    try:
        polinomio_poli=Poly(polinomio)
    except GeneratorsNeeded:
        #aqui se debe de detener el codigo, esto se le debe agragar a Tartaglia
        message = f"Error: La funcion ingresada no es una expresion simbolica valida"
        return message, None, True 
    
    polinomio_poli = Poly(polinomio)
    
    
    coeficientes = polinomio_poli.all_coeffs()
    
    if len(coeficientes) == 4:
        i = 0
        divisor=coeficientes[0]
        
        while i < len(coeficientes):
            coeficientes[i] = coeficientes[i]/divisor
            i = i+1
        a, b, c = coeficientes[1:]    
        p = (3*b - a**2)/3
        q = (2*a**3 - 9*a*b + 27*c)/27
        discriminante = (q/2)**2 + (p/3)**3
 
        if discriminante == 0:
            if p == 0 and q == 0:
                raiz =-(a/3)
               
                message = f'P: {p}\t\t\t\tQ: {q}\t\t\t\tDiscriminante: {discriminante}'
                messge2 = f'La ecuacion {polinomio} tiene 3 raices iguales\nRaiz Raiz 1: {raiz}\nRaiz 2: {raiz}\nRaiz 3: {raiz}'
              
                return message, message2, False
            else:
                raiz_1 = -((3*q)/(2*p)) - (a/3)
                raiz_2 = -(4*(p**2))/(9*q) - (a/3)
               
                message = f'P: {p}\t\t\t\tQ: {q}\t\t\t\tDiscriminante: {discriminante}'
                message2 = f'La ecuacion {polinomio} tiene 3 raices, 2 iguales  y 1 diferente\nRaiz 1: {raiz_1}\nRaiz 2: {raiz_1}\nRaiz 3: {raiz_2}'
                
                return message, message2, False
                
                
        elif discriminante > 0:
            raiz_real = real_root(cbrt(-(q/2) + sqrt(discriminante)) + cbrt(-(q/2) - sqrt(discriminante)) - (a/3)).evalf()
            u = real_root( cbrt(-(q/2) + sqrt(discriminante))).evalf(n=14)
            v = real_root(cbrt(-(q/2) - sqrt(discriminante))).evalf(n=14)
            raiz_imaginaria = (-(u + v)/2) - (a/3) 
            raiz_2imaginaria = ((sqrt(3)/2) * (u - v) * I).evalf()
                        
            message = f'P: {p}\t\t\t\tQ: {q}\t\t\t\tDiscriminante: {discriminante}\t\t\t\tU: {u}\t\t\t\tV: {u}'
            message2 =  f'La ecuación {polinomio} tiene 3 raices, 2 iguales imaginarias  y 1 real\nRaiz imaginarias 1: {raiz_imaginaria} +{raiz_2imaginaria}\nRaiz imaginarias 2: {raiz_imaginaria} -{raiz_2imaginaria}\nRaiz 3 real: {raiz_real}'
            
            return message, message2, False

        elif discriminante < 0: 
            arcocoseno = real_root(acos((-q/2)/(sqrt(-(p/3)**3)))).evalf()
            raiz1 = real_root(2*sqrt(-p/3)*cos((arcocoseno+2*0*pi)/3)-(a/3)).evalf()
            raiz2 = real_root(2*sqrt(-p/3)*cos((arcocoseno+2*1*pi)/3)-(a/3)).evalf()
            raiz3 = real_root(2*sqrt(-p/3)*cos((arcocoseno+2*2*pi)/3)-(a/3)).evalf()
       
            
            message = f'P: {p}\t\t\t\tQ: {q}\t\t\t\tDiscriminante: {discriminante}'
            message2 = f'La ecuacion {polinomio} tiene 3 raices reales\nRaiz Raiz 1: {raiz1}\nRaiz 2: {raiz2}\nRaiz 3: {raiz3}'
            return message, message2, False
    else :
        message = f"La ecuacion ingresada es de grado {len(coeficientes)-1} \npor lo tanto el metodo Tartaglia no puede dar una solucion."        
        
        return message, None, True
        
def show(): # Muestra los resultados 
    def clean(event):
        container_results.visible = False
        row.controls[1].value = ''
        
        row.controls[1].autofocus = True
        event.control.page.update()
    
    def get_data(event): # asigna los datos ingresados a la funcion solve()
        x = sp.symbols('x')
        
        try:
            x=sp.symbols('x')
            
            polinomio = validar_expresion(row.controls[1].value)
            
            es_poli = es_polinomio(polinomio)
            
            if es_poli:
                          
                try:  
                    message, message2, alert = solve(polinomio) 
                    
                    if alert == True:
                        show_alert(event, message)
                    else: 
                        #Mostrar resultados
                        lbl_results.content = ft.Text(value=f'{message}', size=16, text_align=ft.TextAlign.CENTER)
                        lbl_results2.content = ft.Text(value=f'{message2}', weight="bold", size=20, text_align=ft.TextAlign.CENTER)
                        lbl_results2.bgcolor = ft.colors.BLUE
                        lbl_results2.padding = 20
                        lbl_results2.border_radius = 20
                        container_results.visible=True
                        event.control.page.update()
                                    
                except ValueError as e:
                    print(f"Error: {e}")
                    show_alert(event, f'Ingrese una funcion valida {e}')    
            else: 
                show_alert(event, 'La expresion ingresda no es un polinomo\nPor favor ingrese un polinomio')   
    
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
                label="Polinomio", 
                autofocus=True,
                suffix=ft.IconButton(
                    icon=ft.icons.HELP_OUTLINE_OUTLINED, on_click=open_dlg_modal),
                col={"md": 3}),
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
                            col={"sm": 12, "md": 12, "xl": 8},
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
