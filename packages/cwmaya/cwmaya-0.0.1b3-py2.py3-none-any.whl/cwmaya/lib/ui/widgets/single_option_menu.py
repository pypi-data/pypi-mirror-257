# -*- coding: utf-8 -*-

import pymel.core.uitypes as gui
import pymel.core as pm
import cwmaya.lib.const as k


class SingleOptionMenuControl(gui.FormLayout):

    def __init__(self):
        """
        Create the UI.
        """
        super(SingleOptionMenuControl, self).__init__()
        self.model = None

        self.label_ctl = pm.text(label="Something", align="right", width=k.LABEL_WIDTH)
        self.content_menu = pm.optionMenu()

        self.attachForm(self.label_ctl, "left", k.FORM_SPACING_X)
        self.attachNone(self.label_ctl, "right")
        self.attachForm(self.label_ctl, "top", k.FORM_SPACING_Y)
        self.attachForm(self.label_ctl, "bottom", k.FORM_SPACING_Y)

        self.attachControl(self.content_menu, "left", k.FORM_SPACING_X, self.label_ctl)
        self.attachForm(self.content_menu, "right", k.FORM_SPACING_X)
        self.attachForm(self.content_menu, "top", k.FORM_SPACING_Y)
        self.attachForm(self.content_menu, "bottom", k.FORM_SPACING_Y)

    def set_label(self, label):
        """
        Set the label for the control.
        """

        self.label_ctl.setLabel(label)

    def hydrate(self, model):
        """
        Populate the menu.
        """

        self.model = model

        keys = list(self.model.keys())
        pm.setParent(self.content_menu, menu=True)
        self.content_menu.clear()
        for key in keys:
            display = self.model[key].get("display", key)
            pm.menuItem(label=display)

        # set the first item by default
        first_content_key = keys[0]
        display_content = model[first_content_key].get("display", first_content_key)
        self.content_menu.setValue(display_content)

    def bind(self, attribute):
        """
        Bind the UI to the given attribute.
        """

        content_key = attribute.get() or ""

        # get category for the attribute
        keys = list(self.model.keys())
        if content_key not in keys:
            content_key = keys[0]
            attribute.set(content_key)

        display_content = self.model[content_key].get("display", content_key)
        self.content_menu.setValue(display_content)

        self.content_menu.changeCommand(
            pm.Callback(self.on_content_menu_change, attribute)
        )

    def on_content_menu_change(self, attribute):
        display_content = self.content_menu.getValue()

        content_key = self.get_content_key(display_content)
        attribute.set(content_key)

    def get_content_key(self, display_content):
        """
        Get the key for the given display content.
        """
        for key in self.model:
            if self.model[key].get("display", key) == display_content:
                return key
        return None
