# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from uw_upass import get_upass_status
from restclients_core.exceptions import DataFailureException
from uw_upass.util import fdao_upass_override


@fdao_upass_override
class UPassTest(TestCase):
    def test_get_upass_status(self):
        status = get_upass_status("javerage")
        self.assertTrue(status.active_employee_membership)
        self.assertTrue(status.active_student_membership)
        self.assertEqual(
            status.json_data(),
            {'active_employee_membership': True,
             'active_student_membership': True}
        )
        self.assertIsNotNone(str(status))

        status = get_upass_status("faculty")
        self.assertTrue(status.active_employee_membership)
        self.assertIsNone(status.active_student_membership)

        status = get_upass_status("staff")
        self.assertTrue(status.active_employee_membership)
        self.assertFalse(status.active_student_membership)

        status = get_upass_status("none")
        self.assertEqual(
            status.json_data(),
            {
                'active_employee_membership': None,
                'active_student_membership': None
            }
        )

        self.assertRaises(DataFailureException,
                          get_upass_status,
                          "notexist")

        self.assertRaises(Exception,
                          get_upass_status,
                          "jerror")
