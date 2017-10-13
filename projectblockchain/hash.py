## hash
import hashlib
import string
import random
import time

##hash
md5Hash=hashlib.md5()
md5Hash.update('this is sample hash')
#print md5Hash.hexdigest()
md5Hash.update('new hash')
#print md5Hash.hexdigest()
md5Hash.update('old hash')
#print md5Hash.hexdigest()

#hashcash
example_challenge='9jhfhshsusnskl34Y'

def generation(challenge=example_challenge, size=25):
    answer = ''.join(random.choice(string.ascii_lowercase+string.ascii_uppercase+string.digits) for x in range(size))
    #print challenge
    #print answer
    attemp = challenge + answer

    return attemp, answer

def testAttemp():
    Found=False
    start=time.time()
    while Found==False:
        attemp, answer = generation()
        shaHash.update(attemp)
        solution = shaHash.hexdigest()
        if solution.startswith('0000'):
            timetook=time.time()-start
            print solution
            print 'time took:', timetook
            Found=True

if __name__=='__main__':
    shaHash=hashlib.sha256()
    for x in xrange(0, 1000):
        testAttemp()
