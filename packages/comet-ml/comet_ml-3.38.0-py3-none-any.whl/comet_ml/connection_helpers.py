# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2024 Comet ML INC
#  This file can not be copied and/or distributed
#  without the express permission of Comet ML Inc.
# *******************************************************
import platform
import threading
import warnings
from typing import List, Optional

from comet_ml.config import get_config
from comet_ml.utils import get_comet_version

import urllib3
from requests import Session
from requests.adapters import HTTPAdapter
from requests_toolbelt.adapters.socket_options import TCPKeepAliveAdapter
from urllib3 import Retry

STATUS_FORCELIST_NO_AUTH_ERRORS = [500, 502, 503, 504]
STATUS_FORCELIST_FULL = [401, 403]
STATUS_FORCELIST_FULL.extend(STATUS_FORCELIST_NO_AUTH_ERRORS)


def get_http_session(
    retry_strategy: Optional[Retry] = None,
    verify_tls: bool = True,
    tcp_keep_alive: bool = False,
) -> Session:
    session = Session()

    # Add default debug headers
    session.headers.update(
        {
            "X-COMET-DEBUG-SDK-VERSION": get_comet_version(),
            "X-COMET-DEBUG-PY-VERSION": platform.python_version(),
        }
    )

    # Setup retry strategy if asked
    http_adapter = None
    https_adapter = None
    if tcp_keep_alive is True:
        http_adapter = TCPKeepAliveAdapter(
            idle=60, count=5, interval=60, max_retries=retry_strategy
        )
        https_adapter = TCPKeepAliveAdapter(
            idle=60, count=5, interval=60, max_retries=retry_strategy
        )
    elif tcp_keep_alive is False and retry_strategy is not None:
        http_adapter = HTTPAdapter(max_retries=retry_strategy)
        https_adapter = HTTPAdapter(max_retries=retry_strategy)

    if http_adapter is not None:
        session.mount("http://", http_adapter)

    if https_adapter is not None:
        session.mount("https://", https_adapter)

    # Setup HTTP allow header if configured
    config = get_config()  # This can be slow if called for every new session
    allow_header_name = config["comet.allow_header.name"]
    allow_header_value = config["comet.allow_header.value"]

    if allow_header_name and allow_header_value:
        session.headers[allow_header_name] = allow_header_value

    if verify_tls is False:
        # Only the set the verify if it's disabled. The current default for the verify attribute is
        # True but this way we will survive any change of the default value
        session.verify = False
        # Also filter the warning that urllib3 emits to not overflow the output with them
        warnings.filterwarnings(
            "ignore", category=urllib3.exceptions.InsecureRequestWarning
        )

    return session


def get_retry_strategy(
    status_forcelist: Optional[List[int]] = None,
    total_retries: Optional[int] = None,
    backoff_factor: Optional[int] = None,
) -> Retry:

    # The total backoff sleeping time is computed like that:
    # backoff = 2
    # retries = 3
    # s = lambda b, i: b * (2 ** (i - 1))
    # sleep = sum(s(backoff, i) for i in range(1, retries + 1))
    # Will wait up to 14s

    if status_forcelist is None:
        status_forcelist = STATUS_FORCELIST_NO_AUTH_ERRORS

    settings = get_config()
    if total_retries is None:
        total_retries = settings.get_int(None, "comet.http_session.retry_total")
    if backoff_factor is None:
        backoff_factor = settings.get_int(
            None, "comet.http_session.retry_backoff_factor"
        )

    if urllib3.__version__.startswith("2."):
        kwargs = {"allowed_methods": None}
    else:
        kwargs = {"method_whitelist": False}

    return Retry(
        total=total_retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        **kwargs
    )


THREAD_SESSIONS = threading.local()


def get_thread_session(retry: bool, verify_tls: bool, tcp_keep_alive: bool) -> Session:
    # As long as the session is not part of a reference loop, the thread local dict will be cleaned
    # up when each thread ends, garbage-collecting the Session object and closing the
    # resources
    session_key = (retry, tcp_keep_alive, verify_tls)

    cached_session = THREAD_SESSIONS.__dict__.get(
        session_key, None
    )  # type: Optional[Session]

    if cached_session:
        return cached_session

    retry_strategy = False
    if retry is True:
        retry_strategy = get_retry_strategy()

    new_session = get_http_session(
        retry_strategy=retry_strategy,
        tcp_keep_alive=tcp_keep_alive,
        verify_tls=verify_tls,
    )
    THREAD_SESSIONS.__dict__[session_key] = new_session

    return new_session
