import flet as ft
import sympy as sp
from sympy import *
from sympy.core.numbers import *
# from methods.unidad1.grafico import show as show_grafico
from methods.widgets.widgets import show_alert, open_dlg_modal
name = "Método de Newton Raphson"


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


def solve(fx, punto, cifras): # codigo del algoritmo
    rows = []
    x = sp.Symbol('x')
    
    metodo = 'Newton Raphson'
    Es = 0.5 * 10 ** (2 - cifras)
 
    xi = punto
    iteracion = 1
    aprox_anterior = 0
    aprox_actual = 0
    
    #Criterio de convergencia
    fx_prima = fx.diff(x)
    fx2_prima = fx_prima.diff(x)
    print(fx_prima)
    print(fx2_prima)
    
    fxi= fx.subs(x, xi).evalf()
    
    fxi_prima = fx_prima.subs(x, xi).evalf()
    fxi2_prima = fx2_prima.subs(x, xi).evalf()
    
    convergencia=Abs((fxi*fxi2_prima)/((fxi_prima)**2))
    comprobacion=True
    
    if im(fxi) != 0 or isinstance(fxi,ComplexInfinity):
        comprobacion=False
        return rows, xi1, fx, None, metodo, iteracion, True, f"El punto inicial sale del dominio de la función {fx}"
         
    elif im(fxi_prima)!= 0 or isinstance(fxi_prima,ComplexInfinity):
        comprobacion=False
        return rows, xi1, fx, None, metodo, iteracion, True, f"El punto inicial sale del dominio de la derivada 1 {fx_prima} "
        
    elif im(fxi2_prima) != 0 or isinstance(fxi2_prima,ComplexInfinity):
        comprobacion=False
        return rows, xi1, fx, None, metodo, iteracion, True, f"El punto inicial sale del dominio de la derivada 2 {fx} "
    
    elif isinstance(convergencia,ComplexInfinity) or isinstance(convergencia,NaN):
        comprobacion=False
        return rows, xi1, fx, Ea, metodo, iteracion, True, f"Se genero una division entre cero al calcular la convergencia "
   
    else:

        print(comprobacion)    
        print(convergencia)
        print(type(convergencia))
        
        if convergencia < 1 :
            while True: 
                fxi= fx.subs(x, xi).evalf()
                
                if im(fxi)!=0 or isinstance(fxi,ComplexInfinity):
                    return rows, xi1, fx, None, metodo, iteracion, True, f"El punto inicial sale del dominio de la función {fx} "
                
                #calculo de la derivada
                fx_prima = fx.diff(x)
                
                #Se evalua el valor actual de xi en la primera derivada
                fxi_prima= fx_prima.subs(x,xi).evalf()
                
                if im(fxi_prima)!=0 or isinstance(fxi_prima,ComplexInfinity):
                    return rows, xi1, fx, None, metodo, iteracion, True, f"El punto inicial sale del dominio de la derivada {fx_prima} "
                
                #calculo para encontrar la raiz aproximada
                xi1 = (xi - (fxi/fxi_prima))
                
                if  isinstance(xi1,ComplexInfinity):
                    return rows, xi1, fx, None, metodo, iteracion, True, f"Al calcular la xi siguiente se genero una division entre cero "
                
                Ea = Abs(((xi1 - aprox_anterior)/xi1)*100).evalf()
                
                if  isinstance(Ea,ComplexInfinity) or isinstance(Ea,NaN):
                    return rows, xi1, fx, Ea, metodo, iteracion, True, f"Al calcular la Ea se genero una division entre cero "
            
                rows.append(ft.DataRow(
                        cells=[ft.DataCell(ft.Text(str(cell))) for cell in [iteracion, xi, fxi, fxi_prima, xi1, Ea]],
                    ))
            
                if Ea < Es or iteracion == 100:
                    break
                else:
                    xi = xi1
                
                aprox_anterior = xi1
                iteracion += 1
            
            return rows, xi1, fx, Ea, metodo, iteracion, False, 'Se completo con exito' 
        
        else:
            if convergencia >= 1:
                return rows, xi1, fx, None, metodo, iteracion, True, "El criterio de convergencia no se cumplio" 
        
    


          
 
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
        
        # def comprobar_imaginarios(expr):
        #     return sp.im(expr) > 0
        
        try:
            x=sp.symbols('x')
            
            fx = validar_expresion(row.controls[1].value)
            punto = float(row.controls[2].value)
            cifras = int(row.controls[3].value)

            rows, xi1, fx, Ea, metodo, iteracion, alert, messege = solve(fx, punto, cifras)
            
            if cifras > 0:
                if alert == True:
                    show_alert(event, messege)
                    table.rows = rows
                    table.visible = True
                            
                    #Mostrar resultados
                    lbl_root.content = ft.Text(value=f'Solucion: {xi1}', weight="bold", size=20, text_align=ft.TextAlign.CENTER)
                    lbl_root.bgcolor = ft.colors.GREEN
                    lbl_root.padding = 10
                    lbl_root.border_radius = 10
                    lbl_results.value = f'Metodo: {metodo}\nf(x) {fx}\nCon {iteracion} iteraciones\nError porcentual aproximado {Ea}%'
                    container_results.visible=True
                    event.control.page.update()
                else:                
                    try:
  
                        rows, xi1, fx, Ea, metodo, iteracion, alert, messege = solve(fx, punto, cifras)
                        table.rows = rows
                        table.visible = True
                            
                         #Mostrar resultados
                        lbl_root.content = ft.Text(value=f'Solucion: {xi1}', weight="bold", size=20, text_align=ft.TextAlign.CENTER)
                        lbl_root.bgcolor = ft.colors.GREEN
                        lbl_root.padding = 10
                        lbl_root.border_radius = 10
                        lbl_results.value = f'Metodo: {metodo}\nf(x) {fx}\nCon {iteracion} iteraciones\nError porcentual aproximado {Ea}%'
                        container_results.visible=True
                        event.control.page.update()
                            
                    except ValueError as e:
                                print(f"Error: {e}")
                                show_alert(event, f'Ingrese una funcion valida {e}')
            else:

                show_alert(event, 'Las cifras significativas deben ser mayor a cero')
                
    
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
                label="Funcion", 
                autofocus=True,
                suffix=ft.IconButton(
                    icon=ft.icons.HELP_OUTLINE_OUTLINED, on_click=open_dlg_modal),
                col={"md": 4}),
            
            ft.TextField(
                label="Punto",
                col={"md": 4}),
            
            ft.TextField(
                label="Cifras Significativas", 
                col={"md": 4}),
            
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
        columns=[ft.DataColumn(ft.Text(col)) for col in ["Iteracion", " Xi", "f(Xi)", "f'(Xi)", "Xi+1", "Error Aproximado"]],
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
