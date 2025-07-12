import os
import uuid
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image
import logging

logger = logging.getLogger("core.upload")

# Extensões permitidas para imagens e arquivos genéricos
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
ALLOWED_FILE_EXTENSIONS = ['.pdf', '.docx', '.xlsx', '.txt', '.zip']
MAX_IMAGE_SIZE_MB = 5
MAX_FILE_SIZE_MB = 10

def validate_file(file, allowed_extensions=None, max_size_mb=None, is_image=False):
    ext = os.path.splitext(file.name)[1].lower()
    size = file.size
    if allowed_extensions and ext not in allowed_extensions:
        logger.warning(f"Tentativa de upload de extensão proibida: {ext}")
        raise ValidationError(f"Tipo de arquivo '{ext}' não permitido.")
    if max_size_mb and size > max_size_mb * 1024 * 1024:
        logger.warning(f"Tamanho excedido: {file.name} ({size})")
        raise ValidationError(f"Arquivo excede o tamanho máximo permitido de {max_size_mb}MB.")
    if is_image:
        try:
            img = Image.open(file)
            img.verify()
            file.seek(0)
        except Exception:
            logger.warning(f"Arquivo enviado não é imagem válida: {file.name}")
            raise ValidationError("O arquivo enviado não é uma imagem válida.")

def build_upload_path(domain, kind, filename):
    """
    Gera caminho seguro e único para o arquivo:
    Exemplo: company.com.br/logos/20240709_uuid_nome.jpg
    """
    date_str = timezone.now().strftime("%Y%m%d")
    safe_domain = slugify(domain)
    safe_name = slugify(os.path.splitext(filename)[0])
    ext = os.path.splitext(filename)[1].lower()
    unique_id = uuid.uuid4().hex[:8]
    path = f"{safe_domain}/{kind}/{date_str}_{unique_id}_{safe_name}{ext}"
    return path

def save_upload_file(file, domain, kind="uploads", is_image=False, allowed_extensions=None, max_size_mb=None):
    """
    Parâmetros:
    - file: arquivo recebido (request.FILES['logo'] etc)
    - domain: domínio/schema do tenant (ex: company.com.br, use schema_name)
    - kind: subdiretório ('logos', 'avatars', 'docs', etc)
    - is_image: se True, valida como imagem
    - allowed_extensions, max_size_mb: override das políticas padrão
    """
    validate_file(
        file,
        allowed_extensions=allowed_extensions or (ALLOWED_IMAGE_EXTENSIONS if is_image else ALLOWED_FILE_EXTENSIONS),
        max_size_mb=max_size_mb or (MAX_IMAGE_SIZE_MB if is_image else MAX_FILE_SIZE_MB),
        is_image=is_image
    )
    path = build_upload_path(domain, kind, file.name)
    logger.info(f"Salvando arquivo: {path}")
    full_path = default_storage.save(path, file)
    url = default_storage.url(full_path)
    return url  # Este é o caminho para salvar no model (URLField)

