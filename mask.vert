varying vec2 texcoordA;
varying vec2 texcoordB;

void main()
{
	gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
	texcoordA = vec2(gl_TextureMatrix[0] * gl_MultiTexCoord0).st;
	texcoordB = vec2(gl_TextureMatrix[0] * gl_MultiTexCoord1).st;
}


