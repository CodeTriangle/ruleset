# Copyright (C) 2019-2020, CodeTriangle
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#       
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#       
#     * Neither the name of CodeTriangle nor the names of other
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL CODETRIANGLE BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.

import sys
import os
import hashlib
import datetime
import yaml

def smkdir(fn: str):
    """Make the directory `fn` if it does not exist already"""
    
    try:
        os.mkdir(fn)
        print("made directory {}".format(fn))
    except:
        print("directory {} already exists".format(fn))

def get_contents(fn: str) -> str:
    """Open the file `fn`; read and return its contents"""
    
    with open(fn) as f:
        return f.read()

def write_file(fn: str, tx: str):
    """Open the file `fn`; write `tx` to that file"""
    
    with open(fn, "w") as f:
        f.write(tx)

def try_get(d: dict, k):
    """Attempt to get item `k` of `d`; return None if doesn't exist"""

    try:
        return d[k]
    except KeyError:
        return None

def get_hash(tx: str) -> str:
    """Get the SHA1 hash of `tx` and return it as a string of hex digits"""
    
    return hashlib.sha1(bytes(str(tx), "utf8")).hexdigest()

def string_tablist(tx: str) -> dict:
    """Read TSV string, return dict {"col1": ["col2", "col3", ...]}"""

    # Maybe I should use the Python-provided CSV module for this?
    return {id: hash for id, hash in
        [[line.split("\t")[0], line.split("\t")[1:]] for line in tx.split("\n")]
    }

def tablist_string(dc: dict) -> str:
    """Performs `string_tablist()` in reverse"""
    
    return "\n".join(
        ["\t".join([line[0], *[str(i) for i in line[1]]]) for line in dc.items()]
    )

def to_int_list(ls: list) -> str:
    """Run through `ls`, turning all entries into `int` if possible"""
    
    result = []
    for i in ls:
        try: result.append(int(i))
        except ValueError: pass
    return result 

def better_date(dt: datetime.date) -> str:
    """Take a date and return it in a better form"""
    
    return dt.strftime("%d %b %Y")
