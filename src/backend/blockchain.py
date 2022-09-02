# -*- coding: utf-8 -*-
#
# ./blockchain.py
#
# Simple blockchain implementation
#
import sys
import json
import hashlib
import memcache

from random import getrandbits
from time   import time

from config import cfg


class blockchain(object):

  cache  = memcache.Client([f'{cfg.memcached["host"]}:{cfg.memcached["port"]}'])
  memkey = 'blockchain'

  diff  = '42'
  chain = [{
    'index': 1,
    'timestamp': time(),
    'nonce': hex(getrandbits(32)),
    'difficult': '42',
    'size': 1,
    'transactions': [],
    'proof': 1,
    'previous_hash': 1
  }]
  transactions = []

  __def_structure_chain__ = {            # dont use, its for docs and understand
    'index': None,
    'timestamp': 0,
    'size': 0,
    'transactions': [{
      'timestamp': 0,
      'sender': 0,
      'recipient': 0,
      'amount': 0
    }],
    'proof': 10,
    'previous_hash': None
  }

  __def_structure_transaction__ = {      # dont use, its for docs and understand
    'timestamp': 0,
    'sender': 0,
    'recipient': 0,
    'amount': 0
  }

  __def_structure_block__ = {            # dont use, its for docs and understand
    'index': None,
    'timestamp': 0,
    'size': 0,
    'transactions': [],
    'proof': 10,
    'previous_hash': None
  }

  def __init__(self):
    result = self.cache.get(self.memkey)
    if result:
      self.diff = result['diff']
      self.chain = result['chain'].copy()
      self.transactions = result['transactions'].copy()
  #__init__

  def __del__(self):
    self.cache.set(self.memkey, {
      'diff': self.diff,
      'chain': self.chain,
      'transactions': self.transactions
    })
    self.cache.disconnect_all()

  def run_block(self):
    block = {
      'error': 'There aren\'t block for mining'
    }

    if len(self.transactions) > 0:
      block = {
        'index': len(self.chain) + 1,
        'timestamp': time(),
        'nonce': hex(getrandbits(32)),
        'difficult': self.get_diff(len(self.chain) + 1),
        'size': sys.getsizeof(self.transactions),
        'transactions': self.transactions.copy(),
        'proof': self.pow(),
        'previous_hash': self.get_previous_hash()
      }

      self.transactions.clear()
      self.chain.append(block)

    return block
  #runblock

  def run_transaction(self, sender, recipient, amount):
    self.transactions.append({
      'timestamp': time(),
      'sender': hex(sender),
      'recipient': hex(recipient),
      'amount': round(float(amount), 16)
    })

    return self.transactions[-1]
  #run_transaction

  def get_hash(self, block):
    return hashlib.sha256(
      json.dumps(block, sort_keys=True).encode()
    ).hexdigest()
  #get_hash

  def get_previous_hash(self):
    return self.get_hash(self.chain[-1])
  #get_previous_hash

  def get_last_block(self):
    return self.chain[-1]

  def get_diff(self, block_index):
    #every 100 block mine in the blockchain increment diff
    if block_index % 50 == 0:
      self.diff += self.diff

    return self.diff
  #get_diff

  def pow(self):
    """Proof Of Work"""
    hash, c_proof, lastblock = (None, 1, self.get_last_block())

    diff    = lastblock['difficult']
    nonce   = lastblock['nonce']
    p_proof = lastblock['proof']

    while hash is None:
      tstr = str(int(nonce, 16) - c_proof**2 - p_proof**2).encode()
      hash = hashlib.sha256(tstr).hexdigest()
      hash = hash if hash[-len(diff):] == diff else None

      c_proof += 1
    #endwhile

    return c_proof - 1
  #pow

  def verify_chain(self, chain):
    previous = chain.pop(0)

    while len(chain) > 0:
      current = chain.pop(0)

      if current['previous_hash'] != self.get_hash(previous):
        return False

      c_proof, p_proof, nonce, diff = (current['proof'], previous['proof'],
                                       previous['nonce'], previous['difficult'])

      tstr = str(int(nonce, 16) - c_proof**2 - p_proof**2).encode()
      hash = hashlib.sha256(tstr).hexdigest()

      if hash[-len(diff):] != diff:
        return False

      previous = current
    #endwhile

    return True
#blockhain
