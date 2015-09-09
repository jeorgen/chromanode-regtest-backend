from itertools import chain
from Abe import BCDataStream, deserialize, util

XFER_TAG_BITS = [1, 1, 0, 0, 1, 1]
GENESIS_TAG_BITS = [1, 0, 1, 0, 0, 1]


ds = BCDataStream.BCDataStream()

def uint_to_bit_list(n, bits=32):
    """little-endian"""
    return [1 & (n >> i) for i in range(bits)]

def from_nSequence(nSequence):
    bits = uint_to_bit_list(nSequence)
    tag_bits = bits[0:6]

    if ((tag_bits != XFER_TAG_BITS) and
        (tag_bits != GENESIS_TAG_BITS)):
        return None

    padding_code = bit_list_to_uint(bits[6:12])
    return cls(padding_code, tag_bits == cls.GENESIS_TAG_BITS)

# determine how many coins an input spends, going further
# 
def process_transaction(tx, transaction_hash, block_hash):
    if not_colored(tx):
        return
    ouputs = color_outputs(tx)
    
def first_input_color_tagged(tx):
    return uint_to_bit_list(tx['txIn'][0]['sequence'][0:6]) in (XFER_TAG_BITS, GENESIS_TAG_BITS)

def list_seqs(block):
    # import pdb;pdb.set_trace()
    sequences = []
    block_hash = block['hashMerkleRoot']
    for tx in block['transactions']:
        tx_data = tx['__data__']
        # process_transaction(tx, transaction_hash, block_hash)
        input_no = 0
        # if not first_input_color_tagged(tx):
            # pass # should be continue
        # colored_outputs = colored_outputs
        transaction_hash = util.double_sha256(tx['__data__'])

        for input in tx['txIn'] :
            sequences.append( str({'nSequence': input['sequence'], 'input_no': input_no, 'txHash': transaction_hash, 'blockHash': block_hash}))
            input_no += 1

    # inputs_per_transaction = [tr['txIn'] for tr in block['transactions']]
    # inputs = list(chain.from_iterable(inputs_per_transaction))
    # [input for inputs in inputs_per_transaction for input in inputs]
    # [val for sublist in list_of_lists for val in sublist]
    # seqs = [inputs for inputs in inputs_per_transaction]
    # import pdb;pdb.set_trace()
    # seqs2 = [str(uint_to_bit_list(seq['sequence'])) for seq in seqs ] # if uint_to_bit_list(seq['sequence']) in (XFER_TAG_BITS, GENESIS_TAG_BITS)
    return sequences

def rpc(func, *params):
    ret = util.jsonrpc(url, func, *params)
    return ret


def get_height():
    """ """
    pass

def get_blockhash(height):
    try:
        return rpc("getblockhash", height)
    except util.JsonrpcException, e:
        if e.code in (-1, -5, -8):
            # Block number out of range...
            #  -1 is legacy code (pre-10.0), generic error
            #  -8 (RPC_INVALID_PARAMETER) first seen in bitcoind 10.x
            #  -5 (RPC_NOT_FOUND): Been suggested in #bitcoin-dev as more appropriate
            return None
        raise

def longest_chain():
    height = get_height()
    hashes =  [get_block_hash(block_number) for block_number in range(1,height)] # 0 or 1?
    return hashes


def get_block(hash):
    rpc_block = rpc("getblock", rpc_hash)
    return block

file = open('/home/jorgen/.bitcoin/blocks/blk00225.dat', "rb")
ds.map_file(file, 0)
file.close()
magic = ds.read_bytes(4)
length = ds.read_int32()

file_length = len(ds.input)
end = length + ds.read_cursor
ds.read_cursor = 0
blockcount = 0
while True:
    if end >= file_length:
        break
    blockcount += 1
    magic = ds.read_bytes(4)
    length = ds.read_int32()
    end = length + ds.read_cursor
    block_data = deserialize.parse_Block(ds)
    print '\n'.join(list_seqs(block_data))
    ds.read_cursor = end
print "block count: %s" % blockcount

# design: a module that deserializes a block, and prints out sequences, combined with the transaction hash, block hash and block height
# a module that takes files from a directory and pipes them through the above module
# pipeline design simple - find -name "*.dat" | parseblocks --nsequences |
# pipeline design simple - find -name "*.dat" | parseblocks --xpath '/blocks/transaction/input/sequence' |
# complex - cat blk00225.dat

# Question: what are the remaining 20 bits in nSequence used for? Nothing it seems
#  

