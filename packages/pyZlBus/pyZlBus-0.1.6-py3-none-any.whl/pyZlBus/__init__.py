from . import pyZlBus
from . import test


def loading():
    print('import pyZlBus.pyZlBus as zlb')
    print('import pyZlBus.test as ts\r\n')
    print('1. The test module contains demo() and bleDemo() methods')
    print('2. ts.demo()')
    print('3. ts.bleScan() and ts.bleDemo(\'ZL24-00000001-0000\')')
    print('4. Running bleDemo(), Enter \'q\' or  \'Q\' to exit the program methods.')
    print('5. Other ZLBUS protocol interfaces are in the pyZlBus.pyZlBus module\r\n')

loading()
