# My Git Implementation

A Python-based implementation of a subset of Git's core functionality. This project recreates fundamental Git operations including repository initialization, staging, committing, branching, and more.

## About Git

Git is a distributed version control system designed to track changes in source code during software development. It allows multiple developers to work on a project simultaneously while maintaining a complete history of all changes. Git stores snapshots of your project at different points in time, enabling you to revert to previous states, compare changes, and merge contributions from different sources.

### Key Git Concepts

- **Repository**: A directory that Git tracks, containing your project files and Git's metadata (in the `.git` directory)
- **Staging Area (Index)**: A holding area for changes that will be included in the next commit
- **Commit**: A snapshot of your project at a specific point in time
- **Branch**: A pointer to a specific commit, allowing parallel development
- **Tag**: A named reference to a specific commit, typically used for releases
- **HEAD**: A reference to the current commit/branch you're working on

## Installation

Clone this repository and make the `my_git` executable:

```bash
git clone <repository-url>
cd my_git
chmod +x my_git
```

## Available Commands

### 1. `init` - Initialize a Repository

**Syntax**: `./my_git init [directory]`

**Description**: Creates a new Git repository in the specified directory (or current directory if not specified).

**Example**:
```bash
$ ./my_git init my_project
```

**Effect on Repository**:
Creates a `.git` directory with the following structure:
```
.git/
├── HEAD              # Points to current branch (refs/heads/master)
├── config            # Repository configuration
├── description       # Repository description
├── branches/         # Directory for branches (legacy)
├── objects/          # Stores all Git objects (blobs, trees, commits)
└── refs/
    ├── heads/        # Branch references
    └── tags/         # Tag references
```

**Sample Output**:
```
(No output on success - repository is created silently)
```

---

### 2. `add` - Stage Files

**Syntax**: `./my_git add <file>...`

**Description**: Adds file contents to the staging area (index), preparing them for the next commit.

**Example**:
```bash
$ echo "Hello World" > file1.txt
$ ./my_git add file1.txt
```

**Effect on Repository**:
- Creates a blob object in `.git/objects/` containing the file's contents
- Updates the index file (`.git/index`) with the file's metadata and blob SHA

**Sample Session**:
```bash
$ echo "Hello World" > file1.txt
$ echo "Test file" > file2.txt
$ ./my_git add file1.txt file2.txt
$ ./my_git ls-files
file2.txt
file1.txt
```

---

### 3. `commit` - Record Changes

**Syntax**: `./my_git commit -m "message"`

**Description**: Creates a commit object that captures the current state of all staged files.

**Example**:
```bash
$ ./my_git commit -m "Initial commit"
```

**Effect on Repository**:
- Creates tree objects representing the directory structure
- Creates a commit object with metadata (author, timestamp, message, parent)
- Updates the current branch reference in `.git/refs/heads/`
- All objects are stored in `.git/objects/`

**Sample Session**:
```bash
$ ./my_git add file1.txt file2.txt
$ ./my_git commit -m "Initial commit"
$ ./my_git log
digraph wyaglog{
  node[shape=rect]
  c_d602cdc9f7f04367c096c4308a1c3f67953f495a [label="d602cdc: Initial commit"]
}
```

 (If you don’t know how to use Graphviz, just paste the raw output into <a href="https://dreampuf.github.io/GraphvizOnline/">this site</a>. If the link is dead, lookup “graphviz online” in your search engine)

---

### 4. `status` - Show Working Tree Status

**Syntax**: `./my_git status`

**Description**: Displays the state of the working directory and staging area, showing which files are modified, staged, or untracked. Detects if there are no commits yet and displays appropriate messages.

**Example**:
```bash
$ ./my_git status
```

**Sample Output** (before first commit):
```
On branch main.
No commits yet

Changes to be committed:
  new file: file1.txt

Changes not staged for commit:

Untracked files:
```

**Sample Output** (after commits exist):
```
On branch main.
Changes to be committed:
  added:    file2.txt

Changes not staged for commit:
  modified: file1.txt

Untracked files:
  file3.txt
```

**Status Indicators**:
- **No commits yet**: Shown when repository has no commits (initial state)
- **new file**: File being added in initial commit
- **added**: File being added to an existing repository
- **modified**: File has been changed and staged
- **deleted**: File has been removed and staged
- **Changes not staged for commit**: Modified tracked files not yet staged
- **Untracked files**: Files not tracked by Git (unless in .gitignore)

---

### 5. `ls-files` - List Staged Files

**Syntax**: `./my_git ls-files [--verbose]`

**Description**: Lists all files currently in the staging area (index).

**Example**:
```bash
$ ./my_git ls-files
$ ./my_git ls-files --verbose
```

**Sample Output** (basic):
```
file2.txt
file1.txt
```

**Sample Output** (verbose):
```
Index file format v2, containing 2 entries.
file2.txt
  regular file with perms: 644
  on blob: 524acfffa760fd0b8c1de7cf001f8dd348b399d8
  created: 2026-01-07 05:55:51.15429455, modified: 2026-01-07 05:55:51.15429455
  device: 2080, inode: 370936
  user: punit (1000)  group: punit (1000)
  flags: stage=0 assume_valid=False
file1.txt
  regular file with perms: 644
  on blob: 557db03de997c86a4a028e1ebd3a1ceb225be238
  created: 2026-01-07 05:55:51.15429455, modified: 2026-01-07 05:55:51.15429455
  device: 2080, inode: 370935
  user: punit (1000)  group: punit (1000)
  flags: stage=0 assume_valid=False
```

---

### 6. `rm` - Remove Files

**Syntax**: `./my_git rm <file>...`

**Description**: Removes files from both the working directory and the staging area.

**Example**:
```bash
$ ./my_git rm file3.txt
```

**Effect on Repository**:
- Removes the file from the working directory
- Removes the file entry from the index
- The file will not be included in future commits

**Sample Session**:
```bash
$ ./my_git ls-files
file2.txt
.gitignore
file3.txt
file1.txt
$ ./my_git rm file3.txt
$ ./my_git ls-files
file2.txt
.gitignore
file1.txt
```

---

### 7. `log` - Display Commit History

**Syntax**: `./my_git log [commit]`

**Description**: Shows the commit history starting from the specified commit (or HEAD if not specified). Output is in GraphViz DOT format.

**Example**:
```bash
$ ./my_git log
$ ./my_git log HEAD
```

**Sample Output**:
```
digraph wyaglog{
  node[shape=rect]
  c_d602cdc9f7f04367c096c4308a1c3f67953f495a [label="d602cdc: Initial commit"]
}
```

The output can be visualized using GraphViz tools to show the commit graph (If you don’t know how to use Graphviz, just paste the raw output into <a href="https://dreampuf.github.io/GraphvizOnline/">this site</a>. If the link is dead, lookup “graphviz online” in your search engine)

---

### 8. `hash-object` - Compute Object Hash

**Syntax**: `./my_git hash-object [-w] [-t type] <file>`

**Description**: Computes the SHA-1 hash of a file's contents. With `-w`, also writes the object to the repository.

**Options**:
- `-t type`: Specify object type (blob, commit, tree, tag) - default: blob
- `-w`: Write the object to the database

**Example**:
```bash
$ ./my_git hash-object -w file3.txt
ea450f959b935cbf0fb1dc902981ae819386b84d
```

**Effect on Repository**:
When `-w` is used, creates an object file at `.git/objects/ea/450f959b935cbf0fb1dc902981ae819386b84d`

---

### 9. `cat-file` - Display Object Contents

**Syntax**: `./my_git cat-file <type> <object>`

**Description**: Displays the contents of a Git object (blob, commit, tree, or tag).

**Example**:
```bash
$ ./my_git cat-file blob ea450f959b935cbf0fb1dc902981ae819386b84d
New file
```

**Sample Session**:
```bash
$ ./my_git hash-object -w file3.txt
ea450f959b935cbf0fb1dc902981ae819386b84d
$ ./my_git cat-file blob ea450f959b935cbf0fb1dc902981ae819386b84d
New file
```

---

### 10. `ls-tree` - List Tree Contents

**Syntax**: `./my_git ls-tree [-r] <tree-ish>`

**Description**: Lists the contents of a tree object. Use `-r` to recurse into subdirectories.

**Example**:
```bash
$ ./my_git ls-tree HEAD
100644 blob 557db03de997c86a4a028e1ebd3a1ceb225be238    file1.txt
100644 blob 524acfffa760fd0b8c1de7cf001f8dd348b399d8    file2.txt
```

This shows the file mode, type, SHA, and path for each entry in the tree.

---

### 11. `checkout` - Checkout a Commit

**Syntax**: `./my_git checkout <commit> <directory>`

**Description**: Checks out a commit or tree into an empty directory, recreating the files as they existed at that commit.

**Example**:
```bash
$ mkdir /tmp/checkout_test
$ ./my_git checkout HEAD /tmp/checkout_test
$ ls /tmp/checkout_test
file1.txt  file2.txt
```

**Effect**:
Recreates all files from the specified commit in the target directory. The directory must be empty or non-existent.

---

### 12. `tag` - Manage Tags

**Syntax**: 
- `./my_git tag` - List all tags
- `./my_git tag <name> [object]` - Create a lightweight tag

**Description**: Creates, lists, or deletes tags. Tags are references to specific commits, typically used to mark releases.

**Examples**:
```bash
$ ./my_git tag v1.0
$ ./my_git tag
v1.0
```

**Effect on Repository**:
Creates a file at `.git/refs/tags/v1.0` containing the commit SHA.

---

### 13. `show-ref` - List References

**Syntax**: `./my_git show-ref`

**Description**: Lists all references (branches and tags) with their commit SHAs.

**Sample Output**:
```
d602cdc9f7f04367c096c4308a1c3f67953f495a refs/heads/master
```

---

### 14. `rev-parse` - Parse Revision

**Syntax**: `./my_git rev-parse [--wyag-type=<type>] <name>`

**Description**: Resolves a reference name (like HEAD, branch name, tag name) to its SHA-1 hash.

**Example**:
```bash
$ ./my_git rev-parse HEAD
d602cdc9f7f04367c096c4308a1c3f67953f495a
```

---

### 15. `check-ignore` - Check Ignore Rules

**Syntax**: `./my_git check-ignore <path>...`

**Description**: Checks if paths are ignored by `.gitignore` rules. Prints paths that match ignore patterns.

**Example**:
```bash
$ echo "*.log" > .gitignore
$ ./my_git add .gitignore
$ echo "test" > test.log
$ ./my_git check-ignore test.log file3.txt
test.log
```

**Note**: The `.gitignore` file must be staged or committed for the rules to take effect.

---

## Complete Example Workflow

Here's a complete example demonstrating a typical Git workflow:

```bash
# Initialize a new repository
$ cd /tmp
$ mkdir my_project
$ cd my_project
$ /path/to/my_git init .

# Create some files
$ echo "# My Project" > README.md
$ echo "print('Hello World')" > main.py

# Stage the files
$ /path/to/my_git add README.md main.py

# Check status (before first commit)
$ /path/to/my_git status
On branch main.
No commits yet

Changes to be committed:
  new file: README.md
  new file: main.py

Changes not staged for commit:

Untracked files:

# List staged files
$ /path/to/my_git ls-files
main.py
README.md

# Commit the changes
$ /path/to/my_git commit -m "Initial commit with README and main.py"

# View commit history
$ /path/to/my_git log
digraph wyaglog{
  node[shape=rect]
  c_a1b2c3d4... [label="a1b2c3d: Initial commit with README and main.py"]
}

# Create a tag
$ /path/to/my_git tag v0.1

# Modify a file
$ echo "print('Updated')" >> main.py

# Check status to see changes (after commits exist)
$ /path/to/my_git status
On branch main.
Changes to be committed:

Changes not staged for commit:
  modified: main.py

Untracked files:

# Stage and commit the change
$ /path/to/my_git add main.py
$ /path/to/my_git commit -m "Update main.py"

```

## Implementation Details

### Git Objects

This implementation handles four types of Git objects:

1. **Blob**: Stores file contents
2. **Tree**: Represents directory structure (lists of blobs and other trees)
3. **Commit**: Snapshot with metadata (author, message, parent, tree)
4. **Tag**: Named reference to a commit

All objects are stored in `.git/objects/` using SHA-1 hashing and zlib compression.

### Index File

The index (`.git/index`) stores information about staged files including:
- File path
- File permissions and mode
- SHA-1 hash of file contents
- File metadata (timestamps, device, inode, user, group)
- Staging flags

### File Structure

```
project/
├── .git/
│   ├── HEAD                    # Current branch reference
│   ├── config                  # Repository configuration
│   ├── description             # Repository description
│   ├── index                   # Staging area
│   ├── objects/                # Object database
│   │   ├── 55/
│   │   │   └── 7db03de997c86a4a028e1ebd3a1ceb225be238
│   │   └── ...
│   └── refs/
│       ├── heads/              # Branch references
│       │   └── master
│       └── tags/               # Tag references
│           └── v1.0
└── [project files]
```

## Limitations

This implementation includes a subset of Git's functionality:

- No remote repository support (fetch, pull, push)
- No merge functionality
- No branch switching
- No rebase or cherry-pick
- No submodules

## Technical Requirements

- Python 3.10+ (uses match/case statements)
- Standard library only (no external dependencies)

## Module Structure

- `git_main.py` - Main entry point and command handlers
- `git_objects.py` - Git object classes (Repository, Blob, Tree, Commit, Tag)
- `git_utilities.py` - Repository utility functions
- `git_object_helper.py` - Object read/write operations
- `git_index_helper.py` - Index file operations
- `git_add_rm.py` - Add and remove operations
- `git_commit_helper.py` - Commit creation
- `git_status_helper.py` - Status and diff operations
- `git_tree_helper.py` - Tree object operations
- `git_ref_helper.py` - Reference management
- `git_gitignore_helper.py` - Gitignore pattern matching

