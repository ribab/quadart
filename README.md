# QuadArt

Simple module for generating QuadTree art

## Example usage

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

Input:
![QuadArt Input](https://image.freepik.com/free-photo/green-apple-with-leaves_1101-453.jpg)

Output:
![QuadArt Output](examples/green-apple-quadart.jpg)

_Image attribution: kstudio on freepik.com_

## Setup
