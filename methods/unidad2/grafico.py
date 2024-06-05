import flet as ft
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from methods.widgets.widgets import show_alert
name = "Método Gráfico"

class Graficador:
    def __init__(self, fx, event):
        self.fx = fx
        self.page = event.control.page
        self.x = sp.symbols("x")
        self.x_vals = []
        self.y_vals = []
        self.roots = []
        self.dominio = None

    def find_domain(self):
        self.dominio = sp.calculus.util.continuous_domain(self.fx, self.x, sp.S.Reals)
        print("Dominio: ", self.dominio)
        print("Limite inferior: ", self.dominio.start)
        print("Limite superior: ", self.dominio.end)

    def find_roots(self):
        for root in sp.solve(self.fx):
            if root.is_real:
                self.roots.append(root.evalf())
        self.roots.sort()
        print("Raices: ", self.roots)
    
    def generate_values(self):
        if self.roots:
            if self.dominio.start.is_infinite and self.dominio.end.is_infinite:
                self.x_vals = np.linspace(float(self.roots[0]-1), float(self.roots[-1]+1), 1000)
            else:
                # Si el limite superior/derecha es infinito
                if self.dominio.end.is_infinite:
                    if self.dominio.left_open:
                        self.x_vals = np.linspace(float(self.dominio.start)+0.001, float(self.roots[-1]+10), 1000)
                    else:
                        self.x_vals = np.linspace(float(self.dominio.start), float(self.roots[-1]+10), 1000)
                # Si el limite inferior/izquierda es infinito
                elif self.dominio.start.is_infinite:
                    if self.dominio.right_open:
                        self.x_vals = np.linspace(float(self.roots[-1]-10), float(self.dominio.end)-0.001, 1000)
                    else:
                        self.x_vals = np.linspace(float(self.roots[-1]-10), float(self.dominio.end), 1000)

        for x_val in self.x_vals:
            self.y_vals.append(self.fx.subs(self.x, x_val).evalf())
    
    async def plot(self):
        font = {
            'family': 'serif',
            'color': 'darkred',
            'weight': 'normal',
            'size': 16,
        }
        mpl.use("TkAgg")
        cmap = mpl.colormaps['Dark2']
        colors = cmap(np.linspace(0, 1, len(self.roots)))

        plt.style.use('ggplot')
        fig, ax = plt.subplots(layout="constrained")

        # Centrar los ejes en el plano
        ax.spines.left.set_position('zero')
        ax.spines.left.set_color('black')
        ax.spines.bottom.set_position('zero')
        ax.spines.bottom.set_color('black')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')

        # Flechitas en los ejes
        ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
        ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)
        
        ax.plot(self.x_vals, self.y_vals, color="grey")

        ax.set_xlabel(
            "x", 
            fontdict={
                'family': 'serif',
                'color': 'darkred',
                'weight': 'normal',
                'size': 12,
            }, 
            labelpad=0.0,
            loc="right"
        )
        ax.set_ylabel(
            "f(x)",
            fontdict={
                'family': 'serif',
                'color': 'darkred',
                'weight': 'normal',
                'size': 12,
            },
            loc="top",
            labelpad=0.0,
        )

        ax.grid("both")

        for index, root in enumerate(self.roots):
            print(root, type(root))
            ax.scatter(root, [0], color=colors[index], label=f"$ R_{index+1}({root},0)$")

        ax.legend(
            loc="upper left", 
            prop={
                'family': 'serif',
                'weight': 'light',
                'size': 9,
            },
            labelcolor="dimgrey",
            frameon=False,
            title="Raíces",
            title_fontproperties={
                'family': 'serif',
                'weight': 'light',
                'size': 9,
            },
            alignment="left",
            labelspacing=0.35,
            borderaxespad=0.2,
            handletextpad=0.2,
            ncols=10
        )

        plt.show()

    def solve(self):
        self.find_domain()
        self.find_roots()
        self.generate_values()
        self.page.run_task(self.plot)



# def validar_expresion(str):
#     import sympy as sp
#     return sp.parse_expr(str)


def validar_expresion(expr):
    if not expr.strip():
        raise ValueError("La expresión no puede estar vacía")
    try:
        sym_expr = sp.sympify(expr)
        symbols = sym_expr.free_symbols
        if len(symbols) != 1 or sp.Symbol('x') not in symbols:
            raise ValueError("La expresión debe contener exactamente el símbolo 'x'")
        return sym_expr
    except sp.SympifyError:
        raise ValueError("La expresión no es válida")

def show():

    def get_data(event):
        
        try:
            
            fx = validar_expresion(row.controls[1].value)
        except ValueError as e:
            print(f"Error: {e}")
            show_alert(event, f'{e}')

        graficador = Graficador(fx, event)
        graficador.solve()
        #thread = threading.Thread(target=solve, args=(fx))
        #thread.start()
        
    
    row = ft.ResponsiveRow([
        ft.Text(
            value=f'{name}',
            col={"md": 12},
            weight="bold",
            size=20,
            text_align=ft.TextAlign.CENTER            
        ),
        ft.TextField(
            adaptive=True,
            label="Función",
            col={"md": 3}
        ),
        ft.ElevatedButton(
            text="Resolver", 
            on_click=get_data,
            height=45,
            col={"md": 3}
        )    
        ], alignment=ft.MainAxisAlignment.CENTER,
    )

    container_input = ft.Container(
        bgcolor='#565656',
        border_radius=ft.border_radius.all(20),
        padding=20,
        content=row, 
    )
    
    
   

    return container_input