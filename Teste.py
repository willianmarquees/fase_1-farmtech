import os
import assemblyai as aai
from pydub import AudioSegment
from google.cloud import translate_v2 as translate

# Substitua pela sua chave de API do AssemblyAI
aai.settings.api_key = "cbfd65389fe64df280955d4ed88e9669"

# Defina a variável de ambiente para as credenciais do Google Cloud
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/Users/macforpc/Downloads/Testando.json"

# Caminhos para os arquivos
mp4_file_path = "/Users/macforpc/Downloads/Corte 2.mp4"
wav_file_path = "/Users/macforpc/Downloads/Corte 2.wav"

# Converte o arquivo MP4 para WAV usando pydub
audio = AudioSegment.from_file(mp4_file_path, format="mp4")
audio.export(wav_file_path, format="wav")

# Cria a configuração de transcrição
config = aai.TranscriptionConfig(
    language_code="zh",
    punctuate=True,
    format_text=True
)

# Inicializa o transcritor com a configuração
transcriber = aai.Transcriber(config=config)

# Faz a transcrição do áudio
transcript = transcriber.transcribe(wav_file_path)

# Verifica se houve erro
if transcript.status == aai.TranscriptStatus.error:
    print("Erro na transcrição:", transcript.error)
else:
    # Texto transcrito em chinês
    chinese_text = transcript.text
    print("Texto transcrito em chinês:")
    print(chinese_text)

    # Inicializa o cliente de tradução do Google
    translate_client = translate.Client()

    # Traduz o texto para o português
    translation = translate_client.translate(
        chinese_text,
        source_language='zh-CN',
        target_language='pt'
    )

    portuguese_text = translation['translatedText']
    print("\nTexto traduzido para o português:")
    print(portuguese_text)