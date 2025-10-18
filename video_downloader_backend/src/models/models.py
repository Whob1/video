from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from . import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    google_access_token = Column(Text)
    google_refresh_token = Column(Text)
    google_token_expiry = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    downloads = relationship("Download", back_populates="user", cascade="all, delete-orphan")
    settings = relationship("UserSettings", back_populates="user", uselist=False, cascade="all, delete-orphan")

class Download(Base):
    __tablename__ = 'downloads'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    task_id = Column(String(100), unique=True, nullable=False)
    url = Column(Text, nullable=False)
    title = Column(String(500))
    format = Column(String(50))
    quality = Column(String(50))
    status = Column(String(50), default='pending')  # pending, downloading, completed, failed, cancelled
    progress = Column(Float, default=0.0)
    file_path = Column(Text)
    file_size = Column(Integer)
    download_speed = Column(String(50))
    eta = Column(String(50))
    error_message = Column(Text)
    include_subtitles = Column(Boolean, default=False)
    include_thumbnail = Column(Boolean, default=False)
    upload_to_drive = Column(Boolean, default=False)
    cloud_only = Column(Boolean, default=False)
    google_drive_url = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    user = relationship("User", back_populates="downloads")

class Playlist(Base):
    __tablename__ = 'playlists'
    
    id = Column(Integer, primary_key=True)
    playlist_id = Column(String(100), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    url = Column(Text, nullable=False)
    title = Column(String(500))
    total_videos = Column(Integer)
    processed_videos = Column(Integer, default=0)
    status = Column(String(50), default='processing')
    created_at = Column(DateTime, default=datetime.utcnow)

class QueueTask(Base):
    __tablename__ = 'queue_tasks'
    
    id = Column(Integer, primary_key=True)
    task_id = Column(String(100), unique=True, nullable=False)
    task_type = Column(String(50))  # download, upload, extract_info
    priority = Column(Integer, default=0)
    status = Column(String(50), default='pending')
    data = Column(Text)  # JSON data for task
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)

class UserSettings(Base):
    __tablename__ = 'user_settings'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    default_format = Column(String(50), default='mp4')
    default_quality = Column(String(50), default='720p')
    auto_upload_drive = Column(Boolean, default=False)
    cloud_only_mode = Column(Boolean, default=False)
    include_subtitles = Column(Boolean, default=False)
    include_thumbnail = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="settings")
