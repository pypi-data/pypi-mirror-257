# eSCAPyDL - a Deep Learning Side-Channel Analysis Python Framework
# Copyright (C) 2023  Weissbart Léo

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys, logging
import numpy as np
from itertools import chain
import torch

reg_size = 64
ASCON_128_IV_int = 0x80400c0600000000
ASCON_128_IV = (0x80400c0600000000).to_bytes(16, 'big')

ASCON_SBOX_NP = np.array([0x04, 0x0b, 0x1f, 0x14, 0x1a, 0x15, 0x09, 0x02, 
              0x1b, 0x05, 0x08, 0x12, 0x1d, 0x03, 0x06, 0x1c, 
              0x1e, 0x13, 0x07, 0x0e, 0x00, 0x0d, 0x11, 0x18, 
              0x10, 0x0c, 0x01, 0x19, 0x16, 0x0a, 0x0f, 0x17])
ASCON_SBOX_NP_DIM = [np.array([ASCON_SBOX_NP[x] for x in range(1<<4)]), np.array([ASCON_SBOX_NP[x] for x in range(1<<4, 1<<5)])]#If first bit is 0 or 1
ASCON_SBOX = torch.ByteTensor(ASCON_SBOX_NP)

#diffusion layer on register x_i
dr = [[45,36],
      [3,25],
      [63,58],
      [54,47],
      [57,23]]

def bit_value(i, register_value):
    return (register_value>>(reg_size-1-i))&1
    
def select_bit_bytes(i, array):
    """Returns the bit index `i` from the array of bytes `array`
    If array have 2 dimensions, it will select bits given the first axis.
    
    :param i: index of the bit to select.
    :type i: int
    :param aray: array of bytes in bytes/int format.
    :type array: list
    """
    if isinstance(array,np.ndarray) or isinstance(array, torch.Tensor):
        if len(array.shape)==1:
            i = i % (len(array)*8)
            return (array[i//8]>>(7-(i%8)))&1
        elif len(array.shape)==2:
            i = i % (len(array[0])*8)
            return (array[:,i//8]>>(7-(i%8)))&1
    elif isinstance(array, bytes) or isinstance(array, list):
        i = i % (len(array)*8)
        return (array[i//8]>>(7-(i%8)))&1
    else: 
        logging.error("select_bit_bytes: array type not supported, got {}".format(type(array)))
        logging.exception('')

#-----------------------------------------#
# Intermediate value of SBox and Linear Diffusion Layer
reg_num_0 = 4
reg_num_1 = 1
def intermediate_value(keyguess, trace_parameters):
    """Return the intermediate value of a key in the SBox . 
    nonce0 and nonce1 should be byte arrays of size (8) as they both are half of the nonce length (16 bytes).
    k should be a 3-bit value as an integer. This bit corresponds to the part of the key concerned in the attack given subkey.

    :param trace_parameters: Dictionary containing the trace parameters for intermediate value computation
    :type trace_parameters: dict
    :return: Intermediate value
    :rtype: Any
    """        
    if trace_parameters['subkey']<reg_size:
        y0_i = lambda x0,x1,x3,x4: x4&(x1^1)^x3
        # y0_i = lambda x0,x1,x3,x4: x1&(x0+x4+1)+x3+x4
        res = (y0_i(select_bit_bytes(trace_parameters['subkey']%reg_size           ,ASCON_128_IV),   (keyguess>>2)&1, select_bit_bytes(trace_parameters['subkey']%reg_size           , trace_parameters['nonce0']), select_bit_bytes(trace_parameters['subkey']%reg_size           , trace_parameters['nonce1']))) \
            ^ (y0_i(select_bit_bytes((trace_parameters['subkey']+dr[reg_num_0][0])%reg_size,ASCON_128_IV),   (keyguess>>1)&1, select_bit_bytes((trace_parameters['subkey']+dr[reg_num_0][0])%reg_size, trace_parameters['nonce0']), select_bit_bytes((trace_parameters['subkey']+dr[4][0])%reg_size, trace_parameters['nonce1']))) \
            ^ (y0_i(select_bit_bytes((trace_parameters['subkey']+dr[reg_num_0][1])%reg_size,ASCON_128_IV),   (keyguess>>0)&1, select_bit_bytes((trace_parameters['subkey']+dr[reg_num_0][1])%reg_size, trace_parameters['nonce0']), select_bit_bytes((trace_parameters['subkey']+dr[4][1])%reg_size, trace_parameters['nonce1'])))
        return res
    elif trace_parameters['subkey']<2*reg_size:
        y0_i = lambda x0,x12,x3,x4: x3&(x12^1)^x4
        # y0_i = lambda x0,x12,x3,x4: x4&(x3^1)^x12^1
        res = (y0_i(select_bit_bytes(trace_parameters['subkey']%reg_size           ,ASCON_128_IV),(keyguess>>2)&1, select_bit_bytes(trace_parameters['subkey']%reg_size           , trace_parameters['nonce0']), select_bit_bytes(trace_parameters['subkey']%reg_size           , trace_parameters['nonce1']))) \
            ^ (y0_i(select_bit_bytes((trace_parameters['subkey']+dr[reg_num_0][0])%reg_size,ASCON_128_IV),(keyguess>>1)&1, select_bit_bytes((trace_parameters['subkey']+dr[reg_num_1][0])%reg_size, trace_parameters['nonce0']), select_bit_bytes((trace_parameters['subkey']+dr[reg_num_1][0])%reg_size, trace_parameters['nonce1']))) \
            ^ (y0_i(select_bit_bytes((trace_parameters['subkey']+dr[reg_num_0][1])%reg_size,ASCON_128_IV),(keyguess>>0)&1, select_bit_bytes((trace_parameters['subkey']+dr[reg_num_1][1])%reg_size, trace_parameters['nonce0']), select_bit_bytes((trace_parameters['subkey']+dr[reg_num_1][1])%reg_size, trace_parameters['nonce1'])))
        return res
    
def select_subkey(i, key, array=False):
    if i<reg_size:
        sub_key = [select_bit_bytes((i)%reg_size         , key[0:8]), 
                   select_bit_bytes((i+dr[reg_num_0][0])%reg_size, key[0:8]), 
                   select_bit_bytes((i+dr[reg_num_0][1])%reg_size, key[0:8])]
    elif i<2*reg_size:
        sub_key = [x^y for x,y in zip([select_bit_bytes((i)%reg_size         , key[0:8]), 
                                       select_bit_bytes((i+dr[reg_num_1][0])%reg_size, key[0:8]), 
                                       select_bit_bytes((i+dr[reg_num_1][1])%reg_size, key[0:8])], 
                                      [select_bit_bytes((i)%reg_size         , key[8:16]), 
                                       select_bit_bytes((i+dr[reg_num_1][0])%reg_size, key[8:16]), 
                                       select_bit_bytes((i+dr[reg_num_1][1])%reg_size, key[8:16])]
                                    )
        ]
    if not array:
        sub_key = sub_key[0]<<2 | sub_key[1]<<1 | sub_key[2]
    return sub_key
#-----------------------------------------#

#-----------------------------------------#
# Intermediate value for a chunk of bits after the SBox and Linear Diffusion Layer
def intermediate_value_chunk(keyguess, trace_parameters):
    iv = 0
    chunk_size = 3 # Size in bits of the intermidate_value
    targetByte = trace_parameters['subkey'] # 'subkey' is index of the byte to target
    keyguess_bits = [(keyguess>>i)&1 for i in range(3*chunk_size)]
    for bitNum in range(len(keyguess_bits)//chunk_size):
        trace_parameters['subkey'] = (targetByte*chunk_size) + bitNum # Transform into the bit to target
        sub_keyguess = keyguess_bits[bitNum::chunk_size]
        _ret = 0
        for i, sk in enumerate(sub_keyguess):
            _ret ^= sk<<((len(sub_keyguess)-1-i))
        sub_keyguess = _ret
        iv ^= (intermediate_value(sub_keyguess, trace_parameters)<<((chunk_size-1)-bitNum))
    return iv

def select_subkey_chunk(i, key, array=False):
    chunk_size = 3
    sub_key = []
    if i<reg_size:
        sub_key.append([select_bit_bytes((i+c)%reg_size           , key[0:8]) for c in range(chunk_size)])
        sub_key.append([select_bit_bytes((i+c+dr[4][0])%reg_size  , key[0:8]) for c in range(chunk_size)])
        sub_key.append([select_bit_bytes((i+c+dr[4][1])%reg_size  , key[0:8]) for c in range(chunk_size)])
    elif i<2*reg_size:
        sub_key.append([select_bit_bytes((i+c)%reg_size, key[0:8])          ^ select_bit_bytes((i+c)%reg_size, key[8:16])          for c in range(chunk_size)])
        sub_key.append([select_bit_bytes((i+c+dr[1][0])%reg_size, key[0:8]) ^ select_bit_bytes((i+c+dr[1][0])%reg_size, key[8:16]) for c in range(chunk_size)])
        sub_key.append([select_bit_bytes((i+c+dr[1][1])%reg_size, key[0:8]) ^ select_bit_bytes((i+c+dr[1][1])%reg_size, key[8:16]) for c in range(chunk_size)])
    sub_key = list(chain.from_iterable(sub_key)) # flatten the array
    if array==False:
        _ret = 0
        for i,e in enumerate(sub_key):
            _ret += e<<((len(sub_key)-1-i))
        sub_key = _ret
    return sub_key
#-----------------------------------------#

#-----------------------------------------#
# SBOX intermediate value. keygess is a 2bit value
def intermediate_value_sbox(keyguess, trace_parameters):
    if 'nonce0' in trace_parameters.keys():
        if isinstance(trace_parameters['nonce0'], torch.Tensor):
            ind = ((select_bit_bytes(trace_parameters['subkey'], ASCON_128_IV))<<4 | 
                    ((keyguess>>1)&1)<<3 | 
                    ((keyguess>>0)&1)<<2 | 
                    (select_bit_bytes(trace_parameters['subkey'], trace_parameters['nonce0'].numpy()))<<1 | 
                    (select_bit_bytes(trace_parameters['subkey'], trace_parameters['nonce1'].numpy()))<<0)
            return torch.index_select(ASCON_SBOX, 0, ind.int())
        else:
            ind = ((select_bit_bytes(trace_parameters['subkey'], ASCON_128_IV))<<4 | 
                    ((keyguess>>1)&1)<<3 | 
                    ((keyguess>>0)&1)<<2 | 
                    (select_bit_bytes(trace_parameters['subkey'], trace_parameters['nonce0']))<<1 | 
                    (select_bit_bytes(trace_parameters['subkey'], trace_parameters['nonce1']))<<0)
            return ASCON_SBOX_NP[ind]
    elif 'nonce' in trace_parameters.keys():
        if isinstance(trace_parameters['nonce'], torch.Tensor):
            ind = torch.IntTensor([((select_bit_bytes(trace_parameters['subkey'], ASCON_128_IV))<<4 | 
                    ((keyguess[id]>>1)&1)<<3 | 
                    ((keyguess[id]>>0)&1)<<2 | 
                    (select_bit_bytes(trace_parameters['subkey'], trace_parameters['nonce'][id][:8].numpy()))<<1 | 
                    (select_bit_bytes(trace_parameters['subkey'], trace_parameters['nonce'][id][8:16].numpy()))<<0) for id in range(len(keyguess))])
            return torch.index_select(ASCON_SBOX, 0, ind.int())
        else:
            ind = ((select_bit_bytes(trace_parameters['subkey'], ASCON_128_IV))<<4 | 
                    ((keyguess>>1)&1)<<3 | 
                    ((keyguess>>0)&1)<<2 | 
                    (select_bit_bytes(trace_parameters['subkey'], trace_parameters['nonce'][:8]))<<1 | 
                    (select_bit_bytes(trace_parameters['subkey'], trace_parameters['nonce'][8:16]))<<0)
            return ASCON_SBOX_NP[ind]
    
def select_subkey_sbox(i, key):
    return (select_bit_bytes(i%(2*reg_size), key))<<1 | select_bit_bytes((i+reg_size)%(2*reg_size), key)
    
#-----------------------------------------#

#-----------------------------------------#
# Chunk SBOX intermediate value. keygess is a chunk_size-bit value for the two key registers
def intermediate_value_sbox_chunk(keyguess, trace_parameters, chunk_size=8):
    if trace_parameters['subkey']*chunk_size<reg_size:
        y0_i = lambda x0,x1,x3,x4: x1&(x0^x4^1)^x3^x4
        res = 0
        for i in range(chunk_size):
            res |= (y0_i(select_bit_bytes((trace_parameters['subkey']*chunk_size+i)%reg_size,ASCON_128_IV), 
                         (keyguess>>(chunk_size-1 - i))&1, 
                         select_bit_bytes((trace_parameters['subkey']*chunk_size+i)%reg_size, trace_parameters['nonce0']), 
                         select_bit_bytes((trace_parameters['subkey']*chunk_size+i)%reg_size, trace_parameters['nonce1']))) << (chunk_size-1 - i)
        return res
    elif trace_parameters['subkey']*chunk_size<2*reg_size:
        y0_i = lambda x12,x3,x4: x4&(x3^1)^x12^1
        res = 0
        for i in range(chunk_size):
            res |= (y0_i((keyguess>>(chunk_size-1 - i))&1, 
                         select_bit_bytes((trace_parameters['subkey']*chunk_size+i)%reg_size, trace_parameters['nonce0']), 
                         select_bit_bytes((trace_parameters['subkey']*chunk_size+i)%reg_size, trace_parameters['nonce1']))) << (chunk_size-1 - i)
        return res
    
def select_subkey_sbox_chunk(i, key, chunk_size=8):
    ret = 0
    for bit in range(chunk_size):
        ret |= select_bit_bytes(i*chunk_size + bit, key)<<(chunk_size-1 - bit)
    if i*chunk_size>=reg_size:
        for bit in range(chunk_size):
            ret ^= select_bit_bytes((i*chunk_size + bit)%64, key)<<(chunk_size-1 - bit)
    return ret

#-----------------------------------------#