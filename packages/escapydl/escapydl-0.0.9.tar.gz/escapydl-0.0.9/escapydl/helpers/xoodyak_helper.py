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

import torch
import numpy as np

padd = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02'

def to_s(state_bytes):
    s = [0] * 12
    j = 0
    for i in range(12):
        s[i] = state_bytes[j] << 0
        j += 1
        s[i] |= state_bytes[j] << 8
        j += 1
        s[i] |= state_bytes[j] << 16
        j += 1
        s[i] |= state_bytes[j] << 24
        j += 1
    return s

def to_state_bytes(s):
    state_bytes = bytearray(48)
    j = 0
    for i in range(12):
        state_bytes[j] = (s[i] >> 0) & 0xFF
        j += 1
        state_bytes[j] = (s[i] >> 8) & 0xFF
        j += 1
        state_bytes[j] = (s[i] >> 16) & 0xFF
        j += 1
        state_bytes[j] = (s[i] >> 24) & 0xFF
        j += 1
    return state_bytes

def first_round_linear_layer(state_bytes):
    s = to_s(state_bytes)

    # Only round zero is done here
    e = [0, 0, 0, 0]

    #Theta
    for i in range(4):
        r = s[i] ^ s[i + 4] ^ s[i + 8]
        e[i] = (r >> 18) | (r << 14) & 0xFFFF_FFFF
        r = e[i]
        e[i] ^= (r >> 9) | (r << 23) & 0xFFFF_FFFF
    for i in range(12):
        s[i] ^= e[(i - 1) & 3]

    #Rho west
    s[7], s[4] = s[4], s[7]
    s[7], s[5] = s[5], s[7]
    s[7], s[6] = s[6], s[7]
    for i in range(4):
        s[i+8] = (s[i+8] >> 21) | (s[i+8] << 11) & 0xFFFF_FFFF

    state = to_state_bytes(s)
    return state

def first_round_linear_layer_with_iota(state_bytes):
    s = to_s(state_bytes)

    # Only round zero is done here
    e = [0, 0, 0, 0]

    #Theta
    for i in range(4):
        r = s[i] ^ s[i + 4] ^ s[i + 8]
        e[i] = (r >> 18) | (r << 14) & 0xFFFF_FFFF
        r = e[i]
        e[i] ^= (r >> 9) | (r << 23) & 0xFFFF_FFFF
    for i in range(12):
        s[i] ^= e[(i - 1) & 3]

    #Rho west
    s[7], s[4] = s[4], s[7]
    s[7], s[5] = s[5], s[7]
    s[7], s[6] = s[6], s[7]
    for i in range(4):
        s[i+8] = (s[i+8] >> 21) | (s[i+8] << 11) & 0xFFFF_FFFF

    #Iota
    s[0] ^= 0x058

    state = to_state_bytes(s)

    return state

def np_first_round_linear_layer_with_iota(s):

    # Only round zero is done here
    e = [0, 0, 0, 0]

    #Theta
    for i in range(4):
        r = s[:,i] ^ s[:,i + 4] ^ s[:,i + 8]
        e[i] = (r >> 18) | (r << 14) & 0xFFFF_FFFF
        r = e[i]
        e[i] ^= (r >> 9) | (r << 23) & 0xFFFF_FFFF
    for i in range(12):
        s[:,i] ^= e[(i - 1) & 3]

    #Rho west
    tmp = s[:,7].copy()
    s[:,7] = s[:,4]
    s[:,4] = tmp
    tmp = s[:,7].copy()
    s[:,7] = s[:,5]
    s[:,5] = tmp
    tmp = s[:,7].copy()
    s[:,7] = s[:,6]
    s[:,6] = tmp
    for i in range(4):
        s[:,i+8] = (s[:,i+8] >> 21) | (s[:,i+8] << 11) & 0xFFFF_FFFF

    #Iota
    s[:,0] ^= 0x058

    return s

def getBit(state_bytes,x,y,z):
    #input is a bytearray of 48 bytes
    s = to_s(state_bytes)
    lane = s[x+4*y]
    return (lane >> z)&1

def getBitlane(s,x,y,z):
    #input is a numpy array of 12 lanes
    lane = s[:,x+4*y]
    return ((lane >> z)&1).astype(np.uint8)

def getBit_s(s,x,y,z):
    #input is a bytearray of 48 bytes
    # Same as previous but without conversion to state_bytes (speedup factor 13x)
    lane = s[4*(x+4*y):4*(x+4*y+1)]
    return (np.frombuffer(lane,dtype=np.uint32)[0] >> z)&1

def getColumn(state_bytes,x,z):
    return (getBit_s(state_bytes,x,0,z),getBit_s(state_bytes,x,1,z),getBit_s(state_bytes,x,2,z))
    


##
def chi3(a,b,c):
    return (a^((b^1)&c),b^((c^1)&a),c^((a^1)&b))

def rho_east_p(x,y,z):
    if(y==0):
        return (x,y,z)
    else:
       if(y==1):
           return (x,y,(z+1)%32)
       else:
           return ((x+2)%4,y,(z+8)%32)
       
def compute_intermediates(nonce, keyguess, targetbit):
    # Does it make sense to have 'nonceState' and 'nonceBeforeChi' inside trace_parameters?
    x,z = targetbit//32, targetbit%32
    # build nonce state and compute before Chi
    nonceState = bytearray(48)
    # put the nonce
    for j, v in enumerate(nonce):
        nonceState[16+j] ^= v
    # padd
    nonceState[32] ^= 0x10
    nonceState[33] ^= 0x01
    nonceState[47] ^= 0x02
    nonceBeforeChi = first_round_linear_layer_with_iota(nonceState)
    m0,m1,m2 = getColumn(nonceBeforeChi,x,z)

    ## target column is defined by the coordinates of the plane (x,z), with x index of the lane and z index of the of the bit in the lane
    fk0 = (keyguess>>3)&1 # this is the fixed key
    k0 = keyguess & 1 # this is before chi
    k1 = (keyguess>>1)&1
    k2 = (keyguess>>2)&1
    bits_aft = chi3(m0^k0,m1^k1,m2^k2)
    bits_bef = []
    bits_bef.append(fk0)
    (xa,ya,za) = rho_east_p(x,1,z)
    bits_bef.append(getBit_s(nonceState,xa,ya,za))      
    (xa,ya,za) = rho_east_p(x,2,z)              
    bits_bef.append(getBit_s(nonceState,xa,ya,za))
    return (bits_bef[0] ^ bits_aft[0]) + (bits_bef[1] ^ bits_aft[1]) + (bits_bef[2] ^ bits_aft[2])

def intermediate_value(keyguess, trace_parameters):
    # Does it make sense to have 'nonceState' and 'nonceBeforeChi' inside trace_parameters?
    x,z = trace_parameters['subkey']//32, trace_parameters['subkey']%32
    ## target column is defined by the coordinates of the plane (x,z), with x index of the lane and z index of the of the bit in the lane
    fk0 = (keyguess>>3)&1 # this is the fixed key
    k0 = keyguess & 1 # this is before chi
    k1 = (keyguess>>1)&1
    k2 = (keyguess>>2)&1

    if isinstance(trace_parameters['nonce'], np.ndarray) or isinstance(trace_parameters['nonce'], torch.Tensor):
        if len(trace_parameters['nonce'].shape) > 1:
            fk0 = fk0.numpy()
            k0 = k0.numpy()
            k1 = k1.numpy()
            k2 = k2.numpy()
            n_nonces = trace_parameters['nonce'].shape[0]
            nonceState = np.hstack((np.zeros((n_nonces,16), dtype=np.uint8), trace_parameters['nonce'], np.zeros((n_nonces,48-16-trace_parameters['nonce'].shape[1]), dtype=np.uint8)))
            nonceState ^= np.frombuffer(padd, dtype=np.uint8)
            nonceState = np.frombuffer(bytes(nonceState), dtype=np.uint32).reshape((n_nonces,12))
            nonceBeforeChi = nonceState.copy()
            nonceBeforeChi = np_first_round_linear_layer_with_iota(nonceBeforeChi)
            m0, m1, m2 = getBitlane(nonceBeforeChi,x,0,z), getBitlane(nonceBeforeChi,x,1,z), getBitlane(nonceBeforeChi,x,2,z)
            bits_aft = chi3(m0^k0,m1^k1,m2^k2)
            bits_bef = []
            bits_bef.append(fk0)
            (xa,ya,za) = rho_east_p(x,1,z)
            bits_bef.append(getBitlane(nonceState,xa,ya,za))      
            (xa,ya,za) = rho_east_p(x,2,z)              
            bits_bef.append(getBitlane(nonceState,xa,ya,za))
            # return torch.ByteTensor((bits_bef[0] ^ bits_aft[0]) + (bits_bef[1] ^ bits_aft[1]) + (bits_bef[2] ^ bits_aft[2]))
            return torch.ByteTensor(((bits_bef[0] ^ bits_aft[0])<<2) + ((bits_bef[1] ^ bits_aft[1])<<1) + (bits_bef[2] ^ bits_aft[2]))
    
    # build nonce state and compute before Chi
    nonceState = bytearray(16) + bytearray(trace_parameters['nonce'].astype(np.uint8)) + bytearray(48-16-len(trace_parameters['nonce']))
    nonceState = (np.frombuffer(bytes(nonceState), dtype=np.uint32) ^ np.frombuffer(padd, dtype=np.uint32)).tobytes()
    nonceBeforeChi = first_round_linear_layer_with_iota(nonceState)
    m0,m1,m2 = getColumn(nonceBeforeChi,x,z)
    bits_aft = chi3(m0^k0,m1^k1,m2^k2)
    bits_bef = []
    bits_bef.append(fk0)
    (xa,ya,za) = rho_east_p(x,1,z)
    bits_bef.append(getBit_s(nonceState,xa,ya,za))      
    (xa,ya,za) = rho_east_p(x,2,z)              
    bits_bef.append(getBit_s(nonceState,xa,ya,za))
    return ((bits_bef[0] ^ bits_aft[0])<<2) + ((bits_bef[1] ^ bits_aft[1])<<1) + (bits_bef[2] ^ bits_aft[2])

def select_subkey(i, key):
    # return the subkey 
    x,z = i//32, i%32
    # build key state and compute before Chi
    keyInit = bytearray(48)
    # put the key
    for j, v in enumerate(key):
        keyInit[j] ^= v
    keyBeforeChi = first_round_linear_layer(keyInit)
    ck0,ck1,ck2 = getColumn(keyBeforeChi,x,z)
    return (getBit_s(keyInit,x,0,z)<<3) ^ (ck2<<2) ^ (ck1<<1) ^ ck0


################################################
## Chi output without HD
################################################


def intermediate_value_chi(keyguess, trace_parameters):
    # Does it make sense to have 'nonceState' and 'nonceBeforeChi' inside trace_parameters?
    x,z = trace_parameters['subkey']//32, trace_parameters['subkey']%32
    ## target column is defined by the coordinates of the plane (x,z), with x index of the lane and z index of the of the bit in the lane
    # fk0 = (keyguess>>3)&1 # this is the fixed key
    k0 = keyguess & 1 # this is before chi
    k1 = (keyguess>>1)&1
    k2 = (keyguess>>2)&1

    if isinstance(trace_parameters['nonce'], np.ndarray) or isinstance(trace_parameters['nonce'], torch.Tensor):
        if len(trace_parameters['nonce'].shape) > 1:
            # fk0 = fk0.numpy()
            k0 = k0.numpy()
            k1 = k1.numpy()
            k2 = k2.numpy()
            n_nonces = trace_parameters['nonce'].shape[0]
            assert trace_parameters['nonce'].shape[1] == 16
            nonceState = np.hstack((np.zeros((n_nonces,16), dtype=np.uint8), trace_parameters['nonce'], np.zeros((n_nonces,48-16-trace_parameters['nonce'].shape[1]), dtype=np.uint8)))
            nonceState ^= np.frombuffer(padd, dtype=np.uint8)
            nonceState = np.frombuffer(bytes(nonceState), dtype=np.uint32).reshape((n_nonces,12))
            nonceBeforeChi = nonceState.copy()
            nonceBeforeChi = np_first_round_linear_layer_with_iota(nonceBeforeChi)
            m0, m1, m2 = getBitlane(nonceBeforeChi,x,0,z), getBitlane(nonceBeforeChi,x,1,z), getBitlane(nonceBeforeChi,x,2,z)
            bits_aft = chi3(m0^k0,m1^k1,m2^k2)
            # bits_bef = []
            # bits_bef.append(fk0)
            # (xa,ya,za) = rho_east_p(x,1,z)
            # bits_bef.append(getBitlane(nonceState,xa,ya,za))      
            # (xa,ya,za) = rho_east_p(x,2,z)              
            # bits_bef.append(getBitlane(nonceState,xa,ya,za))
            # return torch.ByteTensor((bits_bef[0] ^ bits_aft[0]) + (bits_bef[1] ^ bits_aft[1]) + (bits_bef[2] ^ bits_aft[2]))
            return torch.ByteTensor((bits_aft[0]) + (bits_aft[1]) + (bits_aft[2]))
    
    # build nonce state and compute before Chi
    assert len(bytearray(trace_parameters['nonce'].astype(np.uint8))) == 16
    nonceState = bytearray(16) + bytearray(trace_parameters['nonce'].astype(np.uint8)) + bytearray(48-16-len(trace_parameters['nonce']))
    nonceState = (np.frombuffer(bytes(nonceState), dtype=np.uint32) ^ np.frombuffer(padd, dtype=np.uint32)).tobytes()
    nonceBeforeChi = first_round_linear_layer_with_iota(nonceState)
    m0,m1,m2 = getColumn(nonceBeforeChi,x,z)
    bits_aft = chi3(m0^k0,m1^k1,m2^k2)
    # bits_bef = []
    # bits_bef.append(fk0)
    # (xa,ya,za) = rho_east_p(x,1,z)
    # bits_bef.append(getBit_s(nonceState,xa,ya,za))      
    # (xa,ya,za) = rho_east_p(x,2,z)              
    # bits_bef.append(getBit_s(nonceState,xa,ya,za))
    # return (bits_bef[0] ^ bits_aft[0]) + (bits_bef[1] ^ bits_aft[1]) + (bits_bef[2] ^ bits_aft[2])
    return (bits_aft[0]) + (bits_aft[1]) + (bits_aft[2])

def select_subkey_chi(i, key):
    # return the subkey 
    x,z = i//32, i%32
    # build key state and compute before Chi
    keyInit = bytearray(48)
    # put the key
    for j, v in enumerate(key):
        keyInit[j] ^= v
    keyBeforeChi = first_round_linear_layer(keyInit)
    ck0,ck1,ck2 = getColumn(keyBeforeChi,x,z)
    return (ck2<<2) ^ (ck1<<1) ^ ck0#(getBit_s(keyInit,x,0,z)<<3) ^ 