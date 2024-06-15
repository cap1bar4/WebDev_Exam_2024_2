"""empty message

Revision ID: 1bf7841ca3a2
Revises: 01d61a74b4cf
Create Date: 2024-06-15 13:36:12.823937

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1bf7841ca3a2'
down_revision = '01d61a74b4cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('rating', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('date_added', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False))
        batch_op.drop_constraint('fk_comments_parent_id_comments', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_comments_user_id_users'), 'users', ['user_id'], ['id'])
        batch_op.drop_column('parent_id')
        batch_op.drop_column('author')

    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=mysql.TEXT(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=mysql.TEXT(),
               nullable=False)

    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author', mysql.VARCHAR(length=100), nullable=False))
        batch_op.add_column(sa.Column('parent_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
        batch_op.drop_constraint(batch_op.f('fk_comments_user_id_users'), type_='foreignkey')
        batch_op.create_foreign_key('fk_comments_parent_id_comments', 'comments', ['parent_id'], ['id'])
        batch_op.drop_column('date_added')
        batch_op.drop_column('rating')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
