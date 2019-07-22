# QuadArt

Simple module for generating QuadTree art

## Example usage

Input:
![QuadArt Input](https://image.freepik.com/free-photo/green-apple-with-leaves_1101-453.jpg)

Output:
![QuadArt Output](examples/green-apple-quadart.jpg)

_Image attribution: kstudio on freepik.com_

### Through Shell

Setup:
```bash
$ virtualenv --python=python3 env
$ source env/bin/activate
$ pip3 install -r requirements.txt
```

Run:
```bash
$ wget https://image.freepik.com/free-photo/green-apple-with-leaves_1101-453.jpg
$ ./quadart.py green-apple-with-leaves_1101-453.jpg --thresh 40
```

### As a python module

QuadArt isn't currently a pip module, so you first need to clone it first before you can use it.

Bash:
```bash
$ git clone https://github.com/ribab/quadart
```

Python3:
```python
>>> from quadart import quadart
>>> q = quadart.QuadArt()
>>> q.generate('green-apple-with-leaves_1101-453.jpg')
>>> q.display() # to display without saving
>>> q.save('green-apple-quadart.jpg') # save to file
```
