"""AI Personal Exam Mentor: exam goals, study tasks, mistake notebook, practice sessions, reminder preferences,
mentor chat and cached AI insights; extra evidence columns on user_topic_mastery.

Revision ID: 0003
Revises: 0002
Create Date: 2026-11-05

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '0003'
down_revision: Union[str, Sequence[str], None] = '0002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

JSONB = postgresql.JSONB(astext_type=sa.Text())
TS = sa.DateTime(timezone=True)


def upgrade() -> None:
    for name in ('wrong_count', 'skipped_count', 'time_spent_sec', 'target_time_sec', 'sessions_count'):
        op.add_column('user_topic_mastery', sa.Column(name, sa.Integer(), server_default='0', nullable=False))
    op.add_column('user_topic_mastery', sa.Column('recent_accuracy', sa.Float(), nullable=True))
    op.add_column('user_topic_mastery', sa.Column('previous_recent_accuracy', sa.Float(), nullable=True))
    op.add_column('user_topic_mastery', sa.Column('by_difficulty', JSONB, server_default=sa.text("'{}'::jsonb"),
                                                  nullable=False))

    op.create_table('exam_goals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('exam_id', sa.Uuid(), nullable=False),
    sa.Column('exam_date', sa.Date(), nullable=False),
    sa.Column('daily_minutes', sa.Integer(), nullable=False),
    sa.Column('rest_weekday', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('plan_version', sa.Integer(), nullable=False),
    sa.Column('plan_generated_at', TS, nullable=True),
    sa.Column('plan_meta', JSONB, nullable=False),
    sa.Column('created_at', TS, server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', TS, server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['exam_id'], ['exams.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'exam_id')
    )
    op.create_index(op.f('ix_exam_goals_user_id'), 'exam_goals', ['user_id'], unique=False)
    op.create_index(op.f('ix_exam_goals_status'), 'exam_goals', ['status'], unique=False)

    op.create_table('study_tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('goal_id', sa.Integer(), nullable=False),
    sa.Column('plan_version', sa.Integer(), nullable=False),
    sa.Column('task_date', sa.Date(), nullable=False),
    sa.Column('seq', sa.Integer(), nullable=False),
    sa.Column('kind', sa.String(length=20), nullable=False),
    sa.Column('topic_id', sa.Integer(), nullable=True),
    sa.Column('section_key', sa.String(length=40), nullable=True),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('detail', sa.Text(), nullable=False),
    sa.Column('level', sa.String(length=12), nullable=True),
    sa.Column('minutes', sa.Integer(), nullable=False),
    sa.Column('target_questions', sa.Integer(), nullable=True),
    sa.Column('priority', sa.String(length=12), nullable=True),
    sa.Column('reason', sa.Text(), nullable=False),
    sa.Column('status', sa.String(length=12), nullable=False),
    sa.Column('completed_at', TS, nullable=True),
    sa.Column('actual_minutes', sa.Integer(), nullable=True),
    sa.Column('practice_session_id', sa.Uuid(), nullable=True),
    sa.Column('created_at', TS, nullable=False),
    sa.ForeignKeyConstraint(['goal_id'], ['exam_goals.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['topic_id'], ['topics.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_study_tasks_user_date', 'study_tasks', ['user_id', 'task_date'], unique=False)
    op.create_index('ix_study_tasks_goal_status', 'study_tasks', ['goal_id', 'status'], unique=False)

    op.create_table('mistake_notebook',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('question_id', sa.Uuid(), nullable=False),
    sa.Column('exam_id', sa.Uuid(), nullable=False),
    sa.Column('topic_id', sa.Integer(), nullable=True),
    sa.Column('last_attempt_id', sa.Uuid(), nullable=True),
    sa.Column('last_answer', JSONB, nullable=True),
    sa.Column('reasons', JSONB, nullable=False),
    sa.Column('auto_mistake_type', sa.String(length=30), nullable=True),
    sa.Column('mistake_type', sa.String(length=30), nullable=True),
    sa.Column('times_wrong', sa.Integer(), nullable=False),
    sa.Column('times_skipped', sa.Integer(), nullable=False),
    sa.Column('times_slow', sa.Integer(), nullable=False),
    sa.Column('revision_correct', sa.Integer(), nullable=False),
    sa.Column('revision_wrong', sa.Integer(), nullable=False),
    sa.Column('box', sa.Integer(), nullable=False),
    sa.Column('next_review_at', TS, nullable=True),
    sa.Column('last_reviewed_at', TS, nullable=True),
    sa.Column('last_time_sec', sa.Integer(), nullable=False),
    sa.Column('bookmarked', sa.Boolean(), nullable=False),
    sa.Column('note', sa.Text(), nullable=False),
    sa.Column('status', sa.String(length=12), nullable=False),
    sa.Column('created_at', TS, server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', TS, server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['exam_id'], ['exams.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['last_attempt_id'], ['attempts.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['topic_id'], ['topics.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'question_id')
    )
    op.create_index('ix_mistake_notebook_due', 'mistake_notebook', ['user_id', 'status', 'next_review_at'], unique=False)

    op.create_table('practice_sessions',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('kind', sa.String(length=20), nullable=False),
    sa.Column('goal_id', sa.Integer(), nullable=True),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.Column('topic_id', sa.Integer(), nullable=True),
    sa.Column('items', JSONB, nullable=False),
    sa.Column('status', sa.String(length=12), nullable=False),
    sa.Column('results', JSONB, nullable=False),
    sa.Column('correct', sa.Integer(), nullable=True),
    sa.Column('created_at', TS, nullable=False),
    sa.Column('submitted_at', TS, nullable=True),
    sa.ForeignKeyConstraint(['goal_id'], ['exam_goals.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['task_id'], ['study_tasks.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['topic_id'], ['topics.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_practice_sessions_user_id'), 'practice_sessions', ['user_id'], unique=False)

    op.create_table('notification_preferences',
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('push_enabled', sa.Boolean(), nullable=False),
    sa.Column('email_enabled', sa.Boolean(), nullable=False),
    sa.Column('morning_enabled', sa.Boolean(), nullable=False),
    sa.Column('morning_time', sa.String(length=5), nullable=False),
    sa.Column('afternoon_enabled', sa.Boolean(), nullable=False),
    sa.Column('afternoon_time', sa.String(length=5), nullable=False),
    sa.Column('evening_enabled', sa.Boolean(), nullable=False),
    sa.Column('evening_time', sa.String(length=5), nullable=False),
    sa.Column('countdown_enabled', sa.Boolean(), nullable=False),
    sa.Column('mock_reminders_enabled', sa.Boolean(), nullable=False),
    sa.Column('max_per_day', sa.Integer(), nullable=False),
    sa.Column('timezone', sa.String(length=40), nullable=False),
    sa.Column('updated_at', TS, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id')
    )

    op.create_table('mentor_messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('goal_id', sa.Integer(), nullable=True),
    sa.Column('role', sa.String(length=10), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('meta', JSONB, nullable=False),
    sa.Column('created_at', TS, nullable=False),
    sa.ForeignKeyConstraint(['goal_id'], ['exam_goals.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mentor_messages_user_id'), 'mentor_messages', ['user_id'], unique=False)

    op.create_table('mentor_insights',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('kind', sa.String(length=30), nullable=False),
    sa.Column('ref_key', sa.String(length=80), nullable=False),
    sa.Column('payload', JSONB, nullable=False),
    sa.Column('created_at', TS, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'kind', 'ref_key')
    )
    # Reminder dedup looks up "already sent this kind today" per user.
    op.create_index('ix_notifications_user_kind_created', 'notifications', ['user_id', 'kind', 'created_at'],
                    unique=False)


def downgrade() -> None:
    op.drop_index('ix_notifications_user_kind_created', table_name='notifications')
    op.drop_table('mentor_insights')
    op.drop_index(op.f('ix_mentor_messages_user_id'), table_name='mentor_messages')
    op.drop_table('mentor_messages')
    op.drop_table('notification_preferences')
    op.drop_index(op.f('ix_practice_sessions_user_id'), table_name='practice_sessions')
    op.drop_table('practice_sessions')
    op.drop_index('ix_mistake_notebook_due', table_name='mistake_notebook')
    op.drop_table('mistake_notebook')
    op.drop_index('ix_study_tasks_goal_status', table_name='study_tasks')
    op.drop_index('ix_study_tasks_user_date', table_name='study_tasks')
    op.drop_table('study_tasks')
    op.drop_index(op.f('ix_exam_goals_status'), table_name='exam_goals')
    op.drop_index(op.f('ix_exam_goals_user_id'), table_name='exam_goals')
    op.drop_table('exam_goals')
    for name in ('by_difficulty', 'previous_recent_accuracy', 'recent_accuracy', 'sessions_count', 'target_time_sec',
                 'time_spent_sec', 'skipped_count', 'wrong_count'):
        op.drop_column('user_topic_mastery', name)
