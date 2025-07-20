"""Base schemas for Eagle MCP Server."""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class EagleResponse(BaseModel):
    """Base response from Eagle API."""
    status: str
    data: Optional[Dict[str, Any]] = None
    
    @property
    def is_success(self) -> bool:
        """Check if response is successful."""
        return self.status == "success"


class FolderInfo(BaseModel):
    """Folder information from Eagle API."""
    id: str
    name: str
    description: Optional[str] = None
    children: Optional[list] = None
    modificationTime: Optional[int] = None
    tags: Optional[list] = None
    iconColor: Optional[str] = None
    icon: Optional[str] = None
    newFolderName: Optional[str] = None
    password: Optional[str] = None
    passwordTips: Optional[str] = None
    parent: Optional[str] = None
    size: Optional[int] = None
    isExpand: Optional[bool] = None
    extendTags: Optional[list] = None


class ItemInfo(BaseModel):
    """Item information from Eagle API."""
    id: str
    name: str
    size: int
    ext: str
    tags: list = Field(default_factory=list)
    folders: list = Field(default_factory=list)
    modificationTime: Optional[int] = None
    height: Optional[int] = None
    width: Optional[int] = None
    star: Optional[int] = None
    annotation: Optional[str] = None
    url: Optional[str] = None
    lastModified: Optional[int] = None