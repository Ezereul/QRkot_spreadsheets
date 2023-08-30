"""Add CheckConstraint

Revision ID: df6c3d1e790f
Revises: 9b3152098247
Create Date: 2023-08-20 16:20:26.794214

"""
from alembic import op
import sqlalchemy as sa
from alembic.op import batch_alter_table

# revision identifiers, used by Alembic.
revision = 'df6c3d1e790f'
down_revision = '9b3152098247'
branch_labels = None
depends_on = None


def upgrade():
    with batch_alter_table("donation") as batch_op:
        batch_op.create_check_constraint(
            constraint_name='full_amount_positive',
            condition='full_amount > 0'
        )
        batch_op.create_check_constraint(
            constraint_name='invested_amount_positive',
            condition='invested_amount >= 0'
        )
        batch_op.create_check_constraint(
            constraint_name='invested_amount_lte_full_amount',
            condition='invested_amount <= full_amount'
        )
    with batch_alter_table("charityproject") as batch_op:
        batch_op.create_check_constraint(
            constraint_name='full_amount_positive',
            condition='full_amount > 0'
        )
        batch_op.create_check_constraint(
            constraint_name='invested_amount_positive',
            condition='invested_amount >= 0'
        )
        batch_op.create_check_constraint(
            constraint_name='invested_amount_lte_full_amount',
            condition='invested_amount <= full_amount'
        )


def downgrade():
    with batch_alter_table("donation") as batch_op:
        batch_op.drop_constraint(constraint_name='full_amount_positive')
        batch_op.drop_constraint(constraint_name='invested_amount_positive')
        batch_op.drop_constraint(constraint_name='invested_amount_lte_full_amount')
    with batch_alter_table("charityproject") as batch_op:
        batch_op.drop_constraint(constraint_name='full_amount_positive')
        batch_op.drop_constraint(constraint_name='invested_amount_positive')
        batch_op.drop_constraint(constraint_name='invested_amount_lte_full_amount')
