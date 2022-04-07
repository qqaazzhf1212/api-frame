class AABB:

    cc = "hello"
    pass

# setattr,hasattr,getattr,delattr

setattr(AABB,"name","hello")
print(AABB.name)


print(AABB.__dict__)

values = dict(AABB.__dict__.items())
print(values)
for key,value in values.items():
    if key.startswith("__"):
        pass
    else:
        delattr(AABB,key)

print(AABB.__dict__)
