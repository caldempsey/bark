class LessonNotFoundException(Exception):
    """Should be called if a lesson cannot be found"""
    pass


class NoLessonsExistException(Exception):
    """Should be called if a lesson does not exist"""
    pass
