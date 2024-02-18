# -*- coding: utf-8 -*-

import os
import re
import subprocess
import sys

ROOT = os.path.dirname(__file__)
PACKAGE = 'quantumsculpt'

def main():
    version_projecttoml = get_version_projecttoml()
    version_versionpy = get_version_versionpy()
    version_metayaml = get_version_metayaml()
    version_latest_pip = get_latest_pip_version()
        
    try:
        for i in range(0,3):
            assert version_projecttoml[i] == version_versionpy[i]
            assert version_versionpy[i] == version_metayaml[i]
    except Exception as e:
        print(e)
        raise Exception('Invalid version strings encountered')
        
    if version_latest_pip == version_metayaml:
        raise Exception('Utilized version %s needs to exceed current latest: %s' %
                        (version_latest_pip,version_metayaml))

def get_version_projecttoml():
    """
    Extract the version string from the pyproject.toml file
    """
    pattern = re.compile(r'^\s*version\s*=\s*"(\d+\.\d+.\d+)"\s*$')
    
    f = open(os.path.join(ROOT, 'pyproject.toml'))
    lines = f.readlines()
    for line in lines:
        match = re.match(pattern, line)
        if match:
            version = match.groups(1)[0]
            return [int(i) for i in version.split('.')]
        
    return None
        
def get_version_versionpy():
    """
    Extract the version string from the _version.py file
    """
    pattern = re.compile(r'^__version__\s*=\s*[\'"](\d+\.\d+.\d+)[\'"]\s*$')
    
    f = open(os.path.join(ROOT, PACKAGE, '_version.py'))
    lines = f.readlines()
    for line in lines:
        match = re.match(pattern, line)
        if match:
            version = match.groups(1)[0]
            return [int(i) for i in version.split('.')]
    
    return None

def get_version_metayaml():
    """
    Extract the version string from the pyproject.toml file
    """
    pattern = re.compile(r'^\s*version\s*:\s*"(\d+\.\d+.\d+)"\s*$')
    
    f = open(os.path.join(ROOT, 'meta.yaml'))
    lines = f.readlines()
    for line in lines:
        match = re.match(pattern, line)
        if match:
            version = match.groups(1)[0]
            return [int(i) for i in version.split('.')]
        
    return None

def get_latest_pip_version():
    out = subprocess.check_output([sys.executable, "-m", "pip", "index", "versions", PACKAGE],
                                  stderr=None)
    lines = out.decode().split('\n')
    for line in lines:
        line = line.strip()
        if 'LATEST:' in line:
            return line.split()[1].strip()
    
if __name__ == '__main__':
    main()
