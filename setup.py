#!/usr/bin/env python
import glob
import os
import subprocess  # nosec

from setuptools import Command, setup
from setuptools.command.build import build as _build
from setuptools.command.install import install as _install

BASE_DIR = os.path.dirname((os.path.abspath(__file__)))


class compile_translations(Command):
    description = "Compile i18n translations using gettext."
    user_options = []

    def initialize_options(self):
        self.build_lib = None

    def finalize_options(self):
        self.set_undefined_options("build", ("build_lib", "build_lib"))

    def run(self):
        pattern = "vies/locale/*/LC_MESSAGES/django.po"
        for file in glob.glob(pattern):
            name, ext = os.path.splitext(file)
            cmd = ["msgfmt", "-c", "-o", f"{self.build_lib}/{name}.mo", file]
            self.announce("running command: %s" % " ".join(cmd), level=2)
            subprocess.check_call(cmd, cwd=BASE_DIR)  # nosec


class build(_build):
    sub_commands = [
        *_build.sub_commands,
        ("compile_translations", None),
    ]


class install(_install):
    sub_commands = [
        *_install.sub_commands,
        ("compile_translations", None),
    ]


setup(
    cmdclass={
        "build": build,
        "install": install,
        "compile_translations": compile_translations,
    },
)
