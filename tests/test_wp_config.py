#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             test_wp_website.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       02/01/2016
#
# description:      A unit test for ww module's WPConfig class and methods.
#

import mock
import pytest
from ww import WPConfig, WPSalt
from ww import settings as s


_INPUT = 'ext_pylib.input.prompts.INPUT'

SALTS = """define('AUTH_KEY',         'm`-Di%CcLS>E(V^KUtN?HIq)+GDQ{RpbJ4N~k =Hw[%-{Zt+oHO>JdO!uW-_5,v^');
define('SECURE_AUTH_KEY',  '5c 8cG8kfJ&0!e$x:GE ,jkB/U+tdND[Y`|MjgVA+qQI%.x/qu9)~cfQmb<>H~SU');
define('LOGGED_IN_KEY',    '3Surb*jDad=4(cVPNPM=PJl]&2BnU AJXU4p^EVG,cci%mHxq|MF s1@![=4 ajh');
define('NONCE_KEY',        '8&G*[f=py#+B!8!nIzpqd)B0r;s60]-tx8yWaRJ--2A-)NF4YxV_H`a[?w!iu|rT');
define('AUTH_SALT',        '.ed^{U[~- l^D4hR5^Q/,&b(21L{G04L,*k5v&{~*BbO%#DN xfw@3lVOv]klf--');
define('SECURE_AUTH_SALT', 'q%osy^V&j7#0tQtYbc?Ndr0PFZ1POujHfg+sgDA4Az#WZ|wFG%/2O+N)+>EC[Yd~');
define('LOGGED_IN_SALT',   'i~O~sCX+V4;|d6gUw)M8-]Mpj!|f#ypD5ZFos4|XJbrnQddaVe+[GP83PO@jZVo#');
define('NONCE_SALT',       '1S`>!Q@b2A+vpU-a:A=fqvKbv!*>d+AL|;&QcR!lsR+DO@L)fE;Qh>gz!~>vy5EK');
"""

def test_wpsalt_chars():
    """Tests wpsalt for correct length of chars."""
    salt = WPSalt()
    assert len(salt.secure_auth_key) == 64
    assert len(salt.logged_in_key) == 64
    assert len(salt.nonce_key) == 64
    assert len(salt.auth_salt) == 64
    assert len(salt.secure_auth_salt) == 64
    assert len(salt.logged_in_salt) == 64
    assert len(salt.nonce_salt) == 64

def test_wpsalt_assignment():
    """Tests wpsalt for assignment using multiple salts."""
    original_salt = WPSalt()
    static_salt = WPSalt()
    static_salt.data = SALTS
    for key, value in static_salt.secrets():
        setattr(original_salt, key, value)

    assert original_salt.secure_auth_key == static_salt.secure_auth_key
    assert original_salt.logged_in_key == static_salt.logged_in_key
    assert original_salt.nonce_key == static_salt.nonce_key
    assert original_salt.auth_salt == static_salt.auth_salt
    assert original_salt.secure_auth_salt == static_salt.secure_auth_salt
    assert original_salt.logged_in_salt == static_salt.logged_in_salt
    assert original_salt.nonce_salt == static_salt.nonce_salt

def test_wpconfig_init():
    """Tests wpconfig initialization."""
    config = WPConfig({ 'wp' : {
                        'table_prefix' : 'wp_',
                        'debug'        : 'true',
                        'db_name'      : 'the_dbname',
                        'db_user'      : 'the_username',
                        'db_password'  : 'the_password',
                        'db_host'      : 'localhost', } } )
    assert config.table_prefix == 'wp_'
    assert config.debug == 'true'
    assert config.db_name == 'the_dbname'
    assert config.db_user == 'the_username'
    assert config.db_password == 'the_password'
    assert config.db_host == 'localhost'
    config.debug = 'false'
    assert config.debug == 'false'
    config.db_name = 'a_new_db'
    assert config.db_name == 'a_new_db'

    assert len(config.secure_auth_key) == 64
    assert len(config.logged_in_key) == 64
    assert len(config.nonce_key) == 64
    assert len(config.auth_salt) == 64
    assert len(config.secure_auth_salt) == 64
    assert len(config.logged_in_salt) == 64
    assert len(config.nonce_salt) == 64

def test_wpconfig_parse():
    """Test wpconfig parse()."""
    with mock.patch(_INPUT, return_value='n'):
        config = WPConfig({
            'path' : s.WP_CONFIG_TEMPLATE,
            'wp' : {
                'debug'            : 'true',
                'table_prefix'     : 'xyz',
                'db_name'          : 'the_dbname',
                'db_user'          : 'the_user',
                'db_password'      : 'the_password',
                'db_host'          : 'the_host',
                'disallow_edit'    : 'false',
                'fs_method'        : 'whatever',
                'auth_key'         : 'salt overwritten',
                'secure_auth_key'  : 'salt overwritten',
                'logged_in_key'    : 'salt overwritten',
                'nonce_key'        : 'salt overwritten',
                'auth_salt'        : 'salt overwritten',
                'secure_auth_salt' : 'salt overwritten',
                'logged_in_salt'   : 'salt overwritten',
                'nonce_salt'       : 'salt overwritten', } } )

    with mock.patch(_INPUT, return_value='y'):
        config_2 = WPConfig({'path' : s.WP_CONFIG_TEMPLATE})

    result_in_memory = {
        'debug'            : 'true',
        'table_prefix'     : 'xyz',
        'db_name'          : 'the_dbname',
        'db_user'          : 'the_user',
        'db_password'      : 'the_password',
        'db_host'          : 'the_host',
        'disallow_edit'    : 'false',
        'fs_method'        : 'whatever',
        'auth_key'         : 'salt overwritten',
        'secure_auth_key'  : 'salt overwritten',
        'logged_in_key'    : 'salt overwritten',
        'nonce_key'        : 'salt overwritten',
        'auth_salt'        : 'salt overwritten',
        'secure_auth_salt' : 'salt overwritten',
        'logged_in_salt'   : 'salt overwritten',
        'nonce_salt'       : 'salt overwritten', }

    result_on_disk = {
        'debug'            : 'false',
        'table_prefix'     : 'wp_',
        'db_name'          : 'db_name',
        'db_user'          : 'db_user',
        'db_password'      : 'db_password',
        'db_host'          : 'localhost',
        'disallow_edit'    : 'true',
        'fs_method'        : 'direct',
        'auth_key'         : 'put your unique phrase here',
        'secure_auth_key'  : 'put your unique phrase here',
        'logged_in_key'    : 'put your unique phrase here',
        'nonce_key'        : 'put your unique phrase here',
        'auth_salt'        : 'put your unique phrase here',
        'secure_auth_salt' : 'put your unique phrase here',
        'logged_in_salt'   : 'put your unique phrase here',
        'nonce_salt'       : 'put your unique phrase here', }

    assert config.parse() == result_in_memory
    assert config.parse(True) == result_on_disk
    assert config_2.parse() == result_on_disk

def test_wpconfig_verify():
    """Test wpconfig verify() and repair."""
    with mock.patch(_INPUT, return_value='y'):
        config = WPConfig({'path' : s.WP_CONFIG_TEMPLATE})

    assert config.verify()

    config.debug = 'true'
    assert not config.verify()  # Debug should not be set to true

    config.debug = 'false'
    assert config.verify()  # Debug should be set to false

    config.db_name = 'new_value'
    with mock.patch(_INPUT, return_value='n'):
        assert config.verify(True)  # Change db_name in memory and repair
    assert config.db_name == 'new_value'

    config.db_name = 'db_name'  # Change db_name back
    with mock.patch(_INPUT, return_value='n'):
        assert config.verify(True)  # by doing a repair
    assert config.db_name == 'db_name'
