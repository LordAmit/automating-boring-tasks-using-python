# Duplicate Image Finder

This duplicate image finder source code is inspired/partially copied from https://github.com/philipbl/duplicate-images.git.

Significant changes are:

1. moved from `mongodb` to `sqlite`
2. Is probably better in terms of finding similar images (or perhaps I misunderstood the previous code)

Concepts/Technologies I learned/tried to learn while doing this:

1. `poetry` for dependency
2. `pytest` for unit test
3. `pysqlite3` for database
4. `concurrency` for performance
5. `imagehash` for perpetual image hashing for finding similarity