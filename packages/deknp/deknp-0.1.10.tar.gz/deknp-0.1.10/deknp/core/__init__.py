import os
import shutil
import json
import sys
from collections import OrderedDict, ChainMap
from copy import deepcopy
from dektools.file import write_file, read_text, remove_path
from dektools.yaml import yaml
from dektools.shell import Cli, shell_wrapper
from .plugins.base import PluginBase
from .run import run_plugins, PluginDv3Yaml

project_dir = os.getcwd()
plugin_base = PluginBase(project_dir)

path_project_log = os.path.join(project_dir, 'deknp.log')
path_project_tree_log = os.path.join(project_dir, 'deknp.tree.log')

cli = Cli('pnpm', 'yarn', 'npm').cur


def run_install_package_cmd(data):
    for k, v in (data.get('dependencies') or {}).items():
        shell_wrapper(f'{cli} add "{k}@{v}"', True)
    for k, v in (data.get('devDependencies') or {}).items():
        shell_wrapper(f'{cli} add -D "{k}@{v}"', True)


def filter_packages(data):
    def pop(d):
        for k in list(d):
            if os.path.exists(os.path.join(plugin_base.node_modules_dir, k)):
                d.pop(k)

    data = deepcopy(data)
    pop(data.get('dependencies') or {})
    pop(data.get('devDependencies') or {})
    return data


def merge_package(a, b):
    result = deepcopy(a)
    result.update([
        ('dependencies',
         OrderedDict(ChainMap(a.get('dependencies', OrderedDict()), b.get('dependencies', OrderedDict())))),
        ('devDependencies',
         OrderedDict(ChainMap(a.get('devDependencies', OrderedDict()), b.get('devDependencies', OrderedDict())))),
    ])
    return result


def execute_install():
    def walk(dir_dek, dev=False):
        if dir_dek in handed_set:
            return
        handed_set.add(dir_dek)
        fp = os.path.join(dir_dek, plugin_base.package_dek_name)
        if os.path.exists(fp):
            data_dek = plugin_base.load_json(fp)
            data_dek_list.append(data_dek)
            data = merge_package(plugin_base.load_package_standard(deepcopy(data_dek)), data_dek)
            if dir_dek == project_dir:
                data_dek_run = data.get('dek', {}).get('run') or {}
                data = merge_package(data, data_dek_run)
            plugin_base.save_json(plugin_base.package_standard_filepath, data)
            run_install_package_cmd(filter_packages(data))

            if dir_dek == project_dir:
                data_dek_run = data.get('dek', {}).get('run') or {}
                for k in reversed(data_dek_run.get('dependencies', OrderedDict())):
                    walk(os.path.join(plugin_base.node_modules_dir, k))
            for k in reversed(data.get('dependencies', OrderedDict())):
                walk(os.path.join(plugin_base.node_modules_dir, k))

            if dir_dek == project_dir:
                data_dek_run = data.get('dek', {}).get('run') or {}
                for k in reversed(data_dek_run.get('devDependencies', OrderedDict())):
                    walk(os.path.join(plugin_base.node_modules_dir, k), True)
            for k in reversed(data.get('devDependencies', OrderedDict())):
                walk(os.path.join(plugin_base.node_modules_dir, k), True)

            dek_dir_list.append(dir_dek)
            if dev:
                dek_dev_dir_list.append(dir_dek)
            dek_info = data_dek.get('dek')
            if dek_info:
                dek_info_list.append(dek_info)

    handed_set = set()
    dek_dir_list = []
    dek_dev_dir_list = []
    dek_info_list = []
    data_dek_list = []
    if os.path.exists(plugin_base.package_dek_filepath):
        data_dek = plugin_base.load_json(plugin_base.package_dek_filepath)
        data_dek.update([
            ('dependencies', {}),
            ('devDependencies', {}),
        ])
        plugin_base.save_json(plugin_base.package_standard_filepath, data_dek)
    walk(project_dir)
    write_file(path_project_tree_log, yaml.dumps(data_dek_list))
    write_file(path_project_log,
               json.dumps([dek_info_list, dek_dir_list, dek_dev_dir_list], indent=2, ensure_ascii=False))
    run_plugins(project_dir, dek_info_list, dek_dir_list, dek_dev_dir_list)
    return 0


def execute_package_sure(force=False):
    if os.path.exists(plugin_base.package_dek_filepath) and \
            (force or not os.path.exists(plugin_base.package_standard_filepath)):
        data_dek = plugin_base.load_json(plugin_base.package_dek_filepath)
        data_dek.pop('dek', None)
        plugin_base.save_json(plugin_base.package_standard_filepath, data_dek)


def execute_server(begin=False):
    dir_servers = os.path.join(project_dir, 'dek', 'dv3', 'servers')
    project_name = os.path.basename(project_dir).replace('-', '').replace('_', '').lower()
    if os.path.isdir(dir_servers) and os.listdir(dir_servers):
        dir_work = os.path.join(project_dir, 'server')
        if not os.path.isdir(dir_work):
            os.makedirs(dir_work)
        dir_material = os.path.join(dir_work, '.material')
        if not os.path.exists(dir_material):
            shell_wrapper(f'djcreator wrapper clean --project={project_name}')
            ret = shell_wrapper(f'djcreator project {project_name} {dir_work}')
            if ret != 0:
                raise ChildProcessError(ret)
        dir_project = os.path.join(dir_material, f'{project_name}.yaml')
        if os.path.isdir(dir_project):
            shutil.rmtree(dir_project)
        shutil.copytree(dir_servers, dir_project)
        shell_wrapper(f'dekshell rf .shell.initshell.pysh', chdir=dir_work)
        if begin:
            shell_wrapper(f'dekshell rf .shell.generate.{project_name}.pysh', chdir=dir_material)
            shell_wrapper(f'deknp install', chdir=project_dir)


def run_plugin_yaml():
    run_plugins(project_dir, *json.loads(read_text(path_project_log)), [PluginDv3Yaml])


def get_pnpm_cache_dir():  # https://github.com/pnpm/pnpm/blob/v8.10.5/config/config/src/dirs.ts
    if os.getenv('XDG_CACHE_HOME'):
        return os.path.join(os.getenv('XDG_CACHE_HOME'), 'pnpm')
    if sys.platform == 'darwin':
        return os.path.join(os.path.expanduser('~'), 'Library/Caches/pnpm')
    if sys.platform != 'win32':
        return os.path.join(os.path.expanduser('~'), '.cache/pnpm')
    if os.getenv('LOCALAPPDATA'):
        return os.path.join(os.getenv('LOCALAPPDATA'), 'pnpm-cache')
    return os.path.join(os.path.expanduser('~'), '.pnpm-cache')


def clear_pkg_cache():
    pkg_info = plugin_base.get_package_json(project_dir)
    name, version = pkg_info['name'], pkg_info['version']
    path_meta = os.path.join(get_pnpm_cache_dir(), 'metadata')
    if os.path.isdir(path_meta):
        for host in os.listdir(path_meta):
            path_pkg = os.path.join(path_meta, host, name + '.json')
            if os.path.isfile(path_pkg):
                data = json.loads(read_text(path_pkg))
                versions = data.get('versions') or {}
                exists = versions.pop(version, None)
                if exists is not None:
                    if versions:
                        write_file(path_pkg, json.dumps(data))
                    else:
                        remove_path(path_pkg)
