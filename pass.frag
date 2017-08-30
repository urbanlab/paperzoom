uniform sampler2D tex0;
varying vec2 texcoord;
//varying vec2 middle;

void main()
{
	//vec4 mattex = vec4 (1.0, 1.0, 0.9, 1.0);
	//float offset = dot(middle.xy, vec2(0.0,0.1));
	//vec4 pass = texture2D(tex0, texcoord+vec2(-dot(middle.xy, vec2(1.0*middle.x, 0.0*middle.y)))).rgba;
	gl_FragColor = vec4(texture2D(tex0,texcoord));
}
