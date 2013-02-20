uniform sampler2D tex0;
uniform sampler2D tex1;
varying vec2 texcoordA;
varying vec2 texcoordB;

void main()
{
	vec4 texA = texture2D(tex0, texcoordB.st).rgba;
	vec4 mask = texture2D(tex1, texcoordA.st).rgba;
	gl_FragColor = vec4(texA.r,texA.g,texA.b,mask.r); 
}

