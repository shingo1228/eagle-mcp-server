"""Configuration settings for Eagle MCP Server."""

import os
from pathlib import Path
from typing import Optional
import json
from dotenv import load_dotenv

# Load environment variables from .env.local if it exists
env_file = Path(".env.local")
if env_file.exists():
    load_dotenv(env_file)


class Config:
    """動的設定クラス"""
    
    def __init__(self):
        self.eagle_api_base_url = os.getenv("EAGLE_API_URL", "http://localhost:41595")
        self.eagle_api_timeout = float(os.getenv("EAGLE_API_TIMEOUT", "30.0"))
        
        # MCP Server Configuration
        self.mcp_server_name = os.getenv("MCP_SERVER_NAME", "Eagle MCP Server")
        self.mcp_server_version = os.getenv("MCP_SERVER_VERSION", "0.1.0")
        self.mcp_server_description = "A modern MCP server for Eagle App"
        
        # Logging Configuration
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        
        # Request limits
        self.default_item_limit = int(os.getenv("DEFAULT_ITEM_LIMIT", "50"))
        self.max_item_limit = int(os.getenv("MAX_ITEM_LIMIT", "500"))
        self.default_folder_limit = int(os.getenv("DEFAULT_FOLDER_LIMIT", "100"))
        self.max_folder_limit = int(os.getenv("MAX_FOLDER_LIMIT", "1000"))
        
        # Paths
        self.user_data_dir = self._get_user_data_dir()
        self.cache_dir = self._get_cache_dir()
        self.log_dir = self._get_log_dir()
        
        # MCP config paths
        self.claude_desktop_config_path = self._get_claude_desktop_config_path()
        self.lm_studio_config_path = self._get_lm_studio_config_path()
        self.lm_studio_conversations_dir = self._get_lm_studio_conversations_dir()
    
    def _get_user_data_dir(self) -> Path:
        """ユーザーデータディレクトリを取得"""
        if custom_path := os.getenv("USER_DATA_DIR"):
            return Path(custom_path).expanduser()
        
        if os.name == 'nt':  # Windows
            return Path(os.getenv("LOCALAPPDATA", "~/.local/share")).expanduser() / "eagle-mcp-server"
        else:  # macOS/Linux
            return Path("~/.local/share/eagle-mcp-server").expanduser()
    
    def _get_cache_dir(self) -> Path:
        """キャッシュディレクトリを取得"""
        if custom_path := os.getenv("CACHE_DIR"):
            return Path(custom_path).expanduser()
        
        if os.name == 'nt':  # Windows
            return self.user_data_dir / "cache"
        else:  # macOS/Linux
            return Path("~/.cache/eagle-mcp-server").expanduser()
    
    def _get_log_dir(self) -> Path:
        """ログディレクトリを取得"""
        if custom_path := os.getenv("LOG_DIR"):
            return Path(custom_path).expanduser()
        
        return self.user_data_dir / "logs"
    
    def _get_claude_desktop_config_path(self) -> Path:
        """Claude Desktop設定パスを取得"""
        if custom_path := os.getenv("CLAUDE_DESKTOP_CONFIG_PATH"):
            return Path(custom_path).expanduser()
        
        if os.name == 'nt':  # Windows
            return Path(os.getenv("APPDATA", "~/AppData/Roaming")).expanduser() / "Claude" / "claude_desktop_config.json"
        elif os.name == 'posix':
            import platform
            if platform.system() == 'Darwin':  # macOS
                return Path("~/Library/Application Support/Claude/claude_desktop_config.json").expanduser()
            else:  # Linux
                return Path("~/.config/claude/claude_desktop_config.json").expanduser()
        
        return Path("~/.config/claude/claude_desktop_config.json").expanduser()
    
    def _get_lm_studio_config_path(self) -> Path:
        """LM Studio設定パスを取得"""
        if custom_path := os.getenv("LM_STUDIO_CONFIG_PATH"):
            return Path(custom_path).expanduser()
        
        return Path("~/.cache/lm-studio/mcp.json").expanduser()
    
    def _get_lm_studio_conversations_dir(self) -> Path:
        """LM Studio会話ディレクトリを取得"""
        if custom_path := os.getenv("LM_STUDIO_CONVERSATIONS_DIR"):
            return Path(custom_path).expanduser()
        
        return Path("~/.cache/lm-studio/conversations").expanduser()
    
    def create_directories(self):
        """必要なディレクトリを作成"""
        directories = [
            self.user_data_dir,
            self.cache_dir,
            self.log_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def load_local_config(self) -> Optional[dict]:
        """ローカル設定ファイルがあれば読み込み"""
        local_config_path = Path("config.local.json")
        if local_config_path.exists():
            try:
                with open(local_config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return None
        return None
    
    def to_dict(self) -> dict:
        """設定を辞書形式で返す"""
        return {
            "eagle": {
                "api_url": self.eagle_api_base_url,
                "timeout": self.eagle_api_timeout,
                "default_item_limit": self.default_item_limit,
                "max_item_limit": self.max_item_limit,
                "default_folder_limit": self.default_folder_limit,
                "max_folder_limit": self.max_folder_limit
            },
            "mcp": {
                "server_name": self.mcp_server_name,
                "server_version": self.mcp_server_version,
                "server_description": self.mcp_server_description,
                "log_level": self.log_level,
                "log_format": self.log_format
            },
            "paths": {
                "user_data_dir": str(self.user_data_dir),
                "cache_dir": str(self.cache_dir),
                "log_dir": str(self.log_dir),
                "claude_desktop_config_path": str(self.claude_desktop_config_path),
                "lm_studio_config_path": str(self.lm_studio_config_path),
                "lm_studio_conversations_dir": str(self.lm_studio_conversations_dir)
            }
        }


# グローバル設定インスタンス
config = Config()

# 後方互換性のための定数
EAGLE_API_BASE_URL = config.eagle_api_base_url
EAGLE_API_TIMEOUT = config.eagle_api_timeout
MCP_SERVER_NAME = config.mcp_server_name
MCP_SERVER_VERSION = config.mcp_server_version
MCP_SERVER_DESCRIPTION = config.mcp_server_description
LOG_LEVEL = config.log_level
LOG_FORMAT = config.log_format
DEFAULT_ITEM_LIMIT = config.default_item_limit
MAX_ITEM_LIMIT = config.max_item_limit
DEFAULT_FOLDER_LIMIT = config.default_folder_limit
MAX_FOLDER_LIMIT = config.max_folder_limit