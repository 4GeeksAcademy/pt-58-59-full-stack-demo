"""empty message

Revision ID: 472b0c80f831
Revises: 5fac0921ceb4
Create Date: 2024-01-26 23:36:27.867638

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '472b0c80f831'
down_revision = '5fac0921ceb4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todo_user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=120), nullable=False))
        batch_op.drop_constraint('todo_user_email_key', type_='unique')
        batch_op.create_unique_constraint(None, ['username'])
        batch_op.drop_column('email')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todo_user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_unique_constraint('todo_user_email_key', ['email'])
        batch_op.drop_column('username')

    # ### end Alembic commands ###
