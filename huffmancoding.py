import heapq, os

class BinaryTreeNode:
    def __init__(self, text, freq):
        self.text = text
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

    def __eq__(self, other):
        return self.freq == other.freq

class HuffManCoding:
    def __init__(self, path):
        self.__path = path
        self.__freqDict = {}
        self.__heap = []
        self.__root = None
        self.__codeDict = {}
        self.__revcodeDict = {}

    def __getFreqDict(self, string):
        for x in string:
            self.__freqDict[x] = self.__freqDict.get(x, 0) + 1

    def __getMinHeap(self):
        heapq.heapify(self.__heap)
        for x in self.__freqDict:
            node = BinaryTreeNode(x, self.__freqDict[x])
            heapq.heappush(self.__heap, node)

    def __buildBinaryTree(self):
        while(len(self.__heap) > 1):
            node1 = heapq.heappop(self.__heap)
            node2 = heapq.heappop(self.__heap)

            newNode = BinaryTreeNode('', node1.freq + node2.freq)
            newNode.left = node1
            newNode.right = node2
            heapq.heappush(self.__heap, newNode)

    def __buildCodesHelper(self, root, curBits = ''):
        if root.left is None and root.right is None:
            self.__codeDict[root.text] = curBits
            self.__revcodeDict[curBits] = root.text
            return

        self.__buildCodesHelper(root.left, curBits + '0')
        self.__buildCodesHelper(root.right, curBits + '1')

    def __buildCodes(self):
        self.__buildCodesHelper(self.__root)

    def __getEncodedText(self, string):
        encodedText = ''
        for text in string:
            encodedText += self.__codeDict[text]

        return encodedText

    def __getPaddedEncodedText(self, encodedText):
        paddingValue = 8 - (len(encodedText) % 8)
        x = 0
        while x < paddingValue:
            encodedText += '0'
            x += 1

        k = '{0:08b}'.format(paddingValue) 
        encodedText = k + encodedText
        return encodedText

    def __getByteArray(self, encodedText):
        byteArray = []
        for i in range(0, len(encodedText), 8):
            bytes = encodedText[i : i + 8]
            values = int(bytes, 2)
            byteArray.append(values)

        return byteArray

    def compress(self):
        file_name, file_extension = os.path.splitext(self.__path)
        output_path = file_name + '_compressed' + '.bin'

        with open(self.__path, 'r+') as file, open(output_path, 'wb') as output:
            # Get Frequency Dictionary
            text = file.read()
            text = text.rstrip()
            self.__getFreqDict(text)
            # Build the Heap
            self.__getMinHeap()
            # Build a binary tree node
            self.__buildBinaryTree()
            self.__root = heapq.heappop(self.__heap)
            # Build Codes
            self.__buildCodes()
            # Encoding Text
            encodedText = self.__getEncodedText(text)
            # Padding of Encoded Text
            encodedText = self.__getPaddedEncodedText(encodedText)
            # Converting into the bits
            byteArray = bytes(self.__getByteArray(encodedText))
            output.write(byteArray)
        
        return output_path

    def __removePading(self, bit_string):
        paddingValue = int(bit_string[:8], 2)
        text = bit_string[8 : len(bit_string)-paddingValue]
        return text

    def __getDecodedText(self, text):
        bits = ''
        decoded_text = ''
        for bit in text:
            bits += bit
            if bits in self.__revcodeDict:
                char = self.__revcodeDict[bits]
                decoded_text += char
                bits = ''
        
        return decoded_text

    def decompress(self, input_path):
        file_name, file_extenstion = os.path.splitext(self.__path)
        output_path = file_name + '_decompressed' + '.txt'
        with open(input_path, 'rb') as file, open(output_path, 'w') as output:
            bit_string = ''
            byte = file.read(1)
            while byte:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)
            actual_bits = self.__removePading(bit_string)
            decoded_text = self.__getDecodedText(actual_bits)
            output.write(decoded_text)
        return

    def getFreqDict(self):
        return self.__freqDict

    def getCodeDict(self):
        return self.__codeDict