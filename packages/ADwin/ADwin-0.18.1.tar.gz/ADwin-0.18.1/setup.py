from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.txt").read_text(encoding="utf-8")

setup(name='ADwin',
    version='0.18.1',
    platforms=['linux2, win32, darwin'],
    install_requires=["setuptools", "wheel"],
    description='ADwin API wrapper',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    maintainer='Jaeger Computergesteuerte Messtechnik GmbH',
    maintainer_email='info@ADwin.de',
    author='Markus Borchers',
    url='http://www.ADwin.de',
    license='''Apache License 2.0''',
    py_modules=['ADwin']
)
