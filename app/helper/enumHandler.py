from app.schemas.user import PAL, statusEnum

def handlePAL(userInput: str) -> PAL :
    formattedInput = userInput.replace(" ", "_").lower()
    
    if formattedInput in PAL.__members__:
        return PAL[formattedInput]
    else:
        raise ValueError(f"Invalid input: '{userInput}' is not a valid activity level.")
    
def handlePeriodeKehamilan(userInput: str) -> statusEnum :
    formattedInput = userInput.replace(" ", "").lower()
    
    if formattedInput in statusEnum.__members__:
        return statusEnum[formattedInput]
    else:
        raise ValueError(f"Invalid input: '{userInput}' is not a valid status.")
    
def formatPal(pal: str) -> PAL:
    return handlePAL(pal)