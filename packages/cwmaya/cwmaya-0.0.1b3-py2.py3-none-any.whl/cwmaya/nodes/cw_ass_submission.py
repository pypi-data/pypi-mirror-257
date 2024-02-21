# from __future__ import unicode_literals
import json

from cwmaya.nodes.cw_submission import cwSubmission

# pylint: disable=import-error
import maya.api.OpenMaya as om


def maya_useNewAPI():
    pass


class cwAssSubmission(cwSubmission):
    # pass
    aAexPerTask = None
    aAexInstanceType = None
    aAexSoftware = None
    aAexCommands = None
    aAexEnvironment = None
    aAexEnvironmentKey = None
    aAexEnvironmentValue = None
    aAexExtraAssets = None

    aRenUseCustomRange = None
    aRenCustomRange = None
    aRenStartFrame = None
    aRenEndFrame = None
    aRenByFrame = None
    aRenAnimation = None

    aRenPerTask = None  # chunk size
    aRenInstanceType = None
    aRenSoftware = None
    aRenCommands = None

    aRenEnvironment = None
    aRenEnvironmentKey = None
    aRenEnvironmentValue = None

    id = om.MTypeId(0x880502)

    def __init__(self):
        """Initialize the class."""
        super(cwAssSubmission, self).__init__()

    @staticmethod
    def creator():
        return cwAssSubmission()

    @classmethod
    def isAbstractClass(cls):
        return False

    @classmethod
    def initialize(cls):
        """Create the static attributes."""
        om.MPxNode.inheritAttributesFrom("cwSubmission")

        cls.initializeAex()
        cls.initializeRen()

    @classmethod
    def initializeAex(cls):
        """Create the static attributes for the export column."""

        cls.aAexPerTask = cls.make_int_att("aexPerTask", "expt", default=1, min=1)
        cls.aAexInstanceType = cls.make_string_att("aexInstanceType", "exit")
        cls.aAexSoftware = cls.make_string_att("aexSoftware", "exsw", array=True)
        cls.aAexCommands = cls.make_string_att("aexCommands", "extp", array=True)

        environment = cls.make_kv_pairs_att("aexEnvironment", "exn")
        cls.aAexEnvironment = environment["compound"]
        cls.aAexEnvironmentKey = environment["key"]
        cls.aAexEnvironmentValue = environment["value"]

        cls.aAexExtraAssets = cls.make_string_att("aexExtraAssets", "exea", array=True)

        om.MPxNode.addAttribute(cls.aAexPerTask)
        om.MPxNode.addAttribute(cls.aAexInstanceType)
        om.MPxNode.addAttribute(cls.aAexSoftware)
        om.MPxNode.addAttribute(cls.aAexCommands)
        om.MPxNode.addAttribute(cls.aAexEnvironment)
        om.MPxNode.addAttribute(cls.aAexExtraAssets)

        om.MPxNode.attributeAffects(cls.aAexPerTask, cls.aOutput)
        om.MPxNode.attributeAffects(cls.aAexInstanceType, cls.aOutput)
        om.MPxNode.attributeAffects(cls.aAexSoftware, cls.aOutput)
        om.MPxNode.attributeAffects(cls.aAexCommands, cls.aOutput)
        om.MPxNode.attributeAffects(cls.aAexEnvironment, cls.aOutput)
        om.MPxNode.attributeAffects(cls.aAexExtraAssets, cls.aOutput)

    @classmethod
    def initializeRen(cls):
        """Create the static attributes for the render column."""
        pass

        cls.aRenUseCustomRange = cls.make_bool_att("renUseCustomRange", "rnucr")
        cls.aRenCustomRange = cls.make_string_att("renCustomRange", "rncr")
        cls.aRenStartFrame = cls.make_time_att("renStartFrame", "rnsf")
        cls.aRenEndFrame = cls.make_time_att("renEndFrame", "rnef")
        cls.aRenByFrame = cls.make_string_att("renByFrame", "rnbf")
        cls.aRenAnimation = cls.make_bool_att("renAnimation", "rna")

        cls.aRenPerTask = cls.make_int_att("renPerTask", "rnpt", default=1, min=1)
        cls.aRenInstanceType = cls.make_string_att("renInstanceType", "rnit")
        cls.aRenSoftware = cls.make_string_att("renSoftware", "rnsw", array=True)
        cls.aRenCommands = cls.make_string_att("renCommands", "rntp", array=True)

        environment = cls.make_kv_pairs_att("renEnvironment", "rnn")
        cls.aRenEnvironment = environment["compound"]
        cls.aRenEnvironmentKey = environment["key"]
        cls.aRenEnvironmentValue = environment["value"]

        cls.aRenExtraAssets = cls.make_string_att("renExtraAssets", "rnea", array=True)

        om.MPxNode.addAttribute(cls.aRenUseCustomRange)
        om.MPxNode.addAttribute(cls.aRenCustomRange)
        om.MPxNode.addAttribute(cls.aRenStartFrame)
        om.MPxNode.addAttribute(cls.aRenEndFrame)
        om.MPxNode.addAttribute(cls.aRenByFrame)
        om.MPxNode.addAttribute(cls.aRenAnimation)

        om.MPxNode.addAttribute(cls.aRenPerTask)
        om.MPxNode.addAttribute(cls.aRenInstanceType)
        om.MPxNode.addAttribute(cls.aRenSoftware)
        om.MPxNode.addAttribute(cls.aRenCommands)
        om.MPxNode.addAttribute(cls.aRenEnvironment)
        om.MPxNode.addAttribute(cls.aRenExtraAssets)

        om.MPxNode.attributeAffects(cls.aRenUseCustomRange, cls.aOutput)
        om.MPxNode.attributeAffects(cls.aRenCustomRange, cls.aOutput)
        om.MPxNode.attributeAffects(cls.aRenStartFrame, cls.aOutput)
        om.MPxNode.attributeAffects(cls.aRenEndFrame, cls.aOutput)
        om.MPxNode.attributeAffects(cls.aRenByFrame, cls.aOutput)
        om.MPxNode.attributeAffects(cls.aRenAnimation, cls.aOutput)

        om.MPxNode.attributeAffects(cls.aRenPerTask, cls.aOutput)
        om.MPxNode.attributeAffects(cls.aRenInstanceType, cls.aOutput)
        om.MPxNode.attributeAffects(cls.aRenSoftware, cls.aOutput)
        om.MPxNode.attributeAffects(cls.aRenCommands, cls.aOutput)
        om.MPxNode.attributeAffects(cls.aRenEnvironment, cls.aOutput)
        om.MPxNode.attributeAffects(cls.aRenExtraAssets, cls.aOutput)

    def compute(self, plug, data):
        """Compute output json from input attribs."""
        if not ((plug == self.aOutput)):
            return None
        result = {}
        result.update(self.get_title(data))

        handle = data.outputValue(self.aOutput)
        handle.setString(json.dumps(result))

        data.setClean(plug)
        return self
