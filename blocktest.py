# import BCDataStream
from Abe import BCDataStream, deserialize
ds = BCDataStream.BCDataStream()

def list_seqs(block):
    inputs = [tr['txIn'] for tr in block['transactions']]
    seqs = [input[0] for  input in inputs]
    seqs2 = [seq['sequence'] for seq in seqs]
    return seqs2


file = open('/home/jorgen/.bitcoin/blocks/blk00225.dat', "rb")
ds.map_file(file, 0)
file.close()

magic = ds.read_bytes(4)
# import pdb;pdb.set_trace()
print "magic is %s" % str(magic)
print str(magic)
length = ds.read_int32()
print "length according to block data is %s" % length
print "length according to actual bytes is %s" % len(ds.input)
end = ds.read_cursor + length

res = deserialize.parse_Block(ds)
print list_seqs(res)

ds.read_cursor = end
ds.read_bytes(4)
length = ds.read_int32()

res = deserialize.parse_Block(ds)
print (
"""
============= Next block =====================
""")
print res

# design: a module that deserializes a block, and prints out sequences, combined with the transaction hash, block hash and block height
# a module that takes files from a directory and pipes them through the above module