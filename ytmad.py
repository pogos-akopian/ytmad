#!/usr/bin/env python3
"""
YouTube Album Downloader
Скачивает весь музыкальный альбом/плейлист с YouTube

Установка зависимостей:
pip install yt-dlp

Использование:
python download_album.py "https://www.youtube.com/playlist?list=..."
python download_album.py "https://www.youtube.com/watch?v=...&list=..."
"""

import sys
import os
import subprocess
import re
from pathlib import Path

def check_dependencies():
    """Проверка установки yt-dlp"""
    try:
        subprocess.run(['yt-dlp', '--version'], 
                      capture_output=True, 
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ yt-dlp не установлен!")
        print("\nУстановите его командой:")
        print("  pip install yt-dlp")
        print("\nИли:")
        print("  pip3 install yt-dlp")
        return False

def extract_playlist_id(url):
    """Извлечение ID плейлиста из URL"""
    patterns = [
        r'list=([^&]+)',
        r'youtube\.com/playlist\?list=([^&]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_playlist_info(url):
    """Получение информации о плейлисте"""
    try:
        print("📋 Получаю информацию о плейлисте...")
        
        result = subprocess.run(
            ['yt-dlp', '--dump-json', '--flat-playlist', url],
            capture_output=True,
            text=True,
            check=True
        )
        
        lines = result.stdout.strip().split('\n')
        import json
        
        videos = []
        playlist_title = None
        
        for line in lines:
            if line:
                try:
                    data = json.loads(line)
                    if 'title' in data and 'id' in data:
                        videos.append({
                            'title': data['title'],
                            'id': data['id']
                        })
                    if not playlist_title and 'playlist_title' in data:
                        playlist_title = data['playlist_title']
                except:
                    continue
        
        return {
            'title': playlist_title or 'Unknown Playlist',
            'count': len(videos),
            'videos': videos
        }
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при получении информации: {e}")
        return None

def download_album(url, output_dir='downloads'):
    """Скачивание альбома"""
    
    # Создаем папку для загрузок
    Path(output_dir).mkdir(exist_ok=True)
    
    print(f"\n🎵 Начинаю скачивание альбома...")
    print(f"📁 Папка сохранения: {output_dir}/\n")
    
    # Параметры для yt-dlp
    cmd = [
        'yt-dlp',
        '--extract-audio',              # Извлечь только аудио
        '--audio-format', 'mp3',        # Формат MP3
        '--audio-quality', '0',         # Лучшее качество
        '--embed-thumbnail',            # Встроить обложку
        '--add-metadata',               # Добавить метаданные
        '--output', f'{output_dir}/%(playlist_index)s - %(title)s.%(ext)s',  # Формат имени файла
        '--yes-playlist',               # Скачать весь плейлист
        '--ignore-errors',              # Игнорировать ошибки
        '--no-warnings',                # Без предупреждений
        '--progress',                   # Показывать прогресс
        url
    ]
    
    try:
        # Запускаем скачивание
        subprocess.run(cmd, check=True)
        
        print("\n✅ Скачивание завершено!")
        print(f"📂 Файлы сохранены в папке: {output_dir}/")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Ошибка при скачивании: {e}")
        return False
    except KeyboardInterrupt:
        print("\n\n⚠️  Скачивание прервано пользователем")
        return False

def main():
    print("=" * 60)
    print("🎵 YouTube Album Downloader")
    print("=" * 60)
    
    # Проверка зависимостей
    if not check_dependencies():
        sys.exit(1)
    
    # Получение URL
    if len(sys.argv) < 2:
        print("\n❌ Не указана ссылка на плейлист!")
        print("\nИспользование:")
        print(f"  python {sys.argv[0]} <URL_плейлиста>")
        print("\nПример:")
        print(f"  python {sys.argv[0]} 'https://www.youtube.com/playlist?list=...'")
        sys.exit(1)
    
    url = sys.argv[1]
    
    # Проверка URL
    if 'youtube.com' not in url and 'youtu.be' not in url:
        print("❌ Неверная ссылка! Укажите ссылку на YouTube плейлист.")
        sys.exit(1)
    
    # Получение информации о плейлисте
    info = get_playlist_info(url)
    
    if info:
        print(f"\n📋 Плейлист: {info['title']}")
        print(f"🎵 Количество треков: {info['count']}")
        
        # Подтверждение
        response = input(f"\n⚠️  Начать скачивание {info['count']} треков? (y/n): ")
        if response.lower() != 'y':
            print("❌ Скачивание отменено")
            sys.exit(0)
    
    # Опциональная папка для сохранения
    if len(sys.argv) >= 3:
        output_dir = sys.argv[2]
    else:
        output_dir = 'downloads'
    
    # Скачивание
    success = download_album(url, output_dir)
    
    if success:
        print("\n🎉 Готово! Приятного прослушивания!")
    else:
        print("\n⚠️  Скачивание завершено с ошибками")
        sys.exit(1)

if __name__ == "__main__":
    main()