import flet as ft
import sympy as sp
from sympy import *
from sympy.core.numbers import *
# from methods.unidad1.grafico import show as show_grafico
from methods.widgets.widgets import show_alert, open_dlg_modal, show_modal_alert
name = "Trazadores cubicos"


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


def resolver(fx, valores_x, valores_y, grade, eval_x, selection_option): # codigo del algoritmo
    x = sp.symbols('x')
    f_x = fx
    x_valores = valores_x
    y_valores = valores_y
    numero_intervalos=len(x_valores)-1
    grado = grade
    x_evaluar = eval_x
    
    def esta_ordenada(lista):
        return all(ab <= bc for ab, bc in zip(lista, lista[1:]))

    def list_seccionada( listafinal, intervalos):
        i=0
        solucion = []
        while i<len(listafinal):
            seccion = listafinal[i],intervalos[i]
            solucion.append(seccion)
            i=i+1
        return solucion
    
    def valores_repetidos(lista):
        return len(lista) != len(set(lista))

    if valores_repetidos(x_valores):
        message = "En la tabla de valores de X se encuentran valores repetidos" 
        return None, None, None, message, True

    if not esta_ordenada(x_valores):
        message = "Por favor ingrese los valores de X de menor a mayor\nEsto es necesario para la correcta creación de los intervalos"
        return None, None, None, message, True

    if f_x!="" and len(y_valores)==0:
        i=0
        while i < len(x_valores):
            valor_a_agregar = N(f_x.subs(x,x_valores[i]),7).evalf(n=7)
            if not valor_a_agregar.is_real:
                message = "Error al evaluar el valor x={x_valores[i]},\nEl punto no forma parte del dominio de la funcion ingresada"
                return None, None, None, message, True
            y_valores.append(valor_a_agregar)
            i=i+1
    if selection_option == 1:
        if x_evaluar < x_valores[0] or x_evaluar > x_valores[len(x_valores)-1]:
            message = "El valor a evaluar no esta dentro de los intervalos\nPor lo tanto no se puede evaluar"
            return None, None, None, message, True

    if grado != 1 and grado != 2 and grado != 3:
        message = f"el grado {grado} no esta disponible caso\nlos grados disponibles son 1,2 y 3"
        return None, None, None, message, True

    variables=grado+1
    intervalos=[]

    intervalo=[]
    if len(y_valores) == len(x_valores) and len(x_valores) >= 3 and len(y_valores) >= 3:
        i=0
        while i < numero_intervalos:
            valor1 = x_valores[i]
            vaor2 = x_valores[i+1]
            intervalo.append(valor1)
            intervalo.append(vaor2)
            intervalos.append([])
            intervalos[i].extend(intervalo)
            intervalo.clear()
            i=i+1
        # print(intervalos) 
        simbolos=[]   
        
        if grado == 1:
            variables = ["a","b"]
            tamanio_seccionada=len(intervalos)
            seccionada = [] 
            
            i=0
            while i<len(intervalos):
                o=0
                while o < len(variables):
                    simbolo=sp.symbols(variables[o]+str(i))
                    simbolos.append(simbolo)
                
                    o=o+1
                i=i+1
            
            i=0
            # print(simbolos)
            while i<len(simbolos):
                nueva_ecua=simbolos[i]*x+simbolos[i+1]
                seccionada.append(nueva_ecua)
                i=i+2
                
            evaluar=0
            # print(seccionada)
            ecuaciones=[]
            while evaluar < len(seccionada):
                evaluar1 = N(seccionada[evaluar].subs(x,intervalos[evaluar][0]),7).evalf(n=7)
                evaluar2 = N(seccionada[evaluar].subs(x,intervalos[evaluar][1]),7).evalf(n=7)
                ecuaciones.append(evaluar1-y_valores[evaluar] )    
                ecuaciones.append(evaluar2-y_valores[evaluar+1] )
                evaluar = evaluar + 1
            # print(ecuaciones)
            # print(simbolos)
            soluciones = solve(ecuaciones, simbolos)
            valores = list(soluciones.values())
            listafinal=[]
            
            i=0
            while i<len(seccionada):
                solucion=seccionada[i].subs(soluciones)
                listafinal.append(solucion)
                i=i+1
            
            # print("soluciones simbolos")
            # print(soluciones)
            # print("solucion seccionada")
            seccionada_mostrar = list_seccionada( listafinal, intervalos)
            
            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("S(x)")), 
                    ft.DataColumn(ft.Text("Intervalo")), 
                ],
                rows=[
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(", ".join(map(str, fila[:1] + fila[2:])))),
                        ft.DataCell(ft.Text(str(fila[1]) if len(fila) > 1 else ""))
                        ]) for fila in seccionada_mostrar
                ]
            )
            
            tabla = ft.Row([ft.Container(padding=20, content=ft.Row([table]))], scroll=ft.ScrollMode.ALWAYS)
            
            if f_x != "":
                i=0
                while i < len(intervalos):
                    if x_evaluar >= intervalos[i][0] and x_evaluar <= intervalos[i][1]:
                        cual_ecuacion=i
                        #este break si no me equivico sale de este bucle, no deberia de interferir en los de mas
                        break
                    i=i+1
                    
                evaluacion = listafinal[cual_ecuacion].subs(x,x_evaluar).evalf(n=7)
                vv = N(f_x.subs(x,x_evaluar),12).evalf()
                ep = abs((vv-evaluacion)/vv)*100
                message = f"Error Porcentual: {ep}%"
                               
                return tabla, soluciones, seccionada_mostrar, message, False
                
            x_evaluar = ''      
            return tabla, soluciones, seccionada_mostrar, None, False

        elif grado==2: 
        
            variables=["a","b","c"]
            tamanio_seccionada=len(intervalos)
            seccionada=[] 
            
            i=0
            while i < len(intervalos):
                o = 0
                while o < len(variables):
                    simbolo = sp.symbols(variables[o]+str(i))
                    simbolos.append(simbolo)
                    
                    o=o+1
                i=i+1
                
            i=0
            # print(simbolos)
            while i < len(simbolos):
                nueva_ecua = simbolos[i]*x**2+simbolos[i+1]*x+simbolos[i+2]
                seccionada.append(nueva_ecua)
                i=i+3
                
            evaluar = 0
            ecuaciones = []
            
            evaluar = 0
            while evaluar < len(seccionada):
                evaluar1 = N(seccionada[evaluar].subs(x,intervalos[evaluar][0]),7).evalf(n=7)  
                evaluar2 = N(seccionada[evaluar].subs(x,intervalos[evaluar][1]),7).evalf(n=7)
                ecuaciones.append(evaluar1-y_valores[evaluar])    
                ecuaciones.append(evaluar2-y_valores[evaluar+1])
                evaluar=evaluar+1

            i=0
            seccionada_derivada1=[]
            while i < len(seccionada):
                derivada = diff(seccionada[i],x)
                seccionada_derivada1.append(derivada)
                i=i+1
    
            evaluar = 0
            while evaluar < len(seccionada_derivada1)-1:
                evaluar1 = seccionada_derivada1[evaluar].subs(x,intervalos[evaluar][1]).evalf()-seccionada_derivada1[evaluar+1].subs(x,intervalos[evaluar][1]).evalf() 
                ecuaciones.append(evaluar1)    
                evaluar = evaluar + 1
                
            copia_simbolos = [*simbolos]
            Ec = 0
            # print("copias antes",copia_simbolos)
            while Ec < len(ecuaciones):
                simbolos_libre = ecuaciones[Ec].free_symbols
                simbolos_librel = list(simbolos_libre)
                if len(simbolos_librel) == 1:
                    copia_simbolos.remove(simbolos_librel[0])
                Ec=Ec+1
            #print("copias",copia_simbolos)
            #print(ecuaciones)
            #print("simbolos",simbolos)
            #grado de libertad
            simbolo_agregar = copia_simbolos[0]
            ecuaciones.append(simbolo_agregar)
            i = 0
            soluciones = solve(ecuaciones, simbolos)
            valores=list(soluciones.values())
            listafinal = []
            
            i=0
            while i < len(seccionada):
                solucion = seccionada[i].subs(soluciones).evalf()
                listafinal.append(solucion)
                i=i+1

            # print("soluciones simbolos")
            # print(soluciones)
            # print("solucion seccionada")
            seccionada_mostrar = list_seccionada( listafinal, intervalos)
            
            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("S(x)")), 
                    ft.DataColumn(ft.Text("Intervalo")), 
                ],
                rows=[
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(", ".join(map(str, fila[:1] + fila[2:])))),
                        ft.DataCell(ft.Text(str(fila[1]) if len(fila) > 1 else ""))
                        ]) for fila in seccionada_mostrar
                ]
            )
            
            tabla = ft.Row([ft.Container(padding=20, content=ft.Row([table]))], scroll=ft.ScrollMode.ALWAYS)
            
            if f_x!="":
                i=0
                while i < len(intervalos):
                    if x_evaluar >= intervalos[i][0] and x_evaluar <= intervalos[i][1]:
                        cual_ecuacion = i
                        #este break si no me equivico sale de este bucle, no deberia de interferir en los de mas
                        break
                    i=i+1
                    
                evaluacion = listafinal[cual_ecuacion].subs(x,x_evaluar).evalf()
                
                vv = N(f_x.subs(x,x_evaluar),12).evalf()
                ep = abs((vv - evaluacion)/vv)*100
                message = f"Error Porcentual: {ep}%"
                
                return tabla, soluciones, seccionada_mostrar, message, False
                
            x_evaluar = ''      
            return tabla, soluciones, seccionada_mostrar, None, False 
        
        else:       
            variables = ["a","b","c","d"] 
            tamanio_seccionada = len(intervalos)
            seccionada = [] 
            
            i = 0
            while i < len(intervalos):
                o = 0
                while o < len(variables):
                    simbolo = sp.symbols(variables[o]+str(i))
                    simbolos.append(simbolo)
                    
                    o=o+1
                i=i+1
            i=0
            # print(simbolos)
            while i < len(simbolos):
                nueva_ecua = simbolos[i]*x**3 + simbolos[i+1]*x**2 + simbolos[i+2]*x + simbolos[i+3]
                seccionada.append(nueva_ecua)
                i=i+4
                
            ecuaciones=[]
            evaluar=0
            while evaluar < len(seccionada):
                evaluar1 = N(seccionada[evaluar].subs(x,intervalos[evaluar][0]),7).evalf(n=7)  
                evaluar2 = N(seccionada[evaluar].subs(x,intervalos[evaluar][1]),7).evalf(n=7)
                ecuaciones.append((evaluar1-y_valores[evaluar]).evalf())    
                ecuaciones.append((evaluar2-y_valores[evaluar+1]).evalf())
                evaluar = evaluar + 1
        
            i=0
            seccionada_derivada1=[]
            while i < len(seccionada):
                derivada=diff(seccionada[i],x)
                seccionada_derivada1.append(derivada)
                i=i+1
        
            evaluar = 0
            while evaluar < len(seccionada_derivada1)-1:
                evaluar1 = seccionada_derivada1[evaluar].subs(x,intervalos[evaluar][1]).evalf(n=7)-seccionada_derivada1[evaluar+1].subs(x,intervalos[evaluar][1]).evalf(n=7)
                ecuaciones.append(evaluar1)     
                evaluar = evaluar + 1
    
            i=0
            seccionada_derivada2=[]
            while i < len(seccionada_derivada1):
                derivada = diff(seccionada_derivada1[i],x)
                seccionada_derivada2.append(derivada)
                i=i+1
    
            evaluar = 0
            while evaluar < len(seccionada_derivada2)-1:
                evaluar1 = seccionada_derivada2[evaluar].subs(x,intervalos[evaluar][1]).evalf(n=7)-seccionada_derivada2[evaluar+1].subs(x,intervalos[evaluar][1]).evalf(n=7)
                ecuaciones.append(evaluar1)    
                evaluar = evaluar + 1
    
            #grado de libertad
            grado1=seccionada_derivada2[0].subs(x,x_valores[0]).evalf(n=7)
            grado2=seccionada_derivada2[len(seccionada_derivada2)-1].subs(x,x_valores[len(x_valores)-1]).evalf(n=7)
            ecuaciones.append(grado1)
            ecuaciones.append(grado2)
            soluciones = solve(ecuaciones, simbolos)
        
            valores = list(soluciones.values())
            listafinal = []
            i=0
            while i < len(seccionada):
                solucion = seccionada[i].subs(soluciones)
                listafinal.append(solucion)
                i=i+1
            
            # print("soluciones simbolos")
            # print(soluciones)
            # print("solucion seccionada")
            seccionada_mostrar = list_seccionada( listafinal, intervalos)
            
            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("S(x)")), 
                    ft.DataColumn(ft.Text("Intervalo")), 
                ],
                rows=[
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(", ".join(map(str, fila[:1] + fila[2:])))),
                        ft.DataCell(ft.Text(str(fila[1]) if len(fila) > 1 else ""))
                        ]) for fila in seccionada_mostrar
                ]
            )
            
            tabla = ft.Row([ft.Container(padding=20, content=ft.Row([table]))], scroll=ft.ScrollMode.ALWAYS)
            
            if f_x!="":
                i=0
                while i < len(intervalos):
                    if x_evaluar >= intervalos[i][0] and x_evaluar <= intervalos[i][1]:
                        cual_ecuacion=i
                        #este break si no me equivico sale de este bucle, no deberia de interferir en los de mas
                        break
                    i=i+1
                evaluacion = listafinal[cual_ecuacion].subs(x,x_evaluar).evalf()
                vv = N(f_x.subs(x,x_evaluar),12).evalf()
                ep = abs((vv - evaluacion)/vv)*100
                message = f"Error Porcentual: {ep}%"
                
                return tabla, soluciones, seccionada_mostrar, message, False
                
            x_evaluar = ''
            return tabla, soluciones, seccionada_mostrar, None, False
    else:
        if len(y_valores) != len(x_valores) and f_x == "":
            message = f"Error las tablas deben tener la misma cantidad de datos"
            return None, None, None, message, True
        
        elif len(x_valores)<3 or len(y_valores)<3 :  
            message = f"Error las tablas deben tener tres puntos como minimo"
            return None, None, None, message, True
        

   

def show(): # Muestra los resultados 
      
    def clean(event):
        container_results.visible = False
        row.controls[2].value = ''
        row.controls[3].value = ''
        row.controls[4].value = ''
        row.controls[5].value = '' 
        row.controls[6].value = ''       
        row.controls[2].autofocus = True
        lbl_results3.controls[0].value = ''
        tbl.visible = False
        lbl_eval.visible = False
        event.control.page.update()
    
    def get_data(event): # asigna los datos ingresados a la funcion solve()
        x = sp.symbols('x')
        
        #Limpia los datos del valor a evaluar en el polinomio
        lbl_results3.controls[0].value = row.controls[6].value
        lbl_eval.visible = False
        
        def evaluar(event):
            x = sp.symbols('x')
            try:
                num_evaluar = float(lbl_results3.controls[0].value)
                polinomio = seccionada[0][0]
                poli_eval  = polinomio.subs(x, num_evaluar)
                lbl_eval.content = ft.Text(f'Punto a evalurar X = {num_evaluar}: \t\t\t\t Ecuacion de la seccionada: {polinomio}\nP({num_evaluar}) = {poli_eval}', weight="bold", size=20, text_align = ft.TextAlign.CENTER )
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
                eval_x = float(row.controls[6].value)
                valores_xstr = x.split(',')
                valores_x = [float(valor.strip()) for valor in valores_xstr]
                valores_y = []
                            
                try:  
                    tabla, incognitas, seccionada, message, alert = resolver(fx, valores_x, valores_y, grade, eval_x, selection_option)
                    
                    if alert == True:
                        show_alert(event, message)
                    else: 
                        #Mostrar resultados
                        tbl.content = tabla
                        tbl.visible = True
                        lbl_results.content = ft.Text(value=f'{name}\t\t\t\tError: {message}', size=16, text_align=ft.TextAlign.CENTER)
                        lbl_results2.content = ft.Text(value=f'Incógnitas: {incognitas}', weight="bold", size=20, text_align=ft.TextAlign.CENTER)
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
                eval_x = row.controls[6].value
                valores_xstr = x.split(',')
                valores_x = [float(valor.strip()) for valor in valores_xstr]
                valores_ystr = y.split(',')
                valores_y = [float(valor.strip()) for valor in valores_ystr]
                            
                try:  
                    tabla, incognitas, seccionada, message, alert = resolver(fx, valores_x, valores_y, grade, eval_x, selection_option)
                    
                    if alert == True:
                        show_alert(event, message)
                    else: 
                        #Mostrar resultados
                        tbl.content = tabla
                        tbl.visible = True
                        lbl_results.content = ft.Text(value=f'{name}', size=16, text_align=ft.TextAlign.CENTER)
                        lbl_results2.content = ft.Text(value=f'Incógnitas: {incognitas}', weight="bold", size=20, text_align=ft.TextAlign.CENTER)
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
            row.controls[8].visible = True
            row.controls[2].col = {"md": 3}
            row.controls[3].col = {"md": 3}
            row.controls[5].col = {"md": 1}
            clean(event)
            show_modal_alert(event, 'Ingrese valores separados por coma 1, 2, 3, o 1.000, 2.2222, 3.9999')
            event.control.page.update()
            
        elif selection_option == 2:
            row.controls[2].visible = False
            row.controls[3].visible = True
            row.controls[4].visible = True
            row.controls[5].visible = True
            row.controls[6].visible = False
            row.controls[7].visible = True
            row.controls[8].visible = True
            row.controls[5].col = {"md": 3}
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
                        col={"md": 3},
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
                col={"md": 1}),
            
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
