import re
from setuptools import setup

# Find source version
with open("Include/patchlevel.h") as f:
    m = re.search(r'^#define\s+PY_VERSION\s+"([^"]+)"$', f.read(), re.MULTILINE)
if not m:
    raise RuntimeError("PY_VERSION not found in patchlevel.h")
version = m.group(1)

setup(
    name="turtle-standalone",
    version=version,
    py_modules=["turtle"],
    package_dir={"": "Lib"},
    license="PSF-2.0",
    license_files=["LICENSE"],
)
