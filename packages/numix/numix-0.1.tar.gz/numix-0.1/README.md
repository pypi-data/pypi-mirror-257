Numix
!PyPI version !Build Status !Coverage Status

Numix is a Python package that generates random numbers of various types and distributions. You can use Numix to create random integers, floats, decimals, fractions, complex numbers, and more. Numix also supports generating random numbers from common probability distributions, such as uniform, normal, binomial, Poisson, etc.

Numix is useful for applications that require randomness, such as simulations, cryptography, games, testing, and data analysis. Numix is easy to use, flexible, and fast.

Installation
You can install Numix from PyPI using pip:

pip install Numix

Alternatively, you can clone this repository and install from source:

git clone https://github.com/abelzk/numix.git
cd Numix
python setup.py install

Usage
To use Numix, simply import the Numix module and call the appropriate function for the type of random number you want. For example:

Python

import Numix

# Generate a random integer between 1 and 10
n = Numix.randint(1, 10)
print(n)

# Generate a random float between 0 and 1
x = Numix.random()
print(x)

# Generate a random decimal with 2 digits after the decimal point
d = Numix.decimal(2)
print(d)

# Generate a random fraction with denominator 5
f = Numix.fraction(5)
print(f)

# Generate a random complex number with real and imaginary parts between -1 and 1
c = Numix.complex()
print(c)

# Generate a random number from a normal distribution with mean 0 and standard deviation 1
z = Numix.normal()
print(z)
AI-generated code. Review and use carefully. More info on FAQ.
For more details and examples, please refer to the documentation.

License
Numix is licensed under the MIT License. See the LICENSE file for more information.

Contributing
Numix is an open source project and welcomes contributions from anyone. If you have any suggestions, bug reports, or feature requests, please open an issue on GitHub. If you want to contribute code, please fork the repository and submit a pull request. See the CONTRIBUTING file for more guidelines.