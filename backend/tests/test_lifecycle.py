import pytest

from app.domain.enums import (
    IndexingJobStatus,
    RepositoryStatus,
)
from app.domain.lifecycle import (
    InvalidLifecycleTransition,
    transition_indexing_job,
    transition_repository,
)


def test_repository_allows_initial_indexing():
    result = transition_repository(
        RepositoryStatus.PENDING,
        RepositoryStatus.INDEXING,
    )

    assert result == RepositoryStatus.INDEXING


def test_repository_allows_successful_indexing():
    result = transition_repository(
        RepositoryStatus.INDEXING,
        RepositoryStatus.READY,
    )

    assert result == RepositoryStatus.READY


def test_repository_rejects_invalid_transition():
    with pytest.raises(InvalidLifecycleTransition):
        transition_repository(
            RepositoryStatus.READY,
            RepositoryStatus.FAILED,
        )


def test_failed_repository_can_retry_indexing():
    result = transition_repository(
        RepositoryStatus.FAILED,
        RepositoryStatus.INDEXING,
    )

    assert result == RepositoryStatus.INDEXING


def test_indexing_job_can_complete():
    result = transition_indexing_job(
        IndexingJobStatus.RUNNING,
        IndexingJobStatus.COMPLETED,
    )

    assert result == IndexingJobStatus.COMPLETED


def test_completed_job_cannot_restart():
    with pytest.raises(InvalidLifecycleTransition):
        transition_indexing_job(
            IndexingJobStatus.COMPLETED,
            IndexingJobStatus.RUNNING,
        )


def test_failed_job_is_terminal():
    with pytest.raises(InvalidLifecycleTransition):
        transition_indexing_job(
            IndexingJobStatus.FAILED,
            IndexingJobStatus.RUNNING,
        )