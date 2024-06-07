import flet as ft
import importlib
import sys
import os
from pathlib import Path
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from methods.widgets.widgets import open_dlg_modal, show_alert
import methods.unidad2.biseccion
import methods.unidad2.grafico
import methods.unidad2.falsa_posicion
import methods.unidad2.punto_fijo
import methods.unidad2.secante
import methods.unidad2.newton_raphson
import methods.unidad2.newton_raphson_mod
import methods.unidad2.tartaglia

# def import_modules(packages):

#     try:
#         if module_name not in sys.modules:
#             file_path = os.path.join(
#                             str(Path(__file__).parent), module_name
#             )
#             spec = importlib.util.spec_from_file_location(
#                 module_name, file_path
#             )
#             print("spec: ", spec)
#             module = importlib.util.module_from_spec(spec)
#             sys.modules[module_name] = module
#             spec.loader.exec_module(module)
#             print(f"{module_name!r} has been imported")
#             return module
#         else:
#             print(f"{module_name!r} already in sys.modules")
#             return sys.modules[module_name]

#     except ImportError as err:
#         print('Error:', err)
#         return None


for module in sys.modules:
        print(module)


def select_modulo(module_name):
        # print("modulos antes de importar")
        # for module in sys.modules:
        #     print(module)

        # print("______________________--")
        # methods\unidad2\biseccion.py
        # print("importando ", module_name)
        # try:
        #     if module_name not in sys.modules:
        #         file_path = os.path.join(
        #                         str(Path(__file__).parent), module_name
        #         )
        #         spec = importlib.util.spec_from_file_location(
        #             module_name, file_path
        #         )
        #         print("spec: ", spec)
        #         module = importlib.util.module_from_spec(spec)
        #         sys.modules[module_name] = module
        #         spec.loader.exec_module(module)
        #         print(f"{module_name!r} has been imported")
        #         return module
        #     else:
        #         print(f"{module_name!r} already in sys.modules")
        #         return sys.modules[module_name]

        # except ImportError as err:
        #     print('Error:', err)
        #     return None
    return sys.modules[module_name]

    

def main(page: ft.Page):
        page.theme_mode = ft.ThemeMode.DARK 
        listview = ft.ListView(expand=1, auto_scroll=True )
        

        # method_row = ft.Ref[ft.ResponsiveRow]()

        page.title = "Métodos Numéricos"

        page.fonts = {
            "Roboto Mono": "RobotoMono-VariableFont_wght.ttf",
        }
        

        def method_click(e):
            try:
                unidad = e.control.data[0]
                method = e.control.data[1]
                module = f"methods.{unidad}.{method}"
                selected_module = select_modulo(module)
                if selected_module and hasattr(selected_module, 'show'):
                    view_controls = selected_module.show()
                    listview.controls.clear()  # Limpiar los controles existentes
                    listview.controls.append(view_controls)
                    page.update()
                else:
                    print(f"El módulo {module} no tiene la función 'show'")
            except Exception as ex:
                    print(f"Error al manejar el clic: {ex}")
                    show_alert(e, f'{e}')
        
            # unidad = e.control.data[0]
            # method = e.control.data[1]
            # #module = f"methods.{unidad}.{method}"
            # module = f"methods.{unidad}.{method}"
            # view_controls = select_modulo(module).show()
            # listview.controls.append(view_controls)
            # # print("modulos despues de importar")
            # # for module in sys.modules:
            # #     print(module)

            # # print("______________________--")
            # # print(method_row.current.controls )
            # # print(listview)
            # page.update()

        
        app_bar = ft.AppBar(
            title=ft.Text('Proyecto analisis numerico'),
            center_title=True, 
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(
                    icon=ft.icons.HELP_OUTLINE_OUTLINED,
                    on_click=open_dlg_modal,
                ),
            ]
        )
        
  

        
        menubar = ft.MenuBar(
            expand=True,
            style= ft.MenuStyle(bgcolor=ft.colors.SURFACE_VARIANT),
            controls=[
                ft.SubmenuButton(
                    content=ft.Text("Unidad 2"),
                    controls=[

                        ft.MenuItemButton(
                            content=ft.Text("Bisección"),
                            style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.BLUE}),
                            on_click=method_click,
                            data = ("unidad2", "biseccion")
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("Método Gráfico"),
                            style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.GREEN}),
                            on_click=method_click, 
                            data = ("unidad2", "grafico")
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("Falsa Posición"),
                            style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.RED}),
                            on_click=method_click,
                            data = ("unidad2", "falsa_posicion")
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("Punto fijo"),
                            style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.RED}),
                            on_click=method_click,
                            data = ("unidad2", "punto_fijo")
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("Secante"),
                            style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.RED}),
                            on_click=method_click,
                            data = ("unidad2", "secante")
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("Newton Raphson"),
                            style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.RED}),
                            on_click=method_click,
                            data = ("unidad2", "newton_raphson")
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("Newton Raphson moficado"),
                            style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.RED}),
                            on_click=method_click,
                            data = ("unidad2", "newton_raphson_mod")
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("Tartaglia"),
                            style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.RED}),
                            on_click=method_click,
                            data = ("unidad2", "tartaglia")
                        )
                    ]
                ),
                
                ft.SubmenuButton(
                    content=ft.Text("Unidad 3"),
                    controls=[

                        ft.MenuItemButton(
                            content=ft.Text("Horner"),
                            style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.BLUE}),
                            on_click=method_click,
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("Muller"),
                            style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.GREEN}),
                            on_click=method_click,
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("Ferrari"),
                            style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.RED}),
                            on_click=method_click,
                        )
                    ]
                ),
                
            ]
        )

      
     
        page.add(
            app_bar,
            ft.ResponsiveRow([ menubar]),
            listview
        )


ft.app(target=main, view=ft.WEB_BROWSER)