import json

import maya.api.OpenMaya as om

def maya_useNewAPI():
    pass

class cwSubmission(om.MPxNode):
    aLabel = None
    aDescription = None
    aProjectName = None
    aMetadata = None
    aMetadataKey = None
    aMetadataValue = None
    aCurrentTime = None
    aLocation = None
    aAuthor = None
    aOutput = None

    id = om.MTypeId(0x880501)

    @staticmethod
    def creator():
        return cwSubmission()

    @classmethod
    def isAbstractClass(cls):
        return True

    @classmethod
    def initialize(cls):

        cls.aLabel = cls.make_string_att("label", "lbl")
        cls.aDescription = cls.make_string_att("description", "desc")
        cls.aProjectName = cls.make_string_att("projectName", "prn")
        cls.aCurrentTime = cls.make_time_att("currentTime", "ct")
        cls.aLocationTag = cls.make_string_att("location", "loc")
        cls.aAuthor = cls.make_string_att("author", "ath")

        metadata = cls.make_kv_pairs_att("metadata", "mtd")
        cls.aMetadata = metadata["compound"]
        cls.aMetadataKey = metadata["key"]
        cls.aMetadataValue = metadata["value"]

        cls.aOutput = cls.make_string_att(
            "output",
            "out",
            hidden=True,
            writable=False,
            keyable=False,
            storable=False,
            readable=True,
        )

        om.MPxNode.addAttribute(cls.aLabel)
        om.MPxNode.addAttribute(cls.aDescription)
        om.MPxNode.addAttribute(cls.aProjectName)
        om.MPxNode.addAttribute(cls.aCurrentTime)
        om.MPxNode.addAttribute(cls.aLocationTag)
        om.MPxNode.addAttribute(cls.aAuthor)

        om.MPxNode.addAttribute(cls.aMetadata)

        om.MPxNode.addAttribute(cls.aOutput)

        om.MPxNode.attributeAffects(cls.aLabel, cls.aOutput)
        om.MPxNode.attributeAffects(cls.aDescription, cls.aOutput)
        om.MPxNode.attributeAffects(cls.aProjectName, cls.aOutput)
        om.MPxNode.attributeAffects(cls.aMetadata, cls.aOutput)
        om.MPxNode.attributeAffects(cls.aCurrentTime, cls.aOutput)
        om.MPxNode.attributeAffects(cls.aLocationTag, cls.aOutput)
        om.MPxNode.attributeAffects(cls.aAuthor, cls.aOutput)

    @classmethod
    def make_int_att(cls, attr_name, short_name, **kwargs):
        """
        Create an int attribute.
        """
        default = kwargs.get("default", 0)
        attr = om.MFnNumericAttribute()
        result = attr.create(attr_name, short_name, om.MFnNumericData.kInt, default)
        attr.writable = kwargs.get("writable", True)
        attr.keyable = kwargs.get("keyable", True)
        attr.storable = kwargs.get("storable", True)
        if "min" in kwargs:
            attr.setMin(kwargs["min"])
        if "max" in kwargs:
            attr.setMax(kwargs["max"])
        return result

    @classmethod
    def make_bool_att(cls, attr_name, short_name, **kwargs):
        """
        Create a bool attribute.
        """
        default = kwargs.get("default", True)
        attr = om.MFnNumericAttribute()
        result = attr.create(attr_name, short_name, om.MFnNumericData.kBoolean, default)
        attr.writable = kwargs.get("writable", True)
        attr.keyable = kwargs.get("keyable", True)
        attr.storable = kwargs.get("storable", True)
        return result


    @classmethod
    def make_string_att(cls, attr_name, short_name, **kwargs):
        attr = om.MFnTypedAttribute()
        result = attr.create(attr_name, short_name, om.MFnData.kString)
        attr.hidden = kwargs.get("hidden", False)
        attr.writable = kwargs.get("writable", True)
        attr.readable = kwargs.get("readable", True)
        attr.keyable = kwargs.get("keyable", True)
        attr.storable = kwargs.get("storable", True)
        attr.array = kwargs.get("array", False)
        return result

    @classmethod
    def make_kv_pairs_att(cls, attr_name, short_name, **kwargs):
        cAttr = om.MFnCompoundAttribute()
        tAttr = om.MFnTypedAttribute()

        result_key = tAttr.create(
            f"{attr_name}Key", f"{short_name}k", om.MFnData.kString
        )
        result_value = tAttr.create(
            f"{attr_name}Value", f"{short_name}v", om.MFnData.kString
        )
        result_compound = cAttr.create(attr_name, short_name)
        cAttr.hidden = kwargs.get("hidden", False)
        cAttr.writable = kwargs.get("writable", True)
        cAttr.array = True
        cAttr.addChild(result_key)
        cAttr.addChild(result_value)
        return {"compound": result_compound, "key": result_key, "value": result_value}

    @classmethod
    def make_time_att(cls, attr_name, short_name, **kwargs):
        attr = om.MFnUnitAttribute()
        result = attr.create(attr_name, short_name, om.MFnUnitAttribute.kTime)
        attr.writable = kwargs.get("writable", True)
        attr.keyable = kwargs.get("keyable", True)
        attr.storable = kwargs.get("storable", True)
        return result

    def compute(self, plug, data):
        pass
        """Compute output json from input attribs."""
        if not ((plug == self.aOutput)):
            return None

    @classmethod
    def get_description(cls, data):
        description = data.inputValue(cls.aDescription).asString()
        return {"job_description": description}
