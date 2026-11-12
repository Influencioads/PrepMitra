"""Student AI features: solution store, cached AI content, tutor/coach chat history, versioned personas.

Revision ID: 0005
Revises: 0004
Create Date: 2026-11-12

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '0005'
down_revision: Union[str, Sequence[str], None] = '0004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

JSONB = postgresql.JSONB(astext_type=sa.Text())
TS = sa.DateTime(timezone=True)


def upgrade() -> None:
    op.create_table('solutions',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('fingerprint', sa.String(length=64), nullable=False),
    sa.Column('normalized_text', sa.Text(), nullable=False),
    sa.Column('number_signature', sa.String(length=300), nullable=False),
    sa.Column('options', JSONB, nullable=False),
    sa.Column('embedding', JSONB, nullable=False),
    sa.Column('subject', sa.String(length=20), nullable=False),
    sa.Column('topic', sa.String(length=160), nullable=True),
    sa.Column('difficulty', sa.String(length=10), nullable=False),
    sa.Column('answer', sa.Text(), nullable=False),
    sa.Column('payload', JSONB, nullable=False),
    sa.Column('translations', JSONB, nullable=False),
    sa.Column('numeric_check', sa.String(length=300), nullable=False),
    sa.Column('solver_model', sa.String(length=80), nullable=False),
    sa.Column('prompt_version', sa.String(length=20), nullable=False),
    sa.Column('verification', sa.String(length=20), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('parent_id', sa.Uuid(), nullable=True),
    sa.Column('times_served', sa.Integer(), nullable=False),
    sa.Column('thumbs_up', sa.Integer(), nullable=False),
    sa.Column('thumbs_down', sa.Integer(), nullable=False),
    sa.Column('error_flags', sa.Integer(), nullable=False),
    sa.Column('created_at', TS, server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', TS, server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['solutions.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('fingerprint')
    )
    op.create_index(op.f('ix_solutions_status'), 'solutions', ['status'], unique=False)

    op.create_table('ai_artifacts',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=True),
    sa.Column('kind', sa.String(length=30), nullable=False),
    sa.Column('cache_key', sa.String(length=300), nullable=False),
    sa.Column('language', sa.String(length=10), nullable=False),
    sa.Column('title', sa.String(length=300), nullable=False),
    sa.Column('payload', JSONB, nullable=False),
    sa.Column('model', sa.String(length=80), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('times_served', sa.Integer(), nullable=False),
    sa.Column('score', sa.Float(), nullable=True),
    sa.Column('created_at', TS, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_ai_artifacts_lookup', 'ai_artifacts', ['kind', 'cache_key', 'language'], unique=False)
    op.create_index(op.f('ix_ai_artifacts_user_id'), 'ai_artifacts', ['user_id'], unique=False)
    op.create_index(op.f('ix_ai_artifacts_created_at'), 'ai_artifacts', ['created_at'], unique=False)

    op.create_table('ai_chat_messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('thread', sa.String(length=20), nullable=False),
    sa.Column('session_id', sa.String(length=64), nullable=True),
    sa.Column('role', sa.String(length=10), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('meta', JSONB, nullable=False),
    sa.Column('created_at', TS, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ai_chat_messages_user_id'), 'ai_chat_messages', ['user_id'], unique=False)
    op.create_index(op.f('ix_ai_chat_messages_session_id'), 'ai_chat_messages', ['session_id'], unique=False)
    op.create_index(op.f('ix_ai_chat_messages_created_at'), 'ai_chat_messages', ['created_at'], unique=False)

    op.create_table('personas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('kind', sa.String(length=10), nullable=False),
    sa.Column('version', sa.Integer(), nullable=False),
    sa.Column('data', JSONB, nullable=False),
    sa.Column('source_ref', sa.String(length=64), nullable=True),
    sa.Column('created_at', TS, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_personas_user_id'), 'personas', ['user_id'], unique=False)
    op.create_index(op.f('ix_personas_created_at'), 'personas', ['created_at'], unique=False)


def downgrade() -> None:
    op.drop_table('personas')
    op.drop_table('ai_chat_messages')
    op.drop_index('ix_ai_artifacts_lookup', table_name='ai_artifacts')
    op.drop_table('ai_artifacts')
    op.drop_table('solutions')
