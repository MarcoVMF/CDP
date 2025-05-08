class RemoteFileInterface:
    def get_file_content(self, filename: str) -> str: pass
    def check_master_version(self) -> str: pass
