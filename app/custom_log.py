import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    fmt="[%(levelname)s]       %(asctime)s\n %(message)s\n",
    datefmt="%d/%m/%Y | %H:%M:%S",
)
handler.setFormatter(formatter)
log.addHandler(handler)
