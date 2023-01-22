# -*- coding: utf-8 -*-
u"""spine @ rig
"""

import maya.cmds as mc

from .. base import module
from .. base import control


def build(spineJoints,
          rootJnt,
          spineCurve,
          bodyLocator,
          chestLocator,
          pelvisLocator,
          prefix="spine",
          rigScale=1.0,
          baseRig=None
          ):
    u"""_summary_

    Args:
        spineJoints (list[str]): List of 6 spine joints.
        rootJnt (str): Root joint.
        spineCurve (str): Name of spine cubic curve with 5 CVs matching first 5 spine joints.
        bodyLocator (str): Reference transform for position of body control.
        chestLocator (str): Reference transform for position of chest control.
        pelvisLocator (str): Reference transform for position of pelvis control.
        prefix (str, optional): Prefix to name new objects. Defaults to "spine".
        rigScale (float, optional): Scale factor for size of controls. Defaults to 1.0.
        baseRig (`base.module.Base`, optional): Instance of `base.module.Base` class. Defaults to None.

    Returns:
        Dictionary with rig module object and body control object.

        {"module": `rigLib.base.module.Base`, "bodyCtrl": `rigLib.base.control.Control`}

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

    # make spine curve clusters
    spineCurveCVs = mc.ls("{}.cv[*]".format(spineCurve), fl=1)
    numSpineCVs = len(spineCurveCVs)
    spineCurveClusters = []

    for i in range(numSpineCVs):
        clusterNumber = i + 1
        deformerName = "{}Cluster{}".format(prefix, clusterNumber)
        cls = mc.cluster(spineCurveCVs[i], n=deformerName)[1]
        spineCurveClusters.append(cls)
    mc.hide(spineCurveClusters)

    # parent spine curve
    mc.parent(spineCurve, rigmodule.partsNoTransGrp)

    # make controls
    bodyCtrl = control.Control(prefix="{}Body".format(prefix),
                            translateTo=bodyLocator,
                            scale=(rigScale * 4),
                            parent=rigmodule.controlsGrp)
    chestCtrl = control.Control(prefix="{}Chest".format(prefix),
                                translateTo=chestLocator,
                                scale=(rigScale * 6),
                                parent=bodyCtrl.C,
                                shape="circleZ")
    pelvisCtrl = control.Control(prefix="{}Pelvis".format(prefix),
                                translateTo=pelvisLocator,
                                scale=(rigScale * 6),
                                parent=bodyCtrl.C,
                                shape="circleZ")
    middleCtrl = control.Control(prefix="{}Middle".format(prefix),
                                translateTo=spineCurveClusters[2],
                                scale=(rigScale * 3),
                                parent=bodyCtrl.C,
                                shape="circleZ")

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

    return {"module": rigmodule, "bodyCtrl": bodyCtrl}

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