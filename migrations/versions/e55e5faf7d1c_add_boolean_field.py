"""add boolean field

Revision ID: e55e5faf7d1c
Revises: 52338873675f
Create Date: 2021-07-15 11:54:32.934990

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e55e5faf7d1c'
down_revision = '52338873675f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_settings')
    with op.batch_alter_table('settings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sec_alg', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('settings', schema=None) as batch_op:
        batch_op.drop_column('sec_alg')

    op.create_table('_alembic_tmp_settings',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('thr_num', sa.INTEGER(), nullable=False),
    sa.Column('sec_alg', sa.BOOLEAN(), nullable=False),
    sa.CheckConstraint('sec_alg IN (0, 1)'),
    sa.CheckConstraint('sec_alg IN (0, 1)'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###