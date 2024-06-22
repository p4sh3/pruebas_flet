import flet as ft
import sympy as sp
from sympy import *
from sympy.core.numbers import *
# from methods.unidad1.grafico import show as show_grafico
from methods.widgets.widgets import show_alert, open_dlg_modal
name = "Método de Horner"


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

def solve(polinomio, punto0, cifras): # codigo del algoritmo
    rows = []
    x = sp.Symbol('x')
    f_x = polinomio
    Es = 0.5 * 10 ** (2 - cifras)
    x0 = punto0
    try:
        polinomio_polu=Poly(f_x)
    except GeneratorsNeeded:
        #aqui se debe de detener el codigo, esto se le debe agragar a Tartaglia
        message = f"Error: La funcion ingresada no es una expresion simbolica valida"
        alert = True
        return None, None, None, None, alert, message

    coeficientes=polinomio_polu.all_coeffs()
    coeficientes1=[]
    coeficientes2=[]
    
    iteracion = 0
    if len(coeficientes) > 3:
        while True:
            iteracion = iteracion + 1
            i = 0
            while i < len(coeficientes):
                if i == 0:
                    coeficientes1.append((coeficientes[i]).evalf())
                else:
                    coeficientes1.append((coeficientes[i] + coeficientes1[i-1]*x0).evalf()) 
                i = i + 1        
            i = 0
            while i < len(coeficientes1)-1:
                if i == 0:
                    coeficientes2.append((coeficientes1[i]).evalf())
                else:
                    coeficientes2.append((coeficientes1[i]+coeficientes2[i-1]*x0).evalf()) 
                i = i + 1 
            r = coeficientes1[len(coeficientes1)-1]       
            s = coeficientes2[len(coeficientes2)-1]  
        
            xi =(x0-(r/s)).evalf()
            if xi.is_real==False:
                    message = f"Se genero division entre cero al calcular el Xi, en la iteracion {iteracion}"
                    alert = True
                    return None, None, None, None, alert, message
                
            Ea = abs((xi-x0)/xi)*100
            
            rows.append(ft.DataRow(
                    cells=[ft.DataCell(ft.Text(str(cell))) for cell in [iteracion, x0, xi, Ea]],
            ))
            
            if Ea < Es or iteracion == 100:      
                break
            else:
                x0 = xi
                coeficientes1.clear()
                coeficientes2.clear()
    else:
        message = f"Por favor ingrese una ecuacion de grado mayor o igual a 3"
        alert = True
        return None, None, None, None, alert, message
    
    return rows, iteracion, xi, Ea, False, None
            
 
def show(): # Muestra los resultados 
    def clean(event):
        container_results.visible = False
        table.visible = False
        row.controls[1].value = ''
        row.controls[2].value = ''
        row.controls[3].value = ''
        row.controls[1].autofocus = True
        event.control.page.update()
    
    def get_data(event): # asigna los datos ingresados a la funcion solve()
        x = sp.symbols('x')
        try:
            x=sp.symbols('x')
            
            polinomio = validar_expresion(row.controls[1].value)
            punto0 = float(row.controls[2].value)
            cifras = int(row.controls[3].value)
            
            es_poli = es_polinomio(polinomio)
            
            if es_poli:
            
                if cifras > 0:
                    try:
                        rows, iteracion, xi, Ea, alert, message = solve(polinomio, punto0, cifras)
                    
                        if alert == True:
                            show_alert(event, message)
                        else:                
                            rows, iteracion, xi, Ea, alert, message = solve(polinomio, punto0, cifras)
                            table.rows = rows
                            table.visible = True
                                        
                            #Mostrar resultados
                            lbl_root.content = ft.Text(value=f'Solucion: {xi}', weight="bold", size=20, text_align=ft.TextAlign.CENTER)
                            lbl_root.bgcolor = ft.colors.GREEN
                            lbl_root.padding = 10
                            lbl_root.border_radius = 10
                            lbl_results.value = f'{name}\nf(x) {polinomio}\nCon {iteracion} iteraciones\nError porcentual aproximado {Ea}%'
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
                label="Funcion", 
                autofocus=True,
                suffix=ft.IconButton(
                    icon=ft.icons.HELP_OUTLINE_OUTLINED, on_click=open_dlg_modal),
                col={"md": 4}),
            ft.TextField(
                label="Punto 1",
                col={"md": 4}),
          
            ft.TextField(
                label="Cifras Significativas", 
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
        columns=[ft.DataColumn(ft.Text(col)) for col in ["Iteracion","x0","xi", "Error Aproximado"]],
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
