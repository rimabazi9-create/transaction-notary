import json
import hashlib
import os
from eth_account import Account
from eth_account.messages import encode_defunct

def main():
    # 1. قراءة المفتاح الخاص من البيئة (آمن)
    private_key = os.environ.get("PRIVATE_KEY")
    if not private_key:
        raise Exception("❌ PRIVATE_KEY not found in environment variables!")
    
    # 2. تحميل البيانات الخام
    with open('data/raw.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 3. تحويل الكائن إلى نص JSON مضغوط (بدون مسافات لضمان ثبات الهاش)
    json_string = json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    
    # 4. حساب SHA-256
    hash_obj = hashlib.sha256(json_string.encode('utf-8'))
    file_hash = "0x" + hash_obj.hexdigest()
    print(f"✅ Hash: {file_hash}")
    
    # 5. توقيع النص (وليس الهاش مباشرة، طريقة Ethereum القياسية)
    message = encode_defunct(text=json_string)
    signed = Account.sign_message(message, private_key=private_key)
    signature_hex = "0x" + signed.signature.hex()
    signer_address = signed.signer
    print(f"✅ Signature: {signature_hex}")
    print(f"✅ Signer: {signer_address}")
    
    # 6. إضافة الهاش والتوقيع إلى البيانات
    data["verification"] = {
        "sha256_hash": file_hash,
        "signature": signature_hex,
        "signed_by": signer_address,
        "timestamp": "2026-06-05T18:13:37.928021+00:00"  # ثابت بناءً على وقت التدقيق
    }
    
    # 7. حفظ الملف النهائي الموقّع (سيستخدمه موقع العرض)
    with open('data/signed.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("✅ تم إنشاء data/signed.json بنجاح!")

if __name__ == "__main__":
    main()
