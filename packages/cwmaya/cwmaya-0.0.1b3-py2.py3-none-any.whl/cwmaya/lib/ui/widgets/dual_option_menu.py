import pymel.core.uitypes as gui
import pymel.core as pm
import cwmaya.lib.const as k


class DualOptionMenuControl(gui.FormLayout):

    def __init__(self):
        """
        Create the UI.
        """
        super(DualOptionMenuControl, self).__init__()
        self.model = None
        self.label_ctl = pm.text(label="Dual", align="right", width=k.LABEL_WIDTH)
        self.category_menu = pm.optionMenu()
        self.content_menu = pm.optionMenu()

        self.attachForm(self.label_ctl, "left", k.FORM_SPACING_X)
        self.attachNone(self.label_ctl, "right")
        self.attachForm(self.label_ctl, "top", k.FORM_SPACING_Y)
        self.attachForm(self.label_ctl, "bottom", k.FORM_SPACING_Y)

        self.attachControl(self.category_menu, "left", k.FORM_SPACING_X, self.label_ctl)
        self.attachPosition(self.category_menu, "right", k.FORM_SPACING_X, 30)
        self.attachForm(self.category_menu, "top", k.FORM_SPACING_Y)
        self.attachForm(self.category_menu, "bottom", k.FORM_SPACING_Y)

        self.attachControl(
            self.content_menu, "left", k.FORM_SPACING_X, self.category_menu
        )
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
        Populate the option menus.
        """
        self.model = model
        keys = list(self.model.keys())
        pm.setParent(self.category_menu, menu=True)
        self.category_menu.clear()
        for key in keys:
            display = self.model[key].get("display", key)
            pm.menuItem(label=display)
        self.hydrate_content(keys[0])

    def hydrate_content(self, category):
        """
        Populate the content menu.
        """
        pm.setParent(self.content_menu, menu=True)
        self.content_menu.clear()
        content = self.model[category]["content"]

        for item in content:
            display = content[item].get("display", item)
            pm.menuItem(label=display)

        # set the first item by default
        first_content_key = list(content.keys())[0]
        display_content = content[first_content_key].get("display", first_content_key)
        self.content_menu.setValue(display_content)

    def bind(self, attribute):
        """
        Bind the UI to the given attribute.
        """

        content_key = attribute.get() or ""
        # get category for the attribute
        category_key = self.get_category(content_key, self.model)
        if category_key is None:
            # not found - so the attribute needs to be set to a valid value
            category_key = list(self.model.keys())[0]
            content_key = list(self.model[category_key]["content"].keys())[0]
            attribute.set(content_key)

        display_category = self.model[category_key].get("display", category_key)
        self.category_menu.setValue(display_category)

        self.hydrate_content(category_key)
        display_content = self.model[category_key]["content"][content_key].get(
            "display", content_key
        )
        self.content_menu.setValue(display_content)

        # bind the change commands to the attribute
        self.category_menu.changeCommand(
            pm.Callback(self.on_category_menu_change, attribute)
        )
        self.content_menu.changeCommand(
            pm.Callback(self.on_content_menu_change, attribute)
        )

    def get_category(self, content_key, model):
        """
        Get the category for the given value.
        """
        for key in model:
            if model[key]["content"].get(content_key):
                return key
        return None

    def on_category_menu_change(self, attribute):
        display_category = self.category_menu.getValue()
        category_key = self.get_category_key(display_category)
        self.hydrate_content(category_key)
        first_content = list(self.model[category_key]["content"].keys())[0]
        attribute.set(first_content)

    def on_content_menu_change(self, attribute):
        value = self.content_menu.getValue()
        category = self.category_menu.getValue()
        category_key = self.get_category_key(category)
        content_key = self.get_content_key(category_key, value)
        attribute.set(content_key)

    def get_category_key(self, display_category):
        """
        Get the key for the given display category.
        """
        for key in self.model:
            if self.model[key].get("display", key) == display_category:
                return key
        return None

    def get_content_key(self, category, display_content):
        """
        Get the key for the given display content.
        """
        for key in self.model[category]["content"]:
            if (
                self.model[category]["content"][key].get("display", key)
                == display_content
            ):
                return key
        return None
