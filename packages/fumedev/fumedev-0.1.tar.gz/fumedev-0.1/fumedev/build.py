import shutil
from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import os
from setuptools.command.build_ext import build_ext

class CustomBuildExt(build_ext):
    def build_extensions(self):
        # Specify your custom build directory
        self.build_lib = './cython_build'
        build_ext.build_extensions(self)
        self.copy_javascript_files()



    def copy_javascript_files(self):
        source_dir = '.'  # Source directory containing the JS files
        build_dir = self.build_lib  # Destination directory

        for root, dirs, files in os.walk(source_dir, topdown=True):
            # Skip excluded directories
            if any(excluded_dir in root.split(os.sep) for excluded_dir in exclude_dirs):
                continue

            for file in files:
                if file.endswith('.js') or file.endswith('.mjs') or file.endswith('.json') or file.endswith('requirements.txt'):
                    source_file = os.path.join(root, file)
                    relative_path = os.path.relpath(source_file, source_dir)
                    destination_file = os.path.join(build_dir, relative_path)

                    os.makedirs(os.path.dirname(destination_file), exist_ok=True)
                    shutil.copy(source_file, destination_file)

def find_python_modules(root_dir, exclude_dirs=None):
    if exclude_dirs is None:
        exclude_dirs = []
    # Convert exclude_dirs to absolute paths
    exclude_dirs = [os.path.abspath(os.path.join(root_dir, d)) for d in exclude_dirs]
    cython_extensions = []

    for root, dirs, files in os.walk(root_dir):
        # Check if the current directory or any parent directory is in exclude_dirs
        if any(os.path.abspath(root).startswith(ed) for ed in exclude_dirs):
            continue

        for file in files:
            if file.endswith('.py') and not file.endswith('__init__.py'):  # Change to '.py' if you are using .py files for Cython
                file_path = os.path.join(root, file)
                module_name = os.path.splitext(file_path.replace(root_dir + os.sep, '').replace(os.path.sep, '.'))[0]
                cython_extensions.append(Extension(module_name, [file_path]))

    return cython_extensions

package_root = '.'  # Replace with your package root directory
exclude_dirs = ['codebase','node_modules','cache', 'coder']  # Add paths of directories to exclude

package_root = '.'  # Replace with your package root directory
setup(
    name='YourProject',
    version='0.1',
    packages=find_packages(),
    ext_modules=cythonize(find_python_modules(package_root,exclude_dirs), compiler_directives={'language_level': "3"}),
    cmdclass={
        'build_ext': CustomBuildExt
    }
)
