import huffmancoding
hc = huffmancoding.HuffManCoding('Enter The Complete File Path')
output_path_compress = hc.compress()
hc.decompress(output_path_compress)
