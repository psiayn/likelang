let a = 10

fn somefunc (a, b) {
    let b = 10

    fn somefunc2 () {
        let c = 10 * 10
    }

    let d = (10 * (20 + 30)) / 40
    somefunc2()
}
