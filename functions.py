from dms2dec.dms_convert import dms2dec
import datetime

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

def svcslist(svcs_tbl):
    """
    Processes services table into list of services
    :param svcs_tbl: table with service values
    :return: list of services
    """
    services = {
        "Agua": svcs_tbl.iloc[0][1],
        "Grúa": svcs_tbl.iloc[3][1],
        "Rampa": svcs_tbl.iloc[5][1],
        "Taller": svcs_tbl.iloc[6][1],
        "Muelle de espera": svcs_tbl.iloc[0][3],
        "Bar": svcs_tbl.iloc[1][3],
        "Restaurante": svcs_tbl.iloc[2][3],
        "Supermercado": svcs_tbl.iloc[3][3],
        "Farmacia": svcs_tbl.iloc[1][5],
        "Servicios de primeros auxilios": svcs_tbl.iloc[2][5],
        "Banco": svcs_tbl.iloc[4][5],
        "Alquiler de coches": svcs_tbl.iloc[5][5],
        "Información meteorológica": svcs_tbl.iloc[3][5]
    }
    svcs_items = services.items()
    svcs_list = []
    for key, value in svcs_items:
        if value == 'SI':
            svcs_list.append(key)
    return svcs_list

def yzrdict(name, region, image, boat_tbl, svcs_list, descr, linfo):
    """
    Creates dict from data
    :param name: portname
    :param region: region
    :param image: list of images
    :param boat_tbl: table with info regarding boats (eslora, amarres, etc)
    :param svcs_list: table with info regarding services (grua, agua, etc)
    :param descr: descripcion de puerto
    :param linfo: info auxiliar, dirección, etc
    :return:
    """
    yeezerdict = {
        "port_name": name,
        "region": region,
        # "lat": latlonli[0],
        # "lng": latlonli[1],
        "image_id": image,
        "features": {
            "mooring": ["Número de amarres", str(boat_tbl.iloc[2][1])],
            "length": ["Eslora máxima (mts)", str(boat_tbl.iloc[1][1])],
            "draft": ["Calado mínimo (mts)", str(boat_tbl.iloc[0][1])]
        },
        "services": svcs_list,
        "description": descr,
        "email": "admin@site.co",
        "url": linfo[0],
        "telephone": linfo[2],
        'creation_date': str(datetime.datetime.utcnow()),
        'last_updated': str(datetime.datetime.utcnow()),
        'created_by': 'admin',
        'status': 'up',
        'type': 'anchor'
    }
    return (yeezerdict)