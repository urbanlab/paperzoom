//uniform float width1 = 0.0;
//uniform float height1 = 0.0;

varying vec3 texcoord30;
varying vec2 texcoord;

/*varying vec2 texcoord00;
varying vec2 texcoord01;
varying vec2 texcoord02;
varying vec2 texcoord10;
varying vec2 texcoord12;
varying vec2 texcoord20;
varying vec2 texcoord21;
varying vec2 texcoord22;*/

void main (void)

{
 	gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
	texcoord30 = vec3(gl_TextureMatrix[0] * gl_MultiTexCoord0).xyz;
	texcoord = vec2(gl_TextureMatrix[0] * gl_MultiTexCoord0).xy;

	/*texcoord00 = texcoord + vec2(-width1, -height1);
	texcoord01 = texcoord + vec2( 0,       -height1);
	texcoord02 = texcoord + vec2( width1, -height1);
	texcoord10 = texcoord + vec2(-width1,  0);
	texcoord12 = texcoord + vec2( width1,  0);
	texcoord20 = texcoord + vec2(-width1,  height1);
	texcoord21 = texcoord + vec2( 0,        height1);
	texcoord22 = texcoord + vec2( width1,  height1);*/
	
}
