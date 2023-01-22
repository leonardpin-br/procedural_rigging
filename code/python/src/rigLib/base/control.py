# -*- coding: utf-8 -*-
u"""Module for making rig controls.
"""

import maya.cmds as mc


class Control():

    def __init__(self, prefix="new", scale=1.0, translateTo="", rotateTo="", parent="", shape="circle", lockChannels=["s", "v"]):
        u"""Class for building rig control.

        Args:
            prefix (str, optional): Prefix to name new objects. Defaults to "new".
            scale (float, optional): Scale value for size of control shapes. Defaults to 1.0.
            translateTo (str, optional): Reference object for control position. Defaults to "".
            rotateTo (str, optional): Reference object for control orientation. Defaults to "".
            parent (str, optional): Object to be parent of new control. Defaults to "".
            shape (str, optional): Control shape type. Defaults to "circle".
            lockChannels (list, optional): List of channels on control to be locked and non-keyable. Defaults to ["s", "v"].

        Returns:
            None

        """

        ctrlObject = None
        circleNormal = [1, 0, 0]

        if shape in ["circle", "circleX"]:
            circleNormal = [1, 0, 0]

        elif shape == "circleY":
            circleNormal = [0, 1, 0]

        elif shape == "circleZ":
            circleNormal = [0, 0, 1]

        elif shape == "sphere":
            ctrlObject = mc.circle(n="{}_ctl".format(prefix), ch=False, normal=[1, 0, 0], radius=scale)[0]
            addShape = mc.circle(n="{}_ctl2".format(prefix), ch=False, normal=[0, 0, 1], radius=scale)[0]
            mc.parent(mc.listRelatives(addShape, s=1), ctrlObject, r=1, s=1)
            mc.delete(addShape)

        if not ctrlObject:
            ctrlObject = mc.circle(
                n=prefix + "_ctl", ch=False, normal=circleNormal, radius=scale)[0]

        ctrlOffset = mc.group(n=prefix + "Offset_grp", em=1)
        mc.parent(ctrlObject, ctrlOffset)

        # Color control
        ctrlShapes = mc.listRelatives(ctrlObject, s=1)
        [mc.setAttr("{}.ove".format(s), 1) for s in ctrlShapes]

        if prefix.startswith("l_"):
            [mc.setAttr("{}.ovc".format(s), 6) for s in ctrlShapes]

        elif prefix.startswith("r_"):
            [mc.setAttr("{}.ovc".format(s), 13) for s in ctrlShapes]

        else:
            [mc.setAttr("{}.ovc".format(s), 22) for s in ctrlShapes]

        # Translate control
        if mc.objExists(translateTo):
            mc.delete(mc.pointConstraint(translateTo, ctrlOffset))

        # Rotate control
        if mc.objExists(rotateTo):
            mc.delete(mc.orientConstraint(rotateTo, ctrlOffset))

        # Parent control
        if mc.objExists(parent):
            mc.parent(ctrlOffset, parent)

        # Lock control channels
        singleAttributeLockList = []
        for lockChannel in lockChannels:
            if lockChannel in ["t", "r", "s"]:
                for axis in ["x", "y", "z"]:
                    at = lockChannel + axis
                    singleAttributeLockList.append(at)
            else:
                singleAttributeLockList.append(lockChannel)

        for at in singleAttributeLockList:
            mc.setAttr("{}.{}".format(ctrlObject, at), l=1, k=0)

        # Add public members
        self.C = ctrlObject
        self.Off = ctrlOffset
