#!/usr/bin/env python3
"""Join algorithms: nested loop, hash join, sort-merge join."""
import sys
from collections import defaultdict

def nested_loop_join(R,S,key_r,key_s):
    result=[]
    for r in R:
        for s in S:
            if r[key_r]==s[key_s]:result.append({**r,**s})
    return result

def hash_join(R,S,key_r,key_s):
    ht=defaultdict(list)
    for r in R:ht[r[key_r]].append(r)
    result=[]
    for s in S:
        for r in ht.get(s[key_s],[]):result.append({**r,**s})
    return result

def sort_merge_join(R,S,key_r,key_s):
    R=sorted(R,key=lambda x:x[key_r]);S=sorted(S,key=lambda x:x[key_s])
    result=[];i=j=0
    while i<len(R) and j<len(S):
        if R[i][key_r]==S[j][key_s]:
            jj=j
            while jj<len(S) and S[jj][key_s]==R[i][key_r]:
                result.append({**R[i],**S[jj]});jj+=1
            i+=1
        elif R[i][key_r]<S[j][key_s]:i+=1
        else:j+=1
    return result

def main():
    if len(sys.argv)>1 and sys.argv[1]=="--test":
        R=[{"id":1,"name":"Alice"},{"id":2,"name":"Bob"},{"id":3,"name":"Charlie"}]
        S=[{"uid":1,"order":"A1"},{"uid":1,"order":"A2"},{"uid":3,"order":"C1"}]
        for join_fn in [nested_loop_join,hash_join,sort_merge_join]:
            result=join_fn(R,S,"id","uid")
            assert len(result)==3,f"{join_fn.__name__}: got {len(result)}"
            names={r["name"] for r in result}
            assert names=={"Alice","Charlie"}
            alice_orders=[r["order"] for r in result if r["name"]=="Alice"]
            assert set(alice_orders)=={"A1","A2"}
        # Empty join
        for fn in [nested_loop_join,hash_join,sort_merge_join]:
            assert fn(R,[{"uid":99,"order":"X"}],"id","uid")==[]
        print("All tests passed!")
    else:
        R=[{"id":1,"n":"A"},{"id":2,"n":"B"}]
        S=[{"uid":1,"v":"x"},{"uid":2,"v":"y"}]
        print(f"Hash join: {hash_join(R,S,'id','uid')}")
if __name__=="__main__":main()
