import getpass
from typing import Any

from beni import bcache, bcrypto


@bcache.cache
async def getPypi() -> tuple[str, str]:
    content = 'pypi.org gAABl0ruN3xd3bOT6kGy-Zpb8liT7Qzan7jC3c9nR7mvmoaC3QVJuWl11-9vArCK8AQq_ML5_ghAnW7i2tSQ00W2DITy_eYzwaKLPHz42KSLp5vPkOOmAIWDSBIzVYizDgE1wkDL8TxAGjRvS4nWD1LVAgEC5PSrck4uLw5dDrfa-z_C0WZYaHLMLdmDQ0d060ac7bb8fc523AAAvPXGB2B8ZMT6qnk08ExNYHuYDwCxixIv1FEBRPEEV7q_cCZpYvplscWh1oUKDDFy1gqH0jjvFn7-Fai2y4MGO9Wz081CglHkT66H8MdHa027rc-vdvS-Guk2pIXgExlwtiAFHjQVJLler5pbOk-obuLRIxNqs5ibRuaymMQ4NLZI8G6mH5-NB3M=4058304a696d7f92c'
    data = _getData(content)
    return data['username'], data['password']


@bcache.cache
async def getQiniu() -> tuple[str, str]:
    content = '七牛云 gAABl0RjrmaAQv8ByatIWP0du5igDBP_28GffENjKvw9KQI1lGGeweOO_T01OL-LBUPlJ8SXIOPIv1obubke8Zv_JzyLpBkpVhpJLusDxbcLSUjjT0ce3f1b4f89fd698A3AAvQBXU8UuPUw2FrBKx2EVVhtWim2Oj_pI_B4QD6K-IP9_kHWixTenckI_Lcnw4KPSJIDRmCmtSb4RS45cVLlc4Umd4UT4smTYYlH34BA2RSEbQ==63b3af29f373954f0'
    data = _getData(content)
    return data['ak'], data['sk']


def _getData(content: str) -> dict[str, Any]:
    index = content.find(' ')
    if index > -1:
        tips = f'请输入密码（{content[:index]}）：'
    else:
        tips = '请输入密码：'
    while True:
        try:
            pwd = getpass.getpass(tips)
            return bcrypto.decryptJson(content.encode(), pwd)
        except KeyboardInterrupt:
            raise Exception('操作取消')
        except BaseException:
            pass
