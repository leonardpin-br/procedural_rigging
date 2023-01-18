#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""komodo dragon rig setup.

Deformation setup.



References:
    `Getting Sphinx to work with Maya modules`_

.. _Getting Sphinx to work with Maya modules:
   https://geektalker.wordpress.com/2013/03/26/getting-sphinx-to-work-with-maya-modules/



"""

import os

# Necessary to deal with Sphinx's limitation when parsing the code:
try:
    import sphinx.ext.autodoc.importer
except:
    pass

import maya.cmds as mc
import maya.mel as mm

from rigTools import bSkinSaver

from rigLib.utils import name
from . import project

skinWeightsDir = "weights/skinCluster"
swExt = ".swt"

bodyGeo = 'body_geo'
bodyMidresGeo = "body_midres_geo"


def build(baseRig, characterName):
    u"""Applies the skin weights previously saved onto the model (geometry) and
    the build (joints also previously save).

    Args:
        baseRig (`rigLib.base.module.Base`): Instance of `rigLib.base.module.Base`.
        characterName (str): The character name.
    """

    modelGrp = "%s_model_grp" % characterName

    # make twist joints
    refTwistJoints = ["l_elbow1_jnt", "l_knee1_jnt",
                      "r_elbow1_jnt", "r_knee1_jnt"]
    maketwistJoints(baseRig, refTwistJoints)

    # load skin weights
    geoList = _getModelGeoObjects(modelGrp)
    loadSkinWeights(characterName, geoList)

    # apply delta mush deformer
    _applyDeltaMush(bodyMidresGeo)

    # wrap hires body mesh
    _makeWrap([bodyGeo], bodyMidresGeo)


def _makeWrap(wrappedObjs, wrapperObj):
    u"""Applies the wrap deformer in the meshes.

    Args:
        wrappedObjs (list[str]): List of objects names to be wrapped.
        wrapperObj (str): Name of the wrapper object.

    References:
        `Wrap Deformer makes Maya instantly crash.`_

    .. _Wrap Deformer makes Maya instantly crash.:
       https://www.reddit.com/r/Maya/comments/rpf9an/wrap_deformer_makes_maya_instantly_crash/#t1_hq51skm
    """

    mc.select(wrappedObjs)
    mc.select(wrapperObj, add=True)
    mm.eval('doWrapArgList "7" { "1","0","1", "2", "1", "1", "0", "0" }')


def _applyDeltaMush(geo):
    """Applies a delta mush deformer to the given mesh.

    Args:
        geo (str): The name of the mesh.
    """

    deltaMushDf = mc.deltaMush(geo, smoothingIterations=50)[0]


def _getModelGeoObjects(modelGrp):
    u"""Gets the names of all geometry objects inside the given group.

    Args:
        modelGrp (str): The name of the group containing the geometry objects.

    Returns:
        list(str): A list containing all the names of the geometry objects.
    """

    geoList = [mc.listRelatives(o, p=1)[0]
               for o in mc.listRelatives(modelGrp, ad=1, type="mesh")]

    return geoList


def maketwistJoints(baseRig, parentJoints):
    u"""Creates the joints used for twisting the limbs (like arms).

    Args:
        baseRig (`rigLib.base.module.Base`): Instance of `rigLib.base.module.Base`.
        parentJoints (list(str)): List of strings containing the parent joints' names.

    Warning:
        Sphinx throws an error when parsing the code.

        To deal with it, the `origJntRadius` variable (that should be multiplied)
        is not multiplied when documenting this code.

    References:
        `Getting Sphinx to work with Maya modules`_

        `What's the canonical way to check for type in Python?`_

    .. _Getting Sphinx to work with Maya modules:
       https://geektalker.wordpress.com/2013/03/26/getting-sphinx-to-work-with-maya-modules/
    .. _What's the canonical way to check for type in Python?:
       https://stackoverflow.com/a/152596
    """

    twistJointsMainGrp = mc.group(
        n="twistJoints_grp", p=baseRig.jointsGrp, em=1)

    for parentJnt in parentJoints:
        prefix = name.removeSuffix(parentJnt)
        prefix = prefix[:-1]
        parentJntChild = mc.listRelatives(parentJnt, c=1, type="joint")[0]

        # make twist joints
        twistJntGrp = mc.group(n="{}TwistJoint_grp".format(
            prefix), p=twistJointsMainGrp, em=1)
        twistParentJnt = mc.duplicate(
            parentJnt, n="{}Twist1_jnt".format(prefix), parentOnly=True)[0]
        twistChildJnt = mc.duplicate(
            parentJntChild, n="{}Twist2_jnt".format(prefix), parentOnly=True)[0]

        # adjust twist joints
        origJntRadius = mc.getAttr("{}.radius".format(parentJnt))
        for j in [twistParentJnt, twistChildJnt]:

            # Deals with Sphinx limitation when parsing the code:
            if type(origJntRadius) is sphinx.ext.autodoc.importer._MockObject:
                mc.setAttr("{}.radius".format(j), (origJntRadius))
            else:
                mc.setAttr("{}.radius".format(j), (origJntRadius * 2))

            mc.color(j, ud=1)
        mc.parent(twistChildJnt, twistParentJnt)
        mc.parent(twistParentJnt, twistJntGrp)

        # attach twist joints
        mc.pointConstraint(parentJnt, twistParentJnt)

        # make IK handle
        twistIk = mc.ikHandle(n="{}TwistJoint_ikh".format(
            prefix), sol="ikSCsolver", sj=twistParentJnt, ee=twistChildJnt)[0]
        mc.hide(twistIk)
        mc.parent(twistIk, twistJntGrp)
        mc.parentConstraint(parentJntChild, twistIk)


def saveSkinWeights(characterName, geoList=[]):
    u"""Save weights for character geometry objects.

    Args:
        characterName (str): Character name.
        geoList (list[str], optional): List of selected geometry names. Defaults to [].
    """

    for obj in geoList:
        # weight file
        wtFile = os.path.join(project.mainProjectPath,
                              characterName, skinWeightsDir, obj + swExt)

        # save skin weight file
        mc.select(obj)
        bSkinSaver.bSaveSkinValues(wtFile)


def loadSkinWeights(characterName, geoList=[]):
    u"""Load skin weights for character geometry objects.

    Args:
        characterName (str): Character name.
        geoList (list[str], optional): List of selected geometry names. Defaults to [].
    """

    # weights folder
    wtDir = os.path.join(project.mainProjectPath,
                         characterName, skinWeightsDir).replace("\\", "/")
    wtFiles = os.listdir(wtDir)

    # load skin weights
    for wtFile in wtFiles:
        extRes = os.path.splitext(wtFile)

        # check extension format
        if not extRes > 1:
            continue

        # check skin weight file
        if not extRes[1] == swExt:
            continue

        # check geometry list
        if geoList and not extRes[0] in geoList:
            continue

        # check if objects exist
        if not mc.objExists(extRes[0]):
            continue

        fullpathWtFile = os.path.join(wtDir, wtFile).replace("\\", "/")
        bSkinSaver.bLoadSkinValues(
            loadOnSelection=False, inputFile=fullpathWtFile)
