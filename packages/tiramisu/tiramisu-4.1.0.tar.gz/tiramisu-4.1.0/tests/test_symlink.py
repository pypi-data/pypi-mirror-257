# coding: utf-8
import pytest
from .autopath import do_autopath
do_autopath()
from .config import config_type, get_config

from tiramisu import BoolOption, StrOption, SymLinkOption, submulti, \
    OptionDescription, Leadership, Config, Calculation, calc_value, Params, ParamOption, ParamValue
from tiramisu.error import PropertiesOptionError, ConfigError
from tiramisu.setting import groups, owners
from tiramisu.i18n import _


def return_value():
    pass


#____________________________________________________________
def test_symlink_option(config_type):
    boolopt = BoolOption("b", "", default=False)
    linkopt = SymLinkOption("c", boolopt)
    od1 = OptionDescription("opt", "",
                            [linkopt, OptionDescription("s1", "", [boolopt])],
                            )
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert not cfg.option('s1.b').issymlinkoption()
    assert cfg.option('c').issymlinkoption()
    assert cfg.option('s1.b').type() == _('boolean')
    assert cfg.option('c').type() == _('boolean')
    assert cfg.option('s1.b').value.get() is False
    cfg.option("s1.b").value.set(True)
    cfg.option("s1.b").value.set(False)
    assert cfg.option('s1.b').value.get() is False
    assert cfg.option('c').value.get() is False
    cfg.option('s1.b').value.set(True)
    assert cfg.option('s1.b').value.get() is True
    assert cfg.option('c').value.get() is True
    cfg.option('s1.b').value.set(False)
    assert cfg.option('s1.b').value.get() is False
    assert cfg.option('c').value.get() is False
#    assert not list_sessions()


def test_symlink_default(config_type):
    boolopt = BoolOption("b", "", default=False)
    linkopt = SymLinkOption("c", boolopt)
    od1 = OptionDescription("opt", "",
                            [linkopt, OptionDescription("s1", "", [boolopt])],
                            )
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert not cfg.option('s1.b').ismulti()
    assert not cfg.option('c').ismulti()
    assert not cfg.option('s1.b').issubmulti()
    assert not cfg.option('c').issubmulti()
    assert not cfg.option('s1.b').default()
    assert not cfg.option('c').default()
    assert not cfg.option('s1.b').value.default()
    assert not cfg.option('c').value.default()
    with pytest.raises(ConfigError):
        assert not cfg.option('s1.b').defaultmulti()
    with pytest.raises(ConfigError):
        assert not cfg.option('c').defaultmulti()
    cfg.option("s1.b").value.set(True)
    assert not cfg.option('s1.b').default()
    assert not cfg.option('c').default()
    assert not cfg.option('s1.b').value.default()
    assert not cfg.option('c').value.default()
##    assert not list_sessions()


def test_symlink_default_multi(config_type):
    boolopt = BoolOption("b", "", default=[False], default_multi=True, multi=True)
    linkopt = SymLinkOption("c", boolopt)
    od1 = OptionDescription("opt", "",
                            [linkopt, OptionDescription("s1", "", [boolopt])],
                            )
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.option('s1.b').ismulti()
    assert cfg.option('c').ismulti()
    assert not cfg.option('s1.b').issubmulti()
    assert not cfg.option('c').issubmulti()
    assert cfg.option('s1.b').default() == [False]
    assert cfg.option('c').default() == [False]
    assert cfg.option('s1.b').value.default() == [False]
    assert cfg.option('c').value.default() == [False]
    assert cfg.option('s1.b').defaultmulti()
    assert cfg.option('c').defaultmulti()
    cfg.option("s1.b").value.set([True])
    assert cfg.option('s1.b').default() == [False]
    assert cfg.option('c').default() == [False]
    assert cfg.option('s1.b').value.default() == [False]
    assert cfg.option('c').value.default() == [False]
    assert cfg.option('s1.b').defaultmulti()
    assert cfg.option('c').defaultmulti()
##    assert not list_sessions()


def test_symlink_assign_option(config_type):
    boolopt = BoolOption("b", "", default=False)
    linkopt = SymLinkOption("c", boolopt)
    od1 = OptionDescription("opt", "",
                              [linkopt, OptionDescription("s1", "", [boolopt])])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    with pytest.raises(ConfigError):
        cfg.option('c').value.set(True)
#    assert not list_sessions()


def test_symlink_del_option(config_type):
    boolopt = BoolOption("b", "", default=False)
    linkopt = SymLinkOption("c", boolopt)
    od1 = OptionDescription("opt", "",
                              [linkopt, OptionDescription("s1", "", [boolopt])])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    with pytest.raises(ConfigError):
        cfg.option('c').value.reset()
#    assert not list_sessions()


def test_symlink_addproperties():
    boolopt = BoolOption('b', '', default=True, properties=('test',))
    linkopt = SymLinkOption("c", boolopt)
    od1 = OptionDescription('opt', '', [boolopt, linkopt])
    cfg = Config(od1)
    cfg.property.read_write()
    with pytest.raises(ConfigError):
        cfg.option('c').property.add('new')
    with pytest.raises(ConfigError):
        cfg.option('c').property.reset()
#    assert not list_sessions()


def test_symlink_getpermissive():
    boolopt = BoolOption('b', '', default=True, properties=('test',))
    linkopt = SymLinkOption("c", boolopt)
    od1 = OptionDescription('opt', '', [boolopt, linkopt])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.option('b').permissive.set(frozenset(['perm']))
    cfg.option('c').permissive.get() == frozenset(['perm'])
#    assert not list_sessions()


def test_symlink_addpermissives():
    boolopt = BoolOption('b', '', default=True, properties=('test',))
    linkopt = SymLinkOption("c", boolopt)
    od1 = OptionDescription('opt', '', [boolopt, linkopt])
    cfg = Config(od1)
    cfg.property.read_write()
    with pytest.raises(ConfigError):
        cfg.option('c').permissive.set(frozenset(['new']))
    with pytest.raises(ConfigError):
        cfg.option('c').permissive.reset()
#    assert not list_sessions()


def test_symlink_getproperties():
    boolopt = BoolOption('b', '', default=True, properties=('test',))
    linkopt = SymLinkOption("c", boolopt)
    od1 = OptionDescription('opt', '', [boolopt, linkopt])
    cfg = Config(od1)
    cfg.property.read_write()
    assert boolopt.impl_getproperties() == linkopt.impl_getproperties() == {'test'}
#    assert boolopt.impl_has_callback() == linkopt.impl_has_callback() == False
#    assert not list_sessions()


def test_symlink_getcallback():
    boolopt = BoolOption('b', '', Calculation(return_value))
    linkopt = SymLinkOption("c", boolopt)
    od1 = OptionDescription('opt', '', [boolopt, linkopt])
    cfg = Config(od1)
    cfg.property.read_write()
    #assert boolopt.impl_has_callback() == linkopt.impl_has_callback() == True
    #assert boolopt.impl_get_callback() == linkopt.impl_get_callback() == (return_value, None)
#    assert boolopt.impl_has_callback() == linkopt.impl_has_callback() == False
#    assert not list_sessions()


def test_symlink_requires(config_type):
    boolopt = BoolOption('b', '', default=True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(boolopt),
                                                   'expected': ParamValue(False)}))
    stropt = StrOption('s', '', properties=(disabled_property,))
    linkopt = SymLinkOption("c", stropt)
    od1 = OptionDescription('opt', '', [boolopt, stropt, linkopt])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('b').value.get() is True
    assert cfg.option('s').value.get() is None
    assert cfg.option('c').value.get() is None
    cfg.option('b').value.set(False)
    #
    props = []
    try:
        cfg.option('s').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert props == {'disabled'}
    #
    props = []
    try:
        cfg.option('c').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert props == {'disabled'}
#    assert not list_sessions()


def test_symlink_multi(config_type):
    boolopt = BoolOption("b", "", default=[False], multi=True)
    linkopt = SymLinkOption("c", boolopt)
    od1 = OptionDescription("opt", "",
                              [linkopt, OptionDescription("s1", "", [boolopt])])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.option('s1.b').value.get() == [False]
    assert cfg.option('c').value.get() == [False]
    cfg.option('s1.b').value.set([True])
    assert cfg.option('s1.b').value.get() == [True]
    assert cfg.option('c').value.get() == [True]
    cfg.option('s1.b').value.set([False])
    assert cfg.option('s1.b').value.get() == [False]
    assert cfg.option('c').value.get() == [False]
    cfg.option('s1.b').value.set([False, True])
    assert cfg.option('s1.b').value.get() == [False, True]
    assert cfg.option('c').value.get() == [False, True]
    assert boolopt.impl_is_multi() is True
    assert linkopt.impl_is_multi() is True
#    assert not list_sessions()


def test_symlink_assign(config_type):
    boolopt = BoolOption("b", "", default=False)
    linkopt = SymLinkOption("c", boolopt)
    od1 = OptionDescription("opt", "",
                              [linkopt, OptionDescription("s1", "", [boolopt])])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    with pytest.raises(ConfigError):
        cfg.option('c').value.set(True)
#    assert not list_sessions()


def test_symlink_owner(config_type):
    boolopt = BoolOption("b", "", default=False)
    linkopt = SymLinkOption("c", boolopt)
    od1 = OptionDescription("opt", "",
                              [linkopt, OptionDescription("s1", "", [boolopt])])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.option('s1.b').owner.isdefault()
    assert cfg.option('c').owner.isdefault()
    cfg.option('s1.b').value.set(True)
    assert not cfg.option('s1.b').owner.isdefault()
    assert not cfg.option('c').owner.isdefault()
#    assert not list_sessions()


def test_symlink_get_information():
    boolopt = BoolOption("b", "", default=False)
    linkopt = SymLinkOption("c", boolopt)
    boolopt.impl_set_information('test', 'test')
    assert boolopt.impl_get_information('test') == 'test'
    assert linkopt.impl_get_information('test') == 'test'
    boolopt.impl_set_information('test', 'test2')
    assert boolopt.impl_get_information('test') == 'test2'
    assert linkopt.impl_get_information('test') == 'test2'


def test_symlink_leader():
    a = StrOption('a', "", multi=True)
    ip_admin_eth0 = SymLinkOption('ip_admin_eth0', a)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "", multi=True)
    with pytest.raises(ValueError):
        Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])


def test_symlink_followers():
    a = StrOption('a', "", multi=True)
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = SymLinkOption('netmask_admin_eth0', a)
    with pytest.raises(ValueError):
        Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])


def test_symlink_with_leader(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    leader = SymLinkOption('leader', ip_admin_eth0)
    od1 = OptionDescription('root', '', [interface1, leader])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.value.dict() == {'ip_admin_eth0.ip_admin_eth0': [], 'leader': []}
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['val1', 'val2'])
    assert cfg.value.dict() == {'ip_admin_eth0.ip_admin_eth0': [{'ip_admin_eth0.ip_admin_eth0': 'val1', 'ip_admin_eth0.netmask_admin_eth0': None}, {'ip_admin_eth0.ip_admin_eth0': 'val2', 'ip_admin_eth0.netmask_admin_eth0': None}], 'leader': ['val1', 'val2']}
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.pop(0)
    with pytest.raises(ConfigError):
        cfg.option('leader').value.pop(0)
#    assert not list_sessions()


def test_symlink_with_follower(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    follower = SymLinkOption('follower', netmask_admin_eth0)
    od1 = OptionDescription('root', '', [interface1, follower])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert not cfg.option('follower').isoptiondescription()
    assert cfg.value.dict() == {'ip_admin_eth0.ip_admin_eth0': [], 'follower': []}
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['val1', 'val2'])
    assert cfg.value.dict() == {'ip_admin_eth0.ip_admin_eth0': [{'ip_admin_eth0.ip_admin_eth0': 'val1', 'ip_admin_eth0.netmask_admin_eth0': None}, {'ip_admin_eth0.ip_admin_eth0': 'val2', 'ip_admin_eth0.netmask_admin_eth0': None}], 'follower': [None, None]}
    #
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).owner.get() == 'default'
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).owner.get() == 'default'
    with pytest.raises(ConfigError):
        assert cfg.option('follower', 0).owner.get() == 'default'
    assert cfg.option('follower').owner.get() == 'default'
    #
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == None
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.get() == None
    with pytest.raises(ConfigError):
        assert cfg.option('follower', 0).value.get() == None
    assert cfg.option('follower').value.get() == [None, None]
    #
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.set('val3')
    assert cfg.value.dict() == {'ip_admin_eth0.ip_admin_eth0': [{'ip_admin_eth0.ip_admin_eth0': 'val1', 'ip_admin_eth0.netmask_admin_eth0': None}, {'ip_admin_eth0.ip_admin_eth0': 'val2', 'ip_admin_eth0.netmask_admin_eth0': 'val3'}], 'follower': [None, 'val3']}
    #
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == None
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.get() == 'val3'
    with pytest.raises(ConfigError):
        assert cfg.option('follower', 0).value.get() == None
    assert cfg.option('follower').value.get() == [None, 'val3']
    #
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).owner.get() == 'default'
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).owner.get() == 'user'
    with pytest.raises(ConfigError):
        assert cfg.option('follower', 0).owner.get() == 'default'
    assert cfg.option('follower').owner.get() == 'user'
#    assert not list_sessions()


#____________________________________________________________
def test_symlink_dependency():
    boolopt = BoolOption("b", "", default=False)
    linkopt = SymLinkOption("c", boolopt)
    od1 = OptionDescription("opt", "",
                              [linkopt, OptionDescription("s1", "", [boolopt])])
    cfg = Config(od1)
    assert cfg.option('s1.b').has_dependency() is False
    assert cfg.option('c').has_dependency() is True
    assert cfg.option('s1.b').has_dependency(False) is True
    assert cfg.option('c').has_dependency(False) is False
#    assert not list_sessions()


def test_symlink_makedict(config_type):
    boolopt = BoolOption("b", "", default=False)
    linkopt = SymLinkOption("c", boolopt)
    od1 = OptionDescription("opt", "",
                              [linkopt, OptionDescription("s1", "", [boolopt])])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.value.dict() == {'c': False, 's1.b': False}
    cfg.option('s1.b').value.set(True)
    assert cfg.value.dict() == {'c': True, 's1.b': True}
#    assert not list_sessions()


def test_symlink_list(config_type):
    boolopt = BoolOption("b", "", default=False)
    linkopt = SymLinkOption("c", boolopt)
    od1 = OptionDescription("opt", "",
                              [linkopt, OptionDescription("s1", "", [boolopt])])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    list_opt = []
    for opt in cfg.option.list():
        list_opt.append(opt.path())
    assert list_opt == ['c']
    #
    list_opt = []
    for opt in cfg.option.list(recursive=True):
        list_opt.append(opt.path())
    assert list_opt == ['c', 's1.b']
#    assert not list_sessions()


def test_submulti():
    multi = StrOption('multi', '', multi=submulti)
    multi2 = SymLinkOption('multi2', multi)
    od1 = OptionDescription('od', '', [multi, multi2])
    cfg = Config(od1)
    assert cfg.option('multi').ismulti()
    assert cfg.option('multi').issubmulti()
    assert cfg.option('multi2').ismulti()
    assert cfg.option('multi2').issubmulti()
