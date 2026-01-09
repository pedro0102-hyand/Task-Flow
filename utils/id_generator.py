import uuid

def generate_id(prefix=None):
    # Primeiro converte para string, depois faz o fatiamento [:8]
    short_uuid = str(uuid.uuid4())[:8]
    
    if prefix:
        # Sanitiza o prefixo (remove espaços e coloca em maiúsculo)
        clean_prefix = prefix.replace(" ", "-").upper()
        return f"{clean_prefix}-{short_uuid}"
    
    return short_uuid