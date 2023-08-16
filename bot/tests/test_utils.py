from utils import utils

def testNumberedStrIterable():
    expected = '1. first\n2. second\n3. third'
    exampleList1 = ['first', 'second', 'third']
    exampleList2 = []
    exampleTuple = ('first', 'second', 'third')
    assert utils.numberedStrIterable(exampleList1) == expected
    assert utils.numberedStrIterable(exampleList2) == ''
    assert utils.numberedStrIterable(exampleTuple) == expected
    