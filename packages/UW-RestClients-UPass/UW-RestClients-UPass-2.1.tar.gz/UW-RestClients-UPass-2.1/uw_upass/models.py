# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from restclients_core import models


class UPassStatus(models.Model):
    active_employee_membership = models.BooleanField(
        null=True, default=None)
    active_student_membership = models.BooleanField(
        null=True, default=None)

    def json_data(self):
        return {
            'active_employee_membership': self.active_employee_membership,
            'active_student_membership': self.active_student_membership,
        }

    @classmethod
    def create(cls, data):
        status = cls()
        if "activeEmployeeMembership" in data:
            status.active_employee_membership = data.get(
                'activeEmployeeMembership', False)
        if "activeStudentMembership" in data:
            status.active_student_membership = data.get(
                'activeStudentMembership', False)
        return status

    def __str__(self):
        return json.dumps(self.json_data())
