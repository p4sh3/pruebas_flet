import flet as ft
import sympy as sp
from sympy import *
from sympy.core.numbers import *
# from methods.unidad1.grafico import show as show_grafico
from methods.widgets.widgets import show_alert, open_dlg_modal, show_modal_alert
name = "Metodo Hermite"


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


def solve(fx, vx, vy, derivadas): # codigo del algoritmo
    
    x = sp.symbols('x')
    
    def f(valor):
        return fx.subs(valor, x).evalf()
    
    def Polinomio(coeficientes):
        #Productos para el polinomio:
        lista_Productos = [x-lista_zk[0]]
        for i in range(1,len(lista_zk)):
            lista_Productos.append((x - lista_zk[i])*lista_Productos[i-1])
       
        
        #Polinomio encontrado:
        polinomio = f"{coeficientes[0]}"
        for i in range(len(coeficientes)-1):
            polinomio += f" + {coeficientes[i+1]}*({lista_Productos[i]})"
           
        #Polinomio resuelto:
        polinomio_Resuelto = sp.Poly(polinomio)
        return polinomio_Resuelto

    
    def Hermite(k, zk, fk, n):
        calculos = [k, zk, fk]
        nivel = 1

        while nivel < n:
            lista_n = calculos[nivel+1]
            auxiliar = []
            for i in range(len(lista_n)-1):
                if (zk[i+nivel]-zk[i]) == 0:
                    derivada_buscar = fk[i+nivel]
                    filtro_sublistas_y = lambda sublista: sublista[0] == derivada_buscar
                    sublista_y_de_x = list(filter(filtro_sublistas_y, vy))
                    derivada_Zk =  sublista_y_de_x[0][nivel] / sp.factorial(nivel)
                    auxiliar.append(float(derivada_Zk))

                else:
                    auxiliar.append(float((lista_n[i+1]-lista_n[i])/(zk[i+nivel]-zk[i])))

            calculos += [auxiliar]
            nivel += 1
        return calculos

    
    # Validar función, valores x, valores y, derivadas y cantidad de datos
    
    if fx is not None and not (fx.free_symbols == {x} and isinstance(fx, (sp.Eq, sp.Poly, sp.Expr))):
        message = 'Ingrese una función en terminos de x.'
        
        return None, None, message, True
    
    elif vx is None or not all(isinstance(vxi, (int,float)) and not isinstance(vxi, bool) for vxi in vx):
        message = 'Los valores de x deben ser números reales.'
        
        return None, None, message, True
    
    elif vy is not None and not all(isinstance(sublista, list) and len(sublista)>0 for sublista in vy):
        message = 'Ingrese los valores de y en listas'
        
        return None, None, message, True
    
    elif vy is not None and not all(isinstance(elemento, (int, float)) and not isinstance(elemento, bool) for sublista in vy for elemento in sublista):
        message = 'Los valores de y deben ser números reales.'
        
        return None, None, message, True
    
    elif derivadas is not None and not (isinstance(derivadas, int) and not isinstance(derivadas, bool) and derivadas>0):
        message = 'Derivadas debe ser un entero mayor a 0.'
        
        return None, None, message, True
    
    elif vx is not None and vy is not None and len(vx) != len(vy):
        message = 'Asigne un valor de x con almenos un valor de y.'
        
        return None, None, message, True
    
    # Evaluar si cumple las condiciones para el tipo de ejercicio
    
    if vx is not None and vy is not None and fx is None and derivadas is None:#Sin función:
        """Asumimos que no falta ordenarlo"""
        pass
    
    elif vx is not None and vy is None and fx is not None and derivadas is not None:#Con función:
         #valores y, y', y'' etc
        vy = [[] for valor in vx]
        # print("Valores f(x):")
        for i in range(len(vx)):
            resultado_fx = fx. subs(x, vx[i])
            vy[i].append(resultado_fx)
            # print(f"x{i} = {resultado_fx}")
        for n in range(1, derivadas+1): # Derivadas desde la primera hasta dx
            derivada_n = sp.diff(fx, x, n)
            # print(f"\nDerivada{n}: {derivada_n}")
            for i in range(len(vx)):
                valor_derivada = derivada_n.subs(x, vx[i])
                vy[i].append(valor_derivada)
                # print(f"x{i} = {vx[i]}: {valor_derivada}")
    
    else: 
        message =  'ERROR. Ingrese valores de x, una función y hasta que derivada evaluar, o ingrese valores de x con sus valores de y.'
        
        return None, None, message, True
    
    # Mostramos las lista de los valores con los que trabajaremos
    # print(f"\nValores x: {vx}\nValores y: {vy}\n")
    
    # Crear los puntos
    lista_Puntos = []
    for i in range(len(vx)):
        for j in vy[i]:
            lista_Puntos.append((vx[i], j))
    # print("\nPuntos obtenidos: ", lista_Puntos)
    
    # Crear zk, fk
    n = len(lista_Puntos)
    k = [i for i in range(n)]
    lista_zk = [i[0] for i in lista_Puntos]
    lista_fk = []
    for sublista in vy:
        lista_fk.extend([sublista[0]] * len(sublista))
    # print(f"k : {k}\nZk: {lista_zk}\nFk: {lista_fk}")
    
    #Enviar zk y fk a funcion Hermite
    resultados = Hermite(k, lista_zk, lista_fk, n)
    coeficientes = [i[0] for i in resultados[2:]]
    polinomio_Obtenido = Polinomio(coeficientes)
    
    # print("\nCálculos obtenidos: \n")
    for i in range(len(resultados)):
        if len(resultados[i]) < len(resultados[0]):
            diferencia = len(resultados[0]) - len(resultados[i])
            #print(diferencia)
            resultados[i] = ["-"]*diferencia + resultados[i]        
    
    table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Iteraciones")),
                ft.DataColumn(ft.Text("X")),
                ft.DataColumn(ft.Text("F(x)")),
            ] + [ft.DataColumn(ft.Text(f'Nivel {i}')) for i in range(1, len(resultados) - 2)],
            rows=[
                ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell))) for cell in fila])
                for fila in zip(*resultados)
            ]
    )
    
    tabla = ft.Row([ft.Container(padding=20, content=ft.Row([table]))], scroll=ft.ScrollMode.ALWAYS)
    
    poli = polinomio_Obtenido.as_expr()
   
    return tabla, poli, None, False

def show(): # Muestra los resultados 
      
    def clean(event):
        container_results.visible = False
        row.controls[2].value = ''
        row.controls[3].value = ''
        row.controls[4].value = ''
        row.controls[5].value = ''        
        row.controls[2].autofocus = True
        lbl_results3.controls[0].value = ''
        tbl.visible = False
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
                # fx, vx, vy, derivadas
                fx = validar_expresion(row.controls[2].value)
                x = row.controls[3].value
                vy = row.controls[4].value
                derivadas = int(row.controls[5].value)
                valores_xstr = x.split(',')
                vx = [float(valor.strip()) for valor in valores_xstr]
                vy = None
                            
                try:  
                    tabla, polinomio, message, alert = solve(fx, vx, vy, derivadas)
                    
                    if alert == True:
                        show_alert(event, message)
                    else: 
                        #Mostrar resultados
                        tbl.content = tabla
                        tbl.visible = True
                        lbl_results.content = ft.Text(value=f'{name}', size=16, text_align=ft.TextAlign.CENTER)
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
                # x = sp.symbols('x')
                [-1,-2],[0,10,40]
                fx = row.controls[2].value
                fx = None
                x_values = row.controls[3].value
                y = str(row.controls[4].value)
                derivadas = None
                
                try:
                    y_values = [row.split(",") for row in y.split("#")]
                    vy = [[float(elemento) for elemento in sublista] for sublista in y_values]
                    
                except Exception as e:
                    vy=None
                    show_alert(event, 'Error al ingresar valores de y\nExpresion permitida para valores de y: \ny1, y1\',y1\'\'#y2, y2\', y2\'\'\nDonde # hace la division entre listas de datos')
                
                # try:
                #     vy = eval(y)
                # except Exception as e:
                #     show_alert(event, 'Error al ingresar valores de y\nForma permitida: [ [y1, y1\',y1\'\'], [y2, y2\', y2\'\'] ]')
                
                
                valores_xstr = x_values.split(',')
                vx = [float(valor.strip()) for valor in valores_xstr]
                
                            
                try:  
                    tabla, polinomio, message, alert = solve(fx, vx, vy, derivadas)
                    
                    if alert == True:
                        show_alert(event, message)
                    else: 
                        #Mostrar resultados
                        tbl.content = tabla
                        tbl.visible = True
                        lbl_results.content = ft.Text(value=f'{name}', size=16, text_align=ft.TextAlign.CENTER)
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
            row.controls[5].visible = False
            row.controls[6].visible = True
            row.controls[7].visible = True
            row.controls[3].col = {"md": 4 }
            row.controls[4].col = {"md": 4}
            clean(event)
            show_modal_alert(event, 'Expresion permitida para valores de y: \ny1, y1\',y1\'\'#y2, y2\', y2\'\'\nDonde # hace la division entre listas de datos')
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
                label="Orden de la derivada", 
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
