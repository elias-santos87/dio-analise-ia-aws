import os
import boto3
from dotenv import load_dotenv

# Carrega as chaves seguras do arquivo .env
load_dotenv()

session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
)

# 1. Olhos do Robô: Rekognition (Reconhecimento de Imagens)
def analisar_imagem(caminho_imagem):
    print("\n🔍 [1] ANALISANDO OBJETOS NA IMAGEM (AWS Rekognition)...")
    cliente = session.client("rekognition")
    
    with open(caminho_imagem, "rb") as arquivo:
        imagem_bytes = arquivo.read()
        
    resposta = cliente.detect_labels(
        Image={"Bytes": imagem_bytes},
        MaxLabels=5,
        MinConfidence=75
    )
    
    for label in resposta["Labels"]:
        print(f"  • Encontrado: {label['Name']} | Confiança: {label['Confidence']:.2f}%")

# 2. Lupa de Leitura: Textract (OCR / Extração de Texto)
def extrair_texto(caminho_imagem):
    print("\n📖 [2] LENDO TEXTO DENTRO DA IMAGEM (AWS Textract)...")
    cliente = session.client("textract")
    
    with open(caminho_imagem, "rb") as arquivo:
        imagem_bytes = arquivo.read()
        
    resposta = cliente.detect_document_text(
        Document={"Bytes": imagem_bytes}
    )
    
    textos = [item["Text"] for item in resposta["Blocks"] if item["BlockType"] == "LINE"]
    if textos:
        for linha in textos:
            print(f"  • Texto lido: \"{linha}\"")
    else:
        print("  • Nenhum texto visível encontrado.")

# 3. Sensor de Sentimentos: Comprehend (Análise de Sentimentos)
def analisar_sentimento(texto):
    print(f"\n💭 [3] ANALISANDO O SENTIMENTO DO TEXTO (AWS Comprehend)...")
    print(f"  Texto analisado: \"{texto}\"")
    cliente = session.client("comprehend")
    
    resposta = cliente.detect_sentiment(
        Text=texto,
        LanguageCode="pt"
    )
    
    sentimento = resposta["Sentiment"]
    score = resposta["SentimentScore"]
    
    traducao = {
        "POSITIVE": "😊 POSITIVO",
        "NEGATIVE": "😡 NEGATIVO",
        "NEUTRAL": "😐 NEUTRO",
        "MIXED": "🤔 MISTO"
    }
    
    print(f"  • Sentimento Predominante: {traducao.get(sentimento, sentimento)}")
    print(f"  • Confiança: {score.get(sentimento.capitalize(), 0):.2%}")

if __name__ == "__main__":
    # Coloque uma imagem chamada exemplo.jpg na pasta
    IMAGEM_TESTE = "exemplo.jpg"
    FRASE_TESTE = "Estou impressionado com a facilidade de usar Inteligência Artificial na nuvem da AWS!"
    
    if os.path.exists(IMAGEM_TESTE):
        analisar_imagem(IMAGEM_TESTE)
        extrair_texto(IMAGEM_TESTE)
    else:
        print(f"⚠️ Atenção: Adicione uma imagem chamada '{IMAGEM_TESTE}' para testar Rekognition e Textract.")
        
    analisar_sentimento(FRASE_TESTE)