from enum import Enum

class RepositoryStatus(str, Enum):
    PENDING = "PENDING"
    INDEXING = "INDEXING"
    READY = "READY"
    FAILED = "FAILED"
    REINDEXING = "REINDEXING"

class IndexingJobStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class IndexingJobType(str, Enum):
    INITIAL = "INITIAL"
    REINDEX = "REINDEX"