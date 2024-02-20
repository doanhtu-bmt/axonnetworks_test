import logging
logging.basicConfig(filename='log.log', level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

def test01():
    logging.info("aa")

if __name__ == '__main__':
    
    test01()