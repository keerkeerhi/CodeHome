
function main() {
    let cv = document.getElementById('mycanv');
    // cv.height = 500;
    // cv.width = 1000;
    let ctx = getWebGLContext(cv)
    ctx.clearColor(0.56,0.49,1,1)
    ctx.clear(ctx.COLOR_BUFFER_BIT)
}
main()