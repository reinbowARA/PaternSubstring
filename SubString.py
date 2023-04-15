class Substring:

    # Алгоритм Бойера-Мора
    NO_OF_CHARS = 256
 
    def badCharHeuristic(string, size):
        '''
        Функция предварительной обработки для
        Эвристика плохого характера Бойера Мура
        '''
    
        # Инициализируйте все вхождения как -1
        badChar = [-1]*Substring.NO_OF_CHARS
    
        # Fill the actual value of last occurrence
        for i in range(size):
            badChar[ord(string[i])] = i
    
        # возвращает инициализированный список
        return badChar
    
    def searchBM(txt, pat):
        '''
        Функция поиска по шаблону, использующая 
        эвристику плохих символов алгоритма Бойера Мура
        '''
        m = len(pat)
        n = len(txt)
    
        # создайте список плохих симболов, вызвав
        # функция предварительной обработки badCharHeuristic()
        # для заданного шаблона
        badChar = Substring.badCharHeuristic(pat, m)
    
        # s is shift of the pattern with respect to text
        s = 0
        while(s <= n-m):
            j = m-1
    
            # Продолжайте уменьшать индекс j шаблона, пока
            # символы шаблона и текста совпадают
            # в этот момент
            while j>=0 and pat[j] == txt[s+j]:
                j -= 1
                
            # Если шаблон присутствует при текущем сдвиге,
            # то индекс j станет -1 после приведенного выше цикла
            if j<0:
                print("Паттерн возникает при сдвиге = {}".format(s))
    
                '''   
                Сдвиньте шаблон так, чтобы следующий символ в 
                тексте совпадал с последним его появлением в шаблоне. 
                Условие s+m < n необходимо для случая, 
                когда шаблон встречается в конце текста
                '''
                s += (m-badChar[ord(txt[s+m])] if s+m<n else 1)
            else:
                '''
                Сместите шаблон так, чтобы неправильный символ в тексте совпадал 
                с последним его появлением в шаблоне. 
                Функция max используется для того, чтобы убедиться, 
                что мы получаем положительный сдвиг.
                Мы можем получить отрицательный сдвиг, 
                если последнее появление плохого символа в шаблоне находится справа от текущего символа.
                '''
                s += max(1, j-badChar[ord(txt[s+j])])
    
    # Алгоритм Робин-Карпа
    def searchRK(pat, txt, q):
        M = len(pat)
        N = len(txt)
        i = 0
        j = 0
        p = 0    # хэш-значение для шаблона
        t = 0    # хэш-значение для txt
        h = 1
    
        # Значение h будет равно "pow(d, M-1)% q".
        for i in range(M-1):
            h = (h * Substring.NO_OF_CHARS)% q
    
        # Вычислите хэш-значение шаблона и первого окна
        # текста
        for i in range(M):
            p = (Substring.NO_OF_CHARS * p + ord(pat[i]))% q
            t = (Substring.NO_OF_CHARS * t + ord(txt[i]))% q
    
        # Проведите узором по тексту один за другим
        for i in range(N-M + 1):
            # Проверьте хэш-значения текущего окна текста и
            # шаблон, если хэш-значения совпадают, то только проверьте
            # для символов по одному
            if p == t:
                # Проверяйте наличие символов один за другим
                for j in range(M):
                    if txt[i + j] != pat[j]:
                        break
    
                j+= 1
                # if p == t and pat[0...M-1] = txt[i, i + 1, ...i + M-1]
                if j == M:
                    print ("Шаблон, найденный по индексу " + str(i))
    
            # Вычислить хэш-значение для следующего окна текста: Удалить
            # начальная цифра, добавьте конечную цифру
            if i < N-M:
                t = (Substring.NO_OF_CHARS*(t-ord(txt[i])*h) + ord(txt[i + M]))% q
    
                # Мы могли бы получить отрицательные значения t, преобразовав их в
                # положительные
                if t < 0:
                    t = t + q

    # Алгоритм Кнута-Морриса-Пратт (КМП)
    def KMPSearch(pat, txt):
        M = len(pat)
        N = len(txt)
    
        # создайте lps[], который будет содержать самый длинный префиксный суффикс
        # значения для шаблона
        lps = [0]*M
        j = 0  # индекс для pat[]
    
        # Предварительная обработка шаблона (вычисление массива lps[])
        Substring.computeLPSArray(pat, M, lps)
    
        i = 0  # индекс для txt[]
        while (N - i) >= (M - j):
            if pat[j] == txt[i]:
                i += 1
                j += 1
    
            if j == M:
                print("Обнаруженный паттерн по индексу " + str(i-j))
                j = lps[j-1]
    
            # несоответствие после j совпадений
            elif i < N and pat[j] != txt[i]:
                # Не совпадайте с символами lps[0..lps[j-1]],
                # они все равно будут совпадать
                if j != 0:
                    j = lps[j-1]
                else:
                    i += 1
    
    
    def computeLPSArray(pat, M, lps):
        len = 0  
    
        lps[0] = 0 
        i = 1
    
        # цикл вычисляет lps[i] для i = 1 до M-1
        while i < M:
            if pat[i] == pat[len]:
                len += 1
                lps[i] = len
                i += 1
            else:
                if len != 0:
                    len = lps[len-1]
                else:
                    lps[i] = 0
                    i += 1
    
    # Алгоритм на конечных автоматах
    def getNextState(pat, M, state, x):
        '''
        вычислите следующее состояние
        '''
    
        # Если символ c совпадает со следующим символом
        # в шаблоне, затем просто увеличьте состояние
    
        if state < M and x == ord(pat[state]):
            return state+1
    
        i=0
        # ns сохраняет результат, который является следующим состоянием
    
        # ns, наконец, содержит самый длинный префикс
        # который также является суффиксом в "pat[0..state-1]c"
    
        # Начните с максимально возможного значения и
        # остановитесь, когда найдете префикс, который также является суффиксом
        for ns in range(state,0,-1):
            if ord(pat[ns-1]) == x:
                while(i<ns-1):
                    if pat[i] != pat[state-ns+1+i]:
                        break
                    i+=1
                if i == ns-1:
                    return ns
        return 0
    
    def computeTF(pat, M):
        '''
        Эта функция строит таблицу TF, 
        которая представляет конечные автоматы для данного шаблона
        '''
        
    
        TF = [[0 for i in range(Substring.NO_OF_CHARS)]\
            for _ in range(M+1)]
    
        for state in range(M+1):
            for x in range(Substring.NO_OF_CHARS):
                z = Substring.getNextState(pat, M, state, x)
                TF[state][x] = z
    
        return TF
    
    def searchEA(pat, txt):
        '''
        Печатает все вхождения pat в формате txt
        '''
        
        M = len(pat)
        N = len(txt)
        TF = Substring.computeTF(pat, M)   
        
        state=0
        for i in range(N):
            state = TF[state][ord(txt[i])]
            if state == M:
                print("Шаблон, найденный по индексу: {}".\
                    format(i-M+1))