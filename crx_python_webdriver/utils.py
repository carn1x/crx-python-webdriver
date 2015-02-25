def crx_range(_range, lowest=1):
    """
    Provides a more natural range generator.

    Usage:
    [i for i in crx_range(3)]     // [1, 2, 3]
    [i for i in crx_range(4, 2)]  // [2, 3, 4]
    [i for i in crx_range(-3)]    // [3, 2, 1]
    [i for i in crx_range(-4, 2)] // [4, 3, 2]
    """

    if _range > 0:
        return xrange(lowest, _range + 1, 1)

    elif _range < 0:
        return xrange(abs(_range), lowest - 1, -1)

    else:
        raise Exception('crx_range first parameter must be non-zero.')
