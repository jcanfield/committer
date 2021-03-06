import unittest

from mockito import when, verify, any as any_value, unstub
from committer.vcsclients.git import GitClient

import committer


class GitClientTests (unittest.TestCase):
    def setUp(self):
        self.git_client = GitClient()

    def tearDown(self):
        unstub()

    def test_should_have_command_property(self):
        self.assertEqual('git', self.git_client.command)

    def test_should_have_name_property(self):
        self.assertEqual('Git', self.git_client.name)

    def test_should_prepend_git_to_given_arguments (self):
        when(self.git_client)._git(any_value()).thenReturn(None)

        self.git_client.commit('This is a commit message.')

        verify(self.git_client)._git('commit', '-a', '-m', 'This is a commit message.')
        verify(self.git_client)._git('push')

    def test_should_call_pull(self):
        when(self.git_client)._git(any_value()).thenReturn(None)

        self.git_client.update()

        verify(self.git_client)._git('pull')

    def test_should_call_status(self):
        when(self.git_client)._git(any_value()).thenReturn(None)

        self.git_client.status()

        verify(self.git_client)._git('status', '-sb')

    def test_return_false_if_dot_git_directory_does_not_exist(self):
        when(committer.vcsclients.git.path).isdir(any_value()).thenReturn(False)

        actual_return_value = self.git_client.detect()

        self.assertEqual(False, actual_return_value)
        verify(committer.vcsclients.git.path).isdir('.git')

    def test_return_true_if_dot_git_directory_exists(self):
        when(committer.vcsclients.git.path).isdir(any_value()).thenReturn(True)

        actual_return_value = self.git_client.detect()

        self.assertEqual(True, actual_return_value)
        verify(committer.vcsclients.git.path).isdir('.git')

    def test_should_return_value_of_check(self):
        when(self.git_client).check_if_is_executable(any_value(), any_value()).thenReturn('value from check')

        actual_return_value = self.git_client.is_executable()

        self.assertEqual('value from check', actual_return_value)
        verify(self.git_client).check_if_is_executable('git', '--version')

    def test_should_execute_git_using_arguments(self):
        when(self.git_client).execute_command(any_value(), any_value(), any_value(), any_value()).thenReturn(None)

        self.git_client._git('arg1', 'arg2', 'arg3')

        verify(self.git_client).execute_command('git', 'arg1', 'arg2', 'arg3')

    def test_should_return_stdout_and_stderr_from_execution(self):
        stdout = 'stdout'
        stderr = 'stderr'
        when(self.git_client).execute_command(any_value(), any_value(), any_value(), any_value()).thenReturn((stdout, stderr))

        actual_stdout, actual_stderr = self.git_client._git('arg1', 'arg2', 'arg3')

        self.assertEqual(stdout, actual_stdout)
        self.assertEqual(stderr, actual_stderr)
