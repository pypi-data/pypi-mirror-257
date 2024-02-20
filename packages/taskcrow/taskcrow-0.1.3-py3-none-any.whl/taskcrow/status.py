from enum import Enum


class Status(Enum):
    PENDING = 'pending'  # 작업 시작전
    READY = 'ready'  # 작업 시작전
    IN_PROCESSING = 'in_processing'
    COMPLETE = 'complete'
    RE_DO_COMPLETE = 're_do_complete'
    COMPLETE_BUT_EMPTY = 'complete_but_empty'
    ERROR = 'error'

