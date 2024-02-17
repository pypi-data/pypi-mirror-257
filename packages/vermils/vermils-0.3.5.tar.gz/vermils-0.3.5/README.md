# Vermils Magic Pocket 4 Python

## Installation

### Basic

```Bash
pip install vermils
```

### With HTTP support

Required by `vermils.io.puller`

```Bash
pip install vermils[http]
```

### With full support

```Bash
pip install vermils[all]
```

## Importing

```Python
import vermils
```

## Table of Contents

**Most of the codes are easy to understand or well documented, the documentation is only for the more complex ones.**

### `vermils.asynctools`

Tools for asynchronous programming.

- `sync_await`: Run async functions in a sync environment.
- `ensure_async`: Wraps a function/generator into an async function if it's a sync one.
- `to_async`: Wraps a function into an async function blindly.
- `to_async_gen`: Wraps a generator into an async generator blindly.
- `get_create_loop`: Get the current event loop or create a new one if there isn't one. Works in another thread, unlike `asyncio.`get_event_loop`.
- `async_run`: Run sync functions asynchronously in another thread without wrapping first.
- `AsinkRunner`: A class that runs sync functions asynchronously and sequentially in another thread.
- `select`: Similar to `select` in Go, supports both awaitables and async generators.

Documentation: [vermils.asynctools](./docs_old/asynctools.md)

### `vermils.collections`

Collections of useful classes.

- `fridge`: Make things immutable and hashable.
  - `FrozenDict`: A dict that is immutable and hashable.
  - `FrozenList`: A list that is immutable and hashable. Basically, a tuple but can be compared with lists.
  - `freeze`: Recursively freeze an object.
- `StrChain`: A simple way to create strings. Extremely useful.
- `ObjDict`: A dict that can be accessed like an object.

Documentation: [vermils.asynctools](./docs_old/collections.md)

### `vermils.gadgets`

Snippets of code that I am too lazy to categorize.

- `sidelogging.SideLogger`: Move any `LoggerLike` into another thread.
- `MonoLogger`: Log different levels of messages to different files.
- `stringify_keys`: Recursively convert all keys in a dict to strings.
- `supports_in`: Check if an object supports `in`.
- `mimics`: A decorator that makes a function mimic another function.
- `sort_class`: Sort class by inheritance, child classes first.
- `str_to_object`: Convert a string to an object.
- `real_dir`: Get the real directory of a file. Auto expands `~` and env vars.
- `real_path`: Get the real path of a file. Auto expands `~` and env vars.
- `version_cmp`: Compare two SemVer strings.
- `to_ordinal`: Convert an integer to its ordinal form.
- `selenium_cookies_to_jar`: Convert Selenium cookies to a `http.cookiejar.CookieJar` object.

Documentation: [vermils.gadgets](./docs_old/gadgets.md)

### `vermils.io`

Tools for I/O.

- `aio`: Async IO
  - `os`: Async version of some `os` functions.
    - `fsync`
    - `link`
    - `symlink`
    - `mkdir`
    - `makedirs`
    - `remove`
    - ... and more
  - `path`: Async version of some `os.path` functions
    - `exists`
    - `isdir`
    - `isfile`
    - `islink`
    - ... and more
- `puller`: A multithread async downloader module
  - `AsyncPuller`: A class that downloads files asynchronously.
  - `Modifier`: A class that modifies the behaviour of the puller, e.g show a progress bar.
- `DummyFileStream`: A dummy file stream that does nothing.
- `DummyAioFileStream`: A dummy async file stream that does nothing.

Documentation: [vermils.io](./docs_old/io.md)

### `vermils.react`

A simple event system.

- `ActionChain`: A chain of functions that can be executed in order or in parallel.
- `ActionCentipede`: The output of a function becomes the input of the next function.
- `EventHook`: A simple event hook, that binds events to chains of functions.

Documentation: [vermils.react](./docs_old/react.md)

### `vermils.tensorflow`

TensorFlow related tools.

- `inspect`
- `callbacks`
- `layers`
- `metrics`
- `models`

Documentation: [vermils.tensorflow](./docs_old/tensorflow.md)
