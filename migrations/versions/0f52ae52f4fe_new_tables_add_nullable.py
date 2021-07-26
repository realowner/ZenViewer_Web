"""new tables > add nullable

Revision ID: 0f52ae52f4fe
Revises: d2ee4bb95abe
Create Date: 2021-07-14 15:22:03.159021

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f52ae52f4fe'
down_revision = 'd2ee4bb95abe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('current_viewer', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=10),
               nullable=False)

    with op.batch_alter_table('settings', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=10),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('settings', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=10),
               nullable=True)

    with op.batch_alter_table('current_viewer', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=10),
               nullable=True)

    # ### end Alembic commands ###