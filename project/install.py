#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2016-Today  Carlos Eduardo Vercelino - CLVsol
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from __future__ import print_function

import images

import argparse
import getpass

import openerplib
import erppeek
import xmlrpclib

update = False
CompanyName = 'CLVhealth-PBM'
Slogan = ''
Company_image = images.Company_image
website = 'https://github.com/CLVsol'
admin_user_email = 'admin@clvsol.com'
Administrator_image = images.Administrator_image
Demo_User_image = images.Demo_User_image
DataAdministrator_image = images.DataAdministrator_image
demo_user_name = 'Demo User'
demo_user = 'demo'
demo_user_pw = 'demo'
demo_user_email = 'demo.user@clvsol.com'
data_admin_user_name = 'Data Administrator'
data_admin_user = 'data.admin'
data_admin_user_pw = 'data.admin'
data_admin_user_email = 'data.admin@clvsol.com'

# lang = 'en_US'
lang = 'pt_BR'  # use Translation: Portuguese(BR)/Portugues(BR)
tz = 'America/Sao_Paulo'

hostname = 'localhost'
server = 'http://localhost:8069'
admin = 'admin'
admin_user = 'admin'

admin_pw = 'admin'
admin_user_pw = 'admin'
data_admin_user_pw = 'data.admin'
dbname = 'clvhealth_pbm'
demo_data = False
modules_to_update = []

sock_common_url = 'http://localhost:8069/xmlrpc/common'
sock_str = 'http://localhost:8069/xmlrpc/object'


def get_arguments():

    global update
    global admin_pw
    global admin_user_pw
    global data_admin_user_pw
    global dbname
    global demo_data
    global modules_to_update

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--update_all', action='store_true', help='Update all the modules')
    parser.add_argument('--admin_pw', action="store", dest="admin_pw")
    parser.add_argument('--admin_user_pw', action="store", dest="admin_user_pw")
    parser.add_argument('--data_admin_user_pw', action="store", dest="data_admin_user_pw")
    parser.add_argument('--dbname', action="store", dest="dbname")
    parser.add_argument('-d', '--demo_data', action='store_true', help='Install demo data')
    parser.add_argument('-m', '--modules', nargs='+', help='Modules to update', required=False)

    args = parser.parse_args()

    print('\n%s%s\n' % ('--> ', args))

    update = args.update_all

    if args.admin_pw is not None:
        admin_pw = args.admin_pw
    elif admin_pw == '*':
        admin_pw = getpass.getpass('admin_pw: ')

    if args.admin_user_pw is not None:
        admin_user_pw = args.admin_user_pw
    elif admin_user_pw == '*':
        admin_user_pw = getpass.getpass('admin_user_pw: ')

    if args.data_admin_user_pw is not None:
        data_admin_user_pw = args.data_admin_user_pw
    elif data_admin_user_pw == '*':
        data_admin_user_pw = getpass.getpass('data_admin_user_pw: ')

    if args.dbname is not None:
        dbname = args.dbname
    elif dbname == '*':
        dbname = raw_input('dbname: ')

    demo_data = args.demo_data

    if args.modules is not None:
        modules_to_update = args.modules
    else:
        modules_to_update = []


def create_database():

    connection = openerplib.get_connection(hostname=hostname,
                                           database=None,
                                           login=admin,
                                           password=admin_user_pw)
    db_service = connection.get_service('db')
    print('Databases found: {0}'.format(db_service.list()))
    if not db_service.db_exist(dbname):
        print('Creating database "{0}"...'.format(dbname))
        db_service.create_database(admin_pw,
                                   dbname,
                                   demo_data,
                                   lang,
                                   admin_user_pw)
        print('Created database "{0}".'.format(dbname))
        return True
    else:
        print('Using existing database "{0}".'.format(dbname))
        return False


def MyCompany():

    print('Configuring My Company...')

    sock_common = xmlrpclib.ServerProxy(sock_common_url)
    uid = sock_common.login(dbname, admin_user, admin_user_pw)
    sock = xmlrpclib.ServerProxy(sock_str)

    args = [('name', '=', 'My Company'), ]
    partner_id = sock.execute(dbname, uid, admin_user_pw, 'res.partner', 'search', args)
    values = {
        'name': CompanyName,
        'email': '',
        'website': website,
        'tz': tz,
        'lang': lang,
        'image': Company_image,
    }
    sock.execute(dbname, uid, admin_user_pw, 'res.partner', 'write', partner_id, values)

    args = [('name', '=', 'My Company'), ]
    company_id = sock.execute(dbname, uid, admin_user_pw, 'res.company', 'search', args)
    values = {
        'name': CompanyName,
        'email': '',
        'website': website,
        'rml_header1': Slogan,
        'logo': Company_image,
    }
    sock.execute(dbname, uid, admin_user_pw, 'res.company', 'write', company_id, values)

    print('Done.')


def Administrator():

    print('Configuring user "Administrator"...')

    sock_common = xmlrpclib.ServerProxy(sock_common_url)
    uid = sock_common.login(dbname, admin_user, admin_user_pw)
    sock = xmlrpclib.ServerProxy(sock_str)

    args = [('name', '=', 'Administrator'), ]
    user_id = sock.execute(dbname, uid, admin_user_pw, 'res.users', 'search', args)
    values = {
        'lang': lang,
        'tz': tz,
        'email': admin_user_email,
        'image': Administrator_image,
    }
    sock.execute(dbname, uid, admin_user_pw, 'res.users', 'write', user_id, values)

    values = {
        'groups_id': [(6, 0, [
            sock.execute(
                dbname, uid, admin_user_pw,
                'res.groups', 'search', [('name', '=', 'Access Rights')])[0],
            sock.execute(
                dbname, uid, admin_user_pw,
                'res.groups', 'search', [('name', '=', 'Settings')])[0],
            sock.execute(
                dbname, uid, admin_user_pw,
                'res.groups', 'search', [('name', '=', 'Employee')])[0],
            # sock.execute(
            #     dbname, uid, admin_user_pw,
            #     'res.groups', 'search', [('name', '=', 'Multi Companies')])[0],
            # sock.execute(
            #     dbname, uid, admin_user_pw,
            #     'res.groups', 'search', [('name', '=', 'Multi Currencies')])[0],
            sock.execute(
                dbname, uid, admin_user_pw,
                'res.groups', 'search', [('name', '=', 'Technical Features')])[0],
            sock.execute(
                dbname, uid, admin_user_pw,
                'res.groups', 'search', [('name', '=', 'Contact Creation')])[0],
        ])],
    }
    sock.execute(dbname, uid, admin_user_pw, 'res.users', 'write', user_id, values)

    print('Done.')


def Demo_User():

    print('Configuring user "Demo"...')

    sock_common = xmlrpclib.ServerProxy(sock_common_url)
    uid = sock_common.login(dbname, admin_user, admin_user_pw)
    sock = xmlrpclib.ServerProxy(sock_str)

    args = [('name', '=', CompanyName), ]
    parent_id = sock.execute(dbname, uid, admin_user_pw, 'res.partner', 'search', args)
    args = [('name', '=', CompanyName), ]
    company_id = sock.execute(dbname, uid, admin_user_pw, 'res.company', 'search', args)

    values = {
        'name': demo_user_name,
        'customer': False,
        'employee': False,
        'is_company': False,
        'email': demo_user_email,
        'website': '',
        'parent_id': parent_id[0],
        'company_id': company_id[0],
        'tz': tz,
        'lang': lang
    }
    partner_id = sock.execute(dbname, uid, admin_user_pw, 'res.partner', 'create', values)

    values = {
        'name': demo_user_name,
        'partner_id': partner_id,
        'company_id': company_id[0],
        'login': demo_user,
        'password': demo_user_pw,
        'image': Demo_User_image,
        'groups_id': [(6, 0, [])],
    }
    user_id = sock.execute(dbname, uid, admin_user_pw, 'res.users', 'create', values)

    values = {
        'groups_id': [(6, 0, [
            sock.execute(
                dbname, uid, admin_user_pw,
                'res.groups', 'search', [('name', '=', 'Employee')])[0],
        ])],
    }
    sock.execute(dbname, uid, admin_user_pw, 'res.users', 'write', user_id, values)

    print('Done.')


def Data_Administrator_User():

    print('Configuring user "Data Administrator"...')

    sock_common = xmlrpclib.ServerProxy(sock_common_url)
    uid = sock_common.login(dbname, admin_user, admin_user_pw)
    sock = xmlrpclib.ServerProxy(sock_str)

    args = [('name', '=', CompanyName), ]
    parent_id = sock.execute(dbname, uid, admin_user_pw, 'res.partner', 'search', args)
    args = [('name', '=', CompanyName), ]
    company_id = sock.execute(dbname, uid, admin_user_pw, 'res.company', 'search', args)

    values = {
        'name': data_admin_user_name,
        'customer': False,
        'employee': False,
        'is_company': False,
        'email': data_admin_user_email,
        'website': '',
        'parent_id': parent_id[0],
        'company_id': company_id[0],
        'tz': tz,
        'lang': lang
    }
    partner_id = sock.execute(dbname, uid, admin_user_pw, 'res.partner', 'create', values)

    values = {
        'name': data_admin_user_name,
        'partner_id': partner_id,
        'company_id': company_id[0],
        'login': data_admin_user,
        'password': data_admin_user_pw,
        'image': DataAdministrator_image,
        'groups_id': [(6, 0, [])],
    }
    user_id = sock.execute(dbname, uid, admin_user_pw, 'res.users', 'create', values)

    values = {
        'groups_id': [(6, 0, [
            sock.execute(
                dbname, uid, admin_user_pw,
                'res.groups', 'search', [('name', '=', 'Employee')])[0],
            sock.execute(
                dbname, uid, admin_user_pw,
                'res.groups', 'search', [('name', '=', 'Contact Creation')])[0],
        ])],
    }
    sock.execute(dbname, uid, admin_user_pw, 'res.users', 'write', user_id, values)

    print('Done.')


def install_update(name, update=False):

    print('Processing module "{0}"...'.format(name))

    connection = openerplib.get_connection(hostname=hostname,
                                           database=dbname,
                                           login=admin,
                                           password=admin_user_pw)
    module_model = connection.get_model('ir.module.module')
    module_ids = module_model.search([('name', '=', name)])
    module = module_model.read(module_ids, ['state'])
    module_state = module[0]['state']
    print('Module State: {0}.'.format(module_state))
    if not module_state == 'installed':
        print('Installing module "{0}"...'.format(name))
        module_model.button_immediate_install([module_ids[0]])
        print('Done.'.format(name))
        return True
    elif update:
        print('Upgrading module "{0}"...'.format(name))
        module_model.button_upgrade([module_ids[0]])
        upgrade_id = connection.get_model('base.module.upgrade').create({'module_info': module_ids[0]})
        connection.get_model('base.module.upgrade').upgrade_module(upgrade_id)
        print('Done.'.format(name))
        return False
    else:
        print('Skipping "{0}"...'.format(name))
        print('Done.'.format(name))
        return False


def user_groups_set(user_name, group_name_list):

    print('Executing user_groups_set...')

    sock_common = xmlrpclib.ServerProxy(sock_common_url)
    uid = sock_common.login(dbname, admin_user, admin_user_pw)
    sock = xmlrpclib.ServerProxy(sock_str)

    args = [('name', '=', user_name), ]
    user_id = sock.execute(dbname, uid, admin_user_pw, 'res.users', 'search', args)

    for group_name in group_name_list:
        values = {
            'groups_id': [(
                4, sock.execute(dbname, uid, admin_user_pw,
                                'res.groups', 'search', [('name', '=', group_name)]
                                )[0]
            )],
        }
        sock.execute(dbname, uid, admin_user_pw, 'res.users', 'write', user_id, values)

    print('Done.')


def install_update_module(module, update, group_name_list=[]):

    print('%s%s' % ('--> ', module))
    if module in modules_to_update:
        new_module = install_update(module, True)
    else:
        new_module = install_update(module, update)

    if new_module and group_name_list != []:

        user_name = 'Administrator'
        print('%s%s(%s)' % ('--> ', module, user_name))
        user_groups_set(user_name, group_name_list)

        user_name = 'Data Administrator'
        print('%s%s(%s)' % ('--> ', module, user_name))
        user_groups_set(user_name, group_name_list)

    return new_module


def install():

    global update

    print('--> create_database()')
    newDB = create_database()
    if newDB:
        print('--> newDB: ', newDB)
        print('--> MyCompany()')
        MyCompany()
        print('--> Administrator()')
        Administrator()
        print('--> Demo_User()')
        Demo_User()
        print('--> Data_Administrator_User()')
        Data_Administrator_User()
    else:
        print('--> newDB: ', newDB)
        client = erppeek.Client(server,
                                db=dbname,
                                user=admin_user,
                                password=admin_user_pw,
                                verbose=False)
        print('--> client: ', client)
        proxy = client.model('ir.module.module')
        proxy.update_list()

    # ################################################################################################################
    #
    # Odoo Addons
    #
    # ################################################################################################################

    group_names = []
    install_update_module('mail', update, group_names)

    group_names = []
    install_update_module('sales_team', update, group_names)

    # ################################################################################################################
    #
    # OCA/l10n-brazil
    #
    # ################################################################################################################

    group_names = []
    install_update_module('l10n_br_base', update, group_names)

    group_names = []
    install_update_module('l10n_br_zip', update, group_names)

    group_names = []
    install_update_module('l10n_br_zip_correios', update, group_names)

    # ################################################################################################################
    #
    # OCA/server-tools
    #
    # ################################################################################################################

    # ################################################################################################################
    #
    # CLVsol Odoo Addons
    #
    # ################################################################################################################

    group_names = []
    install_update_module('clv_disable_web_access', update, group_names)

    group_names = [
        'User (Base)',
        'Super User (Base)',
        'Annotation User (Base)',
        'Register User (Base)',
        'Log User (Base)',
        'Manager (Base)',
        'Super Manager (Base)',
    ]
    install_update_module('clv_base', update, group_names)

    group_names = [
        'User (File System)',
        'Manager (File System)',
        'Super Manager (File System)',
    ]
    install_update_module('clv_file_system', update, group_names)

    group_names = [
        'User (Global Tag)',
        'Manager (Global Tag)',
        'Super Manager (Global Tag)',
    ]
    install_update_module('clv_global_tag', update, group_names)

    group_names = [
        'User (Insured)',
        'Manager (Insured)',
        'Super Manager (Insured)',
    ]
    install_update_module('clv_insured', update, group_names)

    # ################################################################################################################
    #
    # CLVsol Odoo Addons - Brazilian Localization
    #
    # ################################################################################################################

    # ################################################################################################################
    #
    # CLVsol Odoo Addons - PBM customizations
    #
    # ################################################################################################################


def secondsToStr(t):

    return "%d:%02d:%02d.%03d" % \
        reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


if __name__ == '__main__':

    from time import time

    get_arguments()

    start = time()

    print('--> Executing install.py...\n')

    print('--> Executing install()...\n')
    install()

    print('\n--> install.py')
    print('--> Execution time:', secondsToStr(time() - start), '\n')
