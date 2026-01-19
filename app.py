import gradio as gr
from faster_whisper import WhisperModel

# Настройки модели
MODEL_NAME = "systran/faster-whisper-large-v3"
DEVICE = "cuda"
COMPUTE_TYPE = "float16"

print("--- Загрузка модели... ---")
model = WhisperModel(MODEL_NAME, device=DEVICE, compute_type=COMPUTE_TYPE)
print("--- Модель готова к работе! ---")

def transcribe(audio_path):
    if audio_path is None:
        return "Ошибка: вы не загрузили аудиофайл!"
    
    # Распознавание
    segments, info = model.transcribe(audio_path, beam_size=5)
    
    text_result = ""
    print(f"Обработка файла: {info.duration:.2f} сек.")
    
    for segment in segments:
        # Формат: [00:00 -> 00:05] Текст
        line = f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}\n"
        text_result += line
        
    return text_result

# Настройка веб-интерфейса
with gr.Blocks(title="Whisper Ru Web") as demo:
    gr.Markdown("## Whisper Large V3 Russian (Demo)")
    gr.Markdown("Загрузите аудиофайл или запишите голос с микрофона.")
    
    with gr.Row():
        with gr.Column():
            # Вход: Файл или Микрофон
            audio_input = gr.Audio(type="filepath", sources=["upload", "microphone"])
            btn = gr.Button("РАСПОЗНАТЬ", variant="primary")
        with gr.Column():
            # Выход: Текст
            text_output = gr.Textbox(label="Результат", lines=15)
    
    # Связь кнопки с функцией
    btn.click(fn=transcribe, inputs=audio_input, outputs=text_output)

# Запуск сервера
# share=True — создаст публичную ссылку (доступную из интернета) на 72 часа
demo.queue().launch(server_name="0.0.0.0", server_port=7860, share=True)
