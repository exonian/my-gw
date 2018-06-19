import glob
import os
import re
import shutil

from jinja2 import Environment, FileSystemLoader


def build():
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    build_dir = os.path.join(parent_dir, 'build')
    src_dir = os.path.join(parent_dir, 'src')
    manifest_template = Environment(loader=FileSystemLoader(parent_dir)).get_template('manifest.json.j2')

    # remove and recreate build dir from src dir
    shutil.rmtree(build_dir, ignore_errors=True)
    shutil.copytree(src_dir, build_dir)

    # render and write manifest
    manifest = manifest_template.render()
    with open(os.path.join(build_dir, 'manifest.json'), 'w') as f:
        f.write(manifest)

    # make archive
    shutil.make_archive(
        base_name=os.path.join(parent_dir, 'extension'),
        format='zip',
        root_dir=build_dir,
    )


if __name__ == '__main__':
    build()
