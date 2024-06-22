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
    
    if len(coeficientes) == 5:
        i = 0
        divisor = coeficientes[0]
        
        while i<len(coeficientes):
            coeficientes[i]=coeficientes[i]/divisor
            i=i+1
                
        a, b, c, d = coeficientes[1:]
        
        p = (8*b - 3*a**2)/8
        q = (8*c - 4*a*b + a**3)/8
        r = (256*d - 64*a*c +16*(a**2)*b - 3*a**4)/256
        
        coeficientes_nuevos = 1,-(p/2),-(r),(4*p*r-q**2)/8
    
        a2, b2, c2 = coeficientes_nuevos[1:]
        p2 = (3*b2 - a2**2)/3
        q2 = (2*a2**3-9*a2*b2+27*c2)/27
        discriminante = (q2/2)**2 + (p2/3)**3

        if discriminante == 0:
            if p2 == 0 and q2 == 0:
                raiz=-(a2/3)
                print("La raiz es(triple):",raiz)
                uf=raiz
            else:
                raiz_1 = -((3*q2)/(2*p2)) - (a2/3)
                raiz_2 = -(4*(p2**2))/(9*q2) - (a2/3)
                uf = raiz_1
        elif discriminante > 0: 
            raiz_real = real_root(cbrt(-(q2/2) + sqrt(discriminante)) + cbrt(-(q2/2) - sqrt(discriminante)) - (a2/3)).evalf()
            u = real_root(cbrt(-(q2/2) + sqrt(discriminante))).evalf(n=14)
            v = real_root(cbrt(-(q2/2) - sqrt(discriminante))).evalf(n=14)
            raiz_imaginaria = (-(u + v)/2) - (a/3) 
            raiz_2imaginaria = ((sqrt(3)/2) * (u - v) * I).evalf()
            uf =raiz_real
        elif discriminante<0: 
            k = 0
            arcocoseno = real_root(acos((-q/2)/(sqrt(-(p/3)**3)))).evalf()
            raiz1=real_root(2*sqrt(-p/3)*cos((arcocoseno+2*0*pi)/3)-(a/3))
            uf = raiz1
     
        v2 = sqrt((2*uf)-p) 
        w = -(q/(2*v2)) 
        x_1 = ((v2 + sqrt((v2**2) - 4*(uf - w)))/2) - a/4
        x_2 = ((v2 - sqrt((v2**2) - 4*(uf - w)))/2) - a/4
        x_3 = ((-v2 + sqrt((v2**2) - 4*(uf + w)))/2) -a/4
        x_4 = ((-v2 - sqrt((v2**2) - 4*(uf + w)))/2)-a/4
        
        message = f'P: {p}\t\t\t\t Q: {q}\t\t\t\t R: {r}\t\t\t\t V: {v2}\t\t\t\t W: {w}\t\t\t\t U: {uf}'
        message2 = f'Raices encontradas:\nRaiz 1: {x_1}\nRaiz 2: {x_2}\nRaiz 3: {x_3}\nRaiz 4: {x_4}'
        return message, message2, False
    else :
        message = f"La ecuacion ingresada es de grado {len(coeficientes)-1} \npor lo tanto el metodo Ferrari no puede dar una solucion."     

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
