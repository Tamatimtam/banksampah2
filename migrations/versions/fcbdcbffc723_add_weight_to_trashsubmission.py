"""Add weight to TrashSubmission

Revision ID: fcbdcbffc723
Revises: a8651a4850a3
Create Date: 2024-08-10 08:11:11.553580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fcbdcbffc723'
down_revision = 'a8651a4850a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trash_submission', schema=None) as batch_op:
        batch_op.add_column(sa.Column('weight', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trash_submission', schema=None) as batch_op:
        batch_op.drop_column('weight')

    # ### end Alembic commands ###
