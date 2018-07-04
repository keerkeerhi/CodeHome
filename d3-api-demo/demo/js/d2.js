function main() {
    let cv = document.getElementById('mycanv');
    let ctx = getWebGLContext(cv)
    initShaders()
}
main()