def save_to_db(f, order, fs):
    try:
        fid = fs.put(f, filename=order)
        return fid
    except Exception as err:
        raise Exception("internal server error: " + str(err))
