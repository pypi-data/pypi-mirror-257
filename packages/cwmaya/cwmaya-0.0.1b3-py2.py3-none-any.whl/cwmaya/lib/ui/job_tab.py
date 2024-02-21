# -*- coding: utf-8 -*-


import pymel.core as pm
from cwmaya.lib.ui.base_tab import BaseTab
import cwmaya.lib.const as k
from cwmaya.lib.ui.widgets.kv_pairs import KvPairsControl
from cwmaya.lib.ui.widgets.single_option_menu import SingleOptionMenuControl
from cwmaya.lib.ui.widgets.text_area import TextAreaControl
from cwmaya.lib.ui.widgets.text_field import TextFieldControl


class JobTab(BaseTab):
    def __init__(self):
        """
        Create the UI.
        """
        super(JobTab, self).__init__()

        self.column = pm.columnLayout()
        self.column.adjustableColumn(True)
        self.form.attachForm(self.column, "left", k.FORM_SPACING_X)
        self.form.attachForm(self.column, "right", k.FORM_SPACING_X)
        self.form.attachForm(self.column, "top", k.FORM_SPACING_Y)
        self.form.attachForm(self.column, "bottom", k.FORM_SPACING_Y)
        self.project_ctl = None
        self.label_ctl = None
        self.description_ctl = None
        self.location_ctl = None
        self.metadata_ctl = None

        self.create_controls()

    def create_controls(self):
        """
        Create the frame that contains the job options.
        """
        pm.setParent(self.column)
        pm.frameLayout(label="General")

        pm.setParent(self.column)
        self.author_ctl = TextFieldControl()
        self.author_ctl.set_label("Author")

        pm.setParent(self.column)
        self.label_ctl = TextFieldControl()
        self.label_ctl.set_label("Job label")

        pm.setParent(self.column)
        self.description_ctl = TextAreaControl()
        self.description_ctl.set_label("Description")

        pm.setParent(self.column)

        self.project_ctl = SingleOptionMenuControl()
        self.project_ctl.set_label("Project")
        self.project_ctl.hydrate(k.PROJECTS)

        pm.setParent(self.column)
        self.location_ctl = TextFieldControl()
        self.location_ctl.set_label("Location")

        pm.setParent(self.column)
        pm.frameLayout(label="Metadata")
        self.metadata_ctl = KvPairsControl()
        pm.setParent(self.column)

    def bind(self, node):
        self.label_ctl.bind(node.attr("label"))
        self.author_ctl.bind(node.attr("author"))
        self.description_ctl.bind(node.attr("description"))
        self.project_ctl.bind(node.attr("projectName"))
        self.location_ctl.bind(node.attr("location"))
        self.metadata_ctl.bind(node.attr("metadata"))

        return
