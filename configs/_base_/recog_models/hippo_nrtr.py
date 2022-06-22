label_convertor = dict(
    type='AttnConvertor',
    dict_list=list('0123456789abcdefghijklmnopqrstuvwxyz'
                   'ABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()'
                   '*+,-./:;<=>?@[\\]_`~'
                   'กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮฤฦะัาำิีึืุูเแโใไๅํ็่้๊๋ฯฺๆ์๎๏๚๛๐๑๒๓๔๕๖๗๘๙฿ '),
    with_unknown=True)

model = dict(
    type='NRTR',
    backbone=dict(type='NRTRModalityTransform'),
    encoder=dict(type='NRTREncoder'),
    decoder=dict(type='NRTRDecoder'),
    loss=dict(type='TFLoss'),
    label_convertor=label_convertor,
    max_seq_len=40)
