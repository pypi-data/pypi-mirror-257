from PySide2.QtWidgets import QDialog
from .AppWidgets import AppLayout, AppButton, AppLabelView, AppInputBox

from .AppScreen.window import Window
from typing import Tuple


class Popup:
    '''
Primary for making a custom popup in SimpleAppGui,
If you don't want to go too complex, Just use the methods like showMessage, etc...

Params:
    parent: SimpleAppGui.AppWindow.window.Window or Popup, Dialog's parent
    title: str, popup title
    size: Tuple[int, int], popup size
    '''
    def __init__(self, parent: Window, title: str, windowSize: Tuple[int, int]) -> None:
        self._dialog = QDialog(parent._main if isinstance(parent, Window) else parent._dialog)
        self._dialog.setWindowTitle(title)
        self._dialog.resize(*windowSize)
    
    def setContentLayout(self, contentLayout: AppLayout) -> None:
        '''
Change the layout of the dialog.

Changes the content in the dialog.
        '''
        self._dialog.setLayout(contentLayout._widget)
    
    def show(self) -> None:
        '''Shows the dialog'''
        self._dialog.show()
    
    def close(self) -> None:
        '''Closes the dialog'''
        self._dialog.destroy()
        
def showMessage(parent: Window, title: str, message: str) -> None:
    '''
Shows a message dialog to the user.
    '''
    dialog = Popup(parent, title=title, windowSize=(200, 100))

    lay = AppLayout(AppLayout.VERTICAL)

    lbl = AppLabelView(message)
    btn = AppButton('Ok')
    btn.resizeWidget(200, 45)
    btn.setOnClick(dialog.close)

    lay.addWidget(lbl)
    lay.addWidget(btn)

    dialog.setContentLayout(lay)
    dialog.show()