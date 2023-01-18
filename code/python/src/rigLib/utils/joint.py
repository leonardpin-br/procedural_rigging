#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""Joint utils @ utils
"""

import maya.cmds as mc


def listHierarchy(topJoint, withEndJoints=True):
    u"""List joint hierarchy starting with top joint.

    Args:
        topJoint (str): Joint to get listed with its joint hierarchy.
        withEndJoints (bool, optional): List hierarchy including end joints. Defaults to True.

    Returns:
        list: Listed joints starting with top joint.
    """

    listedJoints = mc.listRelatives(topJoint, type="joint", ad=True)
    listedJoints.append(topJoint)
    listedJoints.reverse()

    completeJoints = listedJoints[:]

    if not withEndJoints:
        completeJoints = [j for j in listedJoints if mc.listRelatives(j, c=1, type="joint")]

    return completeJoints