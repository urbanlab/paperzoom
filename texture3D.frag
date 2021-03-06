uniform sampler3D tex0;
uniform sampler2D tex1;

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

void main(){
	//vec4 t1 = texture2D(tex1, 0.5 * (texcoord10 + texcoord12)).rgba;

	/*t1 = min(t1, texture2D(tex1, texcoord00).rgba);
	t1 = min(t1, texture2D(tex1, texcoord01).rgba);
	t1 = min(t1, texture2D(tex1, texcoord02).rgba);
	t1 = min(t1, texture2D(tex1, texcoord10).rgba);
	t1 = min(t1, texture2D(tex1, texcoord12).rgba);
	t1 = min(t1, texture2D(tex1, texcoord20).rgba);
	t1 = min(t1, texture2D(tex1, texcoord21).rgba);
	t1 = min(t1, texture2D(tex1, texcoord22).rgba);*/

	vec4 t1 = texture2D(tex1, texcoord).rgba;
	float a = t1.r;
	vec3 t0 = texcoord30.xyz;
	t0.z += (a*0.6)+0.22;
	vec4 color = texture3D(tex0, vec3(t0.x,t0.y,t0.z)).rgba;
  	gl_FragColor = color;
}
