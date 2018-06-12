class URLQueryState(object):
    """
    This entity represents if the url exists in the database & if it exists, is it safe or not.
    """
    def __init__(self, is_found, is_safe):
        self.is_found = is_found
        self.is_safe = is_safe
