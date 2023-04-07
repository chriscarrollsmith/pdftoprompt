import os
import tempfile
from pdftoprompt import compress_pdf, set_openai_api_key
from pypdf import PdfWriter
import pytest
from dotenv import load_dotenv, set_key


def test_set_openai_api_key_with_key():
    test_key = "test_key"
    original_key = os.environ.get('OPENAI_API_KEY')

    try:
        set_openai_api_key(test_key)
        assert os.environ.get('OPENAI_API_KEY') == test_key
    finally:
        if original_key is not None:
            os.environ['OPENAI_API_KEY'] = original_key
        else:
            del os.environ['OPENAI_API_KEY']


def test_set_openai_api_key_without_key(tmp_path):
    original_key = os.environ.get('OPENAI_API_KEY')
    dotenv_path = tmp_path / ".env"
    test_key = "test_key_from_env"
    set_key(str(dotenv_path), "OPENAI_API_KEY", test_key)
    load_dotenv(dotenv_path)

    try:
        set_openai_api_key()
        assert os.environ.get('OPENAI_API_KEY') == test_key
    finally:
        if original_key is not None:
            os.environ['OPENAI_API_KEY'] = original_key
        else:
            del os.environ['OPENAI_API_KEY']
        dotenv_path.unlink()


def test_set_openai_api_key_with_invalid_type():
    with pytest.raises(TypeError):
        set_openai_api_key(123)


def test_set_openai_api_key_without_key_and_env_var(tmp_path):
    original_key = os.environ.get('OPENAI_API_KEY')
    test_key = "test_key_from_env"
    try:
        with open('.env') as f:
            original_env = f.readlines()
        os.unlink(".env")
    except FileNotFoundError:
        pass

    dotenv_path = tmp_path / ".env"
    dotenv_path.write_text("")
    load_dotenv(dotenv_path)

    try:
        with pytest.raises(ValueError):
            set_openai_api_key()
    finally:
        if original_key is not None:
            os.environ['OPENAI_API_KEY'] = original_key
            set_key(str(dotenv_path), "OPENAI_API_KEY", test_key)
        else:
            if 'OPENAI_API_KEY' in os.environ:
                del os.environ['OPENAI_API_KEY']
        if 'original_env' in locals():
            with open(".env", "w") as f:
                f.write(original_env[0])
    os.unlink(dotenv_path)

    # Check if the environment variable has been reset or deleted
    assert os.environ.get('OPENAI_API_KEY') == original_key

    # Check if the temp env file has been deleted
    assert not dotenv_path.exists()


def create_sample_pdf(text):
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf_writer = PdfWriter()
    pdf_writer.add_blank_page(width=72, height=72)

    with open(file.name, "wb") as f:
        pdf_writer.write_stream(f)

    return file.name


def test_compress_pdf_without_ocr():
    set_openai_api_key()
    sample_text = ("This is a sample text for testing the PDF"
                   "compressor function without OCR.")
    pdf_path = create_sample_pdf(sample_text)
    compressed_text = compress_pdf(pdf_path, use_ocr=False)
    # compressed_text = compress_pdf("sample_pdf.pdf", use_ocr=False)
    assert compressed_text is not None
    assert isinstance(compressed_text, str)
    os.remove(pdf_path)


# def test_compress_pdf_with_ocr():
#    sample_text = ("This is a sample text for testing the"
#                   "PDF compressor function with OCR.")
#    pdf_path = create_sample_pdf(sample_text)
#    compressed_text = compress_pdf(pdf_path, use_ocr=True)
#    assert compressed_text is not None
#    assert isinstance(compressed_text, str)
#    os.remove(pdf_path)


if __name__ == '__main__':
    pytest.main()
