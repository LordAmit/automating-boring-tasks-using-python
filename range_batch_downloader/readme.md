##  Batch Download Link Script Generator for Links in Sequence
Lets say we have two example URLs

```
https://example.com/1.txt
...
https://example.com/100.txt
```

This will result in making download links:

```bash
python3 src.py --us <https://example.com/> --ue .txt --ns 1 --ne 100
```

Easy enough!
