readdatacommdct(idfname, iddfile='Energy+.idd') # takes filename
    block,commlst,commdct=parse_idd.extractidddata(iddfile) # takes filename
        # opened only once in function. 
    data = eplusdata.eplusdata(theidd,idfname) # idfname is a filename
        eplusdata.eplusdata.__init__ 
            # if statement has to respond to fname being a file obejct
        eplusdata.eplusdata.makedict(dictfile, fname) # fname is a filename


