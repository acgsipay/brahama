def flatten(items, union='.', serparator=',', prefix=''):
    container = {}

    for key, value in items.iteritems():
        if prefix != '':
            key = '%s%s%s' % (prefix, union, key)

        if isinstance(value, dict):
            container.update(flatten(value, union, serparator, key))


        elif isinstance(value, (list, tuple, set)):
            container[key] = serparator.join(value)

        else:
            container[key] = value

    return container

def implode(items, union='=', separator='; '):
    flat = flatten(items)
    return separator.join('%s%s%s' % (key, union, value) for key, value in flat.iteritems())

def parameterize(keys, *args):
    params = {}

    for key in keys:
        for data in args:
            if key in data:
                params[key] = data[key]

    return params
