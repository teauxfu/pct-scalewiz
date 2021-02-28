"""MenuBar for the MainWindow."""

from __future__ import annotations

# util
import logging
import os
import tempfile
import tkinter as tk
from tkinter import messagebox, ttk
import typing

# internal
from pct_scalewiz.components.evaluation_frame import EvaluationFrame
from pct_scalewiz.components.project_editor import ProjectEditor
from pct_scalewiz.components.rinse_frame import RinseFrame
from pct_scalewiz.helpers.show_help import show_help

if typing.TYPE_CHECKING:
    from pct_scalewiz.components.base_frame import BaseFrame
    from pct_scalewiz.models.test_handler import TestHandler

# todo #9 port over the old chlorides / ppm calculators

logger = logging.getLogger("scalewiz")


class MenuBar(tk.Frame):
    """Menu bar to be displayed on the Main Frame."""

    def __init__(self, parent) -> None:
        tk.Frame.__init__(self, parent)
        # expecting parent to be the toplevel parent of the main frame
        self.parent = parent

        menu_bar = tk.Menu()
        menu_bar.add_command(label="Add System", command=lambda: parent.add_handler())

        project_menu = tk.Menu(tearoff=0)
        project_menu.add_command(
            label="New/Edit", command=lambda: self.request_project_edit()
        )
        project_menu.add_command(
            label="Load existing", command=lambda: self.request_project_load()
        )

        menu_bar.add_cascade(label="Project", menu=project_menu)
        menu_bar.add_command(
            label="Evaluation", command=lambda: self.request_eval_window()
        )
        menu_bar.add_command(
            label="Log", command=lambda: self.parent.parent.log_window.deiconify()
        )
        menu_bar.add_command(label="Rinse", command=lambda: self.show_rinse())
        menu_bar.add_command(label="Help", command=lambda: show_help())

        parent.winfo_toplevel().config(menu=menu_bar)

    def request_project_edit(self) -> None:
        """Requests to open an editor window for the currently selected Project."""
        current_tab = self.parent.tab_control.select()
        widget = self.parent.nametowidget(current_tab)
        self.modify_project(widget.handler)

    def request_eval_window(self) -> None:
        """Requests to open an evalutaion window for the currently selected Project."""
        current_tab = self.parent.tab_control.select()
        widget = self.parent.nametowidget(current_tab)
        if not os.path.isfile(widget.handler.project.path.get()):
            messagebox.showwarning(
                "No Project File",
                "The requested Project file has not yet been saved, or is missing",
            )
        else:
            self.evaluate_project(widget.handler)

    def request_project_load(self) -> None:
        """Request that the currently selected TestHandler load a Project."""
        current_tab = self.parent.tab_control.select()
        widget = self.parent.nametowidget(current_tab)
        widget.handler.load_project()
        widget.build()

    def show_rinse(self) -> None:
        """Shows a RinseFrame in a new Toplevel."""
        current_tab = self.parent.tab_control.select()
        widget = self.parent.nametowidget(current_tab)

        window = tk.Toplevel()
        rinse = RinseFrame(widget.handler, window)
        rinse.grid()
        window.resizable(0, 0)

    # todo move close editors method off of testhandler

    def modify_project(self, handler: TestHandler) -> None:
        """Opens a ProjectEditor to modify the current Project."""
        if len(handler.editors) > 0:
            messagebox.showwarning(
                "Project is locked", "Can't modify a Project while it is being accessed"
            )
            return
        window = tk.Toplevel()
        window.protocol("WM_DELETE_WINDOW", lambda: handler.close_editors())
        window.resizable(0, 0)
        handler.editors.append(window)
        editor = ProjectEditor(window, handler)
        editor.grid()
        logger.info(
            f"{handler.name}: Opened an editor window for {handler.project.name.get()}"
        )

    def evaluate_project(self, handler: TestHandler):
        """Opens a Toplevel with an Evaluation Frame for current Project."""
        if len(handler.editors) > 0:
            messagebox.showwarning(
                "Project is locked", "Can't modify a Project while it is being accessed"
            )
            return
        window = tk.Toplevel()
        window.protocol("WM_DELETE_WINDOW", lambda: handler.close_editors())
        window.resizable(0, 0)
        handler.editors.append(window)
        editor = EvaluationFrame(window, handler)
        editor.grid()
        logger.info(
            "%s: Opened an evaluation window for %s",
            handler.name,
            handler.project.name.get(),
        )
