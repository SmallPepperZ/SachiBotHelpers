def chunks(list:list, size:int):
    """Yield successive chunks of specified size from list."""
    for i in range(0, len(list), size):
        yield list[i:i + size]