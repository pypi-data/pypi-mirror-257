def make_bloom(n_items=1_000_000, fp_rate=0.01, bloom_path="test.bloom", items_path="items.tuple"):
    from .containers import bloom_hash
    from pickle import dump
    from rbloom import Bloom
    from uuid import uuid4

    bloom = Bloom(n_items, fp_rate, bloom_hash)
    uuids = tuple(str(uuid4()) for _ in range(n_items))
    bloom.update(uuids)
    bloom.save(bloom_path)

    with open(items_path, "wb") as f:
        dump(uuids, f)


def test_bloom(iterations=1_000_000, make=True, bloom_path="test.bloom", items_path="items.tuple", **kwargs):
    from .containers import bloom_hash
    from rich import print
    from pickle import load
    from rbloom import Bloom
    from uuid import uuid4    
    
    if make:
        make_bloom(bloom_path=bloom_path, items_path=items_path, **kwargs)

    bloom = Bloom.load(bloom_path, bloom_hash)
    uuids = load(open(items_path, "rb"))
    
    uuid = str(uuid4())
    false_positives = 0
    for i in range(iterations):  # Adjust the number of iterations as needed
        if uuid in bloom:
            print(f"False positive found after {i} iterations")
            false_positives += 1
        # Generate a new random UUID for testing
        uuid = str(uuid4())

    print(f"All uuids in bloom: {all(uuid in bloom for uuid in uuids)}")
    print(f"false positive rate: {false_positives / iterations}")
    return bloom, uuids