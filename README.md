# likelang
A language that allows you to import functions to a namespace based on a pattern.

### Quick Example
```
let tests = collect /*test_util/
```
Here we are collecting all functions that end in `test_util` and assigning it to a "namespace" called `tests`.

Using this we can invoke functions that end with test.

For example if there is a function called `like_test_util` we would invoke it as:
```
like_.tests()
```

## Dependencies
There are two ways to install the dependencies:
- using pip
- using nix

#### Using pip
The recommended way to install dependencies is
```bash
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

#### Using nix
This method is only possible *nix(MacOS, Linux, etc) systems.
Install nix from [here](https://nixos.org/download.html).
Now let it install the dependencies.
```bash
nix-shell
```

## How to run
Once you have the dependencies just run it as follows. 
Here we run an example test file.
```bash
python3 like.py examples/like.like
```
