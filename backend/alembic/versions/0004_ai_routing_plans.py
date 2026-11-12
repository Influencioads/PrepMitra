"""AI routing and blueprint pricing: plan entitlements, per-feature allowance ledger, AI call cost columns.

Revision ID: 0004
Revises: 0003
Create Date: 2026-11-12

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '0004'
down_revision: Union[str, Sequence[str], None] = '0003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

JSONB = postgresql.JSONB(astext_type=sa.Text())
TS = sa.DateTime(timezone=True)


def upgrade() -> None:
    op.add_column('plans', sa.Column('entitlements', JSONB, server_default=sa.text("'{}'::jsonb"), nullable=False))

    op.add_column('ai_usage', sa.Column('feature', sa.String(length=40), nullable=True))
    op.add_column('ai_usage', sa.Column('cached_tokens', sa.Integer(), server_default='0', nullable=False))
    op.add_column('ai_usage', sa.Column('cost_usd', sa.Float(), nullable=True))
    op.create_index(op.f('ix_ai_usage_feature'), 'ai_usage', ['feature'], unique=False)

    op.create_table('feature_uses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('feature', sa.String(length=40), nullable=False),
    sa.Column('source', sa.String(length=64), nullable=False),
    sa.Column('ref_id', sa.String(length=64), nullable=True),
    sa.Column('created_at', TS, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_feature_uses_user_id'), 'feature_uses', ['user_id'], unique=False)
    op.create_index(op.f('ix_feature_uses_feature'), 'feature_uses', ['feature'], unique=False)
    op.create_index(op.f('ix_feature_uses_created_at'), 'feature_uses', ['created_at'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_feature_uses_created_at'), table_name='feature_uses')
    op.drop_index(op.f('ix_feature_uses_feature'), table_name='feature_uses')
    op.drop_index(op.f('ix_feature_uses_user_id'), table_name='feature_uses')
    op.drop_table('feature_uses')
    op.drop_index(op.f('ix_ai_usage_feature'), table_name='ai_usage')
    op.drop_column('ai_usage', 'cost_usd')
    op.drop_column('ai_usage', 'cached_tokens')
    op.drop_column('ai_usage', 'feature')
    op.drop_column('plans', 'entitlements')
