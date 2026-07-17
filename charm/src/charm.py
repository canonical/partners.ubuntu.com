#!/usr/bin/env python3
# Copyright 2026 Ubuntu
# See LICENSE file for licensing details.

"""Django Charm entrypoint."""

import logging
import typing

import ops

import paas_charm.django

logger = logging.getLogger(__name__)


class CharmCharm(paas_charm.django.Charm):
    """Django Charm service."""

    def __init__(self, *args: typing.Any) -> None:
        """Initialize the instance.

        Args:
            args: passthrough to CharmBase.
        """
        super().__init__(*args)


if __name__ == "__main__":
    ops.main(CharmCharm)
