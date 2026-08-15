devices = {
    "light": False,
    "fan": False,
    "ac": False,
    "tv": False,
    "door": False
}


def smart_home(command, speak):
    """
    Process smart-home voice commands.

    command = recognized voice command
    speak = your existing text-to-speech function
    """

    command = command.lower().strip()

    # -------------------------
    # LIGHT
    # -------------------------

    if "turn on light" in command or "switch on light" in command:
        devices["light"] = True
        speak("The light is now on.")
        return True

    elif "turn off light" in command or "switch off light" in command:
        devices["light"] = False
        speak("The light is now off.")
        return True

    # -------------------------
    # FAN
    # -------------------------

    elif "turn on fan" in command or "switch on fan" in command:
        devices["fan"] = True
        speak("The fan is now on.")
        return True

    elif "turn off fan" in command or "switch off fan" in command:
        devices["fan"] = False
        speak("The fan is now off.")
        return True

    # -------------------------
    # AC
    # -------------------------

    elif "turn on ac" in command or "switch on ac" in command:
        devices["ac"] = True
        speak("The air conditioner is now on.")
        return True

    elif "turn off ac" in command or "switch off ac" in command:
        devices["ac"] = False
        speak("The air conditioner is now off.")
        return True

    # -------------------------
    # TV
    # -------------------------

    elif "turn on tv" in command or "switch on tv" in command:
        devices["tv"] = True
        speak("The TV is now on.")
        return True

    elif "turn off tv" in command or "switch off tv" in command:
        devices["tv"] = False
        speak("The TV is now off.")
        return True

    # -------------------------
    # DOOR
    # -------------------------

    elif "unlock door" in command or "open door" in command:
        devices["door"] = True
        speak("The door is now unlocked.")
        return True

    elif "lock door" in command or "close door" in command:
        devices["door"] = False
        speak("The door is now locked.")
        return True

    # -------------------------
    # DEVICE STATUS
    # -------------------------

    elif "smart home status" in command or "home status" in command:
        speak_status(speak)
        return True

    elif "light status" in command:
        status = "on" if devices["light"] else "off"
        speak(f"The light is currently {status}.")
        return True

    elif "fan status" in command:
        status = "on" if devices["fan"] else "off"
        speak(f"The fan is currently {status}.")
        return True

    elif "ac status" in command:
        status = "on" if devices["ac"] else "off"
        speak(f"The air conditioner is currently {status}.")
        return True

    elif "tv status" in command:
        status = "on" if devices["tv"] else "off"
        speak(f"The TV is currently {status}.")
        return True

    elif "door status" in command:
        status = "unlocked" if devices["door"] else "locked"
        speak(f"The door is currently {status}.")
        return True

    return False


def speak_status(speak):
    """Speak the status of all smart-home devices."""

    light = "on" if devices["light"] else "off"
    fan = "on" if devices["fan"] else "off"
    ac = "on" if devices["ac"] else "off"
    tv = "on" if devices["tv"] else "off"
    door = "unlocked" if devices["door"] else "locked"

    message = (
        f"Light is {light}. "
        f"Fan is {fan}. "
        f"Air conditioner is {ac}. "
        f"TV is {tv}. "
        f"Door is {door}."
    )

    speak(message)