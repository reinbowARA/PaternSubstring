class Substring:

    # Алгоритм Бойера-Мора
    NO_OF_CHARS = 256
 
    def badCharHeuristic(string, size):
        '''
        The preprocessing function for
        Boyer Moore's bad character heuristic
        '''
    
        # Initialize all occurrence as -1
        badChar = [-1]*Substring.NO_OF_CHARS
    
        # Fill the actual value of last occurrence
        for i in range(size):
            badChar[ord(string[i])] = i
    
        # return initialized list
        return badChar
    
    def searchBM(txt, pat):
        '''
        A pattern searching function that uses Bad Character
        Heuristic of Boyer Moore Algorithm
        '''
        m = len(pat)
        n = len(txt)
    
        # create the bad character list by calling
        # the preprocessing function badCharHeuristic()
        # for given pattern
        badChar = Substring.badCharHeuristic(pat, m)
    
        # s is shift of the pattern with respect to text
        s = 0
        while(s <= n-m):
            j = m-1
    
            # Keep reducing index j of pattern while
            # characters of pattern and text are matching
            # at this shift s
            while j>=0 and pat[j] == txt[s+j]:
                j -= 1
    
            # If the pattern is present at current shift,
            # then index j will become -1 after the above loop
            if j<0:
                print("Pattern occur at shift = {}".format(s))
    
                '''   
                    Shift the pattern so that the next character in text
                        aligns with the last occurrence of it in pattern.
                    The condition s+m < n is necessary for the case when
                    pattern occurs at the end of text
                '''
                s += (m-badChar[ord(txt[s+m])] if s+m<n else 1)
            else:
                '''
                Shift the pattern so that the bad character in text
                aligns with the last occurrence of it in pattern. The
                max function is used to make sure that we get a positive
                shift. We may get a negative shift if the last occurrence
                of bad character in pattern is on the right side of the
                current character.
                '''
                s += max(1, j-badChar[ord(txt[s+j])])
    
    # Алгоритм Робин-Карпа
    def searchRK(pat, txt, q):
        M = len(pat)
        N = len(txt)
        i = 0
        j = 0
        p = 0    # hash value for pattern
        t = 0    # hash value for txt
        h = 1
    
        # The value of h would be "pow(d, M-1)% q"
        for i in range(M-1):
            h = (h * Substring.NO_OF_CHARS)% q
    
        # Calculate the hash value of pattern and first window
        # of text
        for i in range(M):
            p = (Substring.NO_OF_CHARS * p + ord(pat[i]))% q
            t = (Substring.NO_OF_CHARS * t + ord(txt[i]))% q
    
        # Slide the pattern over text one by one
        for i in range(N-M + 1):
            # Check the hash values of current window of text and
            # pattern if the hash values match then only check
            # for characters one by one
            if p == t:
                # Check for characters one by one
                for j in range(M):
                    if txt[i + j] != pat[j]:
                        break
    
                j+= 1
                # if p == t and pat[0...M-1] = txt[i, i + 1, ...i + M-1]
                if j == M:
                    print ("Pattern found at index " + str(i))
    
            # Calculate hash value for next window of text: Remove
            # leading digit, add trailing digit
            if i < N-M:
                t = (Substring.NO_OF_CHARS*(t-ord(txt[i])*h) + ord(txt[i + M]))% q
    
                # We might get negative values of t, converting it to
                # positive
                if t < 0:
                    t = t + q

    # Алгоритм Кнута-Морриса-Пратт
    def KMPSearch(pat, txt):
        M = len(pat)
        N = len(txt)
    
        # create lps[] that will hold the longest prefix suffix
        # values for pattern
        lps = [0]*M
        j = 0  # index for pat[]
    
        # Preprocess the pattern (calculate lps[] array)
        Substring.computeLPSArray(pat, M, lps)
    
        i = 0  # index for txt[]
        while (N - i) >= (M - j):
            if pat[j] == txt[i]:
                i += 1
                j += 1
    
            if j == M:
                print("Found pattern at index " + str(i-j))
                j = lps[j-1]
    
            # mismatch after j matches
            elif i < N and pat[j] != txt[i]:
                # Do not match lps[0..lps[j-1]] characters,
                # they will match anyway
                if j != 0:
                    j = lps[j-1]
                else:
                    i += 1
    
    
    def computeLPSArray(pat, M, lps):
        len = 0  # length of the previous longest prefix suffix
    
        lps[0] = 0 # lps[0] is always 0
        i = 1
    
        # the loop calculates lps[i] for i = 1 to M-1
        while i < M:
            if pat[i] == pat[len]:
                len += 1
                lps[i] = len
                i += 1
            else:
                # This is tricky. Consider the example.
                # AAACAAAA and i = 7. The idea is similar
                # to search step.
                if len != 0:
                    len = lps[len-1]
    
                    # Also, note that we do not increment i here
                else:
                    lps[i] = 0
                    i += 1
    
    # Алгоритм на конечных автоматах
    def getNextState(pat, M, state, x):
        '''
        calculate the next state
        '''
    
        # If the character c is same as next character
        # in pattern, then simply increment state
    
        if state < M and x == ord(pat[state]):
            return state+1
    
        i=0
        # ns stores the result which is next state
    
        # ns finally contains the longest prefix
        # which is also suffix in "pat[0..state-1]c"
    
        # Start from the largest possible value and
        # stop when you find a prefix which is also suffix
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
        This function builds the TF table which
        represents Finite Automata for a given pattern
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
        Prints all occurrences of pat in txt
        '''
        
        M = len(pat)
        N = len(txt)
        TF = Substring.computeTF(pat, M)   
    
        # Process txt over FA.
        state=0
        for i in range(N):
            state = TF[state][ord(txt[i])]
            if state == M:
                print("Pattern found at index: {}".\
                    format(i-M+1))