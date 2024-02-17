"""gateway compute flag deleted

Revision ID: d3e8af4786fa
Revises: 48ad3ecbaea2
Create Date: 2024-01-09 12:23:40.768208

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d3e8af4786fa"
down_revision = "48ad3ecbaea2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("gateway_computes", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("deleted", sa.Boolean(), server_default=sa.text("0"), nullable=False)
        )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("gateway_computes", schema=None) as batch_op:
        batch_op.drop_column("deleted")

    # ### end Alembic commands ###
