import glob
import os
import sys

import setuptools
import setuptools.command.build

sys.path.insert(0, "slimp")
import compile as slimp_compile

class BuildStanModels(setuptools.Command, setuptools.command.build.SubCommand):
    def __init__(self, *args, **kwargs):
        setuptools.Command.__init__(self, *args, **kwargs)
        setuptools.command.build.SubCommand.__init__(self, *args, **kwargs)
        self.build_lib = None
        self.editable_mode = False
        
        self.sources = []
        self.binaries = []
    
    def initialize_options(self):
        pass
        
    def finalize_options(self):
        self.sources = list(glob.glob("slimp/*.stan"))
        self.set_undefined_options("build_py", ("build_lib", "build_lib"))
    
    def run(self):
        for source in self.sources:
            slimp_compile.compile(
                source, os.path.join(self.build_lib, "slimp"),
                range_checks=False)
    
    def get_source_files(self):
        return self.sources

setuptools.command.build.build.sub_commands.append(("build_stan_models", None))

setuptools.setup(
    name="slimp",
    version="0.1.1",
    
    description="Linear models with stan and Pandas",
    
    author="Julien Lamy",
    author_email="lamy@unistra.fr",
    
    cmdclass={"build_stan_models": BuildStanModels},

    packages=["slimp"],
    
    install_requires=[
        "cmdstanpy",
        "formulaic",
        "numpy",
        "matplotlib",
        "pandas",
        "seaborn"
    ],
)
