Working with files in Python for humans
===

```python
# select all the files (done)
files = FileAlchemy('../something')
for f in files:
    print(f)

# filter fiels
files = FileAlchemy('../something').filter(
                extension='jpeg', # done
                created_at<=datetime(...),
                size>'10MB',
                modified_at<=datetime(...),
            )

# move files (done)
fiels = FileAlchemy('../something')
            .filter(
                extension='jpeg',
            ).move('../else')

# delete files (done)
fiels = FileAlchemy('../something').delete()
```
