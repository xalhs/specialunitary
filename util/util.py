from main import N

global up
up = [1]
global empty
empty = [0]
basic_label = [1]
for i in range(N-1):
    up.append(0)
    empty.append(0)
    basic_label.append(0)
basic_label.pop()


def content_to_label(content):
    label = empty.copy()
    content = list(content)
    for i in range(N):
        label[-(i+1)] = content[-(i+1)]
        for j in range(len(content)):
            content[j]-= content[-(i+1)]
    label.pop()
    return label

def label_to_content(label):
    content = [0 for x in range(N)]
    for i, num in enumerate(label):
        for j in range(i+1):
            content[j] += num

    return tuple(content)
