import os
import glob
import PySimpleGUI as sg
from PyPDF2 import PdfMerger
import sys

# Definir o tema escuro
sg.theme('DarkGrey10')

def mesclar_pdfs(arquivos_entrada, caminho_saida):
    """
    Função para mesclar PDF usando PyPDF2.
    """

    try:
        mesclador = PdfMerger()

        for pdf in arquivos_entrada:
            mesclador.append(pdf)

        mesclador.write(caminho_saida)
        mesclador.close()

        sg.popup(f'PDFs mesclados com sucesso!\nArquivo de saída: {caminho_saida}')

    except Exception as erro:
        sg.popup_error(f'Ocorreu um erro ao tentar mesclar os PDFs.\nMensagem de erro: {erro}')

def obter_caminho_saida(caminho_saida):
    if hasattr(sys, 'frozen'):
        diretorio_script = os.path.dirname(sys.executable)
    else:
        diretorio_script = os.path.dirname(__file__)

    caminho_padrao = os.path.join(diretorio_script, 'mesclado.pdf')

    if caminho_saida:
        caminho_absoluto = os.path.abspath(caminho_saida)

        if caminho_absoluto.lower().endswith('.pdf') or os.path.isdir(caminho_absoluto):
            return caminho_absoluto

    return caminho_padrao

def coletar_pdfs(caminho_entrada):
    arquivos_pdf = []
    for caminho in caminho_entrada:
        caminho_absoluto = os.path.abspath(caminho)
        if os.path.isfile(caminho_absoluto) and caminho_absoluto.lower().endswith('.pdf'):
            arquivos_pdf.append(caminho_absoluto)
        elif os.path.isdir(caminho_absoluto):
            arquivos_pdf.extend(glob.glob(os.path.join(caminho_absoluto, '**', '*.pdf') ,recursive=True))
    return arquivos_pdf

def main():
    layout = [
        [sg.Text('Selecione os arquivos PDF a serem mesclados ou diretórios contendo PDFs:')],
        [sg.Input(key='arquivos', enable_events=True), sg.FilesBrowse(button_text='Selecionar Arquivos')],
        [sg.Text('Caminho do arquivo PDF de saída:')],
        [sg.Input(key='saida'), sg.FileSaveAs(button_text='Selecionar Pasta')],
        [sg.Button('Mesclar PDFs', size=(15, 2))]
    ]

    janela = sg.Window('Mesclar PDFs', layout)

    while True:
        evento, valores = janela.read()

        if evento == sg.WIN_CLOSED:
            break

        if evento == 'Mesclar PDFs':
            arquivos_entrada = coletar_pdfs(valores['arquivos'].split(';'))
            caminho_saida = obter_caminho_saida(valores['saida'])
            mesclar_pdfs(arquivos_entrada, caminho_saida)

    janela.close()

if __name__ == '__main__':
    main()