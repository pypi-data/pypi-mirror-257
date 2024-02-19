import re
from unittest.mock import Mock, PropertyMock, call

import pytest

from upsies import errors
from upsies.jobs.set import SetJob


def test_name():
    assert SetJob.name == 'set'


def test_label():
    assert SetJob.label == 'Set'


def test_hidden():
    assert SetJob.hidden is True


def test_cache_id():
    assert SetJob.cache_id is None


@pytest.mark.parametrize(
    argnames='kwargs, exp_exception, exp_attributes',
    argvalues=(
        pytest.param(
            {
                'config': 'mock config',
            },
            None,
            {
                '_config': 'mock config',
                '_option': None,
                '_value': '',
                '_reset': None,
                '_dump': (),
            },
            id='Display complete configuration',
        ),

        pytest.param(
            {
                'config': 'mock config',
                'option': 'mock option',
            },
            None,
            {
                '_config': 'mock config',
                '_option': 'mock option',
                '_value': '',
                '_reset': None,
                '_dump': (),
            },
            id='Display single option',
        ),

        pytest.param(
            {
                'config': 'mock config',
                'option': 'mock option',
                'value': 'my value',
            },
            None,
            {
                '_config': 'mock config',
                '_option': 'mock option',
                '_value': 'my value',
                '_reset': None,
                '_dump': (),
            },
            id='Change option',
        ),

        pytest.param(
            {
                'config': 'mock config',
                'option': 'mock option',
                'reset': True,
            },
            None,
            {
                '_config': 'mock config',
                '_option': 'mock option',
                '_value': '',
                '_reset': True,
                '_dump': (),
            },
            id='Reset complete configuration',
        ),

        pytest.param(
            {
                'config': 'mock config',
                'reset': True,
            },
            None,
            {
                '_config': 'mock config',
                '_option': None,
                '_value': '',
                '_reset': True,
                '_dump': (),
            },
            id='Reset single option',
        ),

        pytest.param(
            {
                'config': 'mock config',
                'dump': ('this', 'and', 'that'),
            },
            None,
            {
                '_config': 'mock config',
                '_option': None,
                '_value': '',
                '_reset': None,
                '_dump': ('this', 'and', 'that'),
            },
            id='Dump configuration',
        ),

        pytest.param(
            {
                'config': 'mock config',
                'option': 'mock option',
                'dump': ('this', 'and', 'that'),
            },
            RuntimeError('Arguments "option" and "dump" are mutually exclusive.'),
            {},
            id='Invalid arguments: option and dump',
        ),

        pytest.param(
            {
                'config': 'mock config',
                'value': 'my value',
                'reset': True,
            },
            RuntimeError('Arguments "value" and "reset" are mutually exclusive.'),
            {},
            id='Invalid arguments: value and reset',
        ),

        pytest.param(
            {
                'config': 'mock config',
                'value': 'my value',
                'dump': ('this', 'and', 'that'),
            },
            RuntimeError('Arguments "value" and "dump" are mutually exclusive.'),
            {},
            id='Invalid arguments: value and dump',
        ),
    ),
    ids=lambda v: repr(v),
)
def test_initialize(kwargs, exp_exception, exp_attributes, mocker):
    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(SetJob, 'run'), 'run')

    if isinstance(exp_exception, Exception):
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
            SetJob(**kwargs)
    else:
        job = SetJob(**kwargs)
        assert {
            name: getattr(job, name)
            for name in exp_attributes
        } == exp_attributes


@pytest.mark.parametrize(
    argnames='attributes, methods, exp_mock_calls',
    argvalues=(
        pytest.param(
            {'_reset': True, '_value': 'my value', '_dump': ('this', 'and', 'that')},
            {'_reset_mode': Mock()},
            [
                call._reset_mode(),
            ],
            id='Reset mode succeeds',
        ),
        pytest.param(
            {'_reset': True, '_value': 'my value', '_dump': ('this', 'and', 'that')},
            {'_reset_mode': Mock(side_effect=errors.ConfigError('reset error'))},
            [
                call._reset_mode(),
                call.error(errors.ConfigError('reset error')),
            ],
            id='Reset mode fails',
        ),

        pytest.param(
            {'_reset': False, '_value': 'my value', '_dump': ('this', 'and', 'that')},
            {'_set_mode': Mock()},
            [
                call._set_mode(),
            ],
            id='Set mode succeeds',
        ),
        pytest.param(
            {'_reset': False, '_value': 'my value', '_dump': ('this', 'and', 'that')},
            {'_set_mode': Mock(side_effect=errors.ConfigError('set error'))},
            [
                call._set_mode(),
                call.error(errors.ConfigError('set error')),
            ],
            id='Set mode fails',
        ),

        pytest.param(
            {'_reset': False, '_value': '', '_dump': ('this', 'and', 'that')},
            {'_dump_mode': Mock()},
            [
                call._dump_mode(),
            ],
            id='Dump mode succeeds',
        ),
        pytest.param(
            {'_reset': False, '_value': '', '_dump': ('this', 'and', 'that')},
            {'_dump_mode': Mock(side_effect=errors.ConfigError('dump error'))},
            [
                call._dump_mode(),
                call.error(errors.ConfigError('dump error')),
            ],
            id='Dump mode fails',
        ),

        pytest.param(
            {'_reset': False, '_value': '', '_dump': ()},
            {'_display_mode': Mock()},
            [
                call._display_mode(),
            ],
            id='Display mode succeeds',
        ),
        pytest.param(
            {'_reset': False, '_value': '', '_dump': ()},
            {'_display_mode': Mock(side_effect=errors.ConfigError('display error'))},
            [
                call._display_mode(),
                call.error(errors.ConfigError('display error')),
            ],
            id='Display mode fails',
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_run(attributes, methods, exp_mock_calls, mocker):
    job = SetJob(config='mock config')

    for name, value in attributes.items():
        mocker.patch.object(type(job), name, PropertyMock(return_value=value), create=True)

    mocks = Mock()
    for name, mock in methods.items():
        mocks.attach_mock(mocker.patch.object(job, name, mock), name)
    mocks.attach_mock(mocker.patch.object(job, 'error'), 'error')

    await job.run()

    assert mocks.mock_calls == exp_mock_calls


@pytest.mark.parametrize(
    argnames='option, paths, exp_mock_calls',
    argvalues=(
        pytest.param(
            'foo.b.that',
            ('foo.a.this', 'foo.b.that', 'bar.c.baz'),
            [
                call.reset('foo.b.that'),
                call._write('foo.b.that'),
            ],
            id='Reset single option',
        ),
        pytest.param(
            None,
            ('foo.a.this', 'foo.b.that', 'bar.c.baz'),
            [
                call.reset('foo.a.this'), call._write('foo.a.this'),
                call.reset('foo.b.that'), call._write('foo.b.that'),
                call.reset('bar.c.baz'), call._write('bar.c.baz'),
            ],
            id='Reset all options',
        ),
    ),
    ids=lambda v: repr(v),
)
def test__reset_mode(option, paths, exp_mock_calls, mocker):
    job = SetJob(config='mock config')

    mocker.patch.object(job, '_option', option)
    mocker.patch.object(job, '_config', Mock(paths=paths))
    mocker.patch.object(job, '_write', Mock())

    mocks = Mock()
    mocks.attach_mock(job._config.reset, 'reset')
    mocks.attach_mock(job._write, '_write')

    job._reset_mode()

    assert mocks.mock_calls == exp_mock_calls


def test__set_mode(mocker):
    job = SetJob(config='mock config')

    mocker.patch.object(job, '_config', {})
    mocker.patch.object(job, '_option', 'my option')
    mocker.patch.object(job, '_value', 'my value')
    mocker.patch.object(job, '_write', Mock())

    job._set_mode()
    assert job._config['my option'] == 'my value'
    assert job._write.call_args_list == [call('my option')]


@pytest.mark.parametrize(
    argnames='option, paths, exp_mock_calls',
    argvalues=(
        pytest.param(
            'foo.b.that',
            ('foo.a.this', 'foo.b.that', 'bar.c.baz'),
            [
                call._display_option('foo.b.that'),
            ],
            id='Display single option',
        ),
        pytest.param(
            '',
            ('foo.a.this', 'foo.b.that', 'bar.c.baz'),
            [
                call._display_option('foo.a.this'),
                call._display_option('foo.b.that'),
                call._display_option('bar.c.baz'),
            ],
            id='Display all options',
        ),
    ),
    ids=lambda v: repr(v),
)
def test__display_mode(option, paths, exp_mock_calls, mocker):
    job = SetJob(config='mock config')

    mocker.patch.object(job, '_option', option)
    mocker.patch.object(job, '_config', Mock(paths=paths))

    mocks = Mock()
    mocks.attach_mock(
        mocker.patch.object(job, '_display_option', Mock()),
        '_display_option',
    )

    job._display_mode()

    assert mocks.mock_calls == exp_mock_calls


@pytest.mark.parametrize(
    argnames='option, paths, exp_mock_calls',
    argvalues=(
        pytest.param(
            'foo.b.that',
            ('foo.a.this', 'foo.b.that', 'bar.c.baz'),
            [
                call._display_option('foo.b.that'),
            ],
            id='Display single option',
        ),
        pytest.param(
            '',
            ('foo.a.this', 'foo.b.that', 'bar.c.baz'),
            [
                call._display_option('foo.a.this'),
                call._display_option('foo.b.that'),
                call._display_option('bar.c.baz'),
            ],
            id='Display all options',
        ),
    ),
    ids=lambda v: repr(v),
)
def test__dump_mode(option, paths, exp_mock_calls, mocker, tmp_path):
    job = SetJob(config='mock config')

    files = {
        'foo': tmp_path / 'foo.ini',
        'bar': tmp_path / 'bar.ini',
        'baz': tmp_path / 'baz.ini',
    }

    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(job, 'send'), 'send')
    mocker.patch.object(job, '_dump', ('foo', 'baz'))

    def write(section, include_defaults):
        files[section].write_text(f'[mock section {section}, include_defaults={include_defaults}')

    mocker.patch.object(job, '_config', Mock(
        files=files,
        write=Mock(side_effect=write),
    ))
    mocks.attach_mock(job._config.write, '_config_write')

    job._dump_mode()

    assert mocks.mock_calls == [
        call._config_write('foo', include_defaults=True),
        call.send('#' * 64),
        call.send('### ' + (str(files['foo']) + ' ').ljust(60, '#')),
        call.send('#' * 64),
        call.send('[mock section foo, include_defaults=True'),

        call._config_write('baz', include_defaults=True),
        call.send('#' * 64),
        call.send('### ' + (str(files['baz']) + ' ').ljust(60, '#')),
        call.send('#' * 64),
        call.send('[mock section baz, include_defaults=True'),
    ]

    assert files['foo'].read_text() == '[mock section foo, include_defaults=True'
    assert not files['bar'].exists()
    assert files['baz'].read_text() == '[mock section baz, include_defaults=True'


def test__write(mocker):
    job = SetJob(config='mock config')

    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(job, '_config', Mock(write=Mock())), '_config')
    mocks.attach_mock(mocker.patch.object(job, '_display_option', Mock()), '_display_option')

    job._write('my option')
    assert mocks.mock_calls == [
        call._config.write('my option'),
        call._display_option('my option'),
    ]


@pytest.mark.parametrize(
    argnames='option, value, exp_mock_calls',
    argvalues=(
        pytest.param(
            'my option',
            ('foo', 'bar', 'baz'),
            [
                call.send('my option =\n  ' + 'foo\n  bar\n  baz')
            ],
            id='Non-empty sequence',
        ),
        pytest.param(
            'my option',
            (),
            [
                call.send('my option =')
            ],
            id='Empty sequence',
        ),
        pytest.param(
            'my option',
            'hello',
            [
                call.send('my option = hello')
            ],
            id='Non-sequence',
        ),
    ),
    ids=lambda v: repr(v),
)
def test__display_option(option, value, exp_mock_calls, mocker):
    job = SetJob(config='mock config')

    mocker.patch.object(job, '_config', {option: value})

    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(job, 'send'), 'send')

    job._display_option(option)
    assert mocks.mock_calls == exp_mock_calls
