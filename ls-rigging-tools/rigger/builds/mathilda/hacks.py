'''
Created on Jul 14, 2014

@author: Leon
'''
import pymel.core as pm
import pymel.core.nodetypes as nt
from pymel.core.language import Mel
import utils.rigging as rt
mel = Mel()

import rigger.utils.modulate as modulate
reload(modulate)

def addEyelidReaders():
    '''
    '''
    worldSpaceTranslateOffsetReader(pm.PyNode('FACE:LT_eye_aimAt_bnd_19'), 
                                    pm.PyNode('FACE:LT_eye_aimJnts_grp_0'))
    worldSpaceTranslateOffsetReader(pm.PyNode('FACE:LT_eye_aimAt_bnd_15'), 
                                    pm.PyNode('FACE:LT_eye_aimJnts_grp_0'))
    worldSpaceTranslateOffsetReader(pm.PyNode('FACE:LT_eye_aimAt_bnd_12'), 
                                    pm.PyNode('FACE:LT_eye_aimJnts_grp_0'))
    worldSpaceTranslateOffsetReader(pm.PyNode('FACE:LT_eye_aimAt_bnd_9'), 
                                    pm.PyNode('FACE:LT_eye_aimJnts_grp_0'))
    
    worldSpaceTranslateOffsetReader(pm.PyNode('FACE:RT_eye_aimAt_bnd_19'), 
                                    pm.PyNode('FACE:RT_eye_aimJnts_grp_0'))
    worldSpaceTranslateOffsetReader(pm.PyNode('FACE:RT_eye_aimAt_bnd_16'), 
                                    pm.PyNode('FACE:RT_eye_aimJnts_grp_0'))
    worldSpaceTranslateOffsetReader(pm.PyNode('FACE:RT_eye_aimAt_bnd_13'), 
                                    pm.PyNode('FACE:RT_eye_aimJnts_grp_0'))
    worldSpaceTranslateOffsetReader(pm.PyNode('FACE:RT_eye_aimAt_bnd_9'), 
                                    pm.PyNode('FACE:RT_eye_aimJnts_grp_0'))

def addBrowReaders():
    '''
    '''
    worldSpaceTranslateOffsetReader(pm.PyNode('FACE:LT_in_brow_bnd'), 
                                    pm.PyNode('FACE:LT_in_brow_bnd_hm'))
    worldSpaceTranslateOffsetReader(pm.PyNode('FACE:LT_mid_brow_bnd'), 
                                    pm.PyNode('FACE:LT_mid_brow_bnd_hm'))
    worldSpaceTranslateOffsetReader(pm.PyNode('FACE:LT_out_brow_bnd'), 
                                    pm.PyNode('FACE:LT_out_brow_bnd_hm'))
    worldSpaceTranslateOffsetReader(pm.PyNode('FACE:RT_in_brow_bnd'), 
                                    pm.PyNode('FACE:RT_in_brow_bnd_hm'))
    worldSpaceTranslateOffsetReader(pm.PyNode('FACE:RT_mid_brow_bnd'), 
                                    pm.PyNode('FACE:RT_mid_brow_bnd_hm'))
    worldSpaceTranslateOffsetReader(pm.PyNode('FACE:RT_out_brow_bnd'), 
                                    pm.PyNode('FACE:RT_out_brow_bnd_hm'))

def worldSpaceTranslateOffsetReader(node, inverseNode):
    '''
    calculate a node's translate offset
    and add as attribute
    '''
    mm = pm.createNode('multMatrix', n=node+'_translateOffsetReader_mm')
    pmm = pm.createNode('pointMatrixMult', n=node+'_translateOffsetReader_pmm')
    
    node.worldMatrix >> mm.matrixIn[0]
    inverseNode.worldInverseMatrix >> mm.matrixIn[1]
    
    mm.matrixSum >> pmm.inMatrix
    
    for channel in ['x','y','z']:
        node.addAttr('translateOffsetReader_'+channel, k=True)
        pmm.attr('o'+channel) >> node.attr('translateOffsetReader_'+channel)

def modulateEyelashACS():
    '''
    '''
    """
    # left side 9 to 19
    acsNodes = [pm.PyNode('FACE:LT_eye_aimAt_bnd_%d_eyelash_acs'%jntId)
                for jntId in range(9,20)]
    
    drv = pm.PyNode('FACE:LT_eyelid_upper_pri_ctrl')
    drv.addAttr('eyelidDownMod')
    rt.connectSDK(drv.ty, drv.eyelidDownMod, {0:1, -0.5:0})
    
    for node in acsNodes:
        mod = modulate.multiplyInput(node.rz, 1, '_eyelidDownMod')
        drv.eyelidDownMod >> mod 
        """
    # right side 9 to 19
    acsNodes = [pm.PyNode('FACE:RT_eye_aimAt_bnd_%d_eyelash_acs'%jntId)
                for jntId in range(9,20)]
    
    drv = pm.PyNode('FACE:RT_eyelid_upper_pri_ctrl')
    drv.addAttr('eyelidDownMod')
    rt.connectSDK(drv.ty, drv.eyelidDownMod, {0:1, -0.5:0})
    
    for node in acsNodes:
        mod = modulate.multiplyInput(node.rz, 1, '_eyelidDownMod')
        drv.eyelidDownMod >> mod 
        
    

def addAllEyelashBnds():
    '''
    '''
    # left side 9 to 19
    baseName = 'FACE:LT_eye_aimAt_bnd_'
    for jntId in range(9,20):
        addEyelashBnds(baseName+str(jntId))
        
    # right side 9 to 19
    baseName = 'FACE:RT_eye_aimAt_bnd_'
    for jntId in range(9,20):
        addEyelashBnds(baseName+str(jntId))

def addEyelashBnds(eyelidBnd):
    '''
    '''
    pm.select(cl=True)
    bnd = pm.joint(n=eyelidBnd+'_eyelash_bnd')
    bnd.radius.set(0.1)
    bne = pm.joint(n=eyelidBnd+'_eyelash_bne', p=(0.5,0,0))
    bne.radius.set(0.1)
    
    offset = pm.group(em=True, n=eyelidBnd+'_eyelash_offset')
    acs = pm.group(offset, n=eyelidBnd+'_eyelash_acs')
    grp = pm.group(acs, n=eyelidBnd+'_eyelash_grp')
    
    offset | bnd
    
    eyelidBnd = pm.PyNode(eyelidBnd)
    mat = eyelidBnd.getMatrix(worldSpace=True)
    grp.setMatrix(mat, worldSpace=True)
    
    eyelidBnd | grp
    
    

def modulateFleshyEyesUp():
    '''
    DONT USE THIS
    '''
    node = nt.Transform(u'FACE:LT_eyeball_bnd')
    node.addAttr('finalVectorAngle', k=True)
    # replace outputs
    outAttrs = node.vectorAngle.outputs(p=True)
    node.vectorAngle >> node.finalVectorAngle
    for plug in outAttrs:
        node.finalVectorAngle >> plug
    # modulate finalVectorAngle
    mod = modulate.multiplyInput(node.finalVectorAngle, 1, '_eyeY_mod')
    rt.connectSDK('FACE:LT_eyeball_bnd.paramNormalized', mod, {0:0.2, 0.4:1, 0.6:1, 1:0.2})


def addEyelashCollideAimLocGo():
    '''
    '''
    eyelidCtl = nt.Transform(u'FACE:LT_eyelid_inner_upper_ctrl')
    collideCtl = nt.Transform(u'FACE:LT_in_brow_ctrl')
    addEyelashCollideAimLoc(eyelidCtl, collideCtl)
    eyelidCtl = nt.Transform(u'FACE:LT_eyelid_upper_ctrl')
    collideCtl = nt.Transform(u'FACE:LT_mid_brow_ctrl')
    addEyelashCollideAimLoc(eyelidCtl, collideCtl)
    eyelidCtl = nt.Transform(u'FACE:LT_eyelid_outer_upper_ctrl')
    collideCtl = nt.Transform(u'FACE:LT_out_brow_ctrl')
    addEyelashCollideAimLoc(eyelidCtl, collideCtl)
    eyelidCtl = nt.Transform(u'FACE:LT_eyelid_outer_ctrl')
    collideCtl = nt.Transform(u'FACE:LT_out_brow_ctrl')
    addEyelashCollideAimLoc(eyelidCtl, collideCtl)

def addEyelashBnd(eyelashBase, aimLoc):
    '''
    import rigger.builds.mathilda.hacks as hacks
    reload(hacks)
    
    eyelashBase = nt.Transform(u'FACE:LT_eye_aimAt_bnd_15')
    aimLoc = nt.Transform(u'FACE:LT_eyelid_upper_ctrl_aimLoc')
    hacks.addEyelashBnd(eyelashBase, aimLoc)
    
    eyelashBase = nt.Transform(u'FACE:LT_eye_aimAt_bnd_18')
    aimLoc = nt.Transform(u'FACE:LT_eyelid_inner_upper_ctrl_aimLoc')
    hacks.addEyelashBnd(eyelashBase, aimLoc)
    
    eyelashBase = nt.Transform(u'FACE:LT_eye_aimAt_bnd_12')
    aimLoc = nt.Transform(u'FACE:LT_eyelid_outer_upper_ctrl_aimLoc')
    hacks.addEyelashBnd(eyelashBase, aimLoc)
    
    eyelashBase = nt.Transform(u'FACE:LT_eye_aimAt_bnd_9')
    aimLoc = nt.Transform(u'FACE:LT_eyelid_outer_ctrl_aimLoc')
    hacks.addEyelashBnd(eyelashBase, aimLoc)
    '''
    pm.select(cl=True)
    bnd = pm.joint(n=aimLoc.replace('_aimLoc', 'eyelash_bnd'))
    
    mat = eyelashBase.getMatrix(worldSpace=True)
    bnd.setMatrix(mat, worldSpace=True)
    eyelashBase | bnd
    
    bne = pm.joint(n=aimLoc.replace('_aimLoc', 'eyelash_bne'),
                   p=aimLoc.getTranslation(space='world'))
    
    #orient jnt
    pm.makeIdentity(bnd, a=True)
    bnd.orientJoint('xyz', sao='yup')
    
    # aim constraint
    pm.aimConstraint(aimLoc, bnd, aim=(1,0,0))

def addEyelashCollideAimLoc(jnt, eyelidCtl, collideCtl):
    '''
    eyeCtl - actually bnd of eye
    jnt - actually a loc (for aiming)
    
    position 4 joints first, then run:
    jnt = nt.Transform(u'locator1')
    eyelidCtl = nt.Transform(u'FACE:LT_eyelid_upper_ctrl')
    collideCtl = nt.Transform(u'FACE:LT_mid_brow_ctrl')
    hacks.addEyelashCollideAimLoc(jnt, eyelidCtl, collideCtl)
    
    jnt = nt.Transform(u'locator2')
    eyelidCtl = nt.Transform(u'FACE:LT_eyelid_inner_upper_ctrl')
    collideCtl = nt.Transform(u'FACE:LT_in_brow_ctrl')
    hacks.addEyelashCollideAimLoc(jnt, eyelidCtl, collideCtl)
    
    jnt = nt.Transform(u'locator3')
    eyelidCtl = nt.Transform(u'FACE:LT_eyelid_outer_upper_ctrl')
    collideCtl = nt.Transform(u'FACE:LT_out_brow_ctrl')
    hacks.addEyelashCollideAimLoc(jnt, eyelidCtl, collideCtl)
    
    jnt = nt.Transform(u'locator4')
    eyelidCtl = nt.Transform(u'FACE:LT_eyelid_outer_ctrl')
    collideCtl = nt.Transform(u'FACE:LT_out_brow_ctrl')
    hacks.addEyelashCollideAimLoc(jnt, eyelidCtl, collideCtl)
    '''
    name = eyelidCtl.replace('_bnd','_eyelash')
    jnt.rename(name+'_aimLoc')
    # build hierarchy
    # one nodes on the collideCtl
    grp = pm.group(em=True, n=name+'_upLimit_grp')
    
    # two nodes on the eyelidCtl
    offset = pm.group(em=True, n=name+'_offset')
    collide = pm.group(offset, n=name+'_collide')
    mat = jnt.getMatrix(worldSpace=True)
    collide.setMatrix(mat, worldSpace=True)
    offset | jnt
    
    # get bnds in local-rig space
    eyelidBnd = pm.PyNode(eyelidCtl.replace('_ctrl','_bnd'))
    collideBnd = pm.PyNode(collideCtl.replace('_ctrl','_bnd'))
    
    # constraint to collideBnd
#     dcm = pm.createNode('decomposeMatrix', n=name+'_constraintCollide_dcm')
#     collideBnd.worldMatrix >> dcm.inputMatrix
#     dcm.outputTranslate >> grp.t
#     dcm.outputRotate >> grp.r
    pm.pointConstraint(collideBnd, grp)
    
    # constraint to collideBnd
#     dcm = pm.createNode('decomposeMatrix', n=name+'_constraintEyelid_dcm')
#     mm = pm.createNode('multMatrix', n=name+'_constraintEyelid_mm')
#     eyelidBnd.worldMatrix >> mm.matrixIn[0]
#     collide.parentInverseMatrix >> mm.matrixIn[1]
#     mm.matrixSum>> dcm.inputMatrix
#     dcm.outputTranslate >> collide.t
#     dcm.outputRotate >> collide.r
    pm.parentConstraint(eyelidBnd, collide, mo=True)
    grp | collide
    
    # ceiling val
    jnt.addAttr('transY_ceiling', at='float', k=True)
    collide.maxTransYLimitEnable.set(True)
    jnt.attr('transY_ceiling') >> collide.maxTransYLimit
    
    
    

def connectHairToGlobalScale():
    '''
    import rigger.builds.mathilda.hacks as hacks
    reload(hacks)
    hacks.connectHairToGlobalScale()
    '''
    
    crvGrp = nt.Transform(u'CT_hairStartCurves_grp')
    mesh = nt.Transform(u'CT_headHair_geo')
    root = nt.Transform(u'Mathilda_root_ctrl')
    
    # connect masterscale to scale curves
    root.masterScale >> crvGrp.sx
    root.masterScale >> crvGrp.sy
    root.masterScale >> crvGrp.sz
    
    # multiply matrix for follicles
    mm = pm.createNode('multMatrix', n='CT_hairFolliclesGlobalScale_mm')
    mesh.worldMatrix >> mm.matrixIn[0]
    crvGrp.worldInverseMatrix >> mm.matrixIn[1]
    
    # get all follicles
    allFols = crvGrp.getChildren(ad=True, type='follicle')
    
    # connect worldMatrix
    for fol in allFols:
        mm.matrixSum >> fol.inputWorldMatrix
    
    # scale hairSystems
    attrsToScale = ['backHairSystemShape.clumpWidth',
                    'backHairSystemShape.hairWidth',
                    'frontHairSystemShape.clumpWidth',
                    'frontHairSystemShape.hairWidth']
    for attr in attrsToScale:
        mod = modulate.multiplyInput(attr, 1, '_gscale')
        root.masterScale >> mod
    

def connectHairFolliclesToMesh():
    '''
    for each follicle under hairCrvsGrp,
    - unparent the child curve to WS (to maintain ws-position)
    - find closest uv on mesh
    - set uv on follicle
    - mesh.worldMatrix >> follicle.inputWorldMatrix
    - mesh.outMesh >> follicle.inputMesh
    - follicle.outT/R >> follicleDag.t/r
    - reparent curve under follicle
    '''
    mesh = nt.Transform(u'CT_headCollide_geo')
    hairCrvsGrp = nt.Transform(u'CT_hairCurves_grp')
    
    allFollicles = hairCrvsGrp.getChildren(ad=True, type='follicle')
    
    for eachFol in allFollicles:
        folDag = eachFol.getParent()
        # assume only one curve per follicle
        crvDag = folDag.getChildren(ad=True, type='transform')[0]
        
        # unparent to maintain WS
        crvDag.setParent(None)
        
        # calculate UVs
        startPt = crvDag.cv[0].getPosition()
        uVal, vVal = mesh.getUVAtPoint(startPt)
        uvSet = mesh.getCurrentUVSetName()
        eachFol.parameterU.set(uVal)
        eachFol.parameterV.set(vVal)
        eachFol.startDirection.set(1)
        
        # connect mesh to follicle
        mesh.worldMatrix >> eachFol.inputWorldMatrix
        mesh.outMesh >> eachFol.inputMesh
        
        # connect follicle t/r
        eachFol.outTranslate >> folDag.t
        eachFol.outRotate >> folDag.r
        
        # parent curve under follicle
        folDag | crvDag
        

def faceEvaluationSwitch():
    '''
    find all deformers on geos
    when switchAttr = False,
    set nodes to HasNoEffect
    '''
    geos = [nt.Transform(u'FACE:LT_eyelashes_geo'),
            nt.Transform(u'FACE:RT_eyelashes_geo'),
            nt.Transform(u'FACE:CT_face_geo'),
            nt.Transform(u'CT_face_geo_lattice'),
            nt.Transform(u'CT_face_geo_latticeWeights')]
    
    # add switch to face ctrl
    faceCtl = pm.PyNode('FACE:CT_face_ctrl')
    faceCtl.addAttr('disableFace', at='bool', dv=0)
    faceCtl.attr('disableFace').showInChannelBox(True)
    
    for geo in geos:
        dfmNames = mel.findRelatedDeformer(geo)
        for dfmName in dfmNames:
            dfm = pm.PyNode(dfmName)
            faceCtl.attr('disableFace') >> dfm.nodeState
            
    # also hide inner mouth geo
    mouthGeoGrp = pm.PyNode('FACE:CT_mouth_geo_grp')
    rt.connectSDK(faceCtl.attr('disableFace'), 
                  mouthGeoGrp.v, {0:1, 1:0})
        

def addJacketCollarNoRotBinds():
    # add collar joint no-rotate
    collarjnts = pm.ls(sl=True)
    
    for jnt in collarjnts:
        pm.select(cl=True)
        noRotJnt = pm.joint(n=jnt.replace('_jnt', '_norot_bnd'))
        wMat = jnt.getMatrix(worldSpace=True)
        noRotJnt.setMatrix(wMat, worldSpace=True)
        pm.makeIdentity(noRotJnt, a=True)
        noRotJnt.radius.set(0.5)
        grp = jnt.getParent(3)
        grp | noRotJnt
        pm.pointConstraint(jnt, noRotJnt)

def addJacketCollarRig():
    # jacket collar rig
    collarjnts = pm.ls(sl=True)
    # add hm, grp and auto nulls
    for jnt in collarjnts:
        ctl = pm.circle(r=0.5, sweep=359, normal=(1,0,0), n=jnt.replace('_jnt', '_ctl'))
        auto = pm.group(ctl, n=jnt.replace('_jnt', '_auto'))
        grp = pm.group(auto, n=jnt.replace('_jnt', '_grp'))
        hm = pm.group(grp, n=jnt.replace('_jnt', '_hm'))
        wMat = jnt.getMatrix(worldSpace=True)
        hm.setMatrix(wMat, worldSpace=True)
        collarparent = jnt.getParent()
        collarparent | hm
        auto | jnt
    # auto
    import rigger.modules.poseReader as poseReader
    reload(poseReader)
    xfo = nt.Joint(u'Mathilda_neck_jnt')
    poseReader.radial_pose_reader(xfo, (1,0,0), (1,0,0))
    # connect auto to sdks
    import utils.rigging as rt
    import rigger.utils.modulate as modulate
    angleMult = pm.PyNode('Mathilda_neck_jnt.vectorAngle')
    # Left collar A
    rt.connectSDK('Mathilda_neck_jnt.param', 'LT_collarA_auto.rz',
                    {3.25:0, 4.6:50, 5.5:0})
    mod = modulate.multiplyInput(pm.PyNode('LT_collarA_auto.rz'), 0, '_angle')
    angleMult >> mod
    # Letf collar B
    rt.connectSDK('Mathilda_neck_jnt.param', 'LT_collarB_auto.rz',
                    {4:0, 5:180, 6:180, 7:0})
    mod = modulate.multiplyInput(pm.PyNode('LT_collarB_auto.rz'), 0, '_angle')
    angleMult >> mod
    # Letf collar C
    rt.connectSDK('Mathilda_neck_jnt.param', 'LT_collarC_auto.rz',
                    {0:200, 1.4:0, 4:0, 5.5:200, 6.6:280, 8:0})
    mod = modulate.multiplyInput(pm.PyNode('LT_collarC_auto.rz'), 0, '_angle')
    angleMult >> mod
    # center collar
    rt.connectSDK('Mathilda_neck_jnt.param', 'CT_collar_auto.rz',
                    {0:320, 2.5:0, 5.5:0, 8:320})
    mod = modulate.multiplyInput(pm.PyNode('CT_collar_auto.rz'), 0, '_angle')
    angleMult >> mod
    # right collar A
    rt.connectSDK('Mathilda_neck_jnt.param', 'RT_collarA_auto.rz',
                    {4.75:0, 3.4:50, 2.5:0})
    mod = modulate.multiplyInput(pm.PyNode('RT_collarA_auto.rz'), 0, '_angle')
    angleMult >> mod
    # right collar B
    rt.connectSDK('Mathilda_neck_jnt.param', 'RT_collarB_auto.rz',
                    {4:0, 3:180, 2:180, 1:0})
    mod = modulate.multiplyInput(pm.PyNode('RT_collarB_auto.rz'), 0, '_angle')
    angleMult >> mod
    # right collar C
    rt.connectSDK('Mathilda_neck_jnt.param', 'RT_collarC_auto.rz',
                    {0:200, 6.6:0, 4:0, 2.5:200, 1.4:280, 8:0})
    mod = modulate.multiplyInput(pm.PyNode('RT_collarC_auto.rz'), 0, '_angle')
    angleMult >> mod
    
    pm.select(pm.PyNode(u'Mathilda_neck_jnt.param').outputs())