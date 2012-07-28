from mock import call, patch

import unittest_support

from committer import (NO_REPOSITORY_ERROR_CODE,
                       NOT_EXECUTABLE_ERROR_CODE,
                       OK_RETURN_CODE,
                       SHOW_USAGE_ERROR_CODE,
                       TOO_MANY_REPOSITORIES_ERROR_CODE,
                       CommitterException,
                       main,
                       _error)


class CommitterTests (unittest_support.TestCase):
    def test_should_instantiate_committer_using_given_properties (self):
        actual_committer_exception = CommitterException('Hello world', 123)
        
        self.assertEquals('Hello world', actual_committer_exception.message)
        self.assertEquals(123, actual_committer_exception.error_code)
    
    
    @patch('sys.stderr')
    def test_should_write_given_message_to_stderr (self, mock_stderr):
        _error('Failed.')
        
        self.assertEquals(call('Failed.' + '\n'), mock_stderr.write.call_args)


    @patch('sys.stdout')
    @patch('committer._error')
    def test_should_exit_commit_when_no_arguments_given (self, mock_error, mock_stdout):
        actual_return_code = main(['/usr/local/bin/commit'])
        
        self.assertEquals(SHOW_USAGE_ERROR_CODE, actual_return_code)


    @patch('sys.stdout')
    @patch('committer._error')
    @patch('committer.repositories.detect')
    def test_should_return_with_zero_when_updating (self, mock_detect, mock_error, mmock_stdout):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]

        actual_return_code = main(['/usr/local/bin/update'])
        
        self.assertEquals(OK_RETURN_CODE, actual_return_code)


    @patch('sys.stdout')
    @patch('committer.incrementor')    
    @patch('committer.repositories.detect')
    def test_should_check_that_repository_is_executable (self, mock_detect, mock_incrementor, mock_stdout):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]
        mock_repository.is_executable.return_value = True 
        
        actual_return_code = main(['/usr/local/bin/commit', 'message'])
        
        self.assertEquals(call(), mock_repository.is_executable.call_args)
        self.assertEquals(OK_RETURN_CODE, actual_return_code)


    @patch('sys.stdout')
    @patch('committer.incrementor')    
    @patch('committer._error')    
    @patch('committer.repositories.detect')
    def test_should_return_with_error_when_repository_command_is_not_executable (self, mock_detect, mock_error, mock_incrementor, mock_stdout):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]
        mock_repository.is_executable.return_value = False 
        
        actual_return_code = main(['/usr/local/bin/commit', 'message'])
        
        self.assertEquals(call(), mock_repository.is_executable.call_args)
        self.assertEquals(NOT_EXECUTABLE_ERROR_CODE, actual_return_code)


    @patch('sys.stdout')
    @patch('committer.incrementor')    
    @patch('committer.repositories.detect')
    def test_should_detect_repository (self, mock_detect, mock_incrementor, mock_stdout):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]
         
        main(['/usr/local/bin/commit', 'message'])
        
        self.assertEquals(call(), mock_detect.call_args)


    @patch('sys.stdout')
    @patch('committer.incrementor')    
    @patch('committer.repositories.detect')
    def test_should_return_with_zero (self, mock_detect, mock_incrementor, mock_stdout):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]
        
        actual_return_code = main(['/usr/local/bin/commit', 'message'])
        
        self.assertEquals(OK_RETURN_CODE, actual_return_code)


    @patch('sys.stdout')
    @patch('committer.incrementor')    
    @patch('committer.repositories.detect')
    def test_should_call_update_on_repository (self, mock_detect, mock_incrementor, mock_stdout):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]
        
        actual_return_code = main(['/usr/local/bin/commit', 'message'])
        
        self.assertEquals(call(), mock_repository.update.call_args)
        self.assertEquals(OK_RETURN_CODE, actual_return_code)


    @patch('sys.stdout')
    @patch('committer.incrementor')    
    @patch('committer.repositories.detect')
    def test_should_commit_using_first_argument_as_message (self, mock_detect, mock_incrementor, mock_stdout):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]
        
        actual_return_code = main(['/usr/local/bin/commit', 'message'])
        
        self.assertEquals(call('message'), mock_repository.commit.call_args)
        self.assertEquals(OK_RETURN_CODE, actual_return_code)


    @patch('sys.stdout')
    @patch('committer.incrementor')    
    @patch('committer.repositories.detect')
    def test_should_not_commit_when_called_via_update (self, mock_detect, mock_incrementor, mock_stdout):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]
        
        actual_return_code = main(['/usr/local/bin/update', 'message'])
        
        self.assertEquals(None, mock_repository.commit.call_args)
        self.assertEquals(OK_RETURN_CODE, actual_return_code)


    @patch('sys.stdout')
    @patch('committer.incrementor')    
    @patch('committer.repositories.detect')
    def test_should_increment_when_second_argument_is_plus_plus (self, mock_detect, mock_incrementor, mock_stdout):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]
        
        actual_return_code = main(['/usr/local/bin/commit', 'message', '++'])
        
        self.assertEquals(call(), mock_incrementor.increment_version.call_args)
        self.assertEquals(OK_RETURN_CODE, actual_return_code)


    @patch('sys.stdout')
    @patch('committer.incrementor')    
    @patch('committer.repositories.detect')
    def test_should_update_on_update (self, mock_detect, mock_incrementor, mock_stdout):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]
        
        actual_return_code = main(['/usr/local/bin/update'])
        
        self.assertEquals(call(), mock_repository.update.call_args)
        self.assertEquals(OK_RETURN_CODE, actual_return_code)


    @patch('sys.stdout')
    @patch('committer.repositories.detect')
    @patch('committer._error')
    def test_should_exit_when_no_repository_could_be_detected (self, mock_error, mock_detect, mock_stdout):
        mock_detect.return_value = []
        
        actual_return_code = main(['/usr/local/bin/commit', 'message', '++'])
        
        self.assertEquals(NO_REPOSITORY_ERROR_CODE, actual_return_code)


    @patch('sys.stdout')
    @patch('committer.repositories.detect')
    @patch('committer._error')
    def test_should_exit_when_more_than_one_repository_have_been_detected (self, mock_error, mock_detect, mock_stdout):
        mock_detect.return_value = [self.create_mock_repository(), self.create_mock_repository()]
        
        actual_return_code = main(['/usr/local/bin/commit', 'message', '++'])
        
        self.assertEquals(TOO_MANY_REPOSITORIES_ERROR_CODE, actual_return_code)
