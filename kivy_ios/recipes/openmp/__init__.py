from kivy_ios.toolchain import Recipe, shprint
from kivy_ios.context_managers import cd
from os.path import join, exists
import sh
import os


class OpenMPRecipe(Recipe):
    version = "12.0.1"
    url = "https://github.com/llvm/llvm-project/releases/download/llvmorg-{version}/openmp-{version}.src.tar.xz"
    include_per_arch = True
    libraries = [
        "build/runtime/src/libomp.a"
    ]

    def build_arch(self, arch):
        build_env = arch.get_env()
        build_env['CXXFLAGS'] = build_env.get(
            'CXXFLAGS',
            '') + f" -std=c++11 -fembed-bitcode"

        command = sh.Command("cmake")
        if not exists("build"):
            os.mkdir("build")
        with cd("build"):
            shprint(command,
                    "..",
                    "-DLIBOMP_ENABLE_SHARED=OFF",
                    "-DCMAKE_SYSTEM_NAME=iOS",
                    "-DCMAKE_SYSTEM_NAME=Darwin",
                    f"-DCMAKE_OSX_ARCHITECTURES={arch}",
                    f"-DCMAKE_OSX_SYSROOT={arch.sysroot}",
                    "-DCMAKE_C_COMPILER=/usr/bin/clang",
                    "-DCMAKE_C_COMPILER_ID=AppleClang",
                    "-DCMAKE_CXX_COMPILER=/usr/bin/clang++",
                    "-DCMAKE_CXX_COMPILER_ID=AppleClang",
                    _env=build_env)

            command = sh.Command("make")
            shprint(command, _env=build_env)

        super(OpenMPRecipe, self).build_arch(arch)


recipe = OpenMPRecipe()
