#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""Module for making rig controls.
"""

import maya.cmds as mc


class Control():

    def __init__(self, prefix="new", scale=1.0, translateTo="", rotateTo="", parent="", lockChannels=["s", "v"]):
        u"""Class for building rig control.

        Args:
            prefix (str, optional): Prefix to name new objects. Defaults to "new".
            scale (float, optional): Scale value for size of control shapes. Defaults to 1.0.
            translateTo (str, optional): Reference object for control position. Defaults to "".
            rotateTo (str, optional): Reference object for control orientation. Defaults to "".
            parent (str, optional): Object to be parent of new control. Defaults to "".
            lockChannels (list, optional): List of channels on control to be locked and non-keyable. Defaults to ["s", "v"].

        Returns:
            None

        """

        ctrlObject = mc.circle(
            n=prefix + "_ctl", ch=False, normal=[1, 0, 0], radius=scale)[0]
        ctrlOffset = mc.group(n=prefix + "Offset_grp", em=1)
        mc.parent(ctrlObject, ctrlOffset)

        # Color control
        ctrlShape = mc.listRelatives(ctrlObject, s=1)[0]
        mc.setAttr("{}.ove".format(ctrlShape), 1)

        if prefix.startswith("l_"):
            mc.setAttr("{}.ovc".format(ctrlShape), 6)

        elif prefix.startswith("r_"):
            mc.setAttr("{}.ovc".format(ctrlShape), 13)

        else:
            mc.setAttr("{}.ovc".format(ctrlShape), 22)

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
