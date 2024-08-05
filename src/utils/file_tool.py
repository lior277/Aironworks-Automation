def convert_bytes(num):
    for x in ['B', 'KB', 'MB', 'GB', 'TB']:
        if num < 1000:
            return '%3.1f %s' % (num, x)
        num /= 1000
