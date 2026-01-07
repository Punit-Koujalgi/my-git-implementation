import os
import configparser

from git_utilities import *

class GitRepository (object):
    """A git repository"""

    def __init__(self, path, force=False):
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")

        if not (force or os.path.isdir(self.gitdir)):
            raise Exception(f"Not a Git repository {path}")

        # Read configuration file in .git/config
        self.conf = configparser.ConfigParser()
        cf = repo_file(self, "config")

        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Configuration file missing")

        if not force:
            vers = int(self.conf.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception(f"Unsupported repositoryformatversion: {vers}")

class GitObject (object):

    def __init__(self, data=None):
        if data != None:
            self.deserialize(data)
        else:
            self.init()

    def serialize(self, repo):
        """This function MUST be implemented by subclasses.

It must read the object's contents from self.data, a byte string, and
do whatever it takes to convert it into a meaningful representation.
What exactly that means depend on each subclass.

        """
        ...

    def deserialize(self, data):
        ...

    def init(self):
        pass # Just do nothing. This is a reasonable default!
    
class GitBlob(GitObject):
    fmt=b'blob'

    def serialize(self, repo):
        return self.blobdata

    def deserialize(self, data):
        self.blobdata = data


class GitCommit(GitObject):
    fmt=b'commit'

    def deserialize(self, data):
        self.kvlm = kvlm_parse(data)

    def serialize(self, repo):
        return kvlm_serialize(self.kvlm)

    def init(self):
        self.kvlm = dict()

class GitTreeLeaf (object):
    def __init__(self, mode, path, sha):
        self.mode = mode
        self.path = path
        self.sha = sha

class GitTree(GitObject):
    fmt=b'tree'

    def deserialize(self, data):
        from git_tree_helper import tree_parse
        self.items = tree_parse(data)

    def serialize(self, repo):
        from git_tree_helper import tree_serialize
        return tree_serialize(self)

    def init(self):
        self.items = list()
        
class GitTag(GitCommit):
    fmt = b'tag'
    
class GitIndexEntry (object):
    def __init__(self, ctime=None, mtime=None, dev=None, ino=None,
                 mode_type=None, mode_perms=None, uid=None, gid=None,
                 fsize=None, sha=None, flag_assume_valid=None,
                 flag_stage=None, name=None):
        # The last time a file's metadata changed.  This is a pair
        # (timestamp in seconds, nanoseconds)
        self.ctime = ctime
        # The last time a file's data changed.  This is a pair
        # (timestamp in seconds, nanoseconds)
        self.mtime = mtime
        # The ID of device containing this file
        self.dev = dev
        # The file's inode number
        self.ino = ino
        # The object type, either b1000 (regular), b1010 (symlink),
        # b1110 (gitlink).
        self.mode_type = mode_type
        # The object permissions, an integer.
        self.mode_perms = mode_perms
        # User ID of owner
        self.uid = uid
        # Group ID of ownner
        self.gid = gid
        # Size of this object, in bytes
        self.fsize = fsize
        # The object's SHA
        self.sha = sha
        self.flag_assume_valid = flag_assume_valid
        self.flag_stage = flag_stage
        # Name of the object (full path this time!)
        self.name = name

class GitIndex (object):
    version = None
    entries = []
    # ext = None
    # sha = None

    def __init__(self, version=2, entries=None):
        if not entries:
            entries = list()

        self.version = version
        self.entries = entries


class GitIgnore(object):
    absolute = None
    scoped = None

    def __init__(self, absolute, scoped):
        self.absolute = absolute
        self.scoped = scoped