from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL.ARB.shader_objects import *
from OpenGL.GL.ARB.vertex_shader import *
from OpenGL.GL.ARB.fragment_shader import *
from OpenGL.GL.ARB.multitexture import *
from OpenGL.arrays import vbo
from OpenGL.arrays import ArrayDatatype as adt
from OpenGL.GL.ARB.vertex_buffer_object import *
from OpenGL.GL.ARB.framebuffer_object import *
from OpenGL.GL.EXT.framebuffer_object import *
from time import *
import Image
import freenect
import numpy as np
from shaderProg01 import *
import os, fnmatch, re

glGenTextures(4)
tview = 4
slview = 0
sllg, slrlg = 0.05, 0.04
slh, slb = 0.7,-0.7
slz,slrz = 0.2,0.22
slx = [-1.1, -1.0, -0.9, -0.8, 0.4, 0.6, 0.7, 0.9, 1.0, 1.1, -0.6, -0.5, -0.4, -0.3, -0.1, 0.0, 0.1, 0.2]
nbslid = len(slx)
sld = []
slrd = []
slbv = []
slrbv = []
ratioK = 0.75
ratioT = 0.5625
knmin,knmax = 50,900
scaletex = 0.75
nbtex = 1
erodew = erodeh = 0.0
text = "0.0"
shdiv = [0,0,0,0,1,0,1,1]
shfrq = [1.0, 1.0]
near = GL_NEAREST
line = GL_LINEAR
filt = near
reap = GL_REPEAT
clam = GL_CLAMP
cled = GL_CLAMP_TO_EDGE
wrap = cled
invH = -1.0
invL = 1.0
sizedp = [0,0,800,600]
rep = os.getcwd()
scen = newscen = 0

def init():
    global matvbo, gbv, gbt, fbv, fbt, knt, t, sld, slbv, sD, knmin, knmax, knminplus, matKn, maskv, nbt, gtex, scaletex, erodew, erodeh
    print "esc to quit"
    rep = os.getcwd()
    imtex = []
    sD = range(18)
    glInitMultitextureARB()
    initShaders1( )
    initShaders2( )
    initShaders3( )
    initShaders4( )
    gtex = textureFold()
    glActiveTextureARB(GL_TEXTURE0_ARB)
    im3d, sz, nbtex3d, filt = texture3D(gtex[scen], 20)
    glBind3Dcol(im3d, 0, sz,  nbtex3d, filt)
    im = Image.open("bleu.jpg").convert("RGBA")
    im = im.tostring("raw","RGBA",0,-1)
    glActiveTextureARB(GL_TEXTURE1_ARB)
    glBind2Dcol(im, 1, (50,50))
    im = Image.open("rouge.jpg").convert("RGBA")
    im = im.tostring("raw","RGBA",0,-1)
    glActiveTextureARB(GL_TEXTURE2_ARB)
    glBind2Dcol(im, 2, (50,50))
    fdata = open('dataSave.txt', 'r')
    f = fdata.readlines()
    slhr = range(nbslid)
    for i in range(nbslid):
        slhr[i]=sD[i]=f[i]
    sizedp[0]=4*int(((float(f[0])/2.0)+0.5)*200.0)
    sizedp[2]=4*int(((float(f[2])/2.0)+0.5)*200.0)
    sizedp[1]=int((float(f[1])+1.0)*300.0)
    sizedp[3]=int((float(f[3])+1.0)*300.0)
    scaletex=float(f[4])+1.0
    erodew=float(f[5])*0.1
    erodeh=float(f[6])*0.1
    knmin=int((float(f[7])+1.0)*500.0)+300
    knminplus=int((float(f[8])+1.0)*200.0)
    for i in range(8):
        shdiv[i]=float(f[i+10])
    knmax=knmin+knminplus
    propimage = 0.5625
    maskv = np.array([[-1*scaletex*invL+erodew,scaletex*propimage*invH+erodeh,0.1],
                                     [-1*scaletex*invL,-1*scaletex*propimage*invH,0.1],
                                     [scaletex*invL,-1*scaletex*propimage*invH,0.1],
                                     [scaletex*invL,scaletex*propimage*invH,0.1]],'f')
    matt = np.array([[0,1],[0,0],[1,0],[1,1]],'f')
    matKn = np.array([[0,1],[0,0],[1,0],[1,1]],'f')
    for i in range(nbslid):
        slxv = slx[i]
        sld.append(np.array([[slxv-sllg,slh,slz],[slxv-sllg,slb,slz],[slxv+sllg,slb,slz],[slxv+sllg,slh,slz]],'f'))
        slrxv = slx[i]
        slrd.append(np.array([[slrxv-slrlg,slhr[i],slrz],[slrxv-slrlg,slb,slrz],[slrxv+slrlg,slb,slrz],[slrxv+slrlg,slhr[i],slrz]],'f'))
    gbv = glGenBuffersARB(1)
    glBindBufferARB(GL_ARRAY_BUFFER_ARB, gbv)
    glBufferDataARB( GL_ARRAY_BUFFER_ARB, maskv, GL_STATIC_DRAW_ARB )
    gbt = glGenBuffersARB(1)
    glBindBufferARB(GL_ARRAY_BUFFER_ARB, gbt)
    glBufferDataARB( GL_ARRAY_BUFFER_ARB, matt, GL_STATIC_DRAW_ARB )
    fbv = glGenBuffersARB(1)
    glBindBufferARB(GL_ARRAY_BUFFER_ARB, fbv)
    glBufferDataARB( GL_ARRAY_BUFFER_ARB, maskv, GL_STATIC_DRAW_ARB )
    knt = glGenBuffersARB(1)
    glBindBufferARB(GL_ARRAY_BUFFER_ARB, knt)
    glBufferDataARB( GL_ARRAY_BUFFER_ARB, matKn, GL_STATIC_DRAW_ARB )
    for i in range(nbslid):
        slbv.append(glGenBuffersARB(1))
        glBindBufferARB(GL_ARRAY_BUFFER_ARB, slbv[i])
        glBufferDataARB( GL_ARRAY_BUFFER_ARB, sld[i], GL_STATIC_DRAW_ARB )
        slrbv.append(glGenBuffersARB(1))
        glBindBufferARB(GL_ARRAY_BUFFER_ARB, slrbv[i])
        glBufferDataARB( GL_ARRAY_BUFFER_ARB, slrd[i], GL_STATIC_DRAW_ARB )

    glShadeModel(GL_SMOOTH)
    glMatrixMode( GL_PROJECTION )
    glLoadIdentity()
    gluOrtho2D( -1.5, 1.5, -1.5*ratioT, 1.5*ratioT)
    glMatrixMode( GL_MODELVIEW )

def textureFold():
    global nbfold
    folder = []
    gdir = []
    for file in os.listdir('./Images/'):
        if os.path.isdir('./Images/'+file):
            folder.append('/Images/'+file)
    folder.sort()
    nbfold = len(folder)
    for dir in folder:
        group = []
        for file in os.listdir('./'+dir):        
            if not re.match("\.", file) and (fnmatch.fnmatch(file, '*.jpg') or fnmatch.fnmatch(file, '*.tif')):     
                group.append(file)
        group.sort()
        group.insert(0, dir)
        group.insert(0, 'i')
        gdir.append(group)
    return gdir

def texture3D(tf, nb):
    global szt
    if tf[0] == "i" : tfilter = near
    if tf[0] == "v" : tfilter = line
    if  len(tf)-1<nb:
        nb = len(tf)-2
    else:
        nb = nb-2
    file = rep+tf[1]+"/"+tf[2]
    imi = Image.open(file).convert("RGBA")
    size = imi.size
    img = imi.tostring("raw","RGBA",0,1)
    for j in range(nb-1):
        file = rep+tf[1]+"/"+tf[j+3]
        imi = Image.open(file).convert("RGBA")
        imi = imi.tostring("raw","RGBA",0,1)
        img += imi
    szt = size[0]/float(size[1])
    return img , size, nb, tfilter

def initShaders1( ):
    global sPmask
    sPmask = ShaderProgram( )    
    sPmask.addShader( GL_VERTEX_SHADER_ARB, "mask.vert" )
    sPmask.addShader( GL_FRAGMENT_SHADER_ARB, "mask.frag" )
    sPmask.linkShaders( )

def initShaders2( ):
    global sPpass
    sPpass = ShaderProgram( )    
    sPpass.addShader( GL_VERTEX_SHADER_ARB, "pass.vert" )
    sPpass.addShader( GL_FRAGMENT_SHADER_ARB, "pass.frag" )
    sPpass.linkShaders( )

def initShaders3( ):
    global sPalpha
    sPalpha = ShaderProgram( )    
    sPalpha.addShader( GL_VERTEX_SHADER_ARB, "alpha.vert" )
    sPalpha.addShader( GL_FRAGMENT_SHADER_ARB, "alpha.frag" )
    sPalpha.linkShaders( )

def initShaders4( ):
    global sP3d
    sP3d = ShaderProgram( )    
    sP3d.addShader( GL_VERTEX_SHADER_ARB, "texture3D.vert" )
    sP3d.addShader( GL_FRAGMENT_SHADER_ARB, "texture3D.frag" )
    sP3d.linkShaders( )


y = 1.0
x = y*1.333
z1 = 0.0
nbtex1 = 1
def display(*args):
    global t, aaa, shrad, maskv, text, nbtex, nbtex1
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    glLoadIdentity()
    glTexEnvfv(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    if tview == 4:
	glClearColor(0.0,0.0, 0.0, 1.0)
        glEnable(GL_TEXTURE_3D)
        sP3d.enable()
        glUniform1iARB(sP3d.indexOfUniformVariable("tex0"), 0)
        glUniform1iARB(sP3d.indexOfUniformVariable("tex1"), 3)
        glBegin(GL_QUADS)

        glMultiTexCoord2fARB( GL_TEXTURE3_ARB, 0.0, 1.0 )
        glMultiTexCoord3fARB( GL_TEXTURE0_ARB, 0.0, 1.0, 0.0 )
        glVertex3f(maskv[0][0], maskv[0][1], 0.0)
        

        glMultiTexCoord2fARB( GL_TEXTURE3_ARB, 0.0, 0.0 )
        glMultiTexCoord3fARB( GL_TEXTURE0_ARB, 0.0, 0.0, 0.0 )
        glVertex3f(maskv[1][0], maskv[1][1], 0.0)
        

        glMultiTexCoord2fARB( GL_TEXTURE3_ARB, 1.0, 0.0 )
        glMultiTexCoord3fARB( GL_TEXTURE0_ARB, 1.0, 0.0, 0.0)
        glVertex3f(maskv[2][0], maskv[2][1], 0.0)
        

        glMultiTexCoord2fARB( GL_TEXTURE3_ARB, 1.0, 1.0 )
        glMultiTexCoord3fARB( GL_TEXTURE0_ARB, 1.0, 1.0, 0.0)
        glVertex3f(maskv[3][0], maskv[3][1], 0.0)
 
        glEnd()

    if tview == 0:
	glClearColor(0.0,0.0, 0.0, 1.0)
        sPpass.enable()
        #glUniform1iARB(sPpass.indexOfUniformVariable("tex0"), t[1])
        glUniform1iARB(sPpass.indexOfUniformVariable("tex0"), t[nbtex1])
        #glUniform4fARB(sPpass.indexOfUniformVariable("radius"), shrad[0],shrad[1])
        #glUniformMatrix2fvARB(sPpass.indexOfUniformVariable("origin"),2,0, shrad)
        #glUniformMatrix2fvARB(sPpass.indexOfUniformVariable("offset"),2,0, shfrq)
        #glUniform1fARB(sPpass.indexOfUniformVariable("width"), erodew)
        #glUniform1fARB(sPpass.indexOfUniformVariable("height"), erodeh)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(maskv[0][0], maskv[0][1], 0.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(maskv[1][0], maskv[1][1], 0.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(maskv[2][0], maskv[2][1], 0.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(maskv[3][0], maskv[3][1], 0.0)         
        glEnd()   
        sPpass.disable()

        sPmask.enable()
        glUniform1iARB(sPmask.indexOfUniformVariable("tex0"), t[nbtex])
        glUniform1iARB(sPmask.indexOfUniformVariable("tex1"), t[0])
        
        glBegin(GL_QUADS)

        glMultiTexCoord2fARB( glacttex[0], shdiv[0], 1.0-shdiv[1] )
        glMultiTexCoord2fARB( glacttex[1], 0.0, 0.0 )
        glVertex3f(maskv[0][0], maskv[0][1], 0.0)
        
        glMultiTexCoord2fARB( glacttex[0], shdiv[2], shdiv[3] )
        glMultiTexCoord2fARB( glacttex[1], 0.0, 1.0 )
        glVertex3f(maskv[1][0], maskv[1][1], 0.0)
        
        glMultiTexCoord2fARB( glacttex[0], 1.0+shdiv[4], shdiv[5])
        glMultiTexCoord2fARB( glacttex[1], 1.0, 1.0 )
        glVertex3f(maskv[2][0], maskv[2][1], 0.0)
        
        glMultiTexCoord2fARB( glacttex[0], 1.0+shdiv[6], 1.0-shdiv[7])
        glMultiTexCoord2fARB( glacttex[1], 1.0, 0.0 )
        glVertex3f(maskv[3][0], maskv[3][1], 0.0)

        glEnd()
        sPmask.disable()
        
    if tview == 1 or tview == 3:
	glClearColor(1.5,0.0, 0.0, 1.0)
        sPpass.enable()
        #glUniform1iARB(sPpass.indexOfUniformVariable("tex0"), t[1])
        glUniform1iARB(sPpass.indexOfUniformVariable("tex0"), 3)
        #glUniform4fARB(sPpass.indexOfUniformVariable("radius"), shrad[0],shrad[1])
        #glUniformMatrix2fvARB(sPpass.indexOfUniformVariable("origin"),2,0, shrad)
        #glUniformMatrix2fvARB(sPpass.indexOfUniformVariable("offset"),2,0, shfrq)
        #glUniform1fARB(sPpass.indexOfUniformVariable("width"), erodew)
        #glUniform1fARB(sPpass.indexOfUniformVariable("height"), erodeh)
        glBegin(GL_QUADS)
        glTexCoord2f(shdiv[0], 1.0-shdiv[1])
        glVertex3f(maskv[0][0], maskv[0][1], 0.0)
        glTexCoord2f(shdiv[2], shdiv[3])
        glVertex3f(maskv[1][0], maskv[1][1], 0.0)
        glTexCoord2f(1.0+shdiv[4], shdiv[5])
        glVertex3f(maskv[2][0], maskv[2][1], 0.0)
        glTexCoord2f(1.0+shdiv[6], 1.0-shdiv[7])
        glVertex3f(maskv[3][0], maskv[3][1], 0.0)         
        glEnd()   
        sPpass.disable()
    

    
    if slview == 1:
        sPalpha.enable()
        for i in range(nbslid):
            glUniform1iARB(sPalpha.indexOfUniformVariable("tex0"), 1)
            glEnableClientState(GL_VERTEX_ARRAY)
            glEnableClientState(GL_TEXTURE_COORD_ARRAY)
            glBindBufferARB(GL_ARRAY_BUFFER_ARB, slbv[i])
            glVertexPointer( 3, GL_FLOAT, 0, None )
            glBindBufferARB(GL_ARRAY_BUFFER_ARB, gbt)
            glTexCoordPointer( 2, GL_FLOAT, 0, None)
            glDrawArrays(GL_QUADS, 0, 4)
            glDisableClientState(GL_VERTEX_ARRAY)
            glDisableClientState(GL_TEXTURE_COORD_ARRAY)

            glUniform1iARB(sPalpha.indexOfUniformVariable("tex0"), 2)
            glEnableClientState(GL_VERTEX_ARRAY)
            glEnableClientState(GL_TEXTURE_COORD_ARRAY)
            glBindBufferARB(GL_ARRAY_BUFFER_ARB, slrbv[i])
            glVertexPointer( 3, GL_FLOAT, 0, None )
            glBindBufferARB(GL_ARRAY_BUFFER_ARB, gbt)
            glTexCoordPointer( 2, GL_FLOAT, 0, None)
            glDrawArrays(GL_QUADS, 0, 4)
            glDisableClientState(GL_VERTEX_ARRAY)
            glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        sPalpha.disable()

    glutSwapBuffers (  )

def glBind2Dlum(im,idt, size):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, idt)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, size[0], size[1], 0, GL_LUMINANCE, GL_UNSIGNED_BYTE, im)
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER )
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER )
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )

def glBind2Dcol(im,idt, size):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, idt)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, size[0], size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, im)
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP )
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP )
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )

def glBind3Dcol(im,idt, size, nb, filt):
    glEnable(GL_TEXTURE_3D)
    glBindTexture(GL_TEXTURE_3D, idt)
    glTexImage3D(GL_TEXTURE_3D, 0, GL_RGBA, size[0], size[1], nb, 0, GL_RGBA, GL_UNSIGNED_BYTE, im)
    glTexParameterf( GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, cled )
    glTexParameterf( GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, cled )
    glTexParameterf( GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, cled )
    glTexParameterf( GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, filt )
    glTexParameterf( GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, filt )    

bl = 0.0
def DepthGet():
    global text, bl
    knlen = knmax-knmin
    depth1, timestamp = freenect.sync_get_depth()
    depth1 = depth1[sizedp[1]:sizedp[3],sizedp[0]:sizedp[2]]
    dpxsz = sizedp[2]-sizedp[0]
    dpysz = sizedp[3]-sizedp[1]
    np.resize(depth1,(dpysz,dpxsz))
    dpmin = depth1.min()
    dmin = depth1>=knmin
    if tview==3 : depth = 255*(np.logical_and(dmin, depth1<=knmax))    
    np.clip(depth1, knmin, knmax, out=depth1)
    dmask = depth1-knmin
    if tview == 4:depth = 255*(1.0-((dmin*dmask)/float(knlen)))
    #if tview == 3:depth = 255*(1.0-((dmin*dmask)/float(knlen)))
    if tview==1 or tview == 0:depth = 255*dmax
    depth = depth.flatten()
    return depth, (dpxsz,dpysz)

levB = 0
def animationStep( *args ):
    global t, nbtex, scen, newscen, nbt, gtex
    if scen!=newscen:
        glActiveTextureARB(GL_TEXTURE0_ARB)
        im3d, sz, nbtex3d, filt = texture3D(gtex[scen-1], 20)
        glBind3Dcol(im3d, 0, sz,  nbtex3d, filt)
        newscen = scen
    kn, newsize = DepthGet()
    glActiveTextureARB(GL_TEXTURE3_ARB)
    glBind2Dlum(kn, 3, newsize)
    glutPostRedisplay( )

def souris(but, sta, x , y):
    global onsl
    onsl = -1
    gly = -1.0*(y*(3*ratioT/1024.0)-(1.5*ratioT))
    glx = x*(3/1280.0)-1.5
    if gly>=slb and gly<=slh:
        for i in range(nbslid):
            if glx>=sld[i][0][0] and glx<=sld[i][3][0]:
                onsl = i

def sel(x, y):
    global slgly, knmin, knmax, knminplus, erodew, erodeh, shrad, shfrq, text, maskv, scaletex
    gly = -1.0*(y*(3*ratioT/1024.0)-(1.5*ratioT))
    glx = x*(3/1280.0)-1.5
    if onsl!=-1:
        slrd[onsl][0][1] = gly
        slrd[onsl][3][1] = gly
        if onsl==0:
            szgly = 4*int(((gly/2.0)+0.5)*200.0)
            if szgly<sizedp[2] and szgly>=0:
                glBindBufferARB(GL_ARRAY_BUFFER_ARB, slrbv[onsl])
                glBufferDataARB( GL_ARRAY_BUFFER_ARB, slrd[onsl], GL_STATIC_DRAW_ARB )
                sizedp[0]=szgly
                saveData(0, gly)
        if onsl==2:
            szgly = 4*int(((gly/2.0)+0.5)*200.0)
            if szgly>sizedp[0] and szgly<=640:
                glBindBufferARB(GL_ARRAY_BUFFER_ARB, slrbv[onsl])
                glBufferDataARB( GL_ARRAY_BUFFER_ARB, slrd[onsl], GL_STATIC_DRAW_ARB )
                sizedp[2]=szgly
                saveData(2, gly)
        if onsl==1:
            szgly = int((gly+1.0)*300.0)
            if szgly<sizedp[3] and szgly>=0:
                glBindBufferARB(GL_ARRAY_BUFFER_ARB, slrbv[onsl])
                glBufferDataARB( GL_ARRAY_BUFFER_ARB, slrd[onsl], GL_STATIC_DRAW_ARB )
                sizedp[1]=szgly
                saveData(1, gly)
        if onsl==3:
            szgly = int((gly+1.0)*300.0)
            if szgly>sizedp[1] and szgly<=480:
                glBindBufferARB(GL_ARRAY_BUFFER_ARB, slrbv[onsl])
                glBufferDataARB( GL_ARRAY_BUFFER_ARB, slrd[onsl], GL_STATIC_DRAW_ARB )
                sizedp[3]=szgly
                saveData(3, gly)
        if onsl==4:
            szgly = int((gly+1.0)*2048.0)
            if szgly>0:
                glBindBufferARB(GL_ARRAY_BUFFER_ARB, slrbv[onsl])
                glBufferDataARB( GL_ARRAY_BUFFER_ARB, slrd[onsl], GL_STATIC_DRAW_ARB )
                scaletex = gly+1.0
                maskv = np.array([[-1*scaletex*invL+erodew,scaletex*ratioT*invH+erodeh,0.1],
                                     [-1*scaletex*invL,-1*scaletex*ratioT*invH,0.1],
                                     [scaletex*invL,-1*scaletex*ratioT*invH,0.1],
                                     [scaletex*invL,scaletex*ratioT*invH,0.1]],'f')
                saveData(4, gly)
                text = str("maskv"+str(gly))
        if onsl==5:
            glBindBufferARB(GL_ARRAY_BUFFER_ARB, slrbv[onsl])
            glBufferDataARB( GL_ARRAY_BUFFER_ARB, slrd[onsl], GL_STATIC_DRAW_ARB )
            erodew = gly*0.1
            maskv = np.array([[-1*scaletex*invL+erodew,scaletex*ratioT*invH+erodeh,0.1],
                                 [-1*scaletex*invL,-1*scaletex*ratioT*invH,0.1],
                                 [scaletex*invL,-1*scaletex*ratioT*invH,0.1],
                                 [scaletex*invL,scaletex*ratioT*invH,0.1]],'f')
            saveData(5, gly)
        if onsl==6:
            glBindBufferARB(GL_ARRAY_BUFFER_ARB, slrbv[onsl])
            glBufferDataARB( GL_ARRAY_BUFFER_ARB, slrd[onsl], GL_STATIC_DRAW_ARB )
            erodeh = gly*0.1
            maskv = np.array([[-1*scaletex*invL+erodew,scaletex*ratioT*invH+erodeh,0.1],
                                 [-1*scaletex*invL,-1*scaletex*ratioT*invH,0.1],
                                 [scaletex*invL,-1*scaletex*ratioT*invH,0.1],
                                 [scaletex*invL,scaletex*ratioT*invH,0.1]],'f')
            saveData(6, gly)
        if onsl==7:
            szgly = int((gly+1.0)*500.0)+300
            if szgly>0:
                glBindBufferARB(GL_ARRAY_BUFFER_ARB, slrbv[onsl])
                glBufferDataARB( GL_ARRAY_BUFFER_ARB, slrd[onsl], GL_STATIC_DRAW_ARB )
                knmin = szgly
                knmax = knmin+knminplus
		print knmin, knminplus, knmax
                saveData(7, gly)
        if onsl==8:
            szgly = int((gly+1.0)*200.0)
            if  knmin+szgly<2048 and szgly>0:
                glBindBufferARB(GL_ARRAY_BUFFER_ARB, slrbv[onsl])
                glBufferDataARB( GL_ARRAY_BUFFER_ARB, slrd[onsl], GL_STATIC_DRAW_ARB )
                knminplus = szgly
                knmax = knmin+knminplus
		print knmin, knminplus, knmax
                saveData(8, gly)
        if onsl==10:           
            shdiv[0] = text = (gly+0.0)*0.2
            glBindBufferARB(GL_ARRAY_BUFFER_ARB, slrbv[onsl])
            glBufferDataARB( GL_ARRAY_BUFFER_ARB, slrd[onsl], GL_STATIC_DRAW_ARB )
            saveData(10, shdiv[0])
        if onsl==11:           
            shdiv[1] = text =  (gly+0.0)*0.2
            glBindBufferARB(GL_ARRAY_BUFFER_ARB, slrbv[onsl])
            glBufferDataARB( GL_ARRAY_BUFFER_ARB, slrd[onsl], GL_STATIC_DRAW_ARB )
            saveData(11, shdiv[1])
        if onsl==12:           
            shdiv[2] = text =  (gly+0.0)*0.2
            glBindBufferARB(GL_ARRAY_BUFFER_ARB, slrbv[onsl])
            glBufferDataARB( GL_ARRAY_BUFFER_ARB, slrd[onsl], GL_STATIC_DRAW_ARB )
            saveData(12, shdiv[2])
        if onsl==13:           
            shdiv[3] = text =  (gly+0.0)*0.2
            glBindBufferARB(GL_ARRAY_BUFFER_ARB, slrbv[onsl])
            glBufferDataARB( GL_ARRAY_BUFFER_ARB, slrd[onsl], GL_STATIC_DRAW_ARB )
            saveData(13, shdiv[3])
        if onsl==14:           
            shdiv[4] = text =  (gly+0.0)*0.2
            glBindBufferARB(GL_ARRAY_BUFFER_ARB, slrbv[onsl])
            glBufferDataARB( GL_ARRAY_BUFFER_ARB, slrd[onsl], GL_STATIC_DRAW_ARB )
            saveData(14, shdiv[4])
        if onsl==15:           
            shdiv[5] = text =  (gly+0.0)*0.2
            glBindBufferARB(GL_ARRAY_BUFFER_ARB, slrbv[onsl])
            glBufferDataARB( GL_ARRAY_BUFFER_ARB, slrd[onsl], GL_STATIC_DRAW_ARB )
            saveData(15, shdiv[5])
        if onsl==16:           
            shdiv[6] = text =  (gly+0.0)*0.2
            glBindBufferARB(GL_ARRAY_BUFFER_ARB, slrbv[onsl])
            glBufferDataARB( GL_ARRAY_BUFFER_ARB, slrd[onsl], GL_STATIC_DRAW_ARB )
            saveData(16, shdiv[6])
        if onsl==17:           
            shdiv[7] = text =  (gly+0.0)*0.2
            glBindBufferARB(GL_ARRAY_BUFFER_ARB, slrbv[onsl])
            glBufferDataARB( GL_ARRAY_BUFFER_ARB, slrd[onsl], GL_STATIC_DRAW_ARB )
            saveData(17, shdiv[7])

def saveData(i, nsave):
    sD[i] = str(nsave)+"\n"

def keyPressed(*args):
    global scen, tview, slview
    try:
        iscen = int(args[0])
    except:
        iscen = 0
    if args[0] == '\x1b':
        sData = open('dataSave.txt', 'w')
        for i in range(len(sD)):
            sData.write(str(sD[i]))
        sData.close()
        glDeleteTextures(4)
        sys.exit()
    if args[0] == 'w':
        if slview==1:slview=0
        else:slview=1
    if args[0] == 'a':
        tview = 3
        glutSetCursor(GLUT_CURSOR_INHERIT)
    if args[0] == 'p':
        tview = 4
        glutSetCursor(GLUT_CURSOR_NONE) 
    if iscen != 0 and iscen <= nbfold: scen = iscen

def ReSizeGLScene(Width, Height):
    if Height == 0:						
        Height = 1
    f = Height/float(Width)
    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()	
    gluOrtho2D( -1.5, 1.5, -1.5*f, 1.5*f)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
def main():    
    glutInit(  )    
    glutInitDisplayMode( GLUT_DOUBLE)
    glutInitWindowSize( 800,600 )
    glutInitWindowPosition( 10, 10 )
    glutCreateWindow("Yo")    
    glutDisplayFunc( display )
    glutReshapeFunc(ReSizeGLScene)
    glutSetCursor(GLUT_CURSOR_NONE)
    #glutFullScreen()
    glutIdleFunc( animationStep )
    glutMouseFunc(souris)
    glutMotionFunc(sel)
    glutKeyboardFunc(keyPressed)
    init()    
    glutMainLoop( )

if __name__ == "__main__":
    main()
