# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from restclients_core.util.decorators import use_mock
from uw_upass.dao import UPass_DAO

fdao_upass_override = use_mock(UPass_DAO())
