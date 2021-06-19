import huffmancoding
hc = huffmancoding.HuffManCoding('/home/madiv/Coding Ninjas/Projects/Huffman Coding/sample.txt')
output_path_compress = hc.compress()
hc.decompress(output_path_compress)