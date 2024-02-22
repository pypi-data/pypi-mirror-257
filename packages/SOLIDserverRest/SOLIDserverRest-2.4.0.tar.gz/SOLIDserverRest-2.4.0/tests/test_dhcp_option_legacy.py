#
#
# Time-stamp: <2022-05-09 13:26:07 alex>
#

"""test file for DHCP options using simple lib

* test_device_new_object

"""

import logging
import sys
import uuid
import datetime

from SOLIDserverRest.Exception import SDSInitError, SDSRequestError
from SOLIDserverRest.Exception import SDSAuthError, SDSError
from SOLIDserverRest.Exception import SDSEmptyError, SDSSpaceError

from .context import sdsadv
from .context import _connect_to_sds
from .adv_basic import *

DHCP_ID = 3
DHCP_SCOPE_ID = 8
DHCP_RANGE_ID = 13
DHCP_STATIC_ID = 35

# -------------------------------------------------------


def test_list_dhcp_server():
    """
    """

    sds = _connect_to_sds()

    r = sds.query("dhcp_server_list",
                  params={
                      #   'hostdev_name': device_name
                  })

    for _server in r:
        logging.info(
            f"id={_server['dhcp_id']}"
            f" {_server['dhcp_name']}"
            f" {_server['hostaddr']}"
            f" {_server['dhcp_type']}"
            f" {_server['vdhcp_arch']}"
        )

# -------------------------------------------------------


def test_list_dhcp_scope():
    """
    """

    sds = _connect_to_sds()

    r = sds.query("dhcp_scope_list",
                  params={
                      'WHERE': f'dhcp_id={DHCP_ID}'
                  })

    for _server in r:
        logging.info(
            f"id={_server['dhcpscope_id']}"
            f" {_server['dhcpscope_name']}"
            f" {_server['dhcpsn_name']}"
        )


def test_list_dhcp_range():
    """
    """

    sds = _connect_to_sds()

    r = sds.query("dhcp_range_list",
                  params={
                      'WHERE': f'dhcpscope_id={DHCP_SCOPE_ID}'
                  })

    for _range in r:
        logging.info(
            f"id={_range['dhcprange_id']}"
            f" {_range['dhcprange_name']}"
            f" {_range['dhcprange_start_addr']}"
            f"-{_range['dhcprange_end_addr']}"
        )


def test_list_dhcp_static():
    """
    """

    sds = _connect_to_sds()

    r = sds.query("dhcp_static_list",
                  params={
                      'WHERE': f'dhcpscope_id={DHCP_SCOPE_ID}'
                  })

    for _static in r:
        logging.info(
            f"id={_static['dhcphost_id']}"
            f" {_static['dhcphost_name']}"
            f" {_static['dhcphost_addr']}"
            f"-{_static['dhcphost_mac_addr']}"
        )

# -------------------------------------------------------


def test_list_options_server():
    """
    """

    sds = _connect_to_sds()

    r = sds.query("dhcp_options_server_list",
                  params={
                      'dhcp_id': DHCP_ID
                  })

    for _server in r:
        logging.info(
            f"id={_server['dhcpoption_id']}"
            f" {_server['dhcpoption_name']} = "
            f" {_server['dhcpoption_value']}"
        )


def test_list_options_scope():
    """
    """

    sds = _connect_to_sds()

    r = sds.query("dhcp_options_scope_list",
                  params={
                      'dhcpscope_id': DHCP_SCOPE_ID
                  })

    for _scope in r:
        logging.info(
            f"id={_scope['dhcpscopeoption_id']}"
            f" {_scope['dhcpoption_name']} = "
            f" {_scope['dhcpoption_value']}"
        )


def test_list_options_range():
    """
    """

    sds = _connect_to_sds()

    r = sds.query("dhcp_options_range_list",
                  params={
                      'dhcprange_id': DHCP_RANGE_ID
                  })

    for _option in r:
        logging.info(
            f"id={_option['dhcprangeoption_id']}"
            f" {_option['dhcpoption_name']} = "
            f" {_option['dhcpoption_value']}"
        )


def test_list_options_static():
    """
    """

    sds = _connect_to_sds()

    r = sds.query("dhcp_options_static_list",
                  params={
                      'dhcpstatic_id': DHCP_STATIC_ID
                  })

    for _option in r:
        logging.info(
            f"id={_option['dhcphostoption_id']}"
            f" {_option['dhcpoption_name']} = "
            f" {_option['dhcpoption_value']}"
        )

# -------------------------------------------------------


def test_create_options_static():
    """
    """

    sds = _connect_to_sds()

    # add
    r = sds.query("dhcp_option_create",
                  params={
                      'dhcphost_id': DHCP_STATIC_ID,
                      'dhcpoption_type': 'host',
                      'dhcpoption_name': 'option routers',
                      'dhcpoption_value': '10.1.2.3',
                      'add_flag': 'add_only'
                  })

    # update
    r = sds.query("dhcp_option_update",
                  params={
                      'dhcphost_id': DHCP_STATIC_ID,
                      'dhcpoption_type': 'host',
                      'dhcpoption_name': 'option routers',
                      'dhcpoption_value': '10.1.2.5',
                      'add_flag': 'edit_only'
                  })

    # delete
    r = sds.query("dhcp_option_update",
                  params={
                      'dhcphost_id': DHCP_STATIC_ID,
                      'dhcpoption_type': 'host',
                      'dhcpoption_name': 'option routers',
                      'dhcpoption_value': '',
                      'add_flag': 'edit_only'
                  })

    logging.info(r)
