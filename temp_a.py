def a_missingkey_standard_1(comm, key_txt, nofirstfields):
    """
    sometimes IDD has fields with no field description. This happens in extensible.
    This functions picks up the previous field description and adds them
    to the fields that have no field descriptions. This update is done in place to commdct
    commdct is not returned.
    missing field descriptions are actually mising keys of a dict
    hence the function is called a missingkey

    This is very old function. Not sure how it works now.
    """

    # get all fields
    fields = getfields(comm)

    # get repeating field names
    repnames = repeatingfieldsnames(fields)

    try:
        first = repnames[0][0] % (1,)
    except IndexError:
        nofirstfields.append(key_txt)
        return nofirstfields

    # get all comments of the first repeating field names
    firstnames = [repname[0] % (1,) for repname in repnames]
    fcomments = [
        field
        for field in fields
        if bunchhelpers.onlylegalchar(field["field"][0]) in firstnames
    ]
    fcomments = [dict(fcomment) for fcomment in fcomments]
    for cmt in fcomments:
        fld = cmt["field"][0]
        fld = bunchhelpers.onlylegalchar(fld)
        fld = bunchhelpers.replaceint(fld)
        cmt["field"] = [fld]

    for i, cmt in enumerate(comm[1:]):
        thefield = cmt["field"][0]
        thefield = bunchhelpers.onlylegalchar(thefield)
        if thefield == first:
            break
    first_i = i + 1

    newfields = []
    for i in range(1, len(comm[first_i:]) // len(repnames) + 1):
        for fcomment in fcomments:
            nfcomment = dict(fcomment)
            fld = nfcomment["field"][0]
            fld = fld % (i,)
            nfcomment["field"] = [fld]
            newfields.append(nfcomment)

    for i, cmt in enumerate(comm):
        if i < first_i:
            continue
        else:
            afield = newfields.pop(0)
            comm[i] = afield
    return nofirstfields

