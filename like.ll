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

fn randomfunc () {
    let a = "AAAAAAAAAAAAAAAA"
    print(a)
}

fn somefunc3() {
    let a = 10
    print(a)
}

fn somefunc_abc() {
    
}

print(somefunc(20, 30))

let sf = collect /somefunc/
print("Printing collected functions:", sf)
// sf() -> somefunc()
// sf.3() -> somefunc3()
// sf._abc() -> somefunc_abc()