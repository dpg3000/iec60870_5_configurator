def ioa_to_address(ioa):
    s = 0
    k = 0
    h = 0
    address = []
    while True:
        if ((256 * 256) * h + 256 * k + s) == ioa:
            address.append(h)
            address.append(k)
            address.append(s)
            break
        else:
            s = (s + 1) % 256
            if s == 0:
                k = (k + 1) % 256
                if k == 0:
                    h += 1 % 256

    return address


def update_address(address):
    address[2] += 1
    if address[2] == 256:
        address[2] = 0
        address[1] += 1
    if address[1] == 256:
        address[1] = 0
        address[0] += 1

    return address


def update_address_2(address):
    address[3] += 1
    if address[3] == 256:
        address[3] = 0
        address[2] += 1
    if address[2] == 256:
        address[2] = 0
        address[1] += 1
    if address[1] == 256:
        address[1] = 0
        address[0] += 1

    return address


def asdu_to_ioa(asdu):
    return asdu[1] * 256 + asdu[2]
