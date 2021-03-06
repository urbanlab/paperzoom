from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL.ARB.shader_objects import *
from OpenGL.GL.ARB.vertex_shader import *
from OpenGL.GL.ARB.fragment_shader import *
from OpenGL.GL.ARB.multitexture import *
from shaderProg01 import *
import os, fnmatch, re
import Image
import random
from time import sleep
import freenect
import numpy as np

near = GL_NEAREST
line = GL_LINEAR
filt = line
reap = GL_REPEAT
clam = GL_CLAMP
cled = GL_CLAMP_TO_EDGE
wrap = cled
rep = os.getcwd()
tview = 0
slidersOn = 0
glacttex = [GL_TEXTURE1_ARB, GL_TEXTURE2_ARB, GL_TEXTURE3_ARB, GL_TEXTURE4_ARB, GL_TEXTURE5_ARB]

def initShaders1( ):
    global sP1
    sP1 = ShaderProgram( )
    sP1.addShader( GL_VERTEX_SHADER_ARB, "ShaderVert01.vert" )
    sP1.addShader( GL_FRAGMENT_SHADER_ARB, "ShaderFrag01.frag" )
    sP1.linkShaders( )
    sP1.enable( )
    glUniform1iARB(sP1.indexOfUniformVariable("tex0"), 0)
    sP1.disable()

def initShaders2( ):
    global sP2
    sP2 = ShaderProgram( )    
    sP2.addShader( GL_VERTEX_SHADER_ARB, "ShaderVert02.vert" )
    sP2.addShader( GL_FRAGMENT_SHADER_ARB, "ShaderFrag02.frag" )
    sP2.linkShaders( )
    sP2.enable( )
    glUniform1iARB(sP2.indexOfUniformVariable("tex0"), 0)
    glUniform1iARB(sP2.indexOfUniformVariable("tex1"), 1)
    sP2.disable()
    
def textureFold():
    folder = []
    for file in os.listdir('./Images/'):
        if os.path.isdir('./Images/'+file):
            folder.append('/Images/'+file)
    folder.sort()
    gdir = []
    for dir in folder:
        group = []
        for file in os.listdir('./'+dir):        
            if not re.match("\.", file) and (fnmatch.fnmatch(file, '*.jpg') or fnmatch.fnmatch(file, '*.tif')):            
                group.append(file)
        group.sort()
        group.insert(0, dir)
        gdir.append(group)
    return gdir

def texture(tf, nb):
    global szt
    if  len(tf)<nb:
        nb = len(tf)-3
    else:
        nb = nb-2
    file = rep+tf[0]+"/"+tf[1]
    imi = Image.open(file).convert("RGBA")
    size = imi.size
    img = imi.tostring("raw","RGBA",0,1)
    for j in range(nb+1):
        file = rep+tf[0]+"/"+tf[j+2]
        imi = Image.open(file).convert("RGBA")
        imi = imi.tostring("raw","RGBA",0,1)
        img += imi
    szt = size[0]/float(size[1])
    return img, size, nb+2

def init():
    global gtex, tid, nb, t
    t = glGenTextures(4)
    xratio = (glutGet(GLUT_SCREEN_WIDTH)/2)
    yratio = glutGet(GLUT_SCREEN_HEIGHT)
    ratio = float(yratio/float(xratio))
    nb = 10
    tid = []
    szt = []
    size = (1280,1024)
    readData()
    gtex = textureFold()
    glInitMultitextureARB()
    initShaders1( )
    initShaders2( )   
    glActiveTextureARB(GL_TEXTURE0_ARB)
    im, sz, nbtex = texture(gtex[0],  nb)
    glBind3Dcol(im, t[0], sz,  nbtex)
    szt = (sz[0]/float(sz[1]))
    vertexPos(0.8,szt,scapl)
    im = Image.open("bleu.jpg").convert("RGBA")
    im = im.tostring("raw","RGBA",0,-1)
    glActiveTextureARB(GL_TEXTURE1_ARB)
    glBind2Dcol(im, t[2], (50,50))
    im = Image.open("rouge.jpg").convert("RGBA")
    im = im.tostring("raw","RGBA",0,-1)
    glActiveTextureARB(GL_TEXTURE2_ARB)
    glBind2Dcol(im, t[1], (50,50))
    glShadeModel(GL_SMOOTH)
    glMatrixMode( GL_PROJECTION )
    glLoadIdentity()
    gluOrtho2D( -1.5, 1.5, -1.5, 1.5)
    glMatrixMode( GL_MODELVIEW )

def readData():
    global scapl, fdata, f, n, n2, n3, n4, n5, n6, flipKin, flipTex
    fdata = open('dataSave.txt', 'r')
    f = fdata.readlines()
    scapl = f[0]
    n = float(f[1])
    n2 = float(f[2])
    n3 = float(f[3])
    n4 = float(f[4])
    n5 = float(f[5])
    n6 = float(f[6])
    flipKin = int(f[7])
    flipTex = int(f[8])
    
def saveData(i, nsave):
    f[i] = str(nsave)+"\n"
    
def vertexPos(hvp,szt,scapl) :
    global plc
    sc = float(scapl)
    xa = -1.0*hvp*sc*szt
    xb = -1.0*hvp*sc*szt
    xc = hvp*sc*szt
    xd = hvp*sc*szt
    ya = hvp*sc
    yb = -1.0*hvp*sc
    yc = -1.0*hvp*sc
    yd = hvp*sc
    plc = [(xa,ya),(xb,yb),(xc,yc),(xd,yd)]

lg,hg,dc, n = 0.06, 1.0, 0.02, 0.0
sl1x, sl2x, sl3x, sl4x, sl5x, sl6x = -1.1, -0.9, -0.7, -0.5, -0.3, -0.1
def sliders(n1, n2, n3, n4, n5, n6):
    sl1pos = [(sl1x-lg,hg),(sl1x-lg,-hg),(sl1x+lg,-hg),(sl1x+lg,hg)]
    sl1apos = [(sl1x-(lg-dc),n1),(sl1x-(lg-dc),-hg+dc),(sl1x+(lg-dc),-hg+dc),(sl1x+(lg-dc),n1)]
    sl2pos = [(sl2x-lg,hg),(sl2x-lg,-hg),(sl2x+lg,-hg),(sl2x+lg,hg)]
    sl2apos = [(sl2x-(lg-dc),n2),(sl2x-(lg-dc),-hg+dc),(sl2x+(lg-dc),-hg+dc),(sl2x+(lg-dc),n2)]
    sl3pos = [(sl3x-lg,hg),(sl3x-lg,-hg),(sl3x+lg,-hg),(sl3x+lg,hg)]
    sl3apos = [(sl3x-(lg-dc),n3),(sl3x-(lg-dc),-hg+dc),(sl3x+(lg-dc),-hg+dc),(sl3x+(lg-dc),n3)]
    sl4pos = [(sl4x-lg,hg),(sl4x-lg,-hg),(sl4x+lg,-hg),(sl4x+lg,hg)]
    sl4apos = [(sl4x-(lg-dc),n4),(sl4x-(lg-dc),-hg+dc),(sl4x+(lg-dc),-hg+dc),(sl4x+(lg-dc),n4)]
    sl5pos = [(sl5x-lg,hg),(sl5x-lg,-hg),(sl5x+lg,-hg),(sl5x+lg,hg)]
    sl5apos = [(sl5x-(lg-dc),n5),(sl5x-(lg-dc),-hg+dc),(sl5x+(lg-dc),-hg+dc),(sl5x+(lg-dc),n5)]
    sl6pos = [(sl6x-lg,hg),(sl6x-lg,-hg),(sl6x+lg,-hg),(sl6x+lg,hg)]
    sl6apos = [(sl6x-(lg-dc),n6),(sl6x-(lg-dc),-hg+dc),(sl6x+(lg-dc),-hg+dc),(sl6x+(lg-dc),n6)]
    return sl1pos, sl1apos, sl2pos,  sl2apos, sl3pos,  sl3apos, sl4pos,  sl4apos, sl5pos,  sl5apos, sl6pos,  sl6apos

z1, z2, z3 = 0.0, 0.1, 0.11
zt = 0.0
b = 0
def display(*args):
    global zt, n3, n4, n5, n6, b
    if slidersOn == 1:
        glClearColor(1.0,1.0, 1.0, 1.0)
    else :
        glClearColor(0.0,0.0, 0.0, 1.0)
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    glLoadIdentity()
    glTexEnvfv(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glEnable(GL_TEXTURE_2D)
    glDisable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    if tview == 0:
        glEnable(GL_TEXTURE_3D)
        sP1.disable()
        sP2.enable()
        glUniform1fARB(sP2.indexOfUniformVariable("txs"), n3+1.0)
        glUniform1fARB(sP2.indexOfUniformVariable("tys"), n4+1.0)
        glUniform1fARB(sP2.indexOfUniformVariable("txo"), n5)
        glUniform1fARB(sP2.indexOfUniformVariable("tyo"), n6)
        glUniform1iARB(sP2.indexOfUniformVariable("tex0"), 0)
        glUniform1iARB(sP2.indexOfUniformVariable("tex1"), 3)
        if flipTex == 0:
            glBegin(GL_QUADS)
            glMultiTexCoord2fARB( GL_TEXTURE3_ARB, 1, 1)
            glMultiTexCoord3fARB( GL_TEXTURE0_ARB, 0, 0, zt )
            glVertex3f(plc[0][0], plc[0][1], z1)
            glMultiTexCoord2fARB( GL_TEXTURE3_ARB, 1, 0 )
            glMultiTexCoord3fARB( GL_TEXTURE0_ARB, 0, 1, zt )
            glVertex3f(plc[1][0], plc[1][1], z1)
            glMultiTexCoord2fARB( GL_TEXTURE3_ARB, 0, 0 )
            glMultiTexCoord3fARB( GL_TEXTURE0_ARB, 1, 1, zt )
            glVertex3f(plc[2][0], plc[2][1], z1)
            glMultiTexCoord2fARB( GL_TEXTURE3_ARB, 0, 1 )
            glMultiTexCoord3fARB( GL_TEXTURE0_ARB, 1, 0, zt )
            glVertex3f(plc[3][0], plc[3][1], z1)
            glEnd(  )
        else :
            glBegin(GL_QUADS)
            glMultiTexCoord2fARB( GL_TEXTURE3_ARB, 0, 1 )
            glMultiTexCoord3fARB( GL_TEXTURE0_ARB, 0, 0, zt )
            glVertex3f(plc[2][0], plc[2][1], z1)
            glMultiTexCoord2fARB( GL_TEXTURE3_ARB, 0, 0 )
            glMultiTexCoord3fARB( GL_TEXTURE0_ARB, 0, 1, zt )
            glVertex3f(plc[3][0], plc[3][1], z1)
            glMultiTexCoord2fARB( GL_TEXTURE3_ARB, 1, 0 )
            glMultiTexCoord3fARB( GL_TEXTURE0_ARB, 1, 1, zt )
            glVertex3f(plc[0][0], plc[0][1], z1)
            glMultiTexCoord2fARB( GL_TEXTURE3_ARB, 1, 1 )
            glMultiTexCoord3fARB( GL_TEXTURE0_ARB, 1, 0, zt )
            glVertex3f(plc[1][0], plc[1][1], z1)
            glEnd(  )
    if tview == 1 or tview == 2:
        sP2.disable()
        sP1.enable()
        glDisable(GL_TEXTURE_3D)
        glEnable(GL_TEXTURE_2D)    
        glUniform1iARB(sP1.indexOfUniformVariable("tex0"), 3) # tex kinect
        if flipTex == 0:
            glBegin(GL_QUADS)
            glTexCoord2f(0.0+n5, 0.0+n6)
            glVertex3f(plc[0][0], plc[0][1], z1)
            glTexCoord2f(0.0+n5, n4+1.0+n6)
            glVertex3f(plc[1][0], plc[1][1], z1)
            glTexCoord2f(n3+1.0+n5, n4+1.0+n6)
            glVertex3f(plc[2][0], plc[2][1], z1)
            glTexCoord2f(n3+1.0+n5, 0.0+n6)
            glVertex3f(plc[3][0], plc[3][1], z1)
            glEnd(  )
        else :
            glBegin(GL_QUADS)
            glTexCoord2f(0.0+n5, 0.0+n6)
            glVertex3f(plc[2][0], plc[2][1], z1)
            glTexCoord2f(0.0+n5, n4+1.0+n6)
            glVertex3f(plc[3][0], plc[3][1], z1)
            glTexCoord2f(n3+1.0+n5, n4+1.0+n6)
            glVertex3f(plc[0][0], plc[0][1], z1)
            glTexCoord2f(n3+1.0+n5, 0.0+n6)
            glVertex3f(plc[1][0], plc[1][1], z1)
            glEnd(  )
    if slidersOn == 1:
        glEnable(GL_BLEND)
        sP2.disable()
        sP1.enable()
        glDisable(GL_TEXTURE_3D)
        glEnable(GL_TEXTURE_2D)
        glUniform1iARB(sP1.indexOfUniformVariable("tex0"), 1) # slider back 1
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[0][0][0], sliders(n, n2, n3, n4, n5, n6)[0][0][1], z2)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[0][1][0], sliders(n, n2, n3, n4, n5, n6)[0][1][1], z2)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[0][2][0], sliders(n, n2, n3, n4, n5, n6)[0][2][1], z2)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[0][3][0], sliders(n, n2, n3, n4, n5, n6)[0][3][1], z2)
        glEnd(  )

        glUniform1iARB(sP1.indexOfUniformVariable("tex0"), 2) # slider front 1
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[1][0][0], sliders(n, n2, n3, n4, n5, n6)[1][0][1], z3)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[1][1][0], sliders(n, n2, n3, n4, n5, n6)[1][1][1], z3)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[1][2][0], sliders(n, n2, n3, n4, n5, n6)[1][2][1], z3)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[1][3][0], sliders(n, n2, n3, n4, n5, n6)[1][3][1], z3)
        glEnd(  )
        

        glUniform1iARB(sP1.indexOfUniformVariable("tex0"), 1)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[2][0][0], sliders(n, n2, n3, n4, n5, n6)[2][0][1], z2)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[2][1][0], sliders(n, n2, n3, n4, n5, n6)[2][1][1], z2)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[2][2][0], sliders(n, n2, n3, n4, n5, n6)[2][2][1], z2)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[2][3][0], sliders(n, n2, n3, n4, n5, n6)[2][3][1], z2)
        glEnd(  )

        glUniform1iARB(sP1.indexOfUniformVariable("tex0"), 2)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[3][0][0], sliders(n, n2, n3, n4, n5, n6)[3][0][1], z3)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[3][1][0], sliders(n, n2, n3, n4, n5, n6)[3][1][1], z3)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[3][2][0], sliders(n, n2, n3, n4, n5, n6)[3][2][1], z3)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[3][3][0], sliders(n, n2, n3, n4, n5, n6)[3][3][1], z3)
        glEnd(  )

        glUniform1iARB(sP1.indexOfUniformVariable("tex0"), 1)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[4][0][0], sliders(n, n2, n3, n4, n5, n6)[4][0][1], z2)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[4][1][0], sliders(n, n2, n3, n4, n5, n6)[4][1][1], z2)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[4][2][0], sliders(n, n2, n3, n4, n5, n6)[4][2][1], z2)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[4][3][0], sliders(n, n2, n3, n4, n5, n6)[4][3][1], z2)
        glEnd(  )

        glUniform1iARB(sP1.indexOfUniformVariable("tex0"), 2)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[5][0][0], sliders(n, n2, n3, n4, n5, n6)[5][0][1], z3)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[5][1][0], sliders(n, n2, n3, n4, n5, n6)[5][1][1], z3)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[5][2][0], sliders(n, n2, n3, n4, n5, n6)[5][2][1], z3)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[5][3][0], sliders(n, n2, n3, n4, n5, n6)[5][3][1], z3)
        glEnd(  )
    
        glUniform1iARB(sP1.indexOfUniformVariable("tex0"), 1)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[6][0][0], sliders(n, n2, n3, n4, n5, n6)[6][0][1], z2)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[6][1][0], sliders(n, n2, n3, n4, n5, n6)[6][1][1], z2)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[6][2][0], sliders(n, n2, n3, n4, n5, n6)[6][2][1], z2)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[6][3][0], sliders(n, n2, n3, n4, n5, n6)[6][3][1], z2)
        glEnd(  )

        glUniform1iARB(sP1.indexOfUniformVariable("tex0"), 2)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[7][0][0], sliders(n, n2, n3, n4, n5, n6)[7][0][1], z3)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[7][1][0], sliders(n, n2, n3, n4, n5, n6)[7][1][1], z3)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[7][2][0], sliders(n, n2, n3, n4, n5, n6)[7][2][1], z3)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[7][3][0], sliders(n, n2, n3, n4, n5, n6)[7][3][1], z3)
        glEnd(  )

        glUniform1iARB(sP1.indexOfUniformVariable("tex0"), 1)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[8][0][0], sliders(n, n2, n3, n4, n5, n6)[8][0][1], z2)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[8][1][0], sliders(n, n2, n3, n4, n5, n6)[8][1][1], z2)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[8][2][0], sliders(n, n2, n3, n4, n5, n6)[8][2][1], z2)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[8][3][0], sliders(n, n2, n3, n4, n5, n6)[8][3][1], z2)
        glEnd(  )

        glUniform1iARB(sP1.indexOfUniformVariable("tex0"), 2)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[9][0][0], sliders(n, n2, n3, n4, n5, n6)[9][0][1], z3)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[9][1][0], sliders(n, n2, n3, n4, n5, n6)[9][1][1], z3)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[9][2][0], sliders(n, n2, n3, n4, n5, n6)[9][2][1], z3)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[9][3][0], sliders(n, n2, n3, n4, n5, n6)[9][3][1], z3)
        glEnd(  )

        glUniform1iARB(sP1.indexOfUniformVariable("tex0"), 1)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[10][0][0], sliders(n, n2, n3, n4, n5, n6)[10][0][1], z2)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[10][1][0], sliders(n, n2, n3, n4, n5, n6)[10][1][1], z2)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[10][2][0], sliders(n, n2, n3, n4, n5, n6)[10][2][1], z2)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[10][3][0], sliders(n, n2, n3, n4, n5, n6)[10][3][1], z2)
        glEnd(  )

        glUniform1iARB(sP1.indexOfUniformVariable("tex0"), 2)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[11][0][0], sliders(n, n2, n3, n4, n5, n6)[11][0][1], z3)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[11][1][0], sliders(n, n2, n3, n4, n5, n6)[11][1][1], z3)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[11][2][0], sliders(n, n2, n3, n4, n5, n6)[11][2][1], z3)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(sliders(n, n2, n3, n4, n5, n6)[11][3][0], sliders(n, n2, n3, n4, n5, n6)[11][3][1], z3)
        glEnd(  )

    glutSwapBuffers (  )

def glBind3Dcol(im,idt, size, nb):
    glEnable(GL_TEXTURE_3D)
    glBindTexture(GL_TEXTURE_3D, idt)
    glTexImage3D(GL_TEXTURE_3D, 0, GL_RGBA, size[0], size[1], nb, 0, GL_RGBA, GL_UNSIGNED_BYTE, im)
    glTexParameterf( GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, cled )
    glTexParameterf( GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, cled )
    glTexParameterf( GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, cled )
    glTexParameterf( GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, filt )
    glTexParameterf( GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, filt )
    

def glBind2Dlum(im,idt, size):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, idt)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, size[0], size[1], 0, GL_LUMINANCE, GL_UNSIGNED_BYTE, im)
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, cled )
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, cled )
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, filt )
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, filt )

def glBind2Dcol(im,idt, size):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, idt)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, size[0], size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, im)
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, cled )
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, cled )
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, filt )
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, filt )    

def DepthGet(dimin, dimax):
    global tview
    depth, timestamp = freenect.sync_get_depth()
    dmin = depth>=dimin
    dmax = depth<=dimax
    dmult = np.logical_and(dmin, dmax)
    np.clip(depth, dimin, dimax, out=depth)    
    if tview == 0:
        depth = 255*(1.0-((depth-dimin)*dmin)/float(dimax-dimin))
    if tview == 1 :
        depth = 255*(1.0-((depth-dimin)*dmin)/float(dimax-dimin))
    if tview == 2 :
        depth = 255*dmult
    if flipKin == 1 :
        depth = np.flipud(depth)
        depth = np.fliplr(depth)
    depth = depth.flatten()
    return depth

a1 = 0
num = 0
texnb = 0
scen = 1
def animationStep( *args ):
    global a1, num, scapl, scen, texnb
    minkn = (n+1)*(2048.0/2.0)
    maxkn = minkn+((n2+1)*200)
    kn = DepthGet(minkn, maxkn)
    glActiveTextureARB(GL_TEXTURE3_ARB)
    glBind2Dlum(kn, t[3], (640,480))
    if scen == 1:
        glActiveTextureARB(GL_TEXTURE0_ARB)
        im, sz, nbtex = texture(gtex[texnb], nb)
        glBind3Dcol(im, t[0], sz, nbtex)
        vertexPos(0.8,(sz[0]/float(sz[1])),scapl)
        scen = 0
        if texnb<len(gtex)-1:
            texnb += 1
        else:
            texnb = 0
    sleep (1/30.0)
    glutPostRedisplay( )

def souris(but, sta, x ,y):
    global sx, sy, glsx, glsy, butsta, onsl1, onsl2, onsl3, onsl4, onsl5, onsl6
    sx = x
    sy = y
    glsx = (sx*(3.0/WID))-1.5
    glsy = (-sy*(3.0*fScreen/HEI))+(1.5*fScreen)
    butsta = sta
    if slidersOn == 1:
        onsl1 = glsx >= sliders(n, n2, n3, n4, n5, n6)[0][0][0] and glsx <= sliders(n, n2, n3, n4, n5, n6)[0][2][0] and glsy <= sliders(n, n2, n3, n4, n5, n6)[0][0][1] and glsy >= sliders(n, n2, n3, n4, n5, n6)[0][1][1]
        onsl2 = glsx >= sliders(n, n2, n3, n4, n5, n6)[2][0][0] and glsx <= sliders(n, n2, n3, n4, n5, n6)[2][2][0] and glsy <= sliders(n, n2, n3, n4, n5, n6)[2][0][1] and glsy >= sliders(n, n2, n3, n4, n5, n6)[2][1][1]
        onsl3 = glsx >= sliders(n, n2, n3, n4, n5, n6)[4][0][0] and glsx <= sliders(n, n2, n3, n4, n5, n6)[4][2][0] and glsy <= sliders(n, n2, n3, n4, n5, n6)[4][0][1] and glsy >= sliders(n, n2, n3, n4, n5, n6)[4][1][1]
        onsl4 = glsx >= sliders(n, n2, n3, n4, n5, n6)[6][0][0] and glsx <= sliders(n, n2, n3, n4, n5, n6)[6][2][0] and glsy <= sliders(n, n2, n3, n4, n5, n6)[6][0][1] and glsy >= sliders(n, n2, n3, n4, n5, n6)[6][1][1]
        onsl5 = glsx >= sliders(n, n2, n3, n4, n5, n6)[8][0][0] and glsx <= sliders(n, n2, n3, n4, n5, n6)[8][2][0] and glsy <= sliders(n, n2, n3, n4, n5, n6)[8][0][1] and glsy >= sliders(n, n2, n3, n4, n5, n6)[8][1][1]
        onsl6 = glsx >= sliders(n, n2, n3, n4, n5, n6)[10][0][0] and glsx <= sliders(n, n2, n3, n4, n5, n6)[10][2][0] and glsy <= sliders(n, n2, n3, n4, n5, n6)[10][0][1] and glsy >= sliders(n, n2, n3, n4, n5, n6)[10][1][1]
        if onsl1 and sta :
            saveData(1, n)
        if onsl2 and sta :
            saveData(2, n2)
        if onsl3 and sta :
            saveData(3, n3)
        if onsl4 and sta :
            saveData(4, n4)
        if onsl5 and sta :
            saveData(5, n5)
        if onsl6 and sta :
            saveData(6, n6)
        
def sel(x, y):
    global scapl, offsetX, offsetY, n, n2, n3, n4, n5, n6
    dtx = x-sx
    dty = y-sy
    dtglsx = glsx-((x*(3.0/WID))-1.5)
    dtglsy = glsy+((-y*(-3.0*fScreen/HEI))-(1.5*fScreen))
    if slidersOn == 1:
        if tview == 0 and not ( onsl1 or onsl2 or onsl3 or onsl4 or onsl5 or onsl6):
            scapl = (dty/-100.0)+1
            saveData(0,scapl)
            vertexPos(0.8,szt,scapl)
        if onsl1 :
            n = glsy-dtglsy
        if onsl2 :
            n2 = glsy-dtglsy
        if onsl3 :
            n3 = glsy-dtglsy
        if onsl4 :
            n4 = glsy-dtglsy
        if onsl5 :
            n5 = glsy-dtglsy
        if onsl6 :
            n6 = glsy-dtglsy
    
#scen = 0
def keyPressed(*args):
    global scen, tview, invV, flipKin, flipTex, slidersOn
    if args[0] == '\x1b':
        fdata = open('dataSave.txt', 'w')
        for i in range(len(f)):
            fdata.write(f[i])
        fdata.close()
        sys.exit()
    if args[0] == ' ':
        if scen == 1 : scen = 0
        else : scen = 1
    if args[0] == 'a':
        tview = 0
    if args[0] == 'z':
        tview = 1
    if args[0] == 'e':
        tview = 2
    if args[0] == 'p':
        scen = 1
    if args[0] == 'm':
        if flipKin == 0:
            flipKin = 1
        else :
            flipKin = 0
    if args[0] == 'l':
        if flipTex == 0 :
            flipTex = 1
            if flipKin == 0:
                flipKin = 1
            else :
                flipKin = 0
        else :
            flipTex = 0
            if flipKin == 0:
                flipKin = 1
            else :
                flipKin = 0
    if args[0] == 'q':
        if slidersOn == 0:
            slidersOn = 1
        else :
            slidersOn = 0
    saveData(7, flipKin)
    saveData(8, flipTex)

def ReSizeGLScene(Width, Height):
    global WID, HEI, fScreen
    
    if Height == 0:						
        Height = 1
    f = Height/float(Width)
    WID, HEI, fScreen = Width, Height, f
    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()	
    gluOrtho2D( -1.5, 1.5, -1.5*f, 1.5*f)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
def main():
    import logging
    logging.basicConfig()
    glutInit(  )
    glutInitDisplayMode( GLUT_DOUBLE)
    glutInitWindowSize( 640, 480 )
    glutInitWindowPosition( 1300, 10 )
    glutCreateWindow("Yo")    
    glutDisplayFunc( display )
    glutReshapeFunc(ReSizeGLScene)
    glutFullScreen()
    
    glutIdleFunc( animationStep )
    glutKeyboardFunc(keyPressed)
    glutMouseFunc(souris)
    glutMotionFunc(sel)
    init()
    glutMainLoop( )

if __name__ == "__main__":
    main()
