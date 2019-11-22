from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from time import sleep
import freenect
import numpy as np

def init():
    print "esc to quit"
    ratio = 480/640.0
    glClearColor(0.5,0.0, 0.0, 1.0)
    glShadeModel(GL_SMOOTH)
    glMatrixMode( GL_PROJECTION )
    glLoadIdentity()
    gluOrtho2D( -1.5, 1.5, 1.5*ratio, -1.5*ratio)
    glMatrixMode( GL_MODELVIEW )

y = 1.0
x = y*1.333
z1 = 0.0
def display(*args):
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    glLoadIdentity()
    glTexEnvfv(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, 0)
        
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-x, y, z1)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-x, -y, z1)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x, -y, z1)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x, y, z1)
    glEnd(  )

    glutSwapBuffers (  )

def glBind2Dlum(im,idt, size):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, idt)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, size[0], size[1], 0, GL_LUMINANCE, GL_UNSIGNED_BYTE, im)
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT )
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT )
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
    

def DepthGet():
    depth1, timestamp = freenect.sync_get_depth()
    #dmult = np.ma.masked_outside(depth1, 400, 700)
    #print np.amin(dmult), np.amax(dmult)
    dmin = depth1>=50
    dmax = depth1<=1100
    dmult = np.logical_and(dmin, dmax)
    depth = 255*dmult*(depth1/2048.0)
    depth = depth.flatten()
    return depth


tkn = glGenTextures(1)
def animationStep( *args ):
    kn = DepthGet()
    glBind2Dlum(kn, tkn, (640,480))
    sleep (1/30.0)
    glutPostRedisplay( )

def keyPressed(*args):
    global scen, tview
    if args[0] == '\x1b':
        sys.exit()

def ReSizeGLScene(Width, Height):
    if Height == 0:						
        Height = 1
    f = Height/float(Width)
    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()	
    gluOrtho2D( -1.5, 1.5, 1.5*f, -1.5*f)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
def main():
    glutInit(  )
    glutInitDisplayMode( GLUT_DOUBLE)
    glutInitWindowSize( 640, 480 )
    glutInitWindowPosition( 400, 10 )
    glutCreateWindow("Test Kinect")    
    glutDisplayFunc( display )
    glutReshapeFunc(ReSizeGLScene)
    glutIdleFunc( animationStep )
    glutKeyboardFunc(keyPressed)
    init()    
    glutMainLoop( )

if __name__ == "__main__":
    main()
