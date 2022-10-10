import sys, os.path, time
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pyAesCrypt
from os import stat, remove

def FileExist(file):
    fileExists = os.path.exists(file)
    return fileExists

def FileName(file):
    fullName = file[file.rfind("/")+1:]
    return fullName

def Encrypt(file, password, bufferSize):
    if '.aes' in file:
        print("\nArquivo .aes não pode ser criptografado!")
        return False
    else:
        with open(file, "rb") as fIn:
            with open(file + ".aes", "wb") as fOut:
                pyAesCrypt.encryptStream(fIn, fOut, password, bufferSize)
                print("\nCriptografando o arquivo...")
                time.sleep(3)
                return True
        return False


def Descrypt(file, password, bufferSize, fileSize):
    if '.aes' in file:
        with open(file, "rb") as fIn:
            try:
                file = file.replace(".aes", "")
                with open(file, "wb") as fOut:
                    a = pyAesCrypt.decryptStream(fIn, fOut, password, bufferSize, fileSize)
                    print("\nDescriptografando o arquivo...")
                    time.sleep(3)
                    return True
            except ValueError:
                print("\nSenha errada (ou arquivo está corrompido).")
                remove(file)
                return False
    else:
        print("\nO arquivo {} não está criptografado!".format(FileName(file)))
        return False

def SelectFile():
    root = Tk()
    root.overrideredirect(True)
    root.geometry('0x0+0+0')
    root.focus_force()
    ttl = 'Select File'
    filename = askopenfilename(parent=root, title=ttl)  # Isto te permite selecionar um arquivo
    root.withdraw()  # Isto torna oculto a janela principal
    return filename  # printa o arquivo selecionado

# encryption/decryption buffer size - 64K
bufferSize = 128 * 1024

while True:
    options = int(input('\nEscolha: \n1- Criptografar \n2- Descriptografar \n3- Sair\nR: '))

    if (options > 3) or (options < 1):
        print("\nEscolha Inválida")
        continue

    if options == 3:
        print("\nFechando o programa...")
        time.sleep(2)
        sys.exit()

    # selecionar um arquivo
    file = SelectFile()

    password = input("Digite a Senha: ")

    if options == 1:
        if FileExist(file):
            # criptografar
            encryptedFile = Encrypt(file, password, bufferSize)
            if encryptedFile:
                print("Arquivo Criptografado")
                remove(file)
                time.sleep(2)
                print("Arquivo {} Removido". format(FileName(file)))
        else:
            print("\nArquivo não Existe")

    elif options == 2:
        if FileExist(file):
            # obter o tamanho do arquivo criptografado
            fileSize = stat(file).st_size

            # descriptografar
            decryptedFile = Descrypt(file, password, bufferSize, fileSize)
            if decryptedFile:
                print("Arquivo Descriptografado")
                time.sleep(2)
        else:
            print("\nArquivo não Existe")
