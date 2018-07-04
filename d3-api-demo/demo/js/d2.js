let VSHARDER_SOURCE =
    `void main(){
            gl_Position = vec4(0.0,0.0,0.0,1.0);
            gl_PointSize = 10.0;
        }
        `
let FSHARDER_SOURCE =
    `void main(){
            gl_FragColor = vec4(1.0,1.0,0.0,1.0);
        }`

function main() {
    let cv = document.getElementById('mycanv');
    let ctx = getWebGLContext(cv)
    initShaders(ctx,VSHARDER_SOURCE,FSHARDER_SOURCE)
    ctx.clearColor(0.0,0.0,0.0,1.0)
    ctx.clear(ctx.COLOR_BUFFER_BIT)

    ctx.drawArrays(ctx.POINTS,0,1)
}
main()