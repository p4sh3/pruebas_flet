import flet as ft
import sympy as sp
from sympy import *
from sympy.core.numbers import *
# from methods.unidad1.grafico import show as show_grafico
from methods.widgets.widgets import show_alert, open_dlg_modal
name = "Cuadratica"


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


def solve(polinomio): # codigo del algoritmo
    x = sp.symbols('x')
    try:
        polinomio_polu=Poly(polinomio)
    except GeneratorsNeeded:
        #aqui se debe de detener el codigo, esto se le debe agragar a Tartaglia
        message = f"Error: La funcion ingresada no es una expresion simbolica valida"
        return message, None, True 
        
    coeficientes=polinomio_polu.all_coeffs()
    if len(coeficientes)==3:
        i=0
        a, b, c = coeficientes[:]    
       
        raiz1= (-(b) + (sqrt((b**2) - 4*(a*c))) ) / (2*a).evalf()
        # raiz2=((-(b) - sqrt(((b)**2)-4*a*c))/2*a).evalf()
        raiz2 = (-(b) - (sqrt((b**2) - 4*(a*c))) ) / (2*a).evalf()
        message = f'a: {a}\t\t\t\tb: {b}\t\t\t\tc: {c}'
        message2 = f'La ecuacion {polinomio} tiene dos raices\nRaiz 1: {raiz1}\nRaiz 2: {raiz2}'
        
        return message, message2, False
    else :
        message = f"La ecuacion ingresada es de grado {len(coeficientes)-1} \npor lo tanto el metodo cuadratico no puede dar una solucion."
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
                label="Polinomio grado 2", 
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
