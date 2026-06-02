class BaseFileSystemParserPlugin:
    """SDK Base Class for rapid deployment of agency-developed file system modules"""
    def execute_traversal(self, block_stream):
        raise NotImplementedError
