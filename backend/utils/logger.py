import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pii_encryption")

def log_metadata(user_id, category, field_name, sensitivity, action):
    """Log only metadata, never plaintext or ciphertext."""
    logger.info(f"User {user_id} | Category {category} | Field {field_name} "
                f"| Sensitivity {sensitivity} | Action {action}")
