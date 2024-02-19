from PySide2.QtWidgets import QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QComboBox
from PySide2.QtGui import QFont
from .Constants import font
from typing import Tuple


class AppButton:
    '''
Primary class for creating buttons.
Use this for making clickable items that user can interact with.

Params:
    text: str, The text of the button.
    '''

    def __init__(self, text: str) -> None:
        self._widget = QPushButton(text)
        self._widget.setFixedHeight(45)
        self.setFont(font.ARIAL, 18)

    def getSize(self) -> Tuple[int, int]:
        '''
Returns the widget size.

Params: No params
Returns: Tuple[int, int]
        '''

        return (self._widget.width(), self._widget.height())
    
    def setOnClick(self, onClick: callable) -> None:
        '''
Changes what to do when the widget is pressed.

Params:
    onClick: callable/function, The function that'll be called when pressed.
        '''
        self._widget.clicked.connect(lambda: onClick())

    def setFont(self, font_name: str, size: int) -> None:
        '''
Changes the font of the widget.

Params:
    font_name: str, New font (if you don't know which font to use, import SimpleAppGui.Constants.font and then use the module which has constants for different fonts.)
    size: int, New Font size.
Returns:
    None
        '''

        self._widget.setFont(QFont(font_name, size))

    def resizeWidget(self, newWidth: int, newHeight: int) -> None:
        '''
Resize the widget.

Params:
    newWidth: int, The new width of the widget
    newHeight: int, The new height of the widget
        '''
        self._widget.setFixedHeight(newHeight)
        self._widget.setFixedWidth(newWidth)

class AppLabelView(AppButton):
    '''
Primary class for text view in SimpleAppGui.
Use this to show information to the user

Constructors:
    text: str, The label text.
    '''

    def __init__(self, text: str) -> None:
        super().__init__(text)

        self._widget.setStyleSheet('QPushButton { background: none; border: none; }')

class AppInputBox(AppButton):
    '''
Primary class for entries in SimpleAppGui.
Use this to take user input.

Constructors:
    placeholder_text: str, The hint for the user to tell what to enter. Optional ('' as default)
    '''
    def __init__(self, placeholder_text: str) -> None:
        super().__init__('')

        self._widget = QLineEdit()
        self._widget.setPlaceholderText(placeholder_text)
        self._widget.setStyleSheet('''
QLineEdit {
    border-radius: 10pt;
    border: 1px solid black;
    padding: 5px;
    background: #EEEEEE;
}
        ''')
        self._widget.setFixedHeight(45)
        self.setFont(font.ARIAL, 18)
    
    def getText(self) -> str:
        '''
Returns the widget text, (What user inputted.)

Params: No params
Returns:
    str
        '''
        return self._widget.text()
    
    def setOnClick(self, onClick: callable) -> None:
        '''
This method cannot be used on a input box.
        '''
        pass

class AppLayout:
    VERTICAL: int = 1
    HORIZ: int = 0
    
    '''
Primary class for layouts in SimpleAppGui.
Often used in popups.
You can use the normal addWidget function to add it into a window, dialog or another layout

Constrcutors:
    orient: str, Orientation, AppLayout.VERTICAL or AppLayout.HORIZ
    '''
    def __init__(self, orient: int) -> None:
        self._widget = QVBoxLayout() if orient == self.VERTICAL else QHBoxLayout()
    
    def addWidget(self, w: object) -> None:
        '''
Add a widget to the layout.
        '''
        if isinstance(w, AppLayout):
            self._widget.addLayout(w._widget)
            return
        
        self._widget.addWidget(w._widget)
    
    def removeWidget(self, w: object) -> None:
        '''
remove a widget from the layout.
        '''
        self._widget.removeWidget(w._widget)


class AppSelectionBox(AppButton):
    '''
AppSelectionBox:
    Works like a comboBox/Spinner.
    User can select and item

    Params:
        items: list, The items the user can select.
    
    Use the currentItem field to get the selected item
    '''

    def __init__(self, items: list) -> None:
        super().__init__(items[0])
        self._widget = QComboBox()
        self._widget.addItems(items)
        self._widget.setStyleSheet('''
QPushButton {
    background: #DDDDDD;
    border: 1px solid black;
    border-radius: 10pt;
}
        ''')
        self._widget.setFixedHeight(45)
        self.setFont(font.ARIAL, 18)
        self.currentItem = items[0]
        self._widget.currentIndexChanged.connect(self._item_change)
    
    def _item_change(self, _) -> None:
        self.currentItem = self._widget.currentText()
    
    def setOnClick(self, onClick: callable) -> None:
        '''
This method cannot be used on a input box.
        '''
        pass
