import json, struct, os
import base64
import binascii
import time
import logging
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256, HMAC
from Crypto.Protocol.KDF import PBKDF2

logger = logging.getLogger(__name__)

# Default age of a signed token
DEFAULT_AGE=3600  # 1 hour

# give 60 seconds of grace on expiration/not-before times
DEFAULT_GRACE=60

GLOBAL_CONFIG = None

from functools import wraps
def aswt_for_gcf():
    if not is_key_set(): raise Exception("default key isn't set!")
    import flask
    def makewrapper(func):
        @wraps(func)
        def mywrapper(request):
            token = None
            try:
                tokentype,tokenraw = request.headers.get('Authorization').split(' ')
                if tokentype == "Bearer":
                    token = Token(tokenraw)
            except ValueError:
                logger.exception("error parsing token!")
                token = None
            return func(request,token)
        return mywrapper
    return makewrapper
def require_aswt_for_gcf(required_claims=None, authz=None):
    if not is_key_set(): raise Exception("default key isn't set!")
    import flask
    def makewrapper(func):
        @wraps(func)
        def mywrapper(request):
            token = None
            try:
                tokentype,tokenraw = request.headers.get('Authorization').split(' ')
                if tokentype == "Bearer":
                    token = Token.load(tokenraw)
            except ValueError:
                logger.exception("error parsing token!")
                token = None
            if token is None:
                return flask.abort(401)
            else:
                if required_claims is not None:
                    for claim in required_claims:
                        if claim not in token:
                            return "Unauthorized - Missing Claim %s"%(claim), 403
                if authz is not None:
                    if not authz(token):
                        return "Unauthorized - failed authz", 403
                return func(request,token)
        return mywrapper
    return makewrapper
def require_aswt_for_bottle(required_claims=None, authz=None):
    if not is_key_set(): raise Exception("default key isn't set!")
    import bottle
    def makewrapper(func):
        @wraps(func)
        def mywrapper(*args,**kwargs):
            token = None
            try:
                authheader = bottle.request.headers.get('Authorization')
                if authheader is not None:
                    tokentype,tokenraw = authheader.split(' ')
                    if tokentype == "Bearer":
                        token = Token.load(tokenraw)
            except ValueError:
                logger.exception("error parsing token!")
                token = None
            if token is None:
                return bottle.abort(401)
            else:
                if required_claims is not None:
                    for claim in required_claims:
                        if claim not in token:
                            bottle.abort(403,"Unauthorized - Missing Claim %s"%(claim))
                if authz is not None:
                    if not authz(token):
                        bottle.abort(403,"Unauthorized - failed authz")
                return func(*args,**kwargs)
        return mywrapper
    return makewrapper

def require_aswt_for_flask(token_sources, required_claims=None, authz=None, pass_token=False):
    import flask
    def makewrapper(func):
        @wraps(func)
        def mywrapper(*args,**kwargs):
            if not is_key_set(): raise Exception("default key isn't set!")
            token = None
            logger.info("checking for valid token")
            try:
                tokenraw = None
                for ts in token_sources:
                    tokenraw = ts()
                    if tokenraw is not None:
                        token = Token.load(tokenraw)
                        break
            except ValueError:
                logger.exception("error parsing token!")
                token = None
            if token is None:
                return flask.abort(401)
            else:
                if required_claims is not None:
                    for claim in required_claims:
                        if claim not in token:
                            return "Unauthorized - Missing Claim %s"%(claim), 403
                if authz is not None:
                    if not authz(token,**kwargs):
                        return "Unauthorized - failed authz", 403
                if pass_token:
                    kwargs = kwargs.copy()
                    kwargs['token'] = token
                return func(*args,**kwargs)
        return mywrapper
    return makewrapper

try:
    import flask

    def FlaskCookie(name):
        def get_cookie():
            return flask.request.cookies.get(name)
        return get_cookie

    def FlaskForm(name):
        def get_value():
            return flask.request.form.get(name)
        return get_value

    def FlaskAuthorization():
        def get_token():
            authheader = flask.request.headers.get('Authorization')
            if authheader is not None:
                tokentype,tokenraw = authheader.split(' ')
                if tokentype == "Bearer":
                    return tokenraw
            return None
        return get_token
except ImportError:
    logger.error("Couldn't load Flask module")

class HMACKey(object):
    digestmod = SHA256
    header = b"HS"
    def __init__(self, key, keyid, default_age=None):
        if isinstance(key,str): key = key.encode('utf-8')
        self.key = key
        self.id = keyid
        self.default_age = default_age

    def verify(self, mac, content):
        if len(mac) != (self.digestmod.digest_size*2):
            raise ValueError("digest not right length")

        h = HMAC.new(self.key, digestmod=self.digestmod)
        h.update(content)

        try:
            h.hexverify(mac) # this throws an error if the signature is wrong
        except:
            logger.exception("verify error on keyid %s",self.id)
            raise

    def sign(self, content):
        h = HMAC.new(self.key, digestmod=self.digestmod)
        h.update(content)
        return h.hexdigest()

        
class Token(object):
    MAX_STRING = 1024
    def __init__(self, tokenstring=None, key=None, age=None, notnew=False, grace=DEFAULT_GRACE):
        global GLOBAL_CONFIG
        self._dict = {}
        self.dirty = False

        if isinstance(key,HMACKey):
            self.key = key
        elif key is not None:
            self.key = GLOBAL_CONFIG['keys'][key]
        elif GLOBAL_CONFIG['default_key'] is not None:
            self.key = GLOBAL_CONFIG['default_key']
        else:
            self.key = None

        if tokenstring is not None:
            if len(tokenstring)>self.MAX_STRING:
                raise ValueError("token too long!")
            self._load(tokenstring,key,grace=grace)
        elif not notnew:
            # initialize a new token
            now = int(time.time())
            if age is None:
                if self.key is not None and self.key.default_age is not None:
                    age = self.key.default_age
                else:
                    age = DEFAULT_AGE
            if age is not None:
                self['exp'] = now+age
            self['nbf'] = now
        else:
            raise ValueError("token not passed! can't be None")

    @classmethod
    def load(cls, tokenstring, key=None, grace=DEFAULT_GRACE):
        return cls(tokenstring,key=key,notnew=True,grace=grace)

    def _load(self, tokenstring, key=None, grace=DEFAULT_GRACE):
        global GLOBAL_CONFIG
        if isinstance(tokenstring,str): tokenstring = tokenstring.encode('utf-8')
        header, keyid, digest, jsoncontent = tokenstring.split(b'.')
        while jsoncontent[-1] in b"\n \r\t":
            jsoncontent = jsoncontent[:-1]
        
        if header != b"HS":
            raise ValueError("incorrect header")
        
        keyid = keyid.decode('utf-8')
        if key is None:
            key = self.key
        if key is None or key.id != keyid:
            if keyid not in GLOBAL_CONFIG['keys']:
                raise KeyError("can't find keyid in keys!",keyid)
            key = GLOBAL_CONFIG['keys'][keyid]
        # note that we don't compare keyids when a key is manually specified

        if key is not None:
            key.verify(digest, jsoncontent)

        self._dict = json.loads(base64.b64decode(jsoncontent).decode('utf-8'))
        
        if 'exp' not in self or 'nbf' not in self:
            raise ValueError("must have an expiration and not before set in token")
        now = time.time()
        # give (by default) 60 seconds grace
        if (self['nbf']-grace) > now:
            raise ValueError("token not yet valid!")
        if (self['exp']+grace) < now:
            raise ValueError("token expired!")

    def dump(self, key=None):
        if key is None:
            key = self.key
        if key is None:
            raise ValueError("no key specified and no default key setup! Set ASWT_CONFIG environment variable")

        # encode our token
        # use of separators generates more compact JSON
        data = json.dumps(self._dict,separators=(',',':')).encode('utf-8')
        data = base64.b64encode(data)

        # now sign it
        hashfordata = key.sign(data)

        if '.' in key.id:
            raise ValueError("Key id can't contain a period!",key.id)

        #logger.debug("dumps - hashfordata = %s",h.hexdigest())
        data = b'HS.'+(key.id.encode('utf-8'))+b'.'+hashfordata.encode('utf-8')+b'.'+data

        return data

    def dumps(self,key=None):
        return self.dump(key).decode('utf-8')

    def __setitem__(self, name, value):
        # FIXME: we can't go dirty on changes in child objects because only
        # __getitem__ is called in those cases... :(
        if name in self._dict:
            oldvalue = self._dict[name]
            self._dict[name] = value
            # only mark dirty if we changed the value
            if value != oldvalue: self.dirty = True
        else:
            # it's a new value, we are dirty
            self.dirty = True
            self._dict[name] = value

    def __delitem__(self, name):
        del self._dict[name]
        self.dirty = True

    def __getitem__(self, name):
        return self._dict[name]

    def __contains__(self,name):
        return name in self._dict

    def items(self):
        return self._dict.items()

    def get(self, name, default=None):
        if name in self._dict: return self._dict[name]
        else: return default


# FINISHME
# 1. pull config/key location from environment
# 2. if gsutil URL, then go to google cloud storage for the file
# 3. Load keys into an array (or dict by keyid?) and automatically use with the wrappers above
def download_gcs_to_string(bucket,filename):
    global GOOGLE_CLOUD_STORAGE_CLIENT
    import google.cloud.storage
    GOOGLE_CLOUD_STORAGE_CLIENT = google.cloud.storage.Client()
    return GOOGLE_CLOUD_STORAGE_CLIENT.bucket(bucket).blob(filename).download_as_string()

def load_config(config=None):
    global GLOBAL_CONFIG
    GLOBAL_CONFIG = {'keys':{},'default_key':None}
    if config is not None:
        config = json.loads(config)

        keys = [HMACKey(key=binascii.unhexlify(keyconfig['key']), keyid=keyconfig['keyid'], default_age=(keyconfig['age'] if 'age' in keyconfig else None)) for keyconfig in config['keys']]
        for key in keys:
            GLOBAL_CONFIG['keys'][key.id] = key
        
        # choose a default key
        if 'default_key' in config and config['default_key'] in GLOBAL_CONFIG['keys']:
            GLOBAL_CONFIG['default_key'] = GLOBAL_CONFIG['keys'][config['default_key']]
        elif len(keys):
            GLOBAL_CONFIG['default_key'] = keys[0]

def get_config(configpath):
    if configpath is not None:
        if configpath.startswith("{"):
            # it's JSON, try to consume as config
            return configpath
        if configpath.startswith('gs://'):
            bucket, blob = configpath[5:].split('/',1)
            config = download_gcs_to_string(bucket,blob)
        else:
            with open(configpath,"r") as fo:
                config = fo.read()
        return config
    else:
        return None

def is_key_set():
    global GLOBAL_CONFIG
    return GLOBAL_CONFIG['default_key'] is not None

def reload_config():
    load_config(get_config(os.environ['ASWT_CONFIG'] if 'ASWT_CONFIG' in os.environ else None))
reload_config()

if __name__ == "__main__":
    import argparse, os.path, sys
    print(repr(sys.argv))
    parser = argparse.ArgumentParser()
    parser.add_argument('--new-key',action="store_true")
    parser.add_argument('--new-token',action="store_true")
    parser.add_argument("--keyid",default=None)
    parser.add_argument('--verify-token',action="store_true")
    parser.add_argument('--claim',action="append")
    parser.add_argument('--age',type=int,default=None)
    parser.add_argument('config_file',nargs='?')
    args = parser.parse_args()

    if args.config_file and os.path.exists(args.config_file):
        with open(args.config_file,"r") as fo:
            rawconfig = fo.read()
        config = json.loads(rawconfig)
    else:
        config = {'keys':[]}
        rawconfig = None
    dirty = False
    if args.new_key:
        keydata = new_key(args.age)
        # insert the new key at the beginning (so it becomes the default signing key)
        config['keys'].insert(0,keydata)
        dirty = True
    elif args.new_token:
        if rawconfig is None:
            raise ValueError("Missing config file with keys!")
        load_config(rawconfig)
        if GLOBAL_CONFIG['default_key'] is None:
            raise ValueError("No signing key found!")
        t = Token(key=args.keyid,age=args.age)
        for claim in args.claim:
            key,value = claim.split('=',1)
            key = key.strip()
            value = value.strip()
            if value[0:1] in ['[','{']:
                sys.stderr.write("converting %s to json\n"%(value))
                value = json.loads(value)
            t[key]=value
        print(t.dumps())
    elif args.verify_token:
        if rawconfig is None:
            raise ValueError("Missing config file with keys!")
        load_config(rawconfig)
        TOKEN = sys.stdin.read()
        t = Token.load(TOKEN)
        print("valid!")

    if dirty:
        print(json.dumps(config))
        with open(args.config_file,"w") as fobj:
            fobj.write(json.dumps(config))
            fobj.write("\n")
