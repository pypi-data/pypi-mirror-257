"""Add project owners and quotas

Revision ID: d0bb68e48b9f
Revises: fe72c4de8376
Create Date: 2023-11-01 10:19:30.459707

"""
import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op

# revision identifiers, used by Alembic.
revision = "d0bb68e48b9f"
down_revision = "fe72c4de8376"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("backends", schema=None) as batch_op:
        batch_op.alter_column(
            "type",
            existing_type=sa.VARCHAR(length=6),
            type_=sa.Enum(
                "AWS",
                "AZURE",
                "DSTACK",
                "GCP",
                "LAMBDA",
                "LOCAL",
                "TENSORDOCK",
                name="backendtype",
            ),
            existing_nullable=False,
        )

    with op.batch_alter_table("projects", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "owner_id", sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=True
            )
        )
        batch_op.create_foreign_key(
            batch_op.f("fk_projects_owner_id_users"),
            "users",
            ["owner_id"],
            ["id"],
            ondelete="SET NULL",
        )

    with op.batch_alter_table("repos", schema=None) as batch_op:
        batch_op.alter_column(
            "type",
            existing_type=sa.VARCHAR(length=6),
            type_=sa.Enum("REMOTE", "LOCAL", "VIRTUAL", name="repotype"),
            existing_nullable=False,
        )

    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(sa.Column("projects_quota", sa.Integer(), nullable=True))

    # ### end Alembic commands ###

    op.execute(
        "UPDATE projects SET owner_id = (SELECT id FROM users WHERE name == 'admin') WHERE owner_id IS NULL"
    )
    op.execute("UPDATE users SET projects_quota = 3 WHERE projects_quota IS NULL")


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_column("projects_quota")

    with op.batch_alter_table("repos", schema=None) as batch_op:
        batch_op.alter_column(
            "type",
            existing_type=sa.Enum("REMOTE", "LOCAL", "VIRTUAL", name="repotype"),
            type_=sa.VARCHAR(length=6),
            existing_nullable=False,
        )

    with op.batch_alter_table("projects", schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f("fk_projects_owner_id_users"), type_="foreignkey")
        batch_op.drop_column("owner_id")

    with op.batch_alter_table("backends", schema=None) as batch_op:
        batch_op.alter_column(
            "type",
            existing_type=sa.Enum(
                "AWS",
                "AZURE",
                "DSTACK",
                "GCP",
                "LAMBDA",
                "LOCAL",
                "TENSORDOCK",
                name="backendtype",
            ),
            type_=sa.VARCHAR(length=6),
            existing_nullable=False,
        )

    # ### end Alembic commands ###
