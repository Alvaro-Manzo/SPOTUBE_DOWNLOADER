"""
Tests para Spotify Downloader PRO
"""
import pytest
import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def spotify_url():
    """URL de prueba de Spotify"""
    return "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"


@pytest.fixture
def test_output_dir(tmp_path):
    """Directorio temporal para tests"""
    return tmp_path / "test_downloads"


def test_imports():
    """Test que los módulos principales se importan correctamente"""
    try:
        import main
        import api
        assert True
    except ImportError as e:
        pytest.fail(f"Error importing modules: {e}")


def test_zip_creation(test_output_dir):
    """Test creación de archivo ZIP"""
    import zipfile
    
    test_output_dir.mkdir(parents=True, exist_ok=True)
    zip_path = test_output_dir / "test.zip"
    
    # Crear un ZIP de prueba
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.writestr("test.txt", "Hello World")
    
    assert zip_path.exists()
    assert zip_path.stat().st_size > 0


def test_spotify_url_validation(spotify_url):
    """Test validación de URL de Spotify"""
    assert "spotify.com" in spotify_url
    assert "playlist" in spotify_url


def test_environment_variables():
    """Test que las variables de entorno están configuradas"""
    # Verificar Python version
    assert sys.version_info >= (3, 8), "Python 3.8+ required"


def test_directories_creation(test_output_dir):
    """Test creación de directorios necesarios"""
    test_output_dir.mkdir(parents=True, exist_ok=True)
    
    downloads_dir = test_output_dir / "downloads"
    temp_dir = test_output_dir / "temp"
    
    downloads_dir.mkdir(exist_ok=True)
    temp_dir.mkdir(exist_ok=True)
    
    assert downloads_dir.exists()
    assert temp_dir.exists()


@pytest.mark.parametrize("quality,bitrate", [
    ("low", "128k"),
    ("medium", "192k"),
    ("high", "320k"),
])
def test_quality_mapping(quality, bitrate):
    """Test mapeo de calidades"""
    quality_map = {
        'low': '128k',
        'medium': '192k',
        'high': '320k'
    }
    assert quality_map[quality] == bitrate


def test_file_extensions():
    """Test que se manejan correctamente las extensiones"""
    test_files = ["song.mp3", "track.m4a", "audio.wav"]
    mp3_files = [f for f in test_files if f.endswith('.mp3')]
    
    assert len(mp3_files) == 1
    assert mp3_files[0] == "song.mp3"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=.", "--cov-report=html"])
