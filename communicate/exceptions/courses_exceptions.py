class CourseNotFoundException(Exception):
    """Should be called if a course was not found"""
    pass


class NoCoursesExistException(Exception):
    """Should be called if no courses exist"""
    pass


class ProgressNotFound(Exception):
    """Should be called if progress for a user was not found (and needs handling)"""
    pass
