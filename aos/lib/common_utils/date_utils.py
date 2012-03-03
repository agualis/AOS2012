def get_string_from_datetime(dt):
    '''
        Returns a formated string representing a datetime with format 2010-12-02 08:12:23.1234
    '''
    return dt.strftime("%Y-%m-%d %H:%M:%S.") + str(dt.microsecond)