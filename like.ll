let a = 10

fn somefunc (a, b) {
    let b = 10

    fn somefunc2 () {
        let c = 10 * 10

        c
    }

    let d = (b * (a + 30)) / (somefunc2())
    print(d, d)
    d
}

print(somefunc(20, 30))
