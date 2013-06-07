# states
#  hmj
#  ccc   scc   mcc  ^bcc^
#  ccs   scs   mcs   bcs 
#  ccm   scm   mcm   bcm 
#  csc   ssc   msc   bsc 
#  css   sss   mss   bss 
#  csm   ssm   msm   bsm 
#  cmc   smc   mmc   bmc 
#  cms   sms   mms   bms 
# $cmm$  smm   mmm   bmm 

hs = ['c', 's', 'm', 'b']
ms = ['c', 's', 'm']
js = ['c', 's', 'm']

allowed = [hs, ms, js]

def change_state(state, f, t):
    s = list(state)
    if len(s) != 3 or len(f) != 3 or len(t) != 3:
        return None

    for i in range(0, len(allowed)):
        if not (f[i] in allowed[i] or f[i] == '.'):
            return None
        if not (t[i] in allowed[i] or t[i] == '.'):
            return None
        if not s[i] in allowed[i]:
            return None
    
    for i in range(0, len(allowed)):
        if f[i] == '.' or s[i] == f[i]:
            if not t[i] == '.':
                s[i] = t[i]
        else:
            return None

    return ''.join(s)

def m_prepare_honey(s):
    return change_state(s, 'b..', 'm..')
    
def m_take_money(s):
    return change_state(s, '.s.', '.m.')
    
def m_give_honey(s):
    return change_state(s, 'm..', 's..')
    
def m_take_jar(s):
    return change_state(s, '..s', '..m')
    

def s_create_order(s):
    return change_state(s, 'bcc', '...')
    
def s_take_jar(s):
    return change_state(s, '..c', '..s')
    
def s_take_money(s):
    return change_state(s, '.c.', '.s.')
    
def s_give_jar(s):
    return change_state(s, '..s', '..m')
    
def s_give_money(s):
    return change_state(s, '.s.', '.m.')

def s_give_honey(s):
    return change_state(s, 's..', 'c..')
    

def set_state_tests():
    ss = ['ccc', 'ccc', 'bcc', 'cbc', '.',   '...',  '...', 'ccc']
    fs = ['...', '..c', 'bcc', '...', '...', '.',    '...', 'b..']
    ts = ['ccc', '..m', '...', '...', '...', '...',  '.',   'm..']
    rs = ['ccc', 'ccm', 'bcc', None,  None,  None,   None,  None]

    for i in zip(ss, fs, ts, rs):
        ns = change_state(i[0], i[1], i[2])
        if ns == i[3]:
            print str(i) + ' passed: ' + str(ns)
        else:
            print str(i) + ' failed: ' + str(ns)

    ms = [s_create_order, s_take_jar,
          m_prepare_honey, m_take_jar, m_give_honey,
          s_give_honey, s_take_money, s_give_money]

    print 'chain: ' + str(reduce(lambda acc, x: x(acc), ms, 'bcc'))

def run_tests():
    set_state_tests()

if __name__=="__main__":
    run_tests()
