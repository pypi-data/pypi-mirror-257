class BlockchainAttributeTypeError(Exception):
    """incorrect definition of block class attributes."""

    def __str__(self):
        return "invalid attribute data type is specified."


class BlockchainAttributeKeyError(Exception):
    """incorrect definition of block class attributes."""

    def __str__(self):
        return "invalid attribute key is specified."
