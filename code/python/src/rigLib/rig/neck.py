# -*- coding: utf-8 -*-
u"""neck @ rig
"""

import maya.cmds as mc

from .. base import module
from .. base import control


def build(neckJoints,
          headJnt,
          neckCurve,
          prefix="neck",
          rigScale=1.0,
          baseRig=None
          ):
    u"""_summary_

    Args:
        neckJoints (list[str]): List of neck joints.
        headJnt (str): Head joint at the end of neck joint chain.
        neckCurve (str): Name of neck cubic curve with 5 CVs matching neck joints.
        prefix (str, optional): Prefix to name new objects. Defaults to "neck".
        rigScale (float, optional): Scale factor for size of controls. Defaults to 1.0.
        baseRig (`base.module.Base`, optional): Instance of `base.module.Base` class. Defaults to None.

    Returns:
        dict[str, `base.module.Base`]: Dictionary with rig module objects.

    References:
        `A case for better Python docstrings`_

        `class typing.Dict(dict, MutableMapping[KT, VT])`_

    .. _A case for better Python docstrings:
       https://dorukkilitcioglu.com/2018/08/18/python-better-docstring.html#the-google-way
    .. _class typing.Dict(dict, MutableMapping[KT, VT]):
       https://docs.python.org/3/library/typing.html#typing.Dict
    """


    # make rig module
    rigmodule = module.Module(prefix=prefix, baseObj=baseRig)

    # make neck curve clusters
    neckCurveCVs = mc.ls("{}.cv[*]".format(neckCurve), fl=1)
    numNeckCVs = len(neckCurveCVs)
    neckCurveClusters = []

    for i in range(numNeckCVs):
        clusterWithNumber = "Cluster%d" % (i + 1)
        cls = mc.cluster(neckCurveCVs[i], n="{}{}".format(prefix, clusterWithNumber))[1]
        neckCurveClusters.append(cls)
    mc.hide(neckCurveClusters)

    # parent neck curve
    mc.parent(neckCurve, rigmodule.partsNoTransGrp)

    # make attach groups
    bodyAttachGrp = mc.group(n="{}BodyAttach_grp".format(prefix), em=1, p=rigmodule.partsGrp)
    baseAttachGrp = mc.group(n="{}BaseAttach_grp".format(prefix), em=1, p=rigmodule.partsGrp)

    mc.delete(mc.pointConstraint(neckJoints[0], baseAttachGrp))

    # make controls
    headMainCtrl = control.Control(prefix="{}HeadMain".format(prefix),
                            translateTo=neckJoints[-1],
                            scale=(rigScale * 5),
                            parent=rigmodule.controlsGrp,
                            shape="circleZ")
    headLocalCtrl = control.Control(prefix="{}HeadLocal".format(prefix),
                            translateTo=headJnt,
                            rotateTo=headJnt,
                            scale=(rigScale * 4),
                            parent=headMainCtrl.C,
                            shape="circleX")















    _adjustBodyCtrlShape(bodyCtrl, spineJoints, rigScale)

    # attach controls
    mc.parentConstraint(chestCtrl.C, pelvisCtrl.C,
                        middleCtrl.Off, sr=["x", "y", "z"], mo=1)

    # attach clusters
    mc.parent(spineCurveClusters[3:], chestCtrl.C)
    mc.parent(spineCurveClusters[2], middleCtrl.C)
    mc.parent(spineCurveClusters[:2], pelvisCtrl.C)

    # make IK handle
    spineIk = mc.ikHandle(n="{}_ikh".format(prefix),
                          sol="ikSplineSolver",
                          sj=spineJoints[0],
                          ee=spineJoints[-2],
                          c=spineCurve,
                          ccv=0,
                          parentCurve=0)[0]
    mc.hide(spineIk)
    mc.parent(spineIk, rigmodule.partsNoTransGrp)

    # setup IK twist
    mc.setAttr("{}.dTwistControlEnable".format(spineIk), 1)
    mc.setAttr("{}.dWorldUpType".format(spineIk), 4)
    mc.connectAttr("{}.worldMatrix[0]".format(chestCtrl.C),
                   "{}.dWorldUpMatrixEnd".format(spineIk))
    mc.connectAttr("{}.worldMatrix[0]".format(pelvisCtrl.C),
                   "{}.dWorldUpMatrix".format(spineIk))

    # attach root joint
    mc.parentConstraint(pelvisCtrl.C, rootJnt, mo=1)

    return {"module": rigmodule}

def _adjustBodyCtrlShape(bodyCtrl, spineJoints, rigScale):
    """offset body control along spine Y axis.

    Args:
        bodyCtrl (`rigLib.base.control.Control`): Instance of `rigLib.base.control.Control`.
        spineJoints (list[str]): List of 6 spine joints.
        rigScale (float, optional): Scale factor for size of controls.
    """

    offsetGrp = mc.group(em=1, p=bodyCtrl.C)
    mc.parent(offsetGrp, spineJoints[2])
    ctrlCls = mc.cluster(mc.listRelatives(bodyCtrl.C, s=1))[1]
    mc.parent(ctrlCls, offsetGrp)
    mc.move(10 * rigScale, offsetGrp, moveY=1, relative=1, objectSpace=1)
    mc.delete(bodyCtrl.C, ch=1)