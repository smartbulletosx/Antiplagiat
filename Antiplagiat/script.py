import math as m
import docx
import pymorphy2
import binascii

def toFixed(numObj, digits):  #округление до digits
    return f"{numObj:.{digits}f}"

def deconstruct(text , symbol): #разбиение на части через split
    result = text.split(symbol)
    return result

def normalize(source): #нормализация текста
    for i in range(len(source)):
        source[i] = pymorphy2.MorphAnalyzer().parse(source[i])[0].normal_form

def canonize(text):
    stop_symbols = '.,!?:;-\n\r()'

    stop_words = (u'это', u'как', u'так',
    u'и', u'в', u'над',
    u'к', u'до', u'не',
    u'на', u'но', u'за',
    u'то', u'с', u'ли',
    u'а', u'во', u'от',
    u'со', u'для', u'о',
    u'же', u'ну', u'вы',
    u'бы', u'что', u'кто',
    u'он', u'она')

    return ( [x for x in [y.strip(stop_symbols) for y in text.lower().split()] if x and (x not in stop_words)] )

def genshingle(source):
    if len(source) < 10:
        return 1
    else:
        shingleLen = 10 #длина шингла
        out = []
        for i in range(len(source)-(shingleLen-1)):
            out.append (binascii.crc32(' '.join( [x for x in source[i:i+shingleLen]] ).encode('utf-8')))

    return out

def compaire (source1,source2):
    if source1 == 1 or source2 == 1:
        return 10010010002010010001000010100101000010
    same = 0
    for i in range(len(source1)):
        if source1[i] in source2:
            same = same + 1
    return toFixed(same*2/float(len(source1) + len(source2))*100, 2)

def antiplagiat(text_1, text_2): #антиплагиат вектором
    words_1 = deconstruct(text_1, ' ')
    words_2 = deconstruct(text_2, ' ')

    normalize(words_1)
    normalize(words_2)

    words = set()

    vector_1 = []
    vector_2 = []

    for i in words_1:
        words.add(i)

    for i in words_2:
        words.add(i)

    cnt = 0

    for word in words:
        for i in words_1:
            if (i == word):
                cnt+=1;
        vector_1.append(cnt)
        cnt = 0;

    for word in words:
        for i in words_2:
            if (i == word):
                cnt+=1;
        vector_2.append(cnt)
        cnt = 0;

    vector_1 = sorted(vector_1)
    vector_2 = sorted(vector_2)

    ans = 0

    for i in range(len(words)):
        ans+=vector_1[i]*vector_2[i]

    len_1 = 0
    for i in vector_1:
        len_1= len_1 + (i ** 2)
        print
    len_1 = m.sqrt(len_1)


    len_2 = 0
    for i in vector_2:
        len_2 = len_2 + (i ** 2)
    len_2 = m.sqrt(len_2)


    lens = len_1*len_2

    ans *= 100/lens

    return(toFixed(ans,2))

def main():
    text_1 = u'фкупкуфп'
    text_2 = u'фкупкуфп'

    sum1 = genshingle(canonize(text_1))
    sum2 = genshingle(canonize(text_2))

    if compaire(sum1,sum2) == 10010010002010010001000010100101000010:
        print("Слишком маленький текст")
    else:
        print("Шинглами: ", toFixed(float(compaire(sum1,sum2)),2))
        print("Вектором: ", toFixed(float(antiplagiat(text_1,text_2)),2))

        ans = (float(compaire(sum1,sum2)) + float(antiplagiat(text_1,text_2)))/2
        print("Схожесть: " , toFixed(ans,2),"%")

main()
