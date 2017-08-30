uniform sampler2D tex0;
varying vec2 texcoord;

void main()
{
	vec3 alpha = texture2D(tex0, texcoord).rgb;
	gl_FragColor = vec4(alpha,0.5);
}
