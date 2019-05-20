import eppy

# fname = "./eppy/resources/idffiles/V8_5/smallfile.idf"
# idf = eppy.openidf(fname)


from StringIO import StringIO
# idf1 = eppy.openidf(StringIO("version, 8.5;"))

txt = """  
    Version,8.5;
    Timestep,44,4;
"""

idf1 = eppy.openidf(StringIO(txt))

