# -*- coding: utf-8 -*-

import pymel.core.uitypes as gui
import pymel.core as pm
import cwmaya.lib.const as k
from cwmaya.lib import node_utils


class SingleOptionMenuArrayControl(gui.FormLayout):

    def __init__(self):
        """
        Create the UI.
        """
        super(SingleOptionMenuArrayControl, self).__init__()
        self.model = {}
        self.header_row = None
        self.column = None
        self.add_btn = None
        self.build_ui()

    def build_ui(self):
        pm.setParent(self)
        self.label = pm.text(label="", align="right", width=k.LABEL_WIDTH)

        self.add_btn = pm.symbolButton(
            image="item_add.png", width=k.TRASH_COLUMN_WIDTH, height=24
        )

        self.header_text = pm.text(
            align="left",
            label="",
            height=24,
            ebg=True,
            bgc=k.LIST_HEADER_BG,
        )
        self.header_row = _form_layout(
            self.header_text,
            self.add_btn,
        )
        pm.setParent(self)
        self.column = pm.columnLayout(adj=True)

        self.attachForm(self.label, "left", k.FORM_SPACING_X)
        self.attachNone(self.label, "right")
        self.attachForm(self.label, "top", k.FORM_SPACING_Y)
        self.attachForm(self.label, "bottom", k.FORM_SPACING_Y)

        self.attachControl(self.header_row, "left", k.FORM_SPACING_X, self.label)
        self.attachForm(self.header_row, "right", k.FORM_SPACING_X)
        self.attachForm(self.header_row, "top", k.FORM_SPACING_Y)
        self.attachNone(self.header_row, "bottom")

        self.attachControl(self.column, "left", k.FORM_SPACING_X, self.label)
        self.attachForm(self.column, "right", k.FORM_SPACING_X)
        self.attachControl(self.column, "top", 0, self.header_row)
        self.attachForm(self.column, "bottom", k.FORM_SPACING_Y)
        ##########################################

    def set_header_label(self, label):
        self.header_text.setLabel(f" {label}")

    def create_row(self, attr_element):
        pm.setParent(self.column)
        # key_attr, value_attr = attr_element.getChildren()

        content_menu = pm.optionMenu()
        del_ctl = pm.symbolButton(image="item_delete.png", width=k.TRASH_COLUMN_WIDTH)
        row = _form_layout(content_menu, del_ctl)
        pm.symbolButton(
            del_ctl,
            edit=True,
            command=pm.Callback(self.remove_entry, attr_element, row),
        )

        self.hydrate_row(content_menu)

        content_menu.changeCommand(
            pm.Callback(self.on_content_menu_change, attr_element, content_menu)
        )
        self.on_content_menu_change(attr_element, content_menu)
        return row

    def remove_entry(self, attribute, control):
        pm.deleteUI(control)
        pm.removeMultiInstance(attribute, b=True)

    def on_add(self, attribute):
        attr_element = node_utils.next_available_element_plug(attribute)
        attr_element.set("Some Value")
        pm.setParent(self.column)
        self.create_row(attr_element)

    def hydrate(self, model):
        """
        All we can do is store the model for now.
        """
        self.model = model

    def hydrate_row(self, content_menu):
        """
        Populate a menu.
        """

        keys = list(self.model.keys())
        pm.setParent(content_menu, menu=True)
        content_menu.clear()
        for key in keys:
            display = self.model[key].get("display", key)
            pm.menuItem(label=display)

        # set the first item by default
        first_content_key = keys[0]
        display_content = self.model[first_content_key].get(
            "display", first_content_key
        )
        content_menu.setValue(display_content)

    def bind(self, attribute):
        pm.setParent(self.column)
        for widget in pm.columnLayout(self.column, q=True, childArray=True) or []:
            pm.deleteUI(widget)
        for attr_element in attribute:
            self.create_row(attr_element)

        pm.button(self.add_btn, edit=True, command=pm.Callback(self.on_add, attribute))

    # def bind(self, attribute):
    #     """
    #     Bind the UI to the given attribute.
    #     """

    #     content_key = attribute.get() or ""

    #     # get category for the attribute
    #     keys = list(self.model.keys())
    #     if content_key not in keys:
    #         content_key = keys[0]
    #         attribute.set(content_key)

    #     display_content = self.model[content_key].get("display", content_key)
    #     self.content_menu.setValue(display_content)

    #     self.content_menu.changeCommand(
    #         pm.Callback(self.on_content_menu_change, attribute)
    #     )

    def on_content_menu_change(self, attribute, content_menu):
        display_content = content_menu.getValue()

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


def _form_layout(*widgets, **kwargs):

    # There must be 3 widgets.
    form = pm.formLayout(nd=100)
    for widget in widgets:
        pm.control(widget, edit=True, parent=form)

    form.attachForm(widgets[0], "left", k.FORM_SPACING_X)
    form.attachControl(widgets[0], "right", k.FORM_SPACING_X, widgets[1])
    form.attachForm(widgets[0], "top", k.FORM_SPACING_Y)
    form.attachForm(widgets[0], "bottom", k.FORM_SPACING_Y)

    form.attachNone(widgets[1], "left")
    form.attachForm(widgets[1], "right", k.FORM_SPACING_X)
    form.attachForm(widgets[1], "top", k.FORM_SPACING_Y)
    form.attachForm(widgets[1], "bottom", k.FORM_SPACING_Y)

    return form
