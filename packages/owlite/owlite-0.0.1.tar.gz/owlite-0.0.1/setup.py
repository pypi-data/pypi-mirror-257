import sys
from setuptools import setup

print(sys.argv)
if len(sys.argv) < 3:
    raise RuntimeError("Bad parameters to build the package")

ACTION: str = sys.argv[1]
PACKAGE_NAME: str = sys.argv[2]
PACKAGE_VERSION: str = "0.0.1"

sys.argv.remove(PACKAGE_NAME)

ERROR_MSG: str = """


###########################################################################################
*** WARNING ***
The package you are trying to install is only a placeholder project on PyPI.org repository.
This package is hosted on Owlite Python Package Index.

Please visit us at www.squeezebits.com or github.com/SqueezeBits/Owlite.
###########################################################################################


"""
README_MD: str = f"""
{PACKAGE_NAME}
=====================

**WARNING:** The package you are trying to install is only a placeholder project on PyPI.org repository.
This package is hosted on Owlite Python Package Index.

Please visit us at www.squeezebits.com or github.com/SqueezeBits/Owlite.
"""



def main():
    global ACTION, PACKAGE_NAME, PACKAGE_VERSION
    setup(
        name="owlite",
        version="0.0.1",
        description="A fake package to warn the user they are not installing the correct package.",
        url="https://github.com/SqueezeBits/owlite",
        author="SqueezeBits Inc.",
        author_email="owlite@squeezebits.com",
        python_requires="~=3.10.0",
        classifiers=[
            "Development Status :: 1 - Planning",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: Python :: 3.10",
            "Topic :: Scientific/Engineering",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
            "Topic :: Software Development",
            "Topic :: Software Development :: Libraries",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
        keywords=[],
    )


if ACTION == "sdist":
    main()
else:
    raise RuntimeError(ERROR_MSG)

