import flet as ft
import importlib
import sys
import os
from pathlib import Path
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

import methods.unidad2.biseccion
import methods.unidad2.grafico
import methods.unidad3

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
    method_row = ft.Ref[ft.ResponsiveRow]()
    page.padding = 0
    page.spacing = 0
    page.title = "Métodos Numéricos"

    page.fonts = {
        "Roboto Mono": "RobotoMono-VariableFont_wght.ttf",
    }


    def handle_color_click(e):
        unidad = e.control.data[0]
        method = e.control.data[1]
        #module = f"methods.{unidad}.{method}"
        module = f"methods.{unidad}.{method}"
        method_row.current.controls = [select_modulo(module).show()]
        # print("modulos despues de importar")
        # for module in sys.modules:
        #     print(module)

        # print("______________________--")
        print(method_row.current.controls )
        page.update()


    menubar = ft.MenuBar(
        expand=True,
        controls=[
            ft.SubmenuButton(
                content=ft.Text("Unidad 2"),
                controls=[

                    ft.MenuItemButton(
                        content=ft.Text("Bisección"),
                        style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.BLUE}),
                        on_click=handle_color_click,
                        data = ("unidad2", "biseccion")
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Método Gráfico"),
                        style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.GREEN}),
                        on_click=handle_color_click,
                        data = ("unidad2", "grafico")
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Falsa Posición"),
                        style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.RED}),
                        on_click=handle_color_click,
                    )
                ]
            ),
            
            ft.SubmenuButton(
                content=ft.Text("Unidad 3"),
                controls=[

                    ft.MenuItemButton(
                        content=ft.Text("Horner"),
                        style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.BLUE}),
                        on_click=handle_color_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Muller"),
                        style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.GREEN}),
                        on_click=handle_color_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Ferrari"),
                        style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.RED}),
                        on_click=handle_color_click,
                    )
                ]
            ),
            
        ]
    )

    page.add(
        ft.ResponsiveRow([menubar]),
        ft.ResponsiveRow(controls=[], ref=method_row,)
    )


ft.app(target=main)