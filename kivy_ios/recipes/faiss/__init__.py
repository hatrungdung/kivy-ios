import sh

from os.path import join

from kivy_ios.toolchain import CythonRecipe, shprint
from kivy_ios.context_managers import cd


class FaissRecipe(CythonRecipe):
    version = "1.7.1.post2"
    url = "https://pypi.io/packages/source/f/faiss-cpu/faiss-cpu-{version}.tar.gz"
    depends = ["python3", "host_setuptools3"]
    python_depends = ["setuptools"]
    library = "libfaiss.a"
    cythonize = False

    def dest_dir(self):
        return join(self.ctx.dist_dir, "root", "python3")

    def get_netifaces_env(self, arch):
        build_env = arch.get_env()
        build_env["PYTHONPATH"] = self.ctx.site_packages_dir
        return build_env

    def install(self):
        arch = list(self.filtered_archs)[0]
        build_dir = self.get_build_dir(arch.arch)
        build_env = self.get_netifaces_env(arch)
        hostpython = sh.Command(self.ctx.hostpython)
        with cd(build_dir):
            shprint(
                hostpython,
                "setup.py",
                "install",
                "--prefix",
                self.dest_dir(),
                _env=build_env,
            )


recipe = FaissRecipe()
