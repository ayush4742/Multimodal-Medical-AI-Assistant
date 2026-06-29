from core.doctor_engine import doctor_engine

system_prompt = "You are an AI Doctor."

result = doctor_engine.run(
    audio_path="patient_voice_test.mp3",
    system_prompt=system_prompt
)

print(result)