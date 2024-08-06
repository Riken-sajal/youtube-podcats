import datetime

def expiry_extend(expiry_timestamp : int = 0,hours : int = 0):
    return expiry_timestamp + (hours * 3600)
