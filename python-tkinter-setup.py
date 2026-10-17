import os
import re
import sysconfig
from setuptools import Extension, setup

# Find source version
with open("Include/patchlevel.h") as f:
    m = re.search(r'^#define\s+PY_VERSION\s+"([^"]+)"$', f.read(), re.MULTILINE)
if not m:
    raise RuntimeError("PY_VERSION not found in patchlevel.h")
version = m.group(1)

setup(
    name="tkinter-standalone",
    version=version,
    packages=["tkinter"],
    package_dir={"": "Lib"},
    license="PSF-2.0",
    license_files=["LICENSE"],
    ext_modules=[
        Extension(
            name="_tkinter",
            sources=["Modules/_tkinter.c"],
            libraries=["tcl9.0", "tcl9tk9.0"],
            include_dirs=[os.path.join(sysconfig.get_path("include"), "internal")],
        )
    ],
)
