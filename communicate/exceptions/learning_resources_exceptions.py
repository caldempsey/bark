class NoLearningResourcesExistException(Exception):
    """Should be called if no learning resources exist."""
    pass


class LearningResourceNotFoundException(Exception):
    """Should be called if a learning resource was not found"""
    pass
