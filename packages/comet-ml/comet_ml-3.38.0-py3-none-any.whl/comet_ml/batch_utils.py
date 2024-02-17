# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2021 Comet ML INC
#  This file can not be copied and/or distributed
#  without the express permission of Comet ML Inc.
# *******************************************************

import logging
from threading import RLock

from ._typing import Callable, Dict, List
from .messages import BaseMessage, ParameterMessage
from .utils import get_time_monotonic

LOGGER = logging.getLogger(__name__)


class MessageBatchItem(object):
    """Represents batch item holding specific message and offset associated with it."""

    __slots__ = "message"

    def __init__(self, message: BaseMessage) -> None:
        self.message = message


class ParametersBatch(object):
    """The batch object to maintain schedule of parameters sending."""

    def __init__(self, base_interval: float) -> None:
        """Creates new instance of parameters batch. The base_interval value will be used as initial interval
        between accept events and will be incremented with values generated by backoff_gen each time new message
        was accepted.

        Args:
            base_interval:
                The base interval between sending collected parameters
        """
        self.base_interval = base_interval
        self.last_time = 0.0
        self.items = {}  # type: Dict[str, MessageBatchItem]
        # the lock to make sure that ready_to_accept and accept public methods are synchronized
        # and implementation is thread safe
        self.lock = RLock()

    def empty(self) -> bool:
        """Allows to check if this batch is empty"""
        with self.lock:
            return len(self.items) == 0

    def append(self, message: ParameterMessage) -> bool:
        """Appends specified message to the collection of messages maintained by this batch.

        Args:
            message:
                The message to be accepted or ignored

        Returns:
            True if specified message was accepted by this batch.
        """
        if not isinstance(message, ParameterMessage):
            return False

        name = message.get_param_name()
        if name is None or name == "":
            # empty message
            return False

        # include context if present
        if message.context is not None:
            name = "%s_%s" % (message.context, name)

        # include source if present
        if message.get_source() is not None:
            name = "%s_%s" % (message.get_source(), name)

        self.items[name] = MessageBatchItem(message)
        return True

    def accept(
        self,
        callback: Callable[[List[MessageBatchItem]], None],
        unconditional: bool = False,
    ) -> bool:
        """Accepts or ignores provided callback depending on last time this method was invoked and current interval
        between accept events. If time elapsed since last accept exceeds base_interval the provided callback will
        be used to send all collected parameters and batch state will be cleaned.

        Args:
            callback:
                The callback function to be invoked with message, offset as argument if it was accepted.
            unconditional:
                The flag to indicate if  callback should be accepted unconditionally if there are items to be processed.
        Returns:
            True if callback was accepted and all parameters was sent.
        Raises:
            ValueError: is callback is None
        """
        if callback is None:
            raise ValueError("Callback is None")

        with self.lock:
            if self.ready_to_accept(unconditional):
                self._accept(callback)
                return True
            else:
                return False

    def ready_to_accept(self, unconditional: bool = False) -> bool:
        """Method to check if this batch is ready to accept the next callback

        Args:
            unconditional:
                The flag to indicate if  callback should be accepted unconditionally if there are items to be processed.
        Returns:
            True if next callback will be accepted.
        """
        with self.lock:
            if self.empty():
                return False

            if self.last_time == 0 or unconditional:
                return True

            duration_since_last_time = get_time_monotonic() - self.last_time
            return duration_since_last_time >= self.base_interval

    def update_interval(self, interval: float) -> None:
        """The callback method invoked to update the interval between batch processing

        Args:
            interval:
                The new interval value in seconds.
        """
        with self.lock:
            self.base_interval = interval

    def _accept(self, callback: Callable[[List[MessageBatchItem]], None]) -> None:
        """Accepts the specified callback for all parameters collected so forth"""
        with self.lock:
            keys = list(self.items.keys())
            list_to_sent = list()
            for key in keys:
                list_to_sent.append(self.items[key])
                self.items.pop(key)

        # send batch
        try:
            callback(list_to_sent)
        except Exception:
            LOGGER.debug("Failed to send parameters batch", exc_info=True)

        self.last_time = get_time_monotonic()


class MessageBatch(object):
    """The batch object to maintain list of messages to be sent constrained by size and interval between send events."""

    def __init__(self, base_interval: float, max_size: int) -> None:
        """Creates new instance of batch. The base_interval value will be used as initial interval
        between accept events and will be incremented with values generated by backoff_gen each time new message
        was accepted. Also, it would check the current number of collected messages against max_size when new message
        accepted by the batch. When number of collected values exceeds max_size the collected  messages will be sent
        immediately.


        Args:
            base_interval:
                The base interval between sending collected message.
            max_size:
                The maximal size of collected message to be kept.
        """
        self.base_interval = base_interval
        self.max_size = max_size
        self.last_time = 0.0
        self.items = list()  # type: List[MessageBatchItem]
        # the lock to make sure that ready_to_accept and accept public methods are synchronized
        # and implementation is thread safe
        self.lock = RLock()

    def empty(self):
        # type: () -> bool
        """Allows to check if this batch is empty"""
        with self.lock:
            return len(self.items) == 0

    def update_interval(self, interval: float) -> None:
        """The callback method invoked to update the interval between batch processing

        Args:
            interval:
                The new interval value in seconds.
        """
        with self.lock:
            self.base_interval = interval

    def append(self, message: BaseMessage) -> None:
        """Appends specified message to the collection of messages maintained by this batch.

        Args:
            message:
                The message to be accepted or ignored
        """
        assert isinstance(message, BaseMessage)

        self.items.append(MessageBatchItem(message=message))

    def accept(
        self,
        callback: Callable[[List[MessageBatchItem]], None],
        unconditional: bool = False,
    ) -> bool:
        """Accepts or ignores provided callback depending on last time this method was invoked and current interval
        between accept events. If time elapsed since last accept exceeds base_interval the provided callback will
        be used to send all collected messages and batch state will be cleaned. Also, if number of collected
        messages equals or greater than max_size the callback will be accepted.

        Args:
            callback:
                The callback function to be invoked with list of batch items as argument if it is accepted.
            unconditional:
                The flag to indicate if callback should be accepted unconditionally if there are items to be processed.
        Returns:
            True if callback was accepted and all collected messages was successfully sent.
        Raises:
            ValueError: is callback is None
        """
        if callback is None:
            raise ValueError("Callback is None")

        with self.lock:
            if self._ready_to_accept(unconditional):
                return self._accept(callback)
            else:
                return False

    def _ready_to_accept(self, unconditional: bool = False) -> bool:
        """Method to check if this batch is ready to accept the next callback.

        Args:
            unconditional:
                The flag to indicate if  callback should be accepted unconditionally if there are items to be processed.
        Returns:
            True if next callback will be accepted.
        """
        with self.lock:
            if self.empty():
                return False

            if self.last_time == 0 or unconditional:
                return True

            duration_since_last_time = get_time_monotonic() - self.last_time
            if duration_since_last_time >= self.base_interval:
                return True

            return len(self.items) >= self.max_size

    def _accept(self, callback: Callable[[List[MessageBatchItem]], None]) -> bool:
        """Accepts the specified callback for all items collected so forth"""
        with self.lock:
            # copy items to new list to avoid list changes while sending due to appending new items
            list_to_sent = self.items
            self.items = list()

        successful = False
        try:
            callback(list_to_sent)
            successful = True
        except Exception:
            LOGGER.debug("Failed to send messages batch", exc_info=True)

        self.last_time = get_time_monotonic()
        return successful
