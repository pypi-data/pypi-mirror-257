#
#   Module:     DotNet
#   Platform:   Python 3, Windows.NET
#
#   Some general helper classes for use with .NET Windows.Forms:
#
#       CustomMainMenu: 
#           A MainMenu created from a list of menu item parameters
#
#       CustomToolBar:
#           A ToolBar created from a list of toolbar item parameters.
#
#   Copyright Craig Farrow, 2010 - 2024
#

import clr
clr.AddReference("System.Windows.Forms")

from System.Windows.Forms import (
    MainMenu, MenuItem, Shortcut,
    ToolBar, ToolBarButton, ToolBarButtonStyle, ToolBarAppearance,
    ToolStrip, ToolStripContainer, ToolStripSeparator,
    ImageList, 
    ColorDepth,
    DockStyle
    )

from System.Drawing import (Bitmap, Image)
 
# ------------------------------------------------------------------
class CustomMainMenu(MainMenu):
    """
    Creates a .NET MainMenu from an initialised structure:
        List of tuples: (Menu Title, Submenu List)
        Submenu List is a list of tuples:
            (Handler, Text, Shortcut, Tooltip)
            If the Handler is None, then the menu is disabled.
            Shortcut can be None instead of Shortcut.None (which
            has to be 'getattr(Shortcut, "None")' in Python 3.)
            If the tuple is None, then a separator is inserted.
        Handlers are standard .NET Event Handlers, which take two 
        parameters: the sender object, and System.EventArgs.
    """
    def __init__(self, menuList):
        MainMenu.__init__(self)
        for menu in menuList:
            newMenu = MenuItem()
            newMenu.Text, submenuList = menu
            for submenu in submenuList:
                newSubmenu = MenuItem()
                if submenu:
                    handler, newSubmenu.Text, shortcut, newSubmenu.Tooltip = submenu
                    if handler:
                        newSubmenu.Click += handler
                    else:
                        newSubmenu.Enabled = False
                    if shortcut:
                        newSubmenu.Shortcut = shortcut
                else:
                    newSubmenu.Text = "-"       # Separator
                newMenu.MenuItems.Add(newSubmenu)
            self.MenuItems.Add(newMenu)

# ------------------------------------------------------------------
class CustomToolBar(ToolBar):
    """
    Creates a .NET ToolBar from an initialised structure:
        buttonList = List of tuples: 
            (Handler, Text, Image, Tooltip)
            If the Handler is None, then the button is disabled.
            An item of None produces a toolbar separator.
        imagePathTuple = (prefix, suffix) pair to generate a full
            path for loading the images.
    """

    def __init__(self, buttonList, imagePathTuple):
        ToolBar.__init__(self)
        self.Appearance = ToolBarAppearance.Flat
        self.Dock = DockStyle.Top

        self.HandlerList = []
        self.ImageList = ImageList()
        self.ImageList.ColorDepth = ColorDepth.Depth32Bit

        for bParams in buttonList:
            button = ToolBarButton()
            if bParams:
                handler, button.Text, imageName, button.ToolTipText = bParams
                self.ImageList.Images.Add(
                    Bitmap.FromFile(imageName.join(imagePathTuple)))
                button.ImageIndex = self.ImageList.Images.Count-1
                
                self.HandlerList.append(handler)
                button.Tag = len(self.HandlerList)-1 
            else:
                button.Style = ToolBarButtonStyle.Separator
            self.Buttons.Add(button)

        self.ButtonClick += self.__OnButtonClick

    def __OnButtonClick(self, sender, event):
        if event.Button.Tag is not None:               # zero is a valid value
            if self.HandlerList[event.Button.Tag]:
                self.HandlerList[event.Button.Tag]()   # The event handler
                
    def UpdateButtonText(self, buttonIndex, newText):
        self.Buttons[buttonIndex].Text = newText
