#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""add-discovery-url-to-bay

Revision ID: 4ea34a59a64c
Revises: 456126c6c9e9
Create Date: 2015-04-14 18:56:03.440329

"""

# revision identifiers, used by Alembic.
revision = '4ea34a59a64c'
down_revision = '456126c6c9e9'

from alembic import op  # noqa: E402

from oslo_db.sqlalchemy.types import String  # noqa: E402

import sqlalchemy as sa  # noqa: E402

from sqlalchemy.dialects.mysql import TINYTEXT  # noqa: E402


def upgrade():
    op.add_column('bay',
                  sa.Column('discovery_url',
                            String(255, mysql_ndb_type=TINYTEXT),
                            nullable=True))
