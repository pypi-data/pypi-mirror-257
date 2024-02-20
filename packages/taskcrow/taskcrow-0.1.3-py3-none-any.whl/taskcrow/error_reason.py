from enum import Enum


class ErrorReason(Enum):
    MATCHING_FAIL = 'MATCHING_FAIL'
    NOT_FOUND = 'NOT_FOUND'  # 이후에 상태이름 재조정이 필요
    NOT_FOUND_EMPTY = 'NOT_FOUND_EMPTY'  # 이후에 상태이름 재조정이 필요
    UNKNOWN = 'UNKNOWN'
