import asyncio

import pytest
import full_match
from emptylog import MemoryLogger

import escape
from escape.errors import SetDefaultReturnValueForDecoratorError


def test_run_simple_function():
    some_value = 'kek'

    @escape
    def function():
        return some_value

    assert function() == some_value


def test_run_simple_function_with_some_arguments():
    @escape
    def function(a, b, c=5):
        return a + b + c

    assert function(1, 2) == 8
    assert function(1, 2, 5) == 8
    assert function(1, 2, c=5) == 8
    assert function(1, 2, c=8) == 11


def test_run_function_with_exception():
    @escape
    def function(a, b, c=5):
        raise ValueError

    function(1, 2)


def test_run_coroutine_function():
    some_value = 'kek'

    @escape
    async def function():
        return some_value

    assert asyncio.run(function()) == some_value


def test_run_coroutine_function_with_some_arguments():
    @escape
    async def function(a, b, c=5):
        return a + b + c

    assert asyncio.run(function(1, 2)) == 8
    assert asyncio.run(function(1, 2, 5)) == 8
    assert asyncio.run(function(1, 2, c=5)) == 8
    assert asyncio.run(function(1, 2, c=8)) == 11


def test_run_coroutine_function_with_exception():
    @escape
    async def function(a, b, c=5):
        raise ValueError

    asyncio.run(function(1, 2))


def test_run_simple_function_with_empty_brackets():
    some_value = 'kek'

    @escape()
    def function():
        return some_value

    assert function() == some_value


def test_run_simple_function_with_some_arguments_with_empty_brackets():
    @escape()
    def function(a, b, c=5):
        return a + b + c

    assert function(1, 2) == 8
    assert function(1, 2, 5) == 8
    assert function(1, 2, c=5) == 8
    assert function(1, 2, c=8) == 11


def test_run_function_with_exception_with_empty_brackets():
    @escape()
    def function(a, b, c=5):
        raise ValueError

    function(1, 2)


def test_run_coroutine_function_with_empty_brackets():
    some_value = 'kek'

    @escape()
    async def function():
        return some_value

    assert asyncio.run(function()) == some_value


def test_run_coroutine_function_with_some_arguments_with_empty_brackets():
    @escape()
    async def function(a, b, c=5):
        return a + b + c

    assert asyncio.run(function(1, 2)) == 8
    assert asyncio.run(function(1, 2, 5)) == 8
    assert asyncio.run(function(1, 2, c=5)) == 8
    assert asyncio.run(function(1, 2, c=8)) == 11


def test_run_coroutine_function_with_exception_with_empty_brackets():
    @escape()
    async def function(a, b, c=5):
        raise ValueError

    asyncio.run(function(1, 2))


def test_run_simple_function_with_default_return():
    some_value = 'kek'

    @escape(default='lol')
    def function():
        return some_value

    assert function() == some_value


def test_run_simple_function_with_some_arguments_with_default_return():
    @escape(default='lol')
    def function(a, b, c=5):
        return a + b + c

    assert function(1, 2) == 8
    assert function(1, 2, 5) == 8
    assert function(1, 2, c=5) == 8
    assert function(1, 2, c=8) == 11


def test_run_function_with_exception_with_default_return():
    default_value = 13

    @escape(default=default_value)
    def function(a, b, c=5):
        raise ValueError

    assert function(1, 2) == default_value


def test_run_coroutine_function_with_default_return():
    some_value = 'kek'

    @escape(default='lol')
    async def function():
        return some_value

    assert asyncio.run(function()) == some_value


def test_run_coroutine_function_with_some_arguments_with_default_return():
    @escape(default='lol')
    async def function(a, b, c=5):
        return a + b + c

    assert asyncio.run(function(1, 2)) == 8
    assert asyncio.run(function(1, 2, 5)) == 8
    assert asyncio.run(function(1, 2, c=5)) == 8
    assert asyncio.run(function(1, 2, c=8)) == 11


def test_run_coroutine_function_with_exception_with_default_return():
    default_value = 13

    @escape(default=default_value)
    async def function(a, b, c=5):
        raise ValueError

    assert asyncio.run(function(1, 2)) == default_value


def test_wrong_argument_to_decorator():
    with pytest.raises(ValueError, match=full_match('You are using the decorator for the wrong purpose.')):
        escape('kek')


def test_context_manager_with_empty_brackets_muted_by_default_exception():
    with escape():
        raise ValueError


def test_context_manager_with_empty_brackets_not_muted_by_default_exception():
    for not_muted_exception in (GeneratorExit, KeyboardInterrupt, SystemExit):
        with pytest.raises(not_muted_exception):
            with escape():
                raise not_muted_exception


def test_context_manager_with_exceptions_parameter_not_muted_exception():
    with pytest.raises(ValueError):
        with escape(exceptions=(ZeroDivisionError,)):
            raise ValueError

    with pytest.raises(ValueError):
        with escape(exceptions=[ZeroDivisionError]):
            raise ValueError


def test_context_manager_with_exceptions_parameter_muted_exception():
    for muted_exception in (GeneratorExit, KeyboardInterrupt, SystemExit):
        with escape(exceptions=(muted_exception,)):
            raise muted_exception

    for muted_exception in (GeneratorExit, KeyboardInterrupt, SystemExit):
        with escape(exceptions=[muted_exception]):
            raise muted_exception


def test_context_manager_without_breackets_muted_exception():
    for muted_exception in (ValueError, KeyError, Exception):
        with escape:
            raise muted_exception


def test_context_manager_without_breackets_not_muted_exception():
    for not_muted_exception in (GeneratorExit, KeyboardInterrupt, SystemExit):
        with pytest.raises(not_muted_exception):
            with escape:
                raise not_muted_exception


def test_decorator_without_breackets_saves_name_of_function():
    @escape
    def function():
        pass

    assert function.__name__ == 'function'


def test_decorator_without_breackets_saves_name_of_coroutine_function():
    @escape
    async def function():
        pass

    assert function.__name__ == 'function'


def test_context_manager_with_default_return_value():
    with pytest.raises(SetDefaultReturnValueForDecoratorError, match=full_match('You cannot set a default value for the context manager. This is only possible for the decorator.')):
        with escape(default='lol'):
            ...

def test_set_exceptions_types_with_bad_typed_value():
    with pytest.raises(ValueError, match=full_match('The list of exception types can be of the list or tuple type.')):
        escape(exceptions='lol')


def test_set_exceptions_types_with_bad_typed_exceptions_in_list():
    with pytest.raises(ValueError, match=full_match('The list of exception types can contain only exception types.')):
        escape(exceptions=[ValueError, 'lol'])


def test_decorator_with_list_of_muted_exceptions():
    @escape(exceptions=[ValueError])
    def function():
        raise ValueError

    function()


def test_decorator_with_list_of_not_muted_exceptions():
    @escape(exceptions=[ValueError])
    def function():
        raise KeyError

    with pytest.raises(KeyError):
        function()


def test_decorator_with_tuple_of_muted_exceptions():
    @escape(exceptions=(ValueError, ))
    def function():
        raise ValueError

    function()


def test_decorator_with_list_of_not_muted_exceptions():
    @escape(exceptions=(ValueError,))
    def function():
        raise KeyError

    with pytest.raises(KeyError):
        function()


def test_async_decorator_with_list_of_muted_exceptions():
    @escape(exceptions=[ValueError])
    async def function():
        raise ValueError

    asyncio.run(function())


def test_async_decorator_with_list_of_not_muted_exceptions():
    @escape(exceptions=[ValueError])
    async def function():
        raise KeyError

    with pytest.raises(KeyError):
        asyncio.run(function())


def test_async_decorator_with_tuple_of_muted_exceptions():
    @escape(exceptions=(ValueError, ))
    async def function():
        raise ValueError

    asyncio.run(function())


def test_async_decorator_with_list_of_not_muted_exceptions():
    @escape(exceptions=(ValueError,))
    async def function():
        raise KeyError

    with pytest.raises(KeyError):
        asyncio.run(function())


def test_default_default_value_is_none():
    @escape(exceptions=(ValueError,))
    def function():
        raise ValueError

    assert function() is None


def test_default_default_value_is_none_in_async_case():
    @escape(exceptions=(ValueError,))
    async def function():
        raise ValueError

    assert asyncio.run(function()) is None


def test_context_manager_normal_way():
    with escape:
        variable = True

    assert variable


def test_logging_catched_exception_without_message_usual_function():
    logger = MemoryLogger()

    @escape(logger=logger, default='kek')
    def function():
        raise ValueError

    assert function() == 'kek'

    assert len(logger.data.exception) == 1
    assert len(logger.data) == 1
    assert logger.data.exception[0].message == f'When executing function "function", the exception "ValueError" was suppressed.'


def test_logging_catched_exception_with_message_usual_function():
    logger = MemoryLogger()

    @escape(logger=logger, default='kek')
    def function():
        raise ValueError('lol kek cheburek')

    assert function() == 'kek'

    assert len(logger.data.exception) == 1
    assert len(logger.data) == 1
    assert logger.data.exception[0].message == f'When executing function "function", the exception "ValueError" ("lol kek cheburek") was suppressed.'


def test_logging_not_catched_exception_without_message_usual_function():
    logger = MemoryLogger()

    @escape(logger=logger, default='kek', exceptions=[ZeroDivisionError])
    def function():
        raise ValueError

    with pytest.raises(ValueError):
        function()

    assert len(logger.data.exception) == 1
    assert len(logger.data) == 1
    assert logger.data.exception[0].message == f'When executing function "function", the exception "ValueError" was not suppressed.'


def test_logging_not_catched_exception_with_message_usual_function():
    logger = MemoryLogger()

    @escape(logger=logger, default='kek', exceptions=[ZeroDivisionError])
    def function():
        raise ValueError('lol kek cheburek')

    with pytest.raises(ValueError, match='lol kek cheburek'):
        function()

    assert len(logger.data.exception) == 1
    assert len(logger.data) == 1
    assert logger.data.exception[0].message == f'When executing function "function", the exception "ValueError" ("lol kek cheburek") was not suppressed.'


def test_logging_catched_exception_without_message_coroutine_function():
    logger = MemoryLogger()

    @escape(logger=logger, default='kek')
    async def function():
        raise ValueError

    assert asyncio.run(function()) == 'kek'

    assert len(logger.data.exception) == 1
    assert len(logger.data) == 1
    assert logger.data.exception[0].message == f'When executing coroutine function "function", the exception "ValueError" was suppressed.'


def test_logging_catched_exception_with_message_coroutine_function():
    logger = MemoryLogger()

    @escape(logger=logger, default='kek')
    async def function():
        raise ValueError('lol kek cheburek')

    assert asyncio.run(function()) == 'kek'

    assert len(logger.data.exception) == 1
    assert len(logger.data) == 1
    assert logger.data.exception[0].message == f'When executing coroutine function "function", the exception "ValueError" ("lol kek cheburek") was suppressed.'


def test_logging_not_catched_exception_without_message_coroutine_function():
    logger = MemoryLogger()

    @escape(logger=logger, default='kek', exceptions=[ZeroDivisionError])
    async def function():
        raise ValueError

    with pytest.raises(ValueError):
        asyncio.run(function())

    assert len(logger.data.exception) == 1
    assert len(logger.data) == 1
    assert logger.data.exception[0].message == f'When executing coroutine function "function", the exception "ValueError" was not suppressed.'


def test_logging_not_catched_exception_with_message_coroutine_function():
    logger = MemoryLogger()

    @escape(logger=logger, default='kek', exceptions=[ZeroDivisionError])
    async def function():
        raise ValueError('lol kek cheburek')

    with pytest.raises(ValueError, match='lol kek cheburek'):
        asyncio.run(function())

    assert len(logger.data.exception) == 1
    assert len(logger.data) == 1
    assert logger.data.exception[0].message == f'When executing coroutine function "function", the exception "ValueError" ("lol kek cheburek") was not suppressed.'


def test_logging_suppressed_in_a_context_exception_without_message():
    logger = MemoryLogger()

    with escape(logger=logger):
        raise ValueError

    assert len(logger.data.exception) == 1
    assert len(logger.data) == 1
    assert logger.data.exception[0].message == 'The "ValueError" exception was suppressed inside the context.'


def test_logging_suppressed_in_a_context_exception_with_message():
    logger = MemoryLogger()

    with escape(logger=logger):
        raise ValueError('lol kek cheburek')

    assert len(logger.data.exception) == 1
    assert len(logger.data) == 1
    assert logger.data.exception[0].message == 'The "ValueError" ("lol kek cheburek") exception was suppressed inside the context.'


def test_logging_not_suppressed_in_a_context_exception_without_message():
    logger = MemoryLogger()

    with pytest.raises(ValueError):
        with escape(logger=logger, exceptions=[ZeroDivisionError]):
            raise ValueError

    assert len(logger.data.exception) == 1
    assert len(logger.data) == 1
    assert logger.data.exception[0].message == 'The "ValueError" exception was not suppressed inside the context.'


def test_logging_not_suppressed_in_a_context_exception_with_message():
    logger = MemoryLogger()

    with pytest.raises(ValueError, match='lol kek cheburek'):
        with escape(logger=logger, exceptions=[ZeroDivisionError]):
            raise ValueError('lol kek cheburek')

    assert len(logger.data.exception) == 1
    assert len(logger.data) == 1
    assert logger.data.exception[0].message == 'The "ValueError" ("lol kek cheburek") exception was not suppressed inside the context.'
