# -*- coding: utf-8 -*-
u"""Module for making top rig structure and rig module.
"""

import maya.cmds as mc

from . import control

sceneObjectType = "rig"


class Base():

    def __init__(self, characterName="new", scale=1.0, mainCtrlAttachObj=""):
        u"""Class for building top rig structure.

        Args:
            characterName (str, optional): Character name. Defaults to "new".
            scale (float, optional): General scale of the rig. Defaults to 1.0.

        Returns:
            None
        """

        self.topGrp = mc.group(n=characterName + "_rig_grp", em=1)
        self.rigGrp = mc.group(n="rig_grp", em=1, p=self.topGrp)
        self.modelGrp = mc.group(n="model_grp", em=1, p=self.topGrp)

        characterNameAt = "characterName"
        sceneObjectTypeAt = "sceneObjectType"

        for at in [characterNameAt, sceneObjectTypeAt]:
            mc.addAttr(self.topGrp, ln=at, dt="string")

        mc.setAttr("{}.{}".format(self.topGrp, characterNameAt), characterName, type="string", l=1)
        mc.setAttr("{}.{}".format(self.topGrp, sceneObjectTypeAt), sceneObjectType, type="string", l=1)

        # Make global control
        global1Ctrl = control.Control(prefix="global1", scale=scale * 20, parent=self.rigGrp, lockChannels=["v"])
        global2Ctrl = control.Control(prefix="global2", scale=scale * 18, parent=global1Ctrl.C, lockChannels=["s", "v"])

        self._flattenGlobalCtrlShape(global1Ctrl.C)
        self._flattenGlobalCtrlShape(global2Ctrl.C)

        for axis in ["y", "z"]:
            mc.connectAttr("{}.sx".format(global1Ctrl.C), "{}.s{}".format(global1Ctrl.C, axis))
            mc.setAttr("{}.s{}".format(global1Ctrl.C, axis), k=0)

        # Make more groups
        self.jointsGrp = mc.group(n="joints_grp", em=1, p=global2Ctrl.C)
        self.modulesGrp = mc.group(n="modules_grp", em=1, p=global2Ctrl.C)

        self.partGrp = mc.group(n="parts_grp", em=1, p=self.rigGrp)
        mc.setAttr("{}.it".format(self.partGrp), 0, l=1)

        # make main control
        mainCtrl = control.Control(prefix="main",
                                   scale=scale * 1,
                                   parent=global2Ctrl.C,
                                   translateTo=mainCtrlAttachObj,
                                   lockChannels=["t", "r", "s", "v"])

        self._adjustMainCtrlShape(mainCtrl, scale)

        if mc.objExists(mainCtrlAttachObj):
            mc.parentConstraint(mainCtrlAttachObj, mainCtrl.Off, mo=1)

        mainVisAts = ["modelVis", "jointsVis"]
        mainDispAts = ["modelDisp", "jointsDisp"]
        mainObjList = [self.modelGrp, self.jointsGrp]
        mainObjVisDvList = [1, 0]

        # add rig visibility connections
        for at, obj, dfVal in zip(mainVisAts, mainObjList, mainObjVisDvList):

            mc.addAttr(mainCtrl.C, ln=at, at="enum", enumName="off:on", k=1, dv=dfVal)
            mc.setAttr("{}.{}".format(mainCtrl.C, at), cb=1)
            mc.connectAttr("{}.{}".format(mainCtrl.C, at), "{}.v".format(obj))

        # add rig display type connections
        for at, obj in zip(mainDispAts, mainObjList):

            mc.addAttr(mainCtrl.C, ln=at, at="enum",
                       enumName="normal:template:reference", k=1, dv=2)
            mc.setAttr("{}.{}".format(mainCtrl.C, at), cb=1)
            mc.setAttr("{}.ove".format(obj), 1)
            mc.connectAttr("{}.{}".format(mainCtrl.C, at), "{}.ovdt".format(obj))

    def _adjustMainCtrlShape(self, ctrl, scale):

        # adjust shape of main control
        ctrlShapes = mc.listRelatives(ctrl.C, s=1, type="nurbsCurve")
        cls = mc.cluster(ctrlShapes)[1]
        mc.setAttr("{}.ry".format(cls), 90)
        mc.delete(ctrlShapes, ch=1)

        mc.move(5 * scale, ctrl.Off, moveY=True, relative=True)

    def _flattenGlobalCtrlShape(self, ctrlObject):

        # Flatten ctrl object shape
        ctrlShapes = mc.listRelatives(ctrlObject, s=1, type="nurbsCurve")
        cls = mc.cluster(ctrlShapes)[1]
        mc.setAttr("{}.rz".format(cls), 90)
        mc.delete(ctrlShapes, ch=1)


class Module():

    def __init__(self, prefix="new", baseObj=None):
        u"""Class for building module rig structure.

        Args:
            prefix (str, optional): Prefix to name new objects. Defaults to "new".
            baseObj (:obj:`base.module.Base`, optional): Instance of `base.module.Base`. Defaults to None.

        Returns:
            None
        """

        self.topGrp = mc.group(n="{}Module_grp".format(prefix), em=1)
        self.controlsGrp = mc.group(n="{}Controls_grp".format(prefix), em=1, p=self.topGrp)
        self.jointsGrp = mc.group(n="{}Joints_grp".format(prefix), em=1, p=self.topGrp)
        self.partsGrp = mc.group(n="{}Parts_grp".format(prefix), em=1, p=self.topGrp)
        self.partsNoTransGrp = mc.group(n="{}PartsNoTrans_grp".format(prefix), em=1, p=self.topGrp)

        mc.setAttr("{}.it".format(self.partsNoTransGrp), 0, l=1)

        # Parent module
        if baseObj:
            mc.parent(self.topGrp, baseObj.modulesGrp)
