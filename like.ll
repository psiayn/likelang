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
    "hello from somefunc_abc()!"
}

fn sometest() {
   "hello from sometest()!"
}

fn some() {
    print("running 'some' fun")
}

fn func() {
    print("running 'func' fun")
}

// print(somefunc(20, 30))

let func = collect /*func/
let some = collect /some*/
print("Printing collected functions:", func)
print("Printing collected functions:", some)
print(some.test())
print(some.func_abc())
random.func()
print(sometest())

some()
func()
