from core.consultation_agent import consultation_step

history = ""

while True:

    user = input("\nYou : ")

    if user.lower() == "exit":
        break

    history += f"\nPatient: {user}"

    reply = consultation_step(history)

    print("\nDoctor :", reply)

    history += f"\nDoctor: {reply}"