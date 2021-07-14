# https://mac.r-project.org/openmp/
# https://mac.r-project.org/openmp/openmp-96efe90-darwin20-Release.tar.gz

from kivy_ios.toolchain import PythonRecipe, shprint
from os.path import join
import sh
import os


class FaissRecipe(PythonRecipe):
    version = "v1.7.1"
    url = "https://github.com/facebookresearch/faiss/archive/refs/tags/{version}.tar.gz"
    depends = ["python"]
    include_per_arch = True
    libraries = [
        "build/faiss/libfaiss.a",
    ]

    def build_arch(self, arch):
        build_env = arch.get_env()
        build_env['CXXFLAGS'] = build_env.get(
            'CXXFLAGS', ''
        ) + " -I{self.build_dir}/../../../../../../../../usr/local/include"
        build_env['LDFLAGS'] = build_env.get(
            'LDFLAGS', ''
        ) + " -L/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Library/Developer/CoreSimulator/Profiles/Runtimes/iOS.simruntime/Contents/Resources/RuntimeRoot/System/Library/Frameworks/Accelerate.framework/Frameworks/vecLib.framework -lBLAS -lLAPACK"
        command = sh.Command("cmake")
        shprint(
            command,
            "-Bbuild",
            "-S.",
            "-DFAISS_ENABLE_GPU=OFF",
            "-DBUILD_SHARED_LIBS=OFF",
            "-DCMAKE_SYSTEM_NAME=iOS",
            f"-DCMAKE_OSX_ARCHITECTURES={arch}",
            f"-DCMAKE_OSX_SYSROOT={arch.sysroot}",
            "-DCMAKE_CXX_COMPILER=/usr/bin/clang++",
            "-DCMAKE_CXX_COMPILER_ID=AppleClang",
            "-DOpenMP_CXX_FLAGS=-Xclang -fopenmp",
            "-DOpenMP_CXX_LIB_NAMES=omp",
            f"-DOpenMP_omp_LIBRARY={self.build_dir}/../../../../../../../../usr/local/lib/libomp.dylib",
            _env=build_env)
        command = sh.Command("make")
        shprint(command, "-C", "build", "-j", "faiss", _env=build_env)
        shprint(command, "-C", "build", "-j", "swigfaiss", _env=build_env)
        super(FaissRecipe, self).build_arch(arch)

    def install(self):
        arch = list(self.filtered_archs)[0]
        build_dir = self.get_build_dir(arch.arch)
        os.chdir(join(build_dir, "build/faiss/python"))
        hostpython = sh.Command(self.ctx.hostpython)
        build_env = arch.get_env()
        dest_dir = join(self.ctx.dist_dir, "root", "python3")
        build_env['PYTHONPATH'] = self.ctx.site_packages_dir
        shprint(hostpython,
                "setup.py",
                "install",
                "--prefix",
                dest_dir,
                _env=build_env)


recipe = FaissRecipe()
