import os
import re
import sys
import atexit
import shutil
import zipfile
import tempfile
import subprocess
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext
from distutils.command.sdist import sdist
from distutils.errors import CompileError, LinkError
from distutils import log


_version_re = re.compile(r'(?m)^version\s*=\s*"(.*?)"\s*$')


DEBUG_BUILD = os.environ.get("SYMBOLIC_DEBUG") == "1"

with open("README") as f:
    readme = f.read()


if os.path.isfile("../symbolic-cabi/Cargo.toml"):
    with open("../symbolic-cabi/Cargo.toml") as f:
        version = _version_re.search(f.read()).group(1)
else:
    with open("version.txt") as f:
        version = f.readline().strip()


def vendor_rust_deps():
    subprocess.Popen(["scripts/git-archive-all", "py/rustsrc.zip"], cwd="..").wait()


def write_version():
    with open("version.txt", "w") as f:
        f.write("%s\n" % version)


class CustomSDist(sdist):
    def run(self):
        vendor_rust_deps()
        write_version()
        sdist.run(self)


def build_rust_library():
    cmd = ["cargo", "build", "-p", "symbolic-cabi"]
    if not DEBUG_BUILD:
        cmd.append("--release")
        target = "release"
    else:
        target = "debug"

    # Step 0: find rust sources
    if os.path.isdir("rustsrc"):
        rust_path = "rustsrc"
        scratchpad = None
    elif os.path.isfile("../symbolic-cabi/Cargo.toml"):
        rust_path = ".."
        scratchpad = None
    else:
        scratchpad = tempfile.mkdtemp()

        @atexit.register
        def delete_scratchpad():
            try:
                shutil.rmtree(scratchpad)
            except (IOError, OSError):
                pass

        zf = zipfile.ZipFile("rustsrc.zip")
        zf.extractall(scratchpad)
        rust_path = scratchpad + "/rustsrc"

    # Step 1: build the rust library
    print("running `%s` (%s target)" % (" ".join(cmd), target))
    subprocess.check_call(cmd, cwd=rust_path)
    
    # Find the static library
    if os.path.isdir("rustsrc"):
        lib_path = os.path.join("rustsrc", "target", target, "libsymbolic_cabi.a")
    elif os.path.isfile("../symbolic-cabi/Cargo.toml"):
        lib_path = os.path.join("..", "target", target, "libsymbolic_cabi.a")
    else:
        lib_path = os.path.join(scratchpad, "rustsrc", "target", target, "libsymbolic_cabi.a")
    
    if not os.path.exists(lib_path):
        raise RuntimeError("Failed to find static library at: %s" % lib_path)
    
    # Find the header file
    if os.path.isdir("rustsrc"):
        header_path = os.path.join("rustsrc", "symbolic-cabi", "include", "symbolic.h")
    elif os.path.isfile("../symbolic-cabi/Cargo.toml"):
        header_path = os.path.join("..", "symbolic-cabi", "include", "symbolic.h")
    else:
        header_path = os.path.join(scratchpad, "rustsrc", "symbolic-cabi", "include", "symbolic.h")
    
    if not os.path.exists(header_path):
        raise RuntimeError("Failed to find header file at: %s" % header_path)
    
    return lib_path, header_path, scratchpad


class BuildExt(build_ext):
    def run(self):
        lib_path, header_path, scratchpad = build_rust_library()
        
        shared_lib_name = None
        
        # Create a shared library from the static library
        if sys.platform.startswith("linux"):
            temp_dir = tempfile.mkdtemp()
            try:
                shared_lib_path = os.path.join(temp_dir, "libsymbolic_cabi.so")
                cc_cmd = [
                    "g++", "-shared", "-fPIC", "-o", shared_lib_path,
                    "-Wl,--whole-archive", lib_path, "-Wl,--no-whole-archive",
                    "-lpthread", "-ldl", "-lm", "-lstdc++"
                ]
                print("Creating shared library from static library...")
                print("Running: %s" % " ".join(cc_cmd))
                subprocess.check_call(cc_cmd)
                
                shared_lib_name = "_lowlevel__lib.so"
                
                # Copy to source directory
                package_dir = os.path.join(os.path.dirname(__file__), "symbolic")
                shutil.copy(shared_lib_path, os.path.join(package_dir, shared_lib_name))
                
                print("Shared library created successfully")
            finally:
                shutil.rmtree(temp_dir, ignore_errors=True)
        elif sys.platform == "darwin":
            temp_dir = tempfile.mkdtemp()
            try:
                shared_lib_path = os.path.join(temp_dir, "libsymbolic_cabi.dylib")
                cc_cmd = [
                    "clang++", "-dynamiclib", "-fPIC", "-o", shared_lib_path,
                    "-Wl,-force_load", lib_path,
                    "-lpthread", "-ldl", "-lm", "-lc++"
                ]
                print("Creating shared library from static library...")
                print("Running: %s" % " ".join(cc_cmd))
                subprocess.check_call(cc_cmd)
                
                shared_lib_name = "_lowlevel__lib.dylib"
                
                # Copy to source directory
                package_dir = os.path.join(os.path.dirname(__file__), "symbolic")
                shutil.copy(shared_lib_path, os.path.join(package_dir, shared_lib_name))
                
                print("Shared library created successfully")
            finally:
                shutil.rmtree(temp_dir, ignore_errors=True)
        else:
            raise RuntimeError("Unsupported platform: %s" % sys.platform)
        
        build_ext.run(self)
        
        # After building, copy the shared library and _lowlevel.py to the build directory
        if shared_lib_name:
            source_dir = os.path.join(os.path.dirname(__file__), "symbolic")
            target_dir = os.path.join(self.build_lib, "symbolic")
            
            # Copy shared library
            shutil.copy(os.path.join(source_dir, shared_lib_name), os.path.join(target_dir, shared_lib_name))
            
            # Copy _lowlevel.py if it exists
            lowlevel_src = os.path.join(source_dir, "_lowlevel.py")
            if os.path.exists(lowlevel_src):
                shutil.copy(lowlevel_src, os.path.join(target_dir, "_lowlevel.py"))

    def build_extension(self, ext):
        if ext.name == "symbolic._lowlevel":
            return
        build_ext.build_extension(self, ext)


def build_native(spec):
    pass  # We handle this in BuildExt instead


setup(
    name="symbolic",
    version=version,
    packages=find_packages(),
    author="Sentry",
    license="MIT",
    author_email="hello@sentry.io",
    description="A python library for dealing with symbol files and more.",
    long_description=readme,
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    install_requires=["cffi>=1.0.0"],
    setup_requires=["cffi>=1.0.0"],
    ext_modules=[
        Extension(
            "symbolic._lowlevel",
            sources=[],
        )
    ],
    cmdclass={
        "sdist": CustomSDist,
        "build_ext": BuildExt,
    },
)