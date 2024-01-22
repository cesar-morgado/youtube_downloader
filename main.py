from flask import Flask, render_template, request, redirect, url_for
from pytube import YouTube
import os

app = Flask(__name__)

def baixar_audio(yt, output_path):
    stream = yt.streams.get_audio_only()

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    print("Baixando áudio...")
    try:
        stream.download(output_path=output_path)
        print("Download do áudio concluído!")
        return True
    except Exception as e:
        print(f"Erro durante o download do áudio: {e}")
        return False



# Função para baixar e salvar o vídeo na pasta de vídeos
def baixar_video(yt, output_path):
    stream = yt.streams.get_highest_resolution()

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    print("Baixando vídeo...")
    try:
        stream.download(output_path=output_path)
        print("Download do vídeo concluído!")
        return True
    except Exception as e:
        print(f"Erro durante o download do vídeo: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        escolha = request.form['escolha']
        yt = YouTube(url)

        if escolha == 'audio':
            pasta_musicas = os.path.join(os.path.expanduser('~'), 'Music')
            download_sucesso = baixar_audio(yt, pasta_musicas)

        elif escolha == 'video':
            pasta_videos = os.path.join(os.path.expanduser('~'), 'Videos')
            download_sucesso = baixar_video(yt, pasta_videos)

        if download_sucesso:
            return redirect(url_for('download_concluido'))
        else:
            return redirect(url_for('erro'))

    return render_template('index.html')

@app.route('/download_concluido')
def download_concluido():
    return render_template('download_concluido.html')

@app.route('/erro')
def erro():
    return render_template('erro.html')

if __name__ == '__main__':
    app.run(debug=True)
