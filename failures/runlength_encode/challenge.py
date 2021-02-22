"""
The problem:

runlength_encode("aabbbcaa") should return "2a3b1c2a"
"""
def runlength_encode(chars):
    chunks = []
    new_chunk = [chars[0]]

    for next_c in chars[1:]:
        last_c = new_chunk[-1]
        if next_c == last_c:
            new_chunk.append(next_c)
        else:
            chunks.append(new_chunk)
            new_chunk = [next_c]

    # Don't forget your last chunk
    chunks.append(new_chunk)

    encoded_str = ""
    for chunk in chunks:
        chunk_char = chunk[0]
        encoded_frag = "{}{}".format(len(chunk), chunk_char)
        encoded_str += encoded_frag

    return encoded_str


if __name__ == '__main__':
    encoded = runlength_encode("aabbbcaa")
    print(encoded)
    assert encoded == "2a3b1c2a"
