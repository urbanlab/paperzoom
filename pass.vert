varying vec2 texcoord;
//varying vec2 middle;

void main()
{
	gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
	texcoord = vec2(gl_TextureMatrix[0] * gl_MultiTexCoord0);
	//middle = vec2(1.0 * (texcoord.xy - 0.0));
}


