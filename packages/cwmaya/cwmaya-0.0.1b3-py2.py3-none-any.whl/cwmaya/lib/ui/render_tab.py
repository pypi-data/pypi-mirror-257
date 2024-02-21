import pymel.core as pm
from cwmaya.lib.ui.base_tab import BaseTab
from cwmaya.lib.ui.widgets.hidable_text_field import HidableTextFieldControl
import cwmaya.lib.const as k


class RenderTab(BaseTab):
    def __init__(self):
        """
        Create the UI.
        """
        super(RenderTab, self).__init__()

        self.column = pm.columnLayout()
        self.column.adjustableColumn(True)
        self.form.attachForm(self.column, "left", k.FORM_SPACING_X)
        self.form.attachForm(self.column, "right", k.FORM_SPACING_X)
        self.form.attachForm(self.column, "top", k.FORM_SPACING_Y)
        self.form.attachForm(self.column, "bottom", k.FORM_SPACING_Y)

        self.build_ui()

    def build_ui(self):
        """
        Create the frame that contains the export options.
        """
        pm.setParent(self.column)
        frame = pm.frameLayout(label="General")

        self.custom_range_ctl = self.create_custom_range_ctl(frame)
        self.per_task_ctl = self.create_per_task_control(frame)
        self.inst_type_ctl = self.create_inst_type_control(frame, "Instance type")

        self.software_ctl = self.create_software_control(self.column)

        self.commands_ctl = self.create_commands_control(self.column)

        self.extra_assets_ctl = self.create_extra_assets_control(self.column)
        self.environment_ctl = self.create_kvpairs_control(self.column, "Environment")

        return frame

    def create_custom_range_ctl(self, parent):
        pm.setParent(parent)
        result = HidableTextFieldControl()
        result.set_label("Use custom range")
        return result

    def bind(self, node):
        """Bind this UI to the given node."""
        self.custom_range_ctl.bind(
            node.attr("renUseCustomRange"), node.attr("renCustomRange")
        )
        self.per_task_ctl.bind(node.attr("renPerTask"))
        self.inst_type_ctl.bind(node.attr("renInstanceType"))
        self.software_ctl.bind(node.attr("renSoftware"))
        self.environment_ctl.bind(node.attr("renEnvironment"))
        self.extra_assets_ctl.bind(node.attr("renExtraAssets"))
        self.commands_ctl.bind(node.attr("renCommands"))
        return
