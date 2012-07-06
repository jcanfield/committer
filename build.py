from pythonbuilder.core import use_plugin, init, Author

use_plugin('python.core')
use_plugin('python.coverage')
use_plugin('python.unittest')
use_plugin('python.integrationtest')
use_plugin('python.distutils')
use_plugin('python.pychecker')
use_plugin('python.pydev')
use_plugin('python.pylint')

default_task = ['analyze', 'run_integration_tests']

version = '0.0.12'
summary = 'committer - pull, increase version, commit with message, push'
authors = [
    Author('Michael Gruber', 'aelgru@gmail.com'),
]

url = 'https://github.com/aelgru/committer'
license = 'Apache License, Version 2.0'

@init
def set_properties (project):
    project.set_property('coverage_break_build', False)
    project.set_property('pychecker_break_build', True)
    project.set_property('pychecker_args', ['-Q', '-b', 'unittest'])