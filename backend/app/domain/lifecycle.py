from app.domain.enums import IndexingJobStatus, RepositoryStatus


class InvalidLifecycleTransition(ValueError):
    """Raised when a lifecycle transition is not permitted."""


REPOSITORY_TRANSITIONS: dict[
    RepositoryStatus, set[RepositoryStatus]
] = {
    RepositoryStatus.PENDING: {
        RepositoryStatus.INDEXING,
    },
    RepositoryStatus.INDEXING: {
        RepositoryStatus.READY,
        RepositoryStatus.FAILED,
    },
    RepositoryStatus.READY: {
        RepositoryStatus.REINDEXING,
    },
    RepositoryStatus.REINDEXING: {
        RepositoryStatus.READY,
        RepositoryStatus.FAILED,
    },
    RepositoryStatus.FAILED: {
        RepositoryStatus.INDEXING,
    },
}


INDEXING_JOB_TRANSITIONS: dict[
    IndexingJobStatus, set[IndexingJobStatus]
] = {
    IndexingJobStatus.PENDING: {
        IndexingJobStatus.RUNNING,
        IndexingJobStatus.FAILED,
    },
    IndexingJobStatus.RUNNING: {
        IndexingJobStatus.COMPLETED,
        IndexingJobStatus.FAILED,
    },
    IndexingJobStatus.COMPLETED: set(),
    IndexingJobStatus.FAILED: set(),
}


def transition_repository(
    current: RepositoryStatus,
    target: RepositoryStatus,
) -> RepositoryStatus:
    """Validate and return a repository's next status."""

    if target not in REPOSITORY_TRANSITIONS[current]:
        raise InvalidLifecycleTransition(
            f"Invalid repository transition: {current.value} -> {target.value}"
        )

    return target


def transition_indexing_job(
    current: IndexingJobStatus,
    target: IndexingJobStatus,
) -> IndexingJobStatus:
    """Validate and return an indexing job's next status."""

    if target not in INDEXING_JOB_TRANSITIONS[current]:
        raise InvalidLifecycleTransition(
            f"Invalid indexing job transition: "
            f"{current.value} -> {target.value}"
        )

    return target