import os
import json
import hashlib

class FileIntegrityChecker:
    def __init__(self, directory, hash_file="vdb/hashes.json", algorithm="md5"):
        self.directory = directory
        self.hash_file = hash_file
        self.algorithm = algorithm.lower()
        self.hash_func = getattr(hashlib, self.algorithm)

    def _calculate_hash(self, filepath):
        hasher = self.hash_func()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def scan_directory(self):
        hashes = {}
        for root, _, files in os.walk(self.directory):
            for file in files:
                path = os.path.join(root, file)
                try:
                    relative_path = os.path.relpath(path, self.directory)
                    hashes[relative_path] = self._calculate_hash(path)
                except Exception as e:
                    print(f"Error leyendo {path}: {e}")
        return hashes

    def save_hashes(self):
        hashes = self.scan_directory()
        with open(self.hash_file, "w", encoding="utf-8") as f:
            json.dump(hashes, f, indent=2)
        print(f"Hashes guardados en {self.hash_file}")

    def check_integrity(self):
        if not os.path.exists(self.hash_file):
            print("Archivo de hashes no encontrado. Usa primero `save_hashes()`.")
            return None

        with open(self.hash_file, "r", encoding="utf-8") as f:
            saved_hashes = json.load(f)

        current_hashes = self.scan_directory()
        modified = []

        for path, original_hash in saved_hashes.items():
            current_hash = current_hashes.get(path)
            if current_hash != original_hash:
                modified.append(path)

        missing = [path for path in saved_hashes if path not in current_hashes]
        new_files = [path for path in current_hashes if path not in saved_hashes]

        if not modified and not missing and not new_files:
            print("Todos los archivos están intactos.")
            return True
        else:
            print("Cambios detectados:")
            if modified:
                print(" - Archivos modificados:")
                for f in modified:
                    print("   •", f)
            if missing:
                print(" - Archivos faltantes:")
                for f in missing:
                    print("   •", f)
            if new_files:
                print(" - Archivos nuevos no registrados:")
                for f in new_files:
                    print("   •", f)
            return False

# Uso básico
if __name__ == "__main__":
    checker = FileIntegrityChecker(directory="mi_directorio", algorithm="md5")
    
    # Para guardar los hashes
    # checker.save_hashes()
    
    # Para verificar integridad
    # checker.check_integrity()