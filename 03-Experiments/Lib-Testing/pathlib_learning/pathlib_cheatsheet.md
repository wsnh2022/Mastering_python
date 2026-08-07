# Python pathlib Complete Reference

Running example used in most snippets below:

```python
from pathlib import Path

p = Path("/home/user/reports/summary.tar.gz")
```

## Quick Index

| Tier | Methods |
|---|---|
| **Beginner** | `Path()`, `cwd()`, `home()`, `/`, `joinpath()`, `exists()`, `is_file()`, `is_dir()`, `is_absolute()`, `mkdir()`, `touch()`, `read_text()`, `write_text()`, `read_bytes()`, `write_bytes()`, `open()`, `as_posix()`, `name`, `stem`, `suffix`, `suffixes`, `parent` |
| **Intermediate** | `iterdir()`, `glob()`, `rglob()`, `rename()`, `replace()`, `unlink()`, `rmdir()`, `is_relative_to()`, `is_symlink()`, `is_mount()`, `stat()`, `with_suffix()`, `with_name()`, `with_stem()`, `parents`, `parts`, `root`, `anchor`, `drive` |
| **Advanced** | `walk()`, `relative_to()`, `resolve()`, `absolute()`, `expanduser()`, `samefile()`, `symlink_to()`, `hardlink_to()`, `readlink()`, `chmod()`, `lchmod()`, `lstat()`, `owner()`, `group()`, `as_uri()`, `match()`, `full_match()` |
| **Niche / version-specific** | `is_socket()`, `is_fifo()`, `is_block_device()`, `is_char_device()`, `is_junction()` (3.12, Windows), `Path.from_uri()` (3.13), `with_segments()` (3.12, subclassing), `unlink(missing_ok=True)`, `glob(case_sensitive=True)` (3.13) |

---

## Beginner

### `Path(*parts)`
Builds a path from string segments. Returns `PosixPath` on Linux/Mac, `WindowsPath` on Windows.
```python
p = Path("data", "file.txt")  # PosixPath('data/file.txt')
```

### `Path.cwd()`
Current working directory as a `Path`.
```python
Path.cwd()  # PosixPath('/home/user/project')
```

### `Path.home()`
The user's home directory.
```python
Path.home()  # PosixPath('/home/user')
```

### `/` (slash operator)
Joins path segments. Cleanest way to build paths.
```python
Path("/home/user") / "reports" / "summary.txt"
```

### `joinpath()`
Same as `/` but as an explicit method, useful when joining a variable number of segments.
```python
Path("/home/user").joinpath("reports", "summary.txt")
```

### `exists()`
Checks if the path exists on disk (file or directory).
```python
p.exists()  # True / False
```

### `is_file()`
True only if it exists and is a regular file.
```python
p.is_file()
```

### `is_dir()`
True only if it exists and is a directory.
```python
p.is_dir()
```

### `is_absolute()`
True if the path is fully specified from the filesystem root.
```python
Path("report.txt").is_absolute()  # False
Path("/tmp/report.txt").is_absolute()  # True
```

### `mkdir()`
Creates a directory. Use `parents=True` to create missing parent dirs, `exist_ok=True` to not error if it already exists.
```python
Path("a/b/c").mkdir(parents=True, exist_ok=True)
```

### `touch()`
Creates an empty file (or updates its modified time if it exists).
```python
Path("notes.txt").touch()
```

### `read_text()`
Reads the whole file as a string.
```python
content = Path("notes.txt").read_text(encoding="utf-8")
```

### `write_text()`
Writes a string to a file, overwriting it.
```python
Path("notes.txt").write_text("hello world")
```

### `read_bytes()`
Reads the whole file as raw bytes.
```python
data = Path("image.png").read_bytes()
```

### `write_bytes()`
Writes raw bytes to a file.
```python
Path("image.png").write_bytes(data)
```

### `open()`
Opens the file like the builtin `open()`, but as a method on the path.
```python
with p.open("r") as f:
    lines = f.readlines()
```

### `as_posix()`
Returns the path as a string with forward slashes, regardless of OS.
```python
Path(r"C:\Users\yogi").as_posix()  # 'C:/Users/yogi'
```

### `name`
The final path component, including extension.
```python
p.name  # 'summary.tar.gz'
```

### `stem`
The final component *without* its last suffix.
```python
p.stem  # 'summary.tar'
```

### `suffix`
The last file extension only.
```python
p.suffix  # '.gz'
```

### `suffixes`
All extensions as a list, for multi-part extensions.
```python
p.suffixes  # ['.tar', '.gz']
```

### `parent`
The immediate containing directory, as a `Path`.
```python
p.parent  # PosixPath('/home/user/reports')
```

---

## Intermediate

### `iterdir()`
Yields all direct children of a directory (non-recursive).
```python
for item in Path(".").iterdir():
    print(item)
```

### `glob()`
Yields paths matching a shell-style pattern, one directory level at a time unless `**` is used.
```python
list(Path(".").glob("*.py"))
list(Path(".").glob("**/*.py"))  # recursive
```

### `rglob()`
Shortcut for `glob("**/" + pattern)` — recursive by default.
```python
list(Path(".").rglob("*.py"))
```

### `rename()`
Renames/moves the file to a new path. Overwrites silently on some platforms — use carefully.
```python
Path("old.txt").rename("new.txt")
```

### `replace()`
Like `rename()`, but guaranteed atomic overwrite if the target exists (cross-platform safe version).
```python
Path("old.txt").replace("new.txt")
```

### `unlink()`
Deletes a file. Raises `FileNotFoundError` if missing, unless `missing_ok=True`.
```python
Path("temp.txt").unlink(missing_ok=True)
```

### `rmdir()`
Removes an *empty* directory. Use `shutil.rmtree()` for non-empty ones.
```python
Path("empty_folder").rmdir()
```

### `is_relative_to()`
Checks if a path is nested under another path.
```python
Path("/home/user/reports").is_relative_to("/home/user")  # True
```

### `is_symlink()`
True if the path is a symbolic link.
```python
p.is_symlink()
```

### `is_mount()`
True if the path is a mount point (a drive or network share root).
```python
Path("/").is_mount()  # True
```

### `stat()`
Returns filesystem metadata: size, timestamps, permissions.
```python
info = p.stat()
info.st_size  # size in bytes
info.st_mtime  # last modified time
```

### `with_suffix()`
New path with the extension replaced.
```python
p.with_suffix(".zip")  # .../summary.tar.zip
```

### `with_name()`
New path with the entire final component replaced.
```python
p.with_name("backup.zip")  # .../reports/backup.zip
```

### `with_stem()`
New path with just the stem replaced, extension kept.
```python
p.with_stem("archive")  # .../archive.gz
```

### `parents`
Sequence of ancestor directories, closest first.
```python
p.parents[0]  # .../reports
p.parents[1]  # .../user
```

### `parts`
All path components as a tuple of strings.
```python
p.parts  # ('/', 'home', 'user', 'reports', 'summary.tar.gz')
```

### `root`
The root portion of the path (e.g. `/` on Linux).
```python
p.root  # '/'
```

### `anchor`
The concatenation of drive and root — the non-negotiable start of the path.
```python
p.anchor  # '/'
```

### `drive`
The drive letter, on Windows (empty string on Posix).
```python
Path(r"C:\Users").drive  # 'C:'
```

---

## Advanced

### `walk()`
Generator equivalent of `os.walk()`, yields `(dirpath, dirnames, filenames)` at every level. Added in 3.12.
```python
for dirpath, dirnames, filenames in Path(".").walk():
    print(dirpath, filenames)
```

### `relative_to()`
Computes the relative path from one path to another. `walk_up=True` (3.12+) allows `..` segments.
```python
Path("/a/b/c").relative_to("/a")  # b/c
Path("/a/b").relative_to("/a/c", walk_up=True)  # ../b
```

### `resolve()`
Makes the path absolute, resolving symlinks and `..`/`.` segments.
```python
Path("../reports").resolve()
```

### `absolute()`
Makes the path absolute by prepending cwd — does NOT resolve symlinks or normalize `..`.
```python
Path("reports").absolute()
```

### `expanduser()`
Expands a leading `~` to the home directory.
```python
Path("~/notes.txt").expanduser()
```

### `samefile()`
True if two paths point to the same file on disk (even via different routes/symlinks).
```python
Path("a.txt").samefile("b.txt")
```

### `symlink_to()`
Makes this path a symbolic link pointing to a target.
```python
Path("shortcut").symlink_to("/real/target")
```

### `hardlink_to()`
Makes this path a hard link to a target (same inode, no "original vs link" distinction).
```python
Path("copy.txt").hardlink_to("original.txt")
```

### `readlink()`
Reads the target that a symlink points to, without following it.
```python
Path("shortcut").readlink()  # PosixPath('/real/target')
```

### `chmod()`
Changes permissions (Unix-style octal mode).
```python
p.chmod(0o644)
```

### `lchmod()`
Like `chmod()`, but changes the symlink itself, not its target.
```python
Path("shortcut").lchmod(0o644)
```

### `lstat()`
Like `stat()`, but doesn't follow symlinks — gives info about the link itself.
```python
Path("shortcut").lstat()
```

### `owner()`
Username of the file's owner (Unix only).
```python
p.owner()
```

### `group()`
Group name that owns the file (Unix only).
```python
p.group()
```

### `as_uri()`
Path as a `file://` URI. Requires an absolute path.
```python
Path("/etc/passwd").as_uri()  # 'file:///etc/passwd'
```

### `match()`
Tests the path against a glob-style pattern. Does NOT support `**`.
```python
p.match("*.gz")  # True
```

### `full_match()`
Like `match()`, but supports `**` for recursive patterns. Added in 3.13.
```python
p.full_match("**/*.gz")
```

---

## Niche / version-specific

### `is_socket()`
True if the path is a Unix domain socket.
```python
p.is_socket()
```

### `is_fifo()`
True if the path is a named pipe (FIFO).
```python
p.is_fifo()
```

### `is_block_device()` / `is_char_device()`
True for block/character device files (rare outside `/dev`).
```python
Path("/dev/sda").is_block_device()
```

### `is_junction()`
True if the path is a Windows junction point. Added in 3.12, Windows-only (always `False` elsewhere).
```python
p.is_junction()
```

### `Path.from_uri()`
Class method — builds a `Path` from a `file://` URI. Inverse of `as_uri()`. Added in 3.13.
```python
Path.from_uri("file:///etc/passwd")
```

### `with_segments()`
Internal hook used when subclassing `Path` to propagate custom data to derived paths (e.g. `parent`, `/`). Added in 3.12. Rarely called directly.
```python
class MyPath(Path):
    def with_segments(self, *segments):
        return super().with_segments(*segments)
```

### `unlink(missing_ok=True)`
Not a separate method — a parameter on `unlink()` that suppresses the error if the file doesn't exist.
```python
Path("maybe_missing.txt").unlink(missing_ok=True)
```

### `glob(case_sensitive=True)`
Not a separate method — a parameter added to `glob()`/`rglob()` in 3.13 for explicit case sensitivity control.
```python
list(Path(".").glob("*.TXT", case_sensitive=False))
```

---

## Notes on easily-confused pairs

- **`match()` vs `full_match()`** — `match()` can't handle `**`; `full_match()` can. Use `full_match()` for recursive pattern checks.
- **`resolve()` vs `absolute()`** — `absolute()` just prepends cwd; `resolve()` also follows symlinks and collapses `..`.
- **`stat()` vs `lstat()`** — `lstat()` reports on the symlink itself, not what it points to.
- **`rename()` vs `replace()`** — `replace()` guarantees an atomic overwrite across platforms; `rename()`'s overwrite behavior is platform-dependent.
- **`PurePath` vs `Path`** — attributes like `name`, `stem`, `parent`, `parts`, and methods like `match()` work without touching disk (defined on `PurePath`). Anything that hits the filesystem (`exists()`, `stat()`, `open()`, `iterdir()`, etc.) requires the concrete `Path`.
