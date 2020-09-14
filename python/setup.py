import pathlib
import shutil

from setuptools import setup, Command
from setuptools.command.build_py import build_py


class ProtoCommand(Command):

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        proto_dir = pathlib.Path("validate/validate")
        proto_dir.mkdir(parents=True, exist_ok=True)
        dst_validate_proto = proto_dir / "validate.proto"

        repo_root = pathlib.Path().resolve().parent
        src_validate_proto = repo_root / "validate" / "validate.proto"
        shutil.copyfile(src_validate_proto, dst_validate_proto)


class ProtocCommand(Command):
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import grpc_tools.protoc
        # shutil.copyfile()
        grpc_tools.protoc.main([
            'grpc_tools.protoc',
            '-I{}'.format("validate"),
            '--python_out=.',
            '--grpc_python_out=.',
            'validate/validate.proto'
        ])


class BuildPyCommand(build_py):
    def run(self):
        self.run_command('proto')
        self.run_command('protoc')
        super(BuildPyCommand, self).run()


# FixMe: Read Version from Protos
VERSION = "0.0.1"

setup(
    name="protoc-gen-validate",
    version=VERSION,
    description="Python package for protoc-gen-valdiate",
    url="https://github.com/envoyproxy/protoc-gen-validate/tree/master/python",
    author="Abhishek Munagekar",
    packages=["validate"],
    install_requires=[
        "ipaddress >= 1.0.22",
        "validate-email >= 1.3",
        "Jinja2 >= 2.11.1",
        "MarkupSafe >= 1.1.1"
    ],
    setup_requires=[
        "grpcio-tools >= 1.9.1"
    ],
    cmdclass={
        'proto': ProtoCommand,
        'protoc': ProtocCommand,
        'build_py': BuildPyCommand,
    },
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
