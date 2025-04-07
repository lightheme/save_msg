import sys


async def aenumerate(aiterable):
    i = 0
    async for x in aiterable:
        yield i, x
        i += 1

async def aislice(aiterable, start=0, stop=sys.maxsize, step=1):
    it = iter(range(start, stop, step))
    try:
        nexti = next(it)
    except StopIteration:
        return
    async for i, element in aenumerate(aiterable):
        if i == nexti:
            yield element
            try:
                nexti = next(it)
            except StopIteration:
                return