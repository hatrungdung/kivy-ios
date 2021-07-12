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
        command = sh.Command("cmake")
        shprint(command, "-B", "build", ".", "-DFAISS_ENABLE_GPU=OFF",
                "-DBUILD_SHARED_LIBS=OFF", f"-DCMAKE_OSX_ARCHITECTURES={arch}")
        command = sh.Command("make")
        shprint(command, "-C", "build", "-j", "faiss")
        shprint(command, "-C", "build", "-j", "swigfaiss")
        super(FaissRecipe, self).build_arch(arch)

    def install(self):
        arch = list(self.filtered_archs)[0]
        build_dir = self.get_build_dir(arch.arch)
        os.chdir(os.join(build_dir, "build/faiss/python"))
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

