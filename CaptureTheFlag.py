

ROOT = "C:\\assembly\\static analysis\\"
filename="challenge.jpg"
output_file = open("execute_file.bin",'w')
filename = ROOT + filename
f = open(filename, 'rb')
byte = f.read(4)
while byte != b"":
    if byte == b"4d5a90":
        output_file.write(byte)
        output_file.write( f.read())
    byte = f.read(1)

output_file.close()
f.close()
