
import pymel.core as pm
import pymel.core.uitypes as gui
from cwmaya.lib.ui.widgets.dual_option_menu import DualOptionMenuControl
from cwmaya.lib.ui.widgets.kv_pairs import KvPairsControl
from cwmaya.lib.ui.widgets.asset_list import AssetListControl
from cwmaya.lib.ui.widgets.integer_field import IntFieldControl
from cwmaya.lib.ui.widgets.commands import CommandsControl
from cwmaya.lib.ui.widgets.single_option_menu_array import SingleOptionMenuArrayControl
import cwmaya.lib.const as k


class BaseTab(gui.FormLayout):
    def __init__(self):
        """
        Create the UI.
        """
        self.setNumberOfDivisions(100)
        pm.setParent(self)
        self.scroll = pm.scrollLayout(childResizable=True)
        self.layout_scroll()
        pm.setParent(self.scroll)
        self.form = pm.formLayout()

        pm.setParent(self.form)

    def layout_scroll(self):
        self.attachForm(self.scroll, "left", k.FORM_SPACING_X)
        self.attachForm(self.scroll, "right", k.FORM_SPACING_X)
        self.attachForm(self.scroll, "top", k.FORM_SPACING_Y)
        self.attachForm(self.scroll, "bottom", k.FORM_SPACING_Y)

    def layout_children(self):
        pass

    def bind(self, node):
        print("bind", node)

    def create_extra_assets_control(self, parent):
        pm.setParent(parent)
        pm.frameLayout(label="Extra assets")
        return AssetListControl()

    def create_kvpairs_control(self, parent, label):
        pm.setParent(parent)
        pm.frameLayout(label=label)
        return KvPairsControl()

    def create_inst_type_control(self, parent, label):
        pm.setParent(parent)
        result = DualOptionMenuControl()
        result.set_label(label)
        result.hydrate(k.INSTANCE_TYPES)
        return result

    def create_software_control(self, parent):
        pm.setParent(parent)
        pm.frameLayout(label="Software")
        result = SingleOptionMenuArrayControl()
        result.set_header_label("Software stack")
        result.hydrate(k.SOFTWARE)
        return result

    def create_commands_control(self, parent):
        pm.setParent(parent)
        pm.frameLayout(label="Commands")
        return CommandsControl()

    def create_per_task_control(self, parent):
        pm.setParent(parent)
        result = IntFieldControl()
        result.set_label("Frames per task")
        return result
