import hashlib
import re
from datetime import datetime
from decimal import Decimal
from io import BytesIO
from typing import Dict, List, Any

import pandas as pd
import pypdf


def generate_external_id(date: str, amount: str, source: str) -> str:
    """
    Cria um ID único para uma transação para evitar duplicatas na importação.
    Equivalente à função em JS que usava crypto.
    """
    unique_string = f"{date}-{amount}-{source}"
    return hashlib.md5(unique_string.encode()).hexdigest()


def _clean_amount(amount_str: Any) -> Decimal:
    """
    Limpa e converte o valor monetário para Decimal.
    Ex: 'R$ 25,50' -> Decimal('25.50')
    """
    if isinstance(amount_str, (int, float, Decimal)):
        return Decimal(amount_str)
    
    if not isinstance(amount_str, str):
        return Decimal(0)

    # Troca a vírgula do decimal por ponto e remove outros caracteres não numéricos
    cleaned_str = re.sub(r"[^0-9,.]", "", amount_str).replace(",", ".")
    
    # Se houver mais de um ponto, remove todos exceto o último
    if cleaned_str.count('.') > 1:
        parts = cleaned_str.split('.')
        cleaned_str = "".join(parts[:-1]) + "." + parts[-1]

    try:
        return Decimal(cleaned_str)
    except Exception:
        return Decimal(0)


def parse_uber_csv(contents: bytes) -> List[Dict]:
    """Processa um extrato CSV da Uber."""
    transactions = []
    df = pd.read_csv(BytesIO(contents))
    
    # Detecta colunas de data e valor com nomes comuns em extratos da Uber
    date_col = next((col for col in df.columns if 'date' in col.lower() or 'data' in col.lower()), None)
    amount_col = next((col for col in df.columns if 'amount' in col.lower() or 'valor' in col.lower() or 'ganhos' in col.lower()), None)
    
    if not date_col or not amount_col:
        return []

    for _, row in df.iterrows():
        date_str = str(row[date_col])
        amount_val = str(row[amount_col])
        amount = _clean_amount(amount_val)

        if date_str and amount > 0:
            try:
                # Tenta converter a data, suportando vários formatos comuns
                parsed_date = pd.to_datetime(date_str, dayfirst=True, errors='coerce').to_pydatetime()
                if pd.isna(parsed_date):
                    continue
            except Exception:
                continue

            transactions.append({
                "date": parsed_date,
                "amount": amount,
                "description": "Corrida Uber",
                "type": "income",
                "source": "Uber",
                "external_id": generate_external_id(date_str, amount_val, "Uber")
            })
            
    return transactions


def parse_99_csv(contents: bytes) -> List[Dict]:
    """Processa um extrato CSV da 99."""
    # A lógica é similar à da Uber, mas pode ter colunas diferentes
    # Este é um exemplo, ajuste conforme os extratos reais da 99
    return parse_uber_csv(contents) # Reutiliza a lógica genérica por enquanto


def parse_indrive_csv(contents: bytes) -> List[Dict]:
    """Processa um extrato CSV da inDrive."""
    # A lógica é similar à da Uber, mas pode ter colunas diferentes
    # Este é um exemplo, ajuste conforme os extratos reais da inDrive
    return parse_uber_csv(contents) # Reutiliza a lógica genérica por enquanto


def parse_generic_csv(contents: bytes) -> List[Dict]:
    """Tenta processar um CSV genérico, identificando a plataforma pelo conteúdo."""
    text_content = contents.decode('utf-8', errors='ignore').lower()
    if 'uber' in text_content:
        return parse_uber_csv(contents)
    if '99' in text_content:
        return parse_99_csv(contents)
    if 'indrive' in text_content:
        return parse_indrive_csv(contents)
    # Fallback para o parser da Uber
    return parse_uber_csv(contents)


def parse_xlsx(contents: bytes) -> List[Dict]:
    """Processa um arquivo XLSX convertendo-o para CSV em memória."""
    df = pd.read_excel(BytesIO(contents))
    csv_buffer = df.to_csv(index=False).encode('utf-8')
    return parse_generic_csv(csv_buffer)


def parse_pdf(contents: bytes) -> List[Dict]:
    """
    Processa um extrato em PDF.
    AVISO: PDF parsing é frágil e depende muito do layout do documento.
    Esta função é um exemplo e provavelmente precisará de ajustes.
    """
    transactions = []
    reader = pypdf.PdfReader(BytesIO(contents))
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    # Regex para encontrar data e valor (ex: 21/07/2025 ... R$ 35,50)
    # Este Regex é um exemplo e precisa ser adaptado ao formato exato do seu PDF.
    pattern = re.compile(r"(\d{2}/\d{2}/\d{4}).*?R\$\s*([\d,]+\.?\d*)", re.IGNORECASE)
    matches = pattern.findall(text)

    for date_str, amount_str in matches:
        amount = _clean_amount(amount_str)
        if amount > 0:
            try:
                parsed_date = datetime.strptime(date_str, "%d/%m/%Y")
            except ValueError:
                continue

            transactions.append({
                "date": parsed_date,
                "amount": amount,
                "description": "Corrida (PDF)",
                "type": "income",
                "source": "Uber", # Assumindo que o PDF é da Uber
                "external_id": generate_external_id(date_str, amount_str, "Uber-PDF")
            })

    return transactions