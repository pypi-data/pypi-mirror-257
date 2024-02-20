class ValidationError(Exception):
    pass


class BlockNotFound(Exception):
    pass


class TransactionNotFound(Exception):
    pass


class FilterNotFound(Exception):
    pass


class SnapshotNotFound(Exception):
    pass


class TransactionFailed(Exception):
    pass


class TransactionReverted(Exception):
    pass
