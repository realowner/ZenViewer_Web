"""new tables > default

Revision ID: 4ced4a69e358
Revises: 0f52ae52f4fe
Create Date: 2021-07-14 15:28:48.494227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ced4a69e358'
down_revision = '0f52ae52f4fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('settings', schema=None) as batch_op:
        batch_op.drop_column('sec_alg')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('settings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sec_alg', sa.BOOLEAN(), nullable=False))

    # ### end Alembic commands ###