from dms2dec.dms_convert import dms2dec


def funcpat(df):
    """
    (OLD)
    transform from deg,hours,minutes to decimal
    :param df: dataframe to take values from
    :return: dataframe with decimal values
    """
    pattern = r'(?P<d>[\d\.]+).*?(?P<m>[\d\.]+).*?(?P<s>[\d\.]+)'
    dms = df['lat'].str.extract(pattern).astype(float)
    df['lat'] = dms['d'] + dms['m'].div(60) + dms['s'].div(3600)

    # Similarly we do for the longitude
    dms = df['lon'].str.extract(pattern).astype(float)
    df['lon'] = dms['d'] + dms['m'].div(60) + dms['s'].div(3600)

    return df


def latlonconv(strlatlon):
    """
    convert latitude/longitude to decimal
    :param strlatlon: string to convert
    :return: converted value
    """
    strl = strlatlon.strip('\'')
    strl = strl.strip('L=')
    strl = strl.strip('l=')
    strl = strl.split(" ")

    lis_strl = []
    for x in strl:
        p2rn = dms2dec(x)
        lis_strl.append(p2rn)
    return lis_strl


def infotoinfo(info):
    """
    Converts info block from scraping to segments
    :param info: info block of text
    :return: list of info items (website, telephone, address)
    """
    splitst = info.split()
    list = []
    site = "n.d."
    for x in splitst:
        if "www" in x:
            site = "http://" + x
            list.append(site)
    if not list:
        list.append(site)

    splitstb = info.split("Telf:")
    splitstb[1] = splitstb[1].strip(site)
    list.append(splitstb[0])
    splitstb[0] = splitstb[0].strip("Telf.:")
    list.append(splitstb[1])
    return list

