varying vec2 texcoord;

void main()
{
	gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
	texcoord = vec2(gl_TextureMatrix[0] * gl_MultiTexCoord0);
}


